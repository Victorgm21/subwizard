import argparse


def setup_argument_parser():
    parser = argparse.ArgumentParser(description="Demo: Subtitulador automático con faster-whisper")
    parser.add_argument(
        "video", 
        help="Path to the video or audio file"
        )
    parser.add_argument(
        "--max-words", 
        type=int, 
        default=5, 
        help="number of words per line"
        )
    parser.add_argument(
        "--performance", 
        default="normal", 
        help="Performance profiles: efficient(base), normal (small), slow(medium), ultra-slow (large)"
        )
    parser.add_argument(
        "--output-name", 
        default="subwizard", 
        help="Set the file name for the output"
        )
    parser.add_argument(
        "--output-path", 
        default=None, 
        help="Set the subtitle output path"
        )
    parser.add_argument(
        "--output-type", 
        default="srt", 
        help="Set file outpy type: srt/mp4"
        )
    parser.add_argument(
        "--lang", 
        default=None
        , help="Set the original language from the video"
        )
    parser.add_argument(
        "--srt-path", 
        default=None
        , help="Burns .SRT path into a video, write the SRT path"
        )

    return parser