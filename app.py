import os
import re
from pathlib import Path

import gradio as gr
import soundfile as sf
import torch
from omnivoice import OmniVoice

APP_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = APP_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
MODEL_ID = os.environ.get("OMNIVOICE_MODEL", "k2-fsa/OmniVoice")


def load_model():
    if torch.cuda.is_available():
        device = "cuda:0"
        dtype = torch.float16
        print(f"Loading OmniVoice on NVIDIA GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = "cpu"
        dtype = torch.float32
        print("NVIDIA CUDA GPU not detected; loading on CPU (this will be much slower).")
    return OmniVoice.from_pretrained(MODEL_ID, device_map=device, dtype=dtype)


model = load_model()


def make_audio(reference_audio, reference_text, scripts, language):
    if not reference_audio:
        raise gr.Error("Please upload a voice reference audio clip first.")
    script_items = [line.strip() for line in scripts.splitlines() if line.strip()]
    if not script_items:
        raise gr.Error("Paste at least one script, with each short on its own line.")

    ref_text = reference_text.strip() or None
    saved = []
    for i, text in enumerate(script_items, start=1):
        generated = model.generate(
            text=text,
            language=language.strip() or None,
            ref_audio=reference_audio,
            ref_text=ref_text,
        )
        safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", text[:30]).strip("_") or "short"
        path = OUTPUT_DIR / f"short_{i:02d}_{safe_name}.wav"
        sf.write(str(path), generated[0], model.sampling_rate)
        saved.append(str(path))
    return saved


with gr.Blocks(title="OmniVoice Shorts Studio") as demo:
    gr.Markdown(
        "# OmniVoice Shorts Studio\n"
        "Paste scripts (one short per line), upload a reference voice clip, and generate WAV files. "
        "Files are saved on this computer in the `outputs` folder. Use only a voice you own or have permission to clone."
    )
    with gr.Row():
        with gr.Column():
            reference = gr.Audio(label="Reference voice (3–10 seconds recommended)", type="filepath")
            transcript = gr.Textbox(label="Reference transcript (optional)", lines=2,
                                     placeholder="Enter the exact words in the reference clip; blank uses automatic transcription.")
            language = gr.Textbox(label="Language (optional)", placeholder="e.g. Urdu, English, or leave blank for automatic")
        with gr.Column():
            scripts = gr.Textbox(label="Short scripts — one per line", lines=12,
                                 placeholder="Paste each short script on a separate line.")
            files = gr.File(label="Generated WAV files", file_count="multiple")
            generate = gr.Button("Generate voices", variant="primary")
    generate.click(make_audio, inputs=[reference, transcript, scripts, language], outputs=files)

demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True, share=False)
