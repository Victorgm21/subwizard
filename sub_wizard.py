import warnings
# Suprime el UserWarning específico de pkg_resources
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API",
    category=UserWarning
)
import os
from faster_whisper import WhisperModel
import torch
from utils import utils
from cli_args import setup_argument_parser
import sys, io

# Reconfigurar stdout/stderr a UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")



def transcribe_to_srt(
    audio_path, 
    output_path=None, 
    max_words_per_line=5, 
    performance = "normal", 
    file_name = "subs",
    language = None,
    ):

    model_size = "small"
    beam_size = 5
    compute_type="int8"
    device = "cpu"
        
    if (performance == "efficient" ):
        model_size = "base"
        beam_size = 3
        compute_type="int8"
    elif(performance == "normal"):
        model_size = "small"
        beam_size = 5
        compute_type="int8"
    elif(performance == "detailed"):
        model_size = "medium"
        beam_size = 10
        compute_type="float32"
    elif(performance == "ultra-detailed"):
        model_size = "large"
        beam_size = 10
        compute_type="float32"    
    
    # GPU IS AVAILABLE ?
    if(torch.cuda.is_available()):
        print("✨ Detected: GPU available! Optimizing for maximum speed.")
        device = "cuda"
        compute_type = "float16"
    else:
        print("🐌 No GPU detected. Proceeding with CPU, which may be slower.")
    
    

    
    print(f"⚙️ The '{model_size}' model is now processing your audio. Generating transcription!")
    # Load model
    model = WhisperModel(model_size, device= device, compute_type= compute_type)


    if language != None or language == "auto":
        segments, _info = model.transcribe(audio_path, beam_size = beam_size, word_timestamps=True)
    else:
        segments, _info = model.transcribe(audio_path, beam_size = beam_size, word_timestamps=True, language=language)
    
    srt_lines = []
    group = []
    index = 1

    previous_group_end = None

    for segment in segments:
        words = segment.words
        i = 0

        while i < len(words):
            group = words[i:i+max_words_per_line]
            start_time = group[0].start
            if i + max_words_per_line < len(words):
                end_time = words[i + max_words_per_line].start
            else:
                end_time = group[-1].end

            text = " ".join(w.word for w in group)
            srt_lines.append(f"{index}\n{utils.format_timestamp(start_time)} --> {utils.format_timestamp(end_time)}\n{text}\n")
            index += 1
            i += max_words_per_line
    # Save remaining words
    if group:
        start = utils.format_timestamp(group[0].start)
        end = utils.format_timestamp(group[-1].end)
        text = " ".join(w.word for w in group)
        srt_lines.append(f"{index}\n{start} --> {end}\n{text}\n")


    # Write SRT file

    srt_path = utils.create_srt_file(output_path, srt_lines, file_name)

    if(output_path != None):
        print("🎞️ SRT output path: ", output_path)
    else:
        print("🎞️ SRT output path: ", os.path.dirname(srt_path))

    
    # return SRT PATH

    return srt_path



def generate_mp4_file(video_name, video_path, srt_file_path, output_path):
    if args.video and utils.is_video_file(args.video):
        try:
            utils.burn_subtitles_into_video(video_name, video_path, srt_file_path, output_path)
        except Exception as e:
            print(f"error: {e}")
        finally:
            pass
    else:
        print("invalid video file")

    
    
    



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


    # PARSE INPUTS

    # PARSE INPUTS

    if args.output_path != None:
        #args.output_path = utils.normalize_path(args.output_path)
        pass


    # COMPROBE IS THE AUDIO/VIDEO FILE EXIST

    if not(os.path.exists(args.video)):
        print("The audio/video file you entered does not exist.")
        sys.exit(1)
    


    if (args.srt_path != None):
        if not(os.path.exists(args.srt_path)):
            print("The .srt path that you entered does not exist.")
            sys.exit(1)
            
    
    # VERFICATION FILE TYPE
    elif utils.is_video_file(args.video):
        print("🎬 A video file was detected. Extracting audio with ffmpeg...")
        temp_audio_path = utils.extract_audio_from_video(args.video)
        srt_file = transcribe_to_srt(
            temp_audio_path, 
            max_words_per_line=args.max_words, 
            performance = args.performance, 
            file_name=args.output_name,
            output_path= args.output_path,
            language= args.lang,
            )
        
        # .MP4 OUTPUT
        if args.output_type.lower() == "mp4":
            generate_mp4_file(args.output_name, args.video, srt_file, args.output_path)

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
        print("❌ Only video or audio files")
