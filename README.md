# 🎬 SubWizard — Videos Powered by AI 🧙‍♂️

<p align="center">
  <img src="assets/screenshot.png" alt="SubWizard - Main Generator Screen" width="850">
</p>

<p align="center">
  <a href="https://paypal.me/victorgouveia17">
    <img src="https://img.shields.io/badge/Donate-PayPal-7c3aed.svg?style=for-the-badge&logo=paypal" alt="Donate with PayPal">
  </a>
</p>

<p align="center">
  <a href="https://github.com/Victorgm21/subwizard/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Victorgm21/subwizard?color=8b5cf6" alt="License"></a>
  <a href="https://www.python.org/downloads/release/python-380/"><img src="https://img.shields.io/badge/python-3.8+-8b5cf6.svg" alt="Python 3.8+"></a>
  <img src="https://img.shields.io/badge/UI-macOS%20Dark%20%2F%20Apple%20Style-202026.svg" alt="macOS Apple Dark UI">
  <img src="https://img.shields.io/badge/Language-English%20%7C%20Espa%C3%B1ol-8b5cf6.svg" alt="i18n Bilingual">
</p>

**SubWizard** is an all-in-one desktop AI video suite designed to automate video subtitling and social-media content creation. Featuring studio-grade animated typography (Shorts, Reels, TikTok), smart audio censorship with soft beeping, Whisper model cache management, and a refined Apple-inspired dark interface, SubWizard turns raw videos into polished viral content in seconds.

---

## 📸 Screenshots Showcase

<details open>
<summary><b>🖼️ View Interface Gallery (Generator, Appearance, Banned Words, Options)</b></summary>
<br>

| 1. Generator & Batch Processing | 2. Appearance & Animation Studio |
| :---: | :---: |
| ![Generator Screen](assets/screenshot.png) | ![Appearance Screen](assets/screenshot_appearance.png) |

| 3. Banned Words & Audio Censorship | 4. Program Options & Model Manager |
| :---: | :---: |
| ![Banned Words Screen](assets/screenshot_banned.png) | ![Options Screen](assets/screenshot_options.png) |

</details>

---

## ✨ Features & Recent Improvements

### 🎨 1. Apple-Inspired Native Dark Interface
- **Cohesive Dark Palette:** Unified, matte dark tones (`#16161a`, `#19191e`, `#202026`) that eliminate disjointed backgrounds for a seamless macOS glass/aluminum aesthetic.
- **Modern Purple Accent:** Refined Apple-style purple accent (`#8b5cf6`) across active tabs, primary action buttons, checkboxes, and sliders without distracting bright glow or excessive drop-shadows.
- **Clean Iconography:** Minimalist SVG icons placed strictly on sidebar navigation and section headings, keeping individual setting rows clutter-free.
- **Widened Adaptive Canvas:** Native 1260×840 viewport ensuring comfortable right margins and consistent padding on any monitor resolution.

### 🎙️ 2. Accurate AI Transcription (`faster-whisper`)
- **Word-Level Timestamps:** High-precision synchronization for word-by-word animated highlights.
- **Anti-Hallucination Filter (VAD):** Integrated Silero Voice Activity Detector (VAD) that removes background noise hallucinations during silence.
- **Hardware Acceleration:** Automatic GPU acceleration (`CUDA` `float16`) with automatic CPU fallback.
- **Whisper Performance Profiles:**
  - `Efficient` (`base`, `beam_size=3`)
  - `Normal` (`small`, `beam_size=5`)
  - `Detailed` (`medium`, `beam_size=10`)
  - `Ultra-detailed` (`large`, `beam_size=20`)
- **Spoken Language:** Auto-detection or manual selection (`English`, `Spanish`, `French`, `German`, `Japanese`, `Korean`, etc.).

### 📁 3. Single File & Batch Directory Processing
- **Single File Mode:** Transcribe individual video or audio files.
- **Folder Batch Mode:** Select an entire directory to batch-process all media files in a single pass while reusing the loaded model in memory.
- **Smart Destination:** Defaults the destination path to the source directory and features one-click buttons to open the folder or launch the subtitled video.

### 🎞️ 4. Dynamic Live Preview & Subtitle Styles
- **Real-Time Interactive Preview:** The live preview stage faithfully renders each chosen subtitle style:
  - **Simple (`.srt`):** Classic, clean text lines.
  - **Karaoke (`.ass`):** Word-by-word color highlight synchronization.
  - **Word Pop (`.ass`):** Dynamic scale pop animation with highlight color on spoken words.
  - **Zoom In (`.ass`):** Smooth entrance zoom animation for each line.
