# <u>AP</u>ple <u>M</u>edia <u>TO</u> (APMTO)

*APMTO* is a simple Python package wrapper to easily convert apple-formatted media files into highly-compatible formats. 

## Requirements

### Operating System

OS independent.

### Frameworks & Libraries

- [FFmpeg](https://ffmpeg.org/) 

### Python

See [requirements.txt](https://github.com/nda111/APMTO/blob/master/requirements.txt) for more.

- [Python 3](https://www.python.org/) >= 3.9
- [pillow](https://pypi.org/project/pillow/)
- [pillow_heif](https://pypi.org/project/pillow-heif/)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)

## Installation 

### Installing FFmpeg

Please follow the instruction of [ffmpeg-python](https://github.com/kkroening/ffmpeg-python?tab=readme-ov-file#installing-ffmpeg) repository to properly install FFmpeg framework. 

<!-- ### Via Anaconda3

```bash
conda install apmto
``` -->

### Via PyPI

You can install the lastest `apmto` package using the following command:

```bash
pip install apmto
```

or you can install from this GitHub repository.

```bash
pip install git+https://github.com/nda111/APMTO.git
```

<!-- ### Via wheel file -->

## Usage

### Example Code

You can convert the files into high-compatible formats using the following code ([file](https://github.com/nda111/APMTO/blob/master/example/convert.py)). 

```python
# example/convert.py

import apmto 

apmto.heif_to_jpg('example/sample.heif')  # for HEIF (or HEIC, HEIX) image files.
apmto.mov_to_mp4('example/sample.mov', verbose=True)  # for MOV video files. 
```

You can run this example code by this command.

```bash
python -m example.convert
```

If you want to specify `ffmpeg` command arguments, try the following code. 

```python
import apmto

apmto.mov_to_mp4('example/sample.mov', verbose=True, option=dict(
    vcodec='h264', 
    acodec='aac', 
    video_bitrate=1800 * 1000, 
    audio_bitrate=120 * 1000, 
))
```

### Format Support

Following table summarizes the supported formats. 

| Class | Source | Target|
| ----- | ------ | ----- |
| Image | `HEIF` <br /> `HEIC` <br /> `HEIX` | `JPG` <br /> `JPEG` <br /> `PNG` |
| Video | `MOV`  | `MP4` <br /> `MKV` |
