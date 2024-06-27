import sys
from typing import Literal

import ffmpeg

VALID_VIDEO_FORMATS = ['mp4', 'mkv']
    
    
def __get_bitrates(input_file):
    try:
        probe = ffmpeg.probe(input_file)
        audio_bitrate = None
        video_bitrate = None

        streams = probe['streams']
        for stream in streams:
            if stream['codec_type'] == 'video':
                video_bitrate = int(stream.get('bit_rate', 0))
            elif stream['codec_type'] == 'audio':
                audio_bitrate = int(stream.get('bit_rate', 0))

        return video_bitrate, audio_bitrate

    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr}")
        return None, None

    
def convert_mov(filename, format: Literal['mp4', 'mkv'], verbose=False, option=dict()):
    assert format.lower() in VALID_VIDEO_FORMATS
    
    splits = filename.split('.')
    output_file = '.'.join(splits[:-1]) + '.' + format.upper()
    try:
        video_bitrate, audio_bitrate = __get_bitrates(filename)
        option = dict(
            vcodec='h264', 
            acodec='aac', 
            video_bitrate=video_bitrate, 
            audio_bitrate=audio_bitrate, 
            pix_fmt='yuv420p',
            **option
        )
        
        stream = ffmpeg.input(filename)
        stream = ffmpeg.output(stream, output_file, **option)
        ffmpeg.run(stream, cmd='ffmpeg', quiet=not verbose, overwrite_output=True)
    except ffmpeg.Error as e:
        print("An error occurred while converting the file:", file=sys.stderr)
        print(e.stderr.decode('utf8'), file=sys.stderr)
    
    
def mov_to_mkv(filename, verbose=False, option=dict()):
    convert_mov(filename, format='mkv', verbose=verbose, option=option)
    

def mov_to_mp4(filename, verbose=False, option=dict()):
    convert_mov(filename, format='mp4', verbose=verbose, option=option)
