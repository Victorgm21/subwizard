import os
import platform
import shutil
import zipfile
import requests



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE_DIR, "..", "tools")  
FFMPEG_DIR = os.path.join(TOOLS_DIR, "ffmpeg")
FFMPEG_BIN = os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg")


def get_ffmpeg_path():
    # FMPEG IN SYSTEM PATH?
    """
    ffmpeg_global = shutil.which("ffmpeg")
    if ffmpeg_global:
        return ffmpeg_global
    """

    # CHECK LOCAL INSTALL
    if os.path.isfile(FFMPEG_BIN):
        return FFMPEG_BIN

    return None


def install_ffmpeg_windows():
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(TOOLS_DIR, "ffmpeg.zip")
    extract_path = TOOLS_DIR

    os.makedirs(TOOLS_DIR, exist_ok=True)
    print("⬇️ Downloading FFmpeg for Windows...")

    response = requests.get(url)
    with open(zip_path, "wb") as f:
        f.write(response.content)

    print("📦 Extracting FFmpeg...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    # Search for ffmpeg.exe
    ffmpeg_exe = None
    for root, _, files in os.walk(extract_path):
        if "ffmpeg.exe" in files:
            ffmpeg_exe = os.path.join(root, "ffmpeg.exe")
            break

    if ffmpeg_exe:
        bin_dir = os.path.join(FFMPEG_DIR, "bin")
        os.makedirs(bin_dir, exist_ok=True)
        shutil.move(ffmpeg_exe, os.path.join(bin_dir, "ffmpeg.exe"))

    os.remove(zip_path)
    print("✅ FFmpeg installed locally in tools/ffmpeg/bin")


def ensure_ffmpeg():
    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path:
        return ffmpeg_path

    if platform.system() == "Windows":
        install_ffmpeg_windows()
        return get_ffmpeg_path()
    else:
        print("❌ FFmpeg is not available and automatic download is not yet implemented for your OS.")
        print("ℹ️ Install it manually from https://ffmpeg.org/download.html")
        exit(1)
