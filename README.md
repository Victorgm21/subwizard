# 🎬 SubWizard: Your Magical Subtitle Assistant 🧙‍♂️

<p align="center">
  <img src="https://iili.io/KASOvWX.jpg" alt="SubWizard's graphical user interface">
</p>

SubWizard is a powerful and user-friendly tool that automatically generates subtitles for your video and audio files. It leverages the impressive speed and accuracy of `faster-whisper` to transcribe spoken content. Whether you need an `.srt` file or want to burn the subtitles directly into your `.mp4` video, SubWizard has you covered.

## ✨ Features

* **Fast & Accurate Transcription:** Powered by `faster-whisper` for efficient and precise speech-to-text conversion.
* **Flexible Output:** Generate standard `.srt` subtitle files or a new `.mp4` video with the subtitles permanently "burned in."
* **Intuitive GUI:** A clean and easy-to-use graphical user interface built with `tkinter` that works on Windows, macOS, and Linux.
* **Automatic FFmpeg Installation:** The program includes a script to automatically download and set up FFmpeg binaries in a local directory. This means you don't need to install FFmpeg globally, as SubWizard will manage its own dependency.
* **Performance Profiles:** Choose from different profiles (`efficient`, `normal`, `detailed`, `ultra-detailed`) to balance speed and accuracy, leveraging GPU acceleration if available.
* **Language Detection:** Automatically detects the language of the audio, or you can specify it manually for better results.
* **Command-Line Interface (CLI):** For advanced users, a robust CLI is available for automated workflows and scripting.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher.
* **FFmpeg** is required for audio extraction and subtitle burning. This program will download and install the necessary FFmpeg binaries automatically for you in a local directory, so no manual installation is needed.

### Installation

1.  Clone this repository:
    ```bash
    git clone [https://github.com/Victorgm21/subwizard.git](https://github.com/Victorgm21/subwizard.git)
    cd subwizard
    ```
2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    This will install `faster-whisper` and other dependencies.

---

## 🖥️ Usage

### Using the Graphical User Interface (GUI)

The easiest way to use SubWizard is with its intuitive GUI. Simply run:
```bash
python gui.py
This will open a window where you can:

Browse for your video or audio file.

Adjust settings like words per line, performance, and output format.

Specify the output file name and destination folder.

Click "Generate Subtitles" to start the process.

Using the Command-Line Interface (CLI)
For command-line enthusiasts, you can use the sub_wizard.py script directly.

Example Command
This command transcribes the video juli.mp4, limits each subtitle line to 3 words, sets the output file name to juli_sub, saves the output as a new MP4 video with burned-in subtitles, and automatically detects the language.

Bash

python sub_wizard.py "C:/Users/user/Desktop/juli.mp4" --output-path "C:/Users/user/Desktop" --max-words 3 --performance normal --output-name juli_sub --output-type mp4 --lang auto
For a full list of available arguments, use the --help flag:

Bash

python sub_wizard.py --help
🛠️ Project Structure
sub_wizard.py: The main script that handles the core logic for transcription and subtitle burning.

gui.py: The graphical user interface, built with tkinter, that provides an easy-to-use frontend.

cli_args.py: Defines and sets up the command-line arguments using argparse. This keeps the main script clean.

utils.py: Contains utility functions for file handling, audio extraction (ffmpeg), and timestamp formatting.

fmpeg_installer.py: Manages the local installation of ffmpeg for Windows users.

requirements.txt: Lists the necessary Python libraries.

🤝 Contributing
We welcome contributions! Feel free to open an issue or submit a pull request if you have ideas for new features, bug fixes, or improvements.