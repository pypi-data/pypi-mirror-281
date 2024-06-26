import sys
import LangSegment
import torch
import threading
import numpy as np
import librosa
import sys
import importlib.util
from contextlib import contextmanager
from typing import Optional, Any, TypeVar, cast, List, Tuple
from queue import Queue
from transformers import AutoModelForMaskedLM, AutoTokenizer

import gpt_sovits.feature_extractor.cnhubert as cnhubert
from gpt_sovits.module.models import SynthesizerTrn
from gpt_sovits.AR.models.t2s_lightning_module import Text2SemanticLightningModule
from gpt_sovits.text import cleaned_text_to_sequence
from gpt_sovits.text.cleaner import clean_text
from gpt_sovits.module.mel_processing import spectrogram_torch

from gpt_sovits.infer.text_utils import clean_and_cut_text


class DictToAttrRecursive(dict):
    def __init__(self, input_dict):
        super().__init__(input_dict)
        for key, value in input_dict.items():
            if isinstance(value, dict):
                value = DictToAttrRecursive(value)
            self[key] = value
            setattr(self, key, value)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"Attribute {item} not found")

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            value = DictToAttrRecursive(value)
        super(DictToAttrRecursive, self).__setitem__(key, value)
        super().__setattr__(key, value)

    def __delattr__(self, item):
        try:
            del self[item]
        except KeyError:
            raise AttributeError(f"Attribute {item} not found")


@contextmanager
def _tmp_sys_path():
    package_name = "gpt_sovits"
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        package_path = spec.origin
        if package_path is not None:
            tmp_path = package_path[:-11]  # remove __init__.py
        else:
            raise ModuleNotFoundError(f"Package {package_name} not found.")
    else:
        raise ModuleNotFoundError(f"Package {package_name} not found.")

    sys.path.append(tmp_path)
    yield
    sys.path.remove(tmp_path)


def clean_text_inf(text, language):
    phones, word2ph, norm_text = clean_text(text, language)
    phones = cleaned_text_to_sequence(phones)
    return phones, word2ph, norm_text


