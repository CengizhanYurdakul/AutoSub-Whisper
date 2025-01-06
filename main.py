import argparse
from src.Processor import Processor

parser = argparse.ArgumentParser()
parser.add_argument("--inputPath", default="untitled.mp4" ,type=str, help="Path to the input video file")
parser.add_argument("--outputPath", default="untitled-Out.mp4", type=str, help="Path to the output video file")
parser.add_argument("--modelName", default="whisper-large-v3", type=str, choices=["whisper-large-v3", "whisper-medium", "whisper-small", "whisper-tiny", "whisper-base"], help="Model size of whisper to use for inference")
parser.add_argument("--videoLanguage", default="english", type=str, help="Language of the video")
parser.add_argument("--subtitleLanguage", default="french", type=str, help="Language of the subtitles")
parser.add_argument("--fontPath", default="src/fonts/tahoma.ttf", type=str, help="Path to the font file")
parser.add_argument("--fontColor", default="white", type=str, help="Color of the subtitles")
parser.add_argument("--fontSize", default=60, type=int, help="Font size of the subtitles")
parser.add_argument("--fontBackground", default=None, type=str, choices=[None, "black", "white", "red", "green"], help="Background color of the subtitles")
parser.add_argument("--device", default="cuda:0", type=str, help="Device to use for inference")
args = parser.parse_args()

processor = Processor(args)
processor.main()