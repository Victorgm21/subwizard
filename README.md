# 🎬 SubWizard: Your Magical Subtitle Assistant 🧙‍♂️

<p align="center">
  <img src="https://i.ibb.co/mpzpvdQ/Screenshot-1.png" alt="SubWizard's graphical user interface" width="600">
</p>

<p align="center">
  <a href="https://paypal.me/victorgouveia17">
    <img src="https://img.shields.io/badge/Donate-PayPal-blue.svg?style=for-the-badge&logo=paypal" alt="Donate with PayPal">
  </a>
</p>

<p align="center">
  <a href="https://github.com/Victorgm21/subwizard/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Victorgm21/subwizard" alt="License"></a>
  <a href="https://www.python.org/downloads/release/python-380/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+"></a>
</p>

SubWizard is a powerful and user-friendly tool that automatically generates subtitles for your video and audio files (ONLY WINDOWS). It leverages the impressive speed and accuracy of `faster-whisper` to transcribe spoken content. Whether you need an `.srt` file or want to burn the subtitles directly into your `.mp4` video, SubWizard has you covered.

---

## ✨ Features

- **Fast & Accurate Transcription:** Powered by `faster-whisper` for efficient and precise speech-to-text conversion.
- **Multiple Subtitle Styles:**
  - **Simple:** Classic subtitle style.
  - **Karaoke:** Highlighting words as they are spoken.
  - **Word pop:** Words appear with a "pop" animation.
  - **Zoom in:** Dynamic zoom effect on subtitles.
- **Flexible Output:** Generate standard `.srt` / `.ass` subtitle files or a new `.mp4` video with the subtitles permanently "burned in."
- **Intuitive GUI:** A clean and easy-to-use graphical user interface that works on Windows.
- **Automatic FFmpeg Handling:** SubWizard automatically downloads and manages its own FFmpeg dependency, so you don't need to install it globally.
- **Performance Profiles:** Choose from different profiles to balance speed and accuracy:
  - `efficient` (base model)
  - `normal` (small model)
  - `detailed` (medium model)
  - `ultra-detailed` (large model)
- **Language Detection:** Automatically detects the audio language, or you can specify it manually for better results.
- **Command-Line Interface (CLI):** A robust CLI is available for advanced users and automation.

---

## 🛠️ Technologies Used

- **Python:** The core programming language.
- **Faster-Whisper:** For high-performance transcription.
- **PyWebView:** For the modern and cross-platform graphical user interface.
- **FFmpeg:** For audio extraction and subtitle integration.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher.

### Installation

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/Victorgm21/subwizard.git
    cd subwizard
    ```
2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🖥️ Usage

### Using the Graphical User Interface (GUI)

The easiest way to use SubWizard is with its intuitive GUI. Simply run:
```bash
python gui.py
```
This will open a window where you can:

1.  Browse for your video or audio file.
2.  Adjust settings like words per line, performance, output format and subtitle style.
3.  Specify the output file name and destination folder.
4.  Click "Generate Subtitles" to start the process.

### Using the Command-Line Interface (CLI)

For command-line enthusiasts, you can use the `subwizard.py` script directly.

**Basic Usage:**
```bash
python subwizard.py path/to/video.mp4
```

**Advanced Example:**

This command transcribes `video.mp4`, limits each subtitle line to 3 words, uses the `detailed` performance profile, sets the output file name to `my_subs`, saves it as an MP4 with `karaoke` style subtitles, and specifies the language as Spanish.

```bash
python subwizard.py video.mp4 --max-words 3 --performance detailed --output-name my_subs --output-type mp4 --style karaoke --lang es
```

**Full List of Arguments:**

| Argument | Description | Default |
| :--- | :--- | :--- |
| `video` | Path to the video or audio file | (Required) |
| `--max-words` | Number of words per line | `3` |
| `--performance` | Performance profiles: `efficient`, `normal`, `detailed`, `ultra-detailed` | `normal` |
| `--output-name` | Set the file name for the output | `automatic_subtitles_ready` |
| `--output-path` | Set the subtitle output path | `None` |
| `--output-type` | Set file output type: `srt` / `mp4` | `mp4` |
| `--lang` | Set the original language from the video (e.g., `en`, `es`, `fr`) | `None` (Auto) |
| `--style` | Choose the style: `simple`, `karaoke`, `word-pop`, `zoom-in` | `simple` |
| `--subtitle-path` | Burns existing .SRT or .ASS into a video | `None` |

For more info, use the `--help` flag:
```bash
python subwizard.py --help
```
