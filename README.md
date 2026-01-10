# 🎬 SubWizard: Your Magical Subtitle Assistant 🧙‍♂️

<p align="center">
  <img src="https://i.ibb.co/mpzpvdQ/Screenshot-1.png" alt="SubWizard's graphical user interface" width="600">
</p>

<p align="center">
  <a href="https://github.com/Victorgm21/subwizard/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Victorgm21/subwizard" alt="License"></a>
  <a href="https://www.python.org/downloads/release/python-380/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+"></a>
</p>

SubWizard is a powerful and user-friendly tool that automatically generates subtitles for your video and audio files. It leverages the impressive speed and accuracy of `faster-whisper` to transcribe spoken content. Whether you need an `.srt` file or want to burn the subtitles directly into your `.mp4` video, SubWizard has you covered.

---

## ✨ Features

- **Fast & Accurate Transcription:** Powered by `faster-whisper` for efficient and precise speech-to-text conversion.
- **Flexible Output:** Generate standard `.srt` subtitle files or a new `.mp4` video with the subtitles permanently "burned in."
- **Intuitive GUI:** A clean and easy-to-use graphical user interface that works on Windows, macOS, and Linux.
- **Automatic FFmpeg Handling:** SubWizard automatically downloads and manages its own FFmpeg dependency, so you don't need to install it globally.
- **Performance Profiles:** Choose from different profiles (`efficient`, `normal`, `detailed`, `ultra-detailed`) to balance speed and accuracy, with GPU acceleration if available.
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
2.  Adjust settings like words per line, performance, and output format.
3.  Specify the output file name and destination folder.
4.  Click "Generate Subtitles" to start the process.

### Using the Command-Line Interface (CLI)

For command-line enthusiasts, you can use the `subwizard.py` script directly.

**Example Command:**

This command transcribes `juli.mp4`, limits each subtitle line to 3 words, sets the output file name to `juli_sub`, saves the output as a new MP4 video with burned-in subtitles, and automatically detects the language.

```bash
python subwizard.py "C:/Users/user/Desktop/juli.mp4" --output-path "C:/Users/user/Desktop" --max-words 3 --performance normal --output-name juli_sub --output-type mp4 --lang auto
```

For a full list of available arguments, use the `--help` flag:
```bash
python subwizard.py --help
```

---

## 🤝 Contributing

We welcome contributions! Feel free to open an issue or submit a pull request if you have ideas for new features, bug fixes, or improvements.