- **Live Frame Extraction:** Automatically grabs a random frame from your loaded video to preview typography against actual video contrast and aspect ratio (`16:9` landscape or `9:16` vertical).

### 🎛️ 5. Typography & Formatting Controls
- **Windows System Fonts:** Reads all system and user fonts directly from the Windows Registry.
- **Customizable Styling:** Font size (`px`), bold, italic, uppercase (**ALL CAPS**), and **remove punctuation** toggle for ultra-clean Shorts/Reels aesthetics.
- **Colors & Transparency:** Customizable primary text, active word highlight, outline thickness & color, and background shadow with 0–100% opacity slider.
- **Screen Positioning:** Top center, Middle center, and Bottom center with adjustable vertical margin.

### 🔇 6. Banned Words & Audio Censorship (Soft Beep)
- **Automatic Text Censorship:** Replaces prohibited keywords with asterisks (`***`) across all subtitle styles.
- **Soft Audio Beep:** Automatically cuts original audio during banned words and inserts a gentle sine-wave beep.
- **Volume Slider & Testing:** Adjust the beep loudness from 0% to 100% and listen to a real-time audio test before rendering.

### 🌐 7. Program Options & Bilingual Interface
- **Instant Language Switching:** Seamlessly switch the entire UI between **English** and **Español** with persistent configuration.
- **Installed Whisper Models Manager:**
  - Lists all models stored in your Hugging Face / faster-whisper cache directory.
  - Displays individual and total disk space used (e.g., `463.7 MB`, `753.8 MB`).
  - **Delete Model** button to free up gigabytes of drive space with a single click.
  - Quick link to open the cache directory directly in Windows Explorer.

---

## 🔮 Roadmap / Future Vision

SubWizard is evolving into a comprehensive AI video automation workstation:

- [ ] **AI Podcast Auto-Clipping:** Automatically detect highlights, engaging topics, and hook sentences from long-form video podcasts.
- [ ] **Active-Speaker Auto-Framing:** Detect faces and dynamically crop landscape (`16:9`) videos into vertical (`9:16`) format, automatically panning toward whoever is speaking.
- [ ] **Silence & Dead-Air Removal:** Auto-detect and trim silent pauses and filler words.
- [ ] **Automated B-Roll Insertion:** Fetch contextual visuals and clips based on speech semantics.

---

## 📂 Supported Formats

- **Video:** `.mp4`, `.mkv`, `.mov`, `.avi`, `.flv`, `.webm`
- **Audio:** `.mp3`, `.wav`, `.aac`, `.flac`, `.m4a`, `.ogg`

---

## 🛠️ Tech Stack

- **Python 3.8+:** Core business logic, subtitle synthesis, and audio processing.
- **faster-whisper & PyTorch:** High-performance, memory-efficient speech recognition.
- **PyWebView:** Lightweight, native desktop client with hardware-accelerated WebKit/Blink engine.
- **FFmpeg & FFprobe:** Audio extraction, resolution parsing, and hardware-friendly subtitle burning.

---

## 🚀 Installation & Quick Start

### Prerequisites
- **OS:** Windows 10 / 11 (64-bit)
- **Python:** 3.8 to 3.14
- *Optional:* NVIDIA GPU with CUDA drivers for ultra-fast transcription.

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Victorgm21/subwizard.git
   cd subwizard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch SubWizard:**
   ```bash
   python subwizard.py
   ```
   *(SubWizard will automatically detect or download portable FFmpeg binaries on first run if not found on your system).*

---

## 💡 How to Use

1. **Select Source Media:**
   - Under **Origin (Input)**, choose **Select File** for a single video/audio, or **Select Folder** for batch operations.
2. **Configure Style & Destination:**
   - Pick your desired subtitle style (`Karaoke`, `Word Pop`, `Zoom In`, etc.) and output format (`Only Video`, `Only Subtitles`, or `Both`).
   - Customize fonts, colors, and margins in the **Appearance** tab.
3. **Set Censorship & Language (Optional):**
   - Add restricted keywords in the **Banned Words** tab and adjust the beep volume.
   - Switch program language or manage installed models in the **Options** tab.
4. **Generate:**
   - Click **Generate Subtitles** and watch the real-time progress bar and status updates in the footer.
   - Once finished, click **Open Output Folder** to view your ready-to-publish video!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
