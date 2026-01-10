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
        default=3, 
        help="number of words per line"
        )
    parser.add_argument(
        "--performance", 
        default="normal", 
        help="Performance profiles: efficient(base), normal (small), slow(medium), ultra-slow (large)"
        )
    parser.add_argument(
        "--output-name", 
        default="automatic_subtitles_ready", 
        help="Set the file name for the output"
        )
    parser.add_argument(
        "--output-path", 
        default=None, 
        help="Set the subtitle output path"
        )
    parser.add_argument(
        "--output-type", 
        default="mp4", 
        help="Set file outpy type: srt/mp4"
        )
    parser.add_argument(
        "--lang", 
        default=None
        , help="Set the original language from the video"
        )
    parser.add_argument(
        "--subtitle-path", 
        default=None
        , help="Burns .SRT or .ASS into a video, write the .SRT or .ASS path"
        )
    parser.add_argument(
        "--style", 
        default="simple"
        , help="Choose the style of the subtitles: simple, karaoke"
        )

    return parser