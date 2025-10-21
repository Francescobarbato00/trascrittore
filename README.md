# 🎧 Trascrittore Audio/Video — Desktop Software  
### by **Ing. Francesco Barbato**

> A standalone desktop application for **automatic transcription** of audio and video files using **OpenAI Whisper**, featuring a clean UI, dark/light mode, real progress tracking, and a full Windows installer.

---

## 🧩 Overview

The **Audio/Video Transcriber** is a Python-based desktop tool that automates speech-to-text transcription for a wide range of file formats.  
It combines the power of **OpenAI Whisper**, **FFmpeg**, and **CustomTkinter** to provide a simple yet professional user interface — all packaged as a single Windows executable.

The software is ideal for professionals, journalists, researchers, and developers who need fast, local, and accurate transcription without relying on cloud APIs.

---

## ⚙️ Key Features

✅ **Automatic Transcription** – Converts audio/video into text using the OpenAI Whisper model  
✅ **Multi-format Support** – Compatible with MP3, MP4, WAV, AVI, and more  
✅ **Modern Interface** – Built with CustomTkinter (dark/light theme support)  
✅ **Progress Feedback** – Real-time progress bar synchronized with the transcription process  
✅ **Splash Screen & Branding** – Professional startup screen and custom icons  
✅ **Standalone Installer** – Built with Inno Setup for seamless Windows installation  
✅ **Offline Processing** – No external dependencies once installed  

---

## 🧠 Technologies Used

| Technology | Purpose |
|-------------|----------|
| **Python 3.x** | Core programming language |
| **CustomTkinter** | Modern GUI for desktop applications |
| **FFmpeg** | Audio/video decoding and extraction |
| **OpenAI Whisper** | AI model for multilingual speech recognition |
| **PyInstaller** | Packaging Python app into `.exe` |
| **Inno Setup** | Windows installer creation and branding |

---

## 🧰 Development Process

> A brief overview of the project lifecycle and build pipeline.

1. 🎨 **Design & Planning** — Interface mockups and UX workflow  
2. 🧠 **Model Integration** — Implementation of OpenAI Whisper for transcription  
3. 💻 **GUI Implementation** — Interactive layout using CustomTkinter  
4. 🎧 **Audio/Video Handling** — Managed via FFmpeg backend  
5. ⚙️ **Packaging** — PyInstaller used to bundle dependencies  
6. 🧪 **Testing & Debugging** — Validation on multiple file formats  
7. 🚀 **Deployment** — Final installer built with Inno Setup  

---

## 🧾 Project Structure

VideoAudioExtractor/
│
├── main.py # Main Python script (GUI + logic)
├── installer_script.iss # Inno Setup installer configuration
├── LICENSE.txt # License file
├── fonts/ # Custom fonts (Titillium Web family)
├── icona/ # App icon and branding
├── dist/ # Build artifacts (PyInstaller output)
└── output/ # Final installer (.exe)

yaml
Copia codice

---

## 🚀 Installation & Usage

### 🪄 Option 1 — Download Prebuilt Installer
Download the latest version here:  
👉 [**Download via Mega**](https://mega.nz/folder/X9QxDARS#4O1z5ppcHODleiAOQu5RdQ)

Run the `.exe` installer and follow on-screen instructions.

### 🧑‍💻 Option 2 — Build from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/Francescobarbato00/trascrittore.git
   cd trascrittore
Install dependencies:

bash
Copia codice
pip install -r requirements.txt
Run the app:

bash
Copia codice
python main.py
To create the .exe:

bash
Copia codice
pyinstaller --onefile --noconsole --icon=icona/icon.ico main.py
🧪 Example Screenshot
<p align="center"> <img src="https://github.com/Francescobarbato00/trascrittore/blob/main/trascrittore.png" width="600" alt="Trascrittore App Preview"> </p>
📦 Packaging Details
Executable Generator: PyInstaller

Installer Builder: Inno Setup Compiler

Architecture Target: Windows x64

Approximate Size: ~220MB (includes Whisper model + FFmpeg)

🧭 Future Improvements
Add live transcription from microphone input

Introduce multi-language interface

Optimize Whisper model size with quantization

Support macOS/Linux packaging

🧑‍💼 Author
Francesco Barbato
Software Engineer & AI Developer
📧 Contact via LinkedIn

🪪 License
This project is distributed under the MIT License.
See the LICENSE file for more details.

⭐ If you like this project, consider starring it on GitHub!
Your support helps improve and maintain future updates.