class GPTSoVITSInference:
    device: str
    is_half: bool

    tokenizer: AutoTokenizer
    bert_model: AutoModelForMaskedLM
    ssl_model: cnhubert.CNHubert

    vq_model: SynthesizerTrn
    hps: DictToAttrRecursive

    hz: int
    max_sec: int
    t2s_model: Text2SemanticLightningModule

    prompt_audio_data: np.ndarray
    prompt_audio_sr: int
    prompt_text: Optional[str]
    prompt: torch.Tensor
    phones1: Optional[list]
    bert1: Optional[torch.Tensor]

    def __init__(
        self,
        bert_path: str,
        cnhubert_base_path: str,
        device: Optional[str] = None,
        is_half: bool = True,
    ):
        if device is None:
            if torch.cuda.is_available():
                device = "cuda"
            elif torch.backends.mps.is_available():
                device = "mps"
            else:
                device = "cpu"
        self.device = device
        self.is_half = is_half

        self.tokenizer = AutoTokenizer.from_pretrained(bert_path)
        bert_model = AutoModelForMaskedLM.from_pretrained(bert_path)
        self.bert_model = self._prepare_torch(bert_model)

        cnhubert.cnhubert_base_path = cnhubert_base_path
        self.ssl_model = self._prepare_torch(cnhubert.get_model())

    def load_sovits(self, sovits_path: str):
        with _tmp_sys_path():
            dict_s2 = torch.load(sovits_path, map_location="cpu")
        hps = dict_s2["config"]
        hps = DictToAttrRecursive(hps)
        hps.model.semantic_frame_rate = "25hz"
        vq_model = SynthesizerTrn(
            hps.data.filter_length // 2 + 1,
            hps.train.segment_size // hps.data.hop_length,
            n_speakers=hps.data.n_speakers,
            **hps.model,
        )
        del vq_model.enc_q
        vq_model = self._prepare_torch(vq_model)
        vq_model.eval()
        vq_model.load_state_dict(dict_s2["weight"], strict=False)
        self.hps = hps
        self.vq_model = vq_model

    def load_gpt(self, gpt_path: str):
        dict_s1 = torch.load(gpt_path, map_location="cpu")
        config = dict_s1["config"]
        t2s_model = Text2SemanticLightningModule(config, "****", is_train=False)
        t2s_model.load_state_dict(dict_s1["weight"])
        if self.is_half == True:
            t2s_model = t2s_model.half()
        t2s_model = t2s_model.to(self.device)
        t2s_model.eval()
        self.hz = 50
        self.max_sec = config["data"]["max_sec"]
        self.t2s_model = t2s_model

    @property
    def torch_dtype(self):
        return torch.float16 if self.is_half == True else torch.float32

    @property
    def np_dtype(self):
        return np.float16 if self.is_half == True else np.float32

    T = TypeVar("T")

    def _prepare_torch(self, torch: T) -> T:
        if self.is_half:
            return torch.half().to(self.device)
        else:
            return torch.to(self.device)

    def _get_bert_feature(self, text, word2ph):
        with torch.no_grad():
            inputs = self.tokenizer(text, return_tensors="pt")
            for i in inputs:
                inputs[i] = inputs[i].to(self.device)
            res = self.bert_model(**inputs, output_hidden_states=True)
            res = torch.cat(res["hidden_states"][-3:-2], -1)[0].cpu()[1:-1]
        assert len(word2ph) == len(text)
        phone_level_feature = []
        for i in range(len(word2ph)):
            repeat_feature = res[i].repeat(word2ph[i], 1)
            phone_level_feature.append(repeat_feature)
        phone_level_feature = torch.cat(phone_level_feature, dim=0)
        return phone_level_feature.T

    def _get_bert_inf(self, phones, word2ph, norm_text, language):
        language = language.replace("all_", "")
        if language == "zh":
            bert = self._get_bert_feature(norm_text, word2ph).to(
                self.device
            )  # .to(dtype)
        else:
            bert = torch.zeros(
                (1024, len(phones)),
                dtype=torch.float16 if self.is_half == True else torch.float32,
            ).to(self.device)

        return bert

    def _get_phones_and_bert(self, text, language):
        if language in {"en", "all_zh", "all_ja"}:
            language = language.replace("all_", "")
            if language == "en":
                LangSegment.setfilters(["en"])
                formattext = " ".join(tmp["text"] for tmp in LangSegment.getTexts(text))
            else:
                # 因无法区别中日文汉字,以用户输入为准
                formattext = text
            while "  " in formattext:
                formattext = formattext.replace("  ", " ")
            phones, word2ph, norm_text = clean_text_inf(formattext, language)
            if language == "zh":
                bert = self._get_bert_feature(norm_text, word2ph).to(self.device)
            else:
                bert = torch.zeros(
                    (1024, len(phones)),
                    dtype=torch.float16 if self.is_half == True else torch.float32,
                ).to(self.device)
        elif language in {"zh", "ja", "auto"}:
            textlist = []
            langlist = []
            LangSegment.setfilters(["zh", "ja", "en", "ko"])
            if language == "auto":
                for tmp in LangSegment.getTexts(text):
                    if tmp["lang"] == "ko":
                        langlist.append("zh")
                        textlist.append(tmp["text"])
                    else:
                        langlist.append(tmp["lang"])
                        textlist.append(tmp["text"])
            else:
                for tmp in LangSegment.getTexts(text):
                    if tmp["lang"] == "en":
                        langlist.append(tmp["lang"])
                    else:
                        # 因无法区别中日文汉字,以用户输入为准
                        langlist.append(language)
                    textlist.append(tmp["text"])
            phones_list = []
            bert_list = []
            norm_text_list = []
            for i in range(len(textlist)):
                lang = langlist[i]
                phones, word2ph, norm_text = clean_text_inf(textlist[i], lang)
                bert = self._get_bert_inf(phones, word2ph, norm_text, lang)
                phones_list.append(phones)
                norm_text_list.append(norm_text)
                bert_list.append(bert)
            bert = torch.cat(bert_list, dim=1)
            phones = sum(phones_list, [])
            norm_text = "".join(norm_text_list)

        return phones, bert.to(self.torch_dtype), norm_text

    def _get_spepc(self):
        audio = librosa.resample(
            self.prompt_audio_data,
            orig_sr=self.prompt_audio_sr,
            target_sr=self.sample_rate,
        )
        audio = torch.FloatTensor(audio)
        audio_norm = audio
        audio_norm = audio_norm.unsqueeze(0)
        spec = spectrogram_torch(
            audio_norm,
            self.hps.data.filter_length,
            self.sample_rate,
            self.hps.data.hop_length,
            self.hps.data.win_length,
            center=False,
        )
        return spec

    @property
    def zero_wav(self):
        return np.zeros(
            int(self.sample_rate * 0.3),
            dtype=self.np_dtype,
        )

    @property
    def sample_rate(self) -> int:
        return self.hps.data.sampling_rate

    def set_prompt_audio(
        self,
        prompt_text: Optional[str],
        prompt_language: str = "auto",
        prompt_audio_path: Optional[str] = None,
        prompt_audio_data: Optional[np.ndarray] = None,
        prompt_audio_sr: Optional[int] = None,
    ):
        if prompt_text:
            prompt_text = prompt_text.strip("\n")
        self.prompt_text = prompt_text

        if prompt_audio_path:
            prompt_audio_data, prompt_audio_sr = librosa.load(
                path=prompt_audio_path, sr=None
            )
        else:
            if (prompt_audio_data is None) or (prompt_audio_sr is None):
                raise ValueError(
                    "When prompt_audio_path is not given, prompt_audio_data and prompt_audio_sr must be given."
                )
        self.prompt_audio_sr = cast(int, prompt_audio_sr)
        self.prompt_audio_data = cast(np.ndarray, prompt_audio_data)
        if self.prompt_audio_data.dtype == np.int16:
            self.prompt_audio_data = (
                self.prompt_audio_data.astype(self.np_dtype) / 32768
            )

        with torch.no_grad():
            wav16k = librosa.resample(
                self.prompt_audio_data,
                orig_sr=prompt_audio_sr,
                target_sr=self.sample_rate // 2,
            )
            wav16k = torch.from_numpy(wav16k)
            wav16k = self._prepare_torch(wav16k)
            zero_wav_torch = torch.from_numpy(self.zero_wav)
            zero_wav_torch = self._prepare_torch(zero_wav_torch)
            wav16k = torch.cat([wav16k, zero_wav_torch])
            ssl_content = self.ssl_model.model(wav16k.unsqueeze(0))[
                "last_hidden_state"
            ].transpose(
                1, 2
            )  # .float()
            codes = self.vq_model.extract_latent(ssl_content)
            prompt_semantic = codes[0, 0]
            self.prompt = prompt_semantic.unsqueeze(0).to(self.device)

        if prompt_text:
            phones1, bert1, norm_text1 = self._get_phones_and_bert(
                prompt_text, prompt_language
            )
            self.phones1 = phones1
            self.bert1 = bert1
        else:
            self.phones1 = None
            self.bert1 = None

    def get_tts_wav_piece(
        self,
        text: str,
        text_language: str = "auto",
        top_k=5,
        top_p=1,
        temperature=1,
    ) -> Tuple[int, np.ndarray]:
        phones2, bert2, norm_text2 = self._get_phones_and_bert(text, text_language)
        if self.prompt_text:
            bert = torch.cat([self.bert1, bert2], 1)
            all_phoneme_ids = (
                torch.LongTensor(self.phones1 + phones2).to(self.device).unsqueeze(0)
            )
        else:
            bert = bert2
            all_phoneme_ids = torch.LongTensor(phones2).to(self.device).unsqueeze(0)

        bert = bert.to(self.device).unsqueeze(0)
        all_phoneme_len = torch.tensor([all_phoneme_ids.shape[-1]]).to(self.device)
        with torch.no_grad():
            pred_semantic, idx = self.t2s_model.model.infer_panel(
                all_phoneme_ids,
                all_phoneme_len,
                self.prompt if self.prompt_text else None,
                bert,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
                early_stop_num=self.hz * self.max_sec,
            )
        pred_semantic = pred_semantic[:, -idx:].unsqueeze(
            0
        )  # .unsqueeze(0)#mq要多unsqueeze一次
        refer = self._get_spepc()  # .to(device)
        refer = self._prepare_torch(refer)
        audio = (
            self.vq_model.decode(
                pred_semantic,
                torch.LongTensor(phones2).to(self.device).unsqueeze(0),
                refer,
            )
            .detach()
            .cpu()
            .numpy()[0, 0]
        )  ###试试重建不带上prompt部分
        max_audio = np.abs(audio).max()  # 简单防止16bit爆音
        if max_audio > 1:
            audio /= max_audio
        return self.sample_rate, (
            np.concatenate((audio, self.zero_wav)) * 32768
        ).astype(np.int16)

    def produce_tts_wav(
        self,
        queue: Queue,
        text: str,
        text_language="auto",
        top_k=5,
        top_p=1,
        temperature=1,
    ):
        texts = clean_and_cut_text(text)
        for text in texts:
            _, audio = self.get_tts_wav_piece(
                text,
                text_language,
                top_k,
                top_p,
                temperature,
            )
            queue.put(audio)
        queue.put(None)

    def get_tts_wav_stream(
        self,
        text: str,
        text_language="auto",
        top_k=5,
        top_p=1,
        temperature=1,
    ):
        queue = Queue()
        produce = threading.Thread(
            target=self.produce_tts_wav,
            args=(queue, text, text_language, top_k, top_p, temperature),
        )
        produce.start()
        while True:
            audio = queue.get()
            if audio is not None:
                yield (self.sample_rate, audio)
            else:
                break
        produce.join()

    def get_tts_wav(
        self,
        text: str,
        text_language="auto",
        top_k=5,
        top_p=1,
        temperature=1,
    ):
        audio_opt = []
        texts = clean_and_cut_text(text)
        audio_opt = [
            self.get_tts_wav_piece(
                text,
                text_language,
                top_k,
                top_p,
                temperature,
            )[1]
            for text in texts
        ]
        return self.sample_rate, np.concatenate(audio_opt)


if __name__ == "__main__":

    from scipy.io import wavfile

    inference = GPTSoVITSInference(
        bert_path="pretrained_models/chinese-roberta-wwm-ext-large",
        cnhubert_base_path="pretrained_models/chinese-hubert-base",
    )
    inference.load_sovits("pretrained_models/s2G488k.pth")
    inference.load_gpt(
        "pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt"
    )
    prompt_text = "你好 ChatGPT，请问你知道为什么鲁迅暴打周树人吗？"
    inference.set_prompt_audio(
        prompt_audio_path=f"playground/{prompt_text}.wav",
        prompt_text=prompt_text,
    )

    sample_rate, data = inference.get_tts_wav(
        text="鲁迅为什么暴打周树人？？？这是一个问题\n\n自古以来，文人相轻，鲁迅和周树人也不例外。鲁迅和周树人是中国现代文学史上的两位伟大作家，他们的文学成就都是不可磨灭的。但是，鲁迅和周树人之间的关系并不和谐，两人之间曾经发生过一次激烈的冲突，甚至还打了起来。那么，鲁迅为什么会暴打周树人呢？这是一个问题。  ",
    )
    wavfile.write(f"playground/output.wav", sample_rate, data)
