# AutoSub
![Demo](animated.gif)

# Installation
```
conda create --name autosub python==3.11
conda activate autosub
pip install -r requirements.txt
```

# Usage
```
python main.py --inputPath input.mp4 --outputPath output.mp4 --modelName whisper-large-v3 --videoLanguage english --subtitleLanguage turkish --fontPath src/fonts/tahoma.ttf --fontColor white --fontSize 60 --fontBackground None --device cuda:0
```

# Arguments Description
- `--inputPath`: Path to the input video file.
- `--outputPath`: Path to the output video file.
- `--modelName`: Model size of whisper to use for inference. Options are "whisper-large-v3", "whisper-medium", "whisper-small", "whisper-tiny", "whisper-base".
- `--videoLanguage`: Language of the video.
- `--subtitleLanguage`: Language of the subtitles.
- `--fontPath`: Path to the font file.
- `--fontColor`: Color of the subtitles. Options are None, "black", "white", "red", "green".
- `--fontSize`: Font size of the subtitles.
- `--fontBackground`: Background color of the subtitles. Options are None, "black", "white", "red", "green".
- `--device`: Device to use for inference. Options are "cuda:0", "cpu".


# Supported Languages for Subtitles
```
english
spanish
german
italian
portuguese
french
russian
turkish
azerbaijani
japanese
greek
```