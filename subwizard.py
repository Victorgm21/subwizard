

# Standard library
import os
import sys
import io
import warnings

# Warnings
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API",
    category=UserWarning
)

# Third-party
import torch
from faster_whisper import WhisperModel

# Local
from utils import utils
from cli_args import setup_argument_parser
import styles



# Resolvian un problema de impresion por consola, pero no hace falta ya
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
#sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

global video_width, video_height


def transcribe_to_srt(
    audio_path, 
    style="simple",
    output_path=None, 
    max_words_per_line=5, 
    performance = "normal", 
    file_name = "subs",
    language = None,
    ):

    perf_settings = {
            "efficient":      {"model": "base",   "beam": 3,  "compute": "int8"},
            "normal":         {"model": "small",  "beam": 5,  "compute": "int8"},
            "detailed":       {"model": "medium", "beam": 10, "compute": "float32"},
            "ultra-detailed": {"model": "large",  "beam": 20, "compute": "float32"}
        }
        
    
    settings = perf_settings.get(performance, perf_settings["normal"])
    model_size = settings["model"]
    beam_size = settings["beam"]
    compute_type = settings["compute"]
    device = "cpu"
    extension = ".srt"
    
    # GPU IS AVAILABLE ?
    if(torch.cuda.is_available()):
        print("Detected: GPU available! Optimizing for maximum speed.")
        device = "cuda"
        compute_type = "float16"
    else:
        print("No GPU detected. Proceeding with CPU, which may be slower.")
    
    
    print(f"The '{model_size}' model is now processing your audio. Generating transcription!")
    model = WhisperModel(model_size, device= device, compute_type= compute_type)


    if language != None or language == "auto":
        segments, _info = model.transcribe(audio_path, beam_size = beam_size, word_timestamps=True)
    else:
        segments, _info = model.transcribe(audio_path, beam_size = beam_size, word_timestamps=True, language=language)
    


    if style=="simple":
        #sort words in SRT simple
        srt_lines = styles.sort_in_srt(segments, max_words_per_line)
        extension = ".srt"
    elif style == "karaoke":
        extension = ".ass"
        srt_lines = styles.karaoke_style(segments, max_words_per_line, video_width, video_height)

    # Write subtitle file in disk
    subtitles_path = utils.create_srt_file(output_path, srt_lines, file_name, extension)

    if output_path is not None:
        print("SRT output path: ", output_path)
    else:
        print("SRT output path: ", os.path.dirname(subtitles_path))

    
    # return subtitles_path

    return subtitles_path



def generate_mp4_file(video_name, video_path, srt_file_path, output_path, style):

    if style == "simple":
        styles.render_video(video_path, video_name, srt_file_path, output_path)
    if style == "karaoke":
        styles.render_video(video_path, video_name, srt_file_path, output_path)


if __name__ == "__main__":

    os.system("cls")

    """

    Set up arguments.

    If you need to add or modify command-line arguments for this script,
    you should do so within the `setup_argument_parser` function located
    in the `cli_args.py` file. This centralizes argument definition
    and keeps the main script clean.
    
    """

    parser = setup_argument_parser()

    args = parser.parse_args()


    # COMPROBE IS THE AUDIO/VIDEO FILE EXIST

    if not(os.path.exists(args.video)):
        print("The audio/video file you entered does not exist.")
        sys.exit(1)
    
    
    # VERFICATION FILE TYPE
    elif utils.is_video_file(args.video):
        print("A video file was detected. Extracting audio with ffmpeg...")
        temp_audio_path, video_width, video_height = utils.extract_audio_from_video(args.video)
        srt_file = transcribe_to_srt(
            temp_audio_path, 
            max_words_per_line=args.max_words, 
            performance = args.performance, 
            file_name=args.output_name,
            output_path= args.output_path,
            language= args.lang,
            style = args.style,
            )
        
        # .MP4 OUTPUT
        if args.output_type.lower() == "mp4":
            generate_mp4_file(args.output_name, args.video, srt_file, args.output_path, args.style)

    elif utils.is_audio_file(args.video):
        transcribe_to_srt(
            args.video, 
            max_words_per_line=args.max_words, 
            performance = args.performance, 
            file_name=args.output_name, 
            output_path= args.output_path,
            language= args.lang,
            )
    else:
        print("Only video or audio files")
