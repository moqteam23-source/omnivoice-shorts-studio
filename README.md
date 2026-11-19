# OmniVoice Shorts Studio (local GPU)

This runs OmniVoice on your own Windows computer and opens a private local web page in your browser. The browser page is at `http://127.0.0.1:7860`; it is not a public internet link. GitHub cannot remotely start software on your laptop or access its GPU—the launcher must be run on the computer that owns the GPU.

## First-time setup

1. Install Python 3.10 or newer for Windows from [python.org](https://www.python.org/downloads/windows/). During installation, enable **Add Python to PATH**.
2. Download this repository using **Code → Download ZIP**, then extract it.
3. Double-click `start_windows.bat`. On first run it creates a Python environment, installs OmniVoice, and downloads model files. This can take a while and needs internet access and several GB of free storage.
4. The local studio opens in your browser. Keep the black command window open while using it.
5. Upload a short reference clip, paste one script per line, and click **Generate voices**. WAV files are saved in this repository's `outputs` folder.

## Later use

Double-click `start_windows.bat` again. The model files and Python environment stay on the computer, so they are not downloaded from scratch each time. The app uses an NVIDIA GPU with CUDA automatically when available; otherwise it falls back to CPU, which is much slower. First model load and each generation still take time.

## Notes

- This app is bound to `127.0.0.1` and does not create a public Gradio link or expose your computer to the internet.
- Your computer must remain on, and the launcher window must remain open while generating.
- GPU compatibility and available VRAM depend on your computer. An out-of-memory error means the GPU may not have enough VRAM for this model.
- A reference transcript is optional; if left blank, OmniVoice may download/load an automatic speech-recognition model.
- Only clone voices you own or have permission to use.
