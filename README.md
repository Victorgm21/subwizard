# 🎬 SubWizard: Your Magical Subtitle Assistant 🧙‍♂️

<p align="center">
  <img src="https://images.unsplash.com/photo-1620786938928-863a3a416b71?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1MDcxMzJ8MHwxfHNlYXJjaHwxfHx3aXphcmQlMjBjcmVhdGluZyUyMHN1YnRpZGxlc3xlbnwwfHx8fDE3MjY1MTk0OTZ8MA&ixlib=rb-4.0.3&q=80&w=1080" alt="A wizard creating subtitles">
</p>

SubWizard is a powerful and user-friendly tool that automatically generates subtitles for your video and audio files. It leverages the impressive speed and accuracy of `faster-whisper` to transcribe spoken content. Whether you need an `.srt` file or want to burn the subtitles directly into your `.mp4` video, SubWizard has you covered.

## ✨ Features

* **Fast & Accurate Transcription:** Powered by `faster-whisper` for efficient and precise speech-to-text conversion.
* **Flexible Output:** Generate standard `.srt` subtitle files or a new `.mp4` video with the subtitles permanently "burned in."
* **Cross-Platform GUI:** A clean and intuitive graphical user interface built with `tkinter` makes it easy to use on Windows, macOS, and Linux.
* **Performance Profiles:** Choose from different profiles (`efficient`, `normal`, `detailed`, `ultra-detailed`) to balance speed and accuracy, leveraging GPU acceleration if available.
* **Language Detection:** Automatically detects the language of the audio, or you can specify it manually for better results.
* **Command-Line Interface (CLI):** For advanced users, a robust CLI is available for automated workflows and scripting.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher.
* `ffmpeg` for extracting audio from video and burning subtitles. SubWizard includes an automatic installer for Windows users.

### Installation

1.  Clone this repository:
    ```bash
    git clone [https://github.com/your-username/sub-wizard.git](https://github.com/your-username/sub-wizard.git)
    cd sub-wizard
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

Basic Usage
Generate an .srt file for a video:

Bash

python sub_wizard.py "path/to/your/video.mp4"
The .srt file will be saved in the same directory as the video.

Advanced Options
Specify output path:

Bash

python sub_wizard.py "path/to/video.mp4" --output-path "/Users/You/Documents/MySubtitles"
Burn subtitles into a new video:

Bash

python sub_wizard.py "path/to/video.mp4" --output-type mp4 --output-name "video_with_subs"
This will create video_with_subs.mp4 with the subtitles embedded.

Set a specific language:

Bash

python sub_wizard.py "path/to/video.mp4" --lang en
Choose a performance profile:

Bash

python sub_wizard.py "path/to/video.mp4" --performance ultra-detailed
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