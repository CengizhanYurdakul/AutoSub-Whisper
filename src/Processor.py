import os
import torch
from deep_translator import GoogleTranslator
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

class Processor:
    def __init__(self, args):
        self.args = args
        self.torchDtype = torch.float16 if torch.cuda.is_available() else torch.float32

        self.initWhisper()
        self.initTranslator()

    def initTranslator(self):
        self.translator = GoogleTranslator(source=self.args.videoLanguage, target=self.args.subtitleLanguage)

    def initWhisper(self):
        self.args.modelName = os.path.join("openai", self.args.modelName)

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.args.modelName, torch_dtype=self.torchDtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(self.args.device)
        processor = AutoProcessor.from_pretrained(self.args.modelName)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=self.torchDtype,
            device=self.args.device,
        )

    def exportAudio(self):
        self.inputVideo = VideoFileClip(self.args.inputPath)
        self.inputVideo.audio.write_audiofile(self.args.inputPath.replace(self.args.inputPath.rsplit(".")[-1], "mp3"))

    def main(self):
        subtitleList = []

        # Extract audio from video
        self.exportAudio()

        # Speech-to-text
        result = self.pipe(self.args.inputPath.replace(self.args.inputPath.rsplit(".")[-1], "mp3"), return_timestamps=True, generate_kwargs={"language": self.args.videoLanguage})
        
        part = 0
        for c, subtitle in enumerate(result["chunks"]):
            startTime = subtitle["timestamp"][0]
            endTime = subtitle["timestamp"][1]
            text = subtitle["text"]
            translatedText = self.translator.translate(text)

            if startTime == 0 and c != 0:
                part += 30
            
            subtitle_clip = TextClip(text=translatedText, font_size=self.args.fontSize, color=self.args.fontColor, font=self.args.fontPath, bg_color=self.args.fontBackground)
            subtitle_clip = subtitle_clip.with_start(startTime+part)
            subtitle_clip = subtitle_clip.with_position(('center', self.inputVideo.size[1]-150)).with_duration(float(endTime - startTime))
            subtitleList.append(subtitle_clip)

        final_video = CompositeVideoClip([VideoFileClip(self.args.inputPath)] + subtitleList)
        audio = AudioFileClip(self.args.inputPath.replace(self.args.inputPath.rsplit(".")[-1], "mp3"))
        video = final_video.with_audio(audio)
        video.write_videofile(self.args.outputPath, codec='libx264', audio_codec='aac')