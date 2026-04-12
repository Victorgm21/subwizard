import utils


def render_video(video_path, video_name, srt_file_path, output_path):
    if utils.is_video_file(video_path):
        try:
            utils.burn_subtitles_into_video(video_name, video_path, srt_file_path, output_path)
        except Exception as e:
            print(f"error: {e}")
        finally:
            pass
    else:
        print("invalid video file")