# Misti TTS

Misti TTS is a local, terminal-based application for generating normal Text-to-Speech in various Indian languages using open-source **Meta MMS (Massively Multilingual Speech)** models.

This tool does NOT require a reference voice or internet access once the models are downloaded. It generates high-quality audio directly from text.

## Features
- **Normal TTS**: No voice cloning, no reference audio required. Just type and generate.
- **Multilingual**: Supports Hindi, Bengali, Tamil, Telugu, Marathi, Kannada, Malayalam, Gujarati, Punjabi, Odia, Assamese.
- **Local Execution**: Uses `facebook/mms-tts-*` models running locally on CPU or NVIDIA GPU.
- **Direct to MP3**: Output is normalized and directly saved as a 192kbps MP3.

## Prerequisites

- **Python 3.10 or higher**
- **FFmpeg** (Required for MP3 conversion)

### Installing FFmpeg on Windows
You can install FFmpeg using PowerShell with Winget:
```powershell
winget install ffmpeg
```
*Note: Restart your terminal after installing FFmpeg to ensure it is added to your PATH.*

## Setup & Installation

1. **Open PowerShell** and navigate to this project folder:
   ```powershell
   cd d:\mistiii\Misti_TTS
   ```

2. **Create a Virtual Environment**:
   ```powershell
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   *(If you encounter a permissions error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` and try again.)*

4. **Install PyTorch (CUDA recommended for GPU users)**:
   For NVIDIA GPUs, install PyTorch with CUDA for faster generation:
   ```powershell
   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```
   *(If you don't have an NVIDIA GPU, you can skip this step. Standard CPU PyTorch will be installed in the next step, which works fine but is slower).*

5. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## Running the Application

Start the generator by running:
```powershell
python app.py
```

### Example Usage:

```text
========================================
             MISTI TTS
========================================
Normal Indian Text-to-Speech

1. Generate Speech
2. Exit

Choose an option: 1

Select language:
1. Hindi
2. Bengali
3. Tamil
...

Select language: 2

Enter text:
> নমস্কার, আমি মিষ্টি।

Loading TTS model... (May take a moment if downloading for the first time)
[*] Using device: CUDA

Generating speech...

Speech generated successfully.
[*] File saved to: D:\mistiii\Misti_TTS\output\bengali\bengali_20260917_120000.mp3
```
