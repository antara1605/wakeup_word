import os
import time
import winsound

import torch
import soundfile as sf
from transformers import VitsModel, AutoTokenizer


# ============================================================
# MISTI TTS
# Normal Indian Text-to-Speech
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUT_DIR, exist_ok=True)


LANGUAGES = {
    "1": {
        "name": "Hindi",
        "model": "facebook/mms-tts-hin"
    },
    "2": {
        "name": "Bengali",
        "model": "facebook/mms-tts-ben"
    },
    "3": {
        "name": "Tamil",
        "model": "facebook/mms-tts-tam"
    },
    "4": {
        "name": "Telugu",
        "model": "facebook/mms-tts-tel"
    },
    "5": {
        "name": "Marathi",
        "model": "facebook/mms-tts-mar"
    },
    "6": {
        "name": "Kannada",
        "model": "facebook/mms-tts-kan"
    },
    "7": {
        "name": "Malayalam",
        "model": "facebook/mms-tts-mal"
    },
    "8": {
        "name": "Gujarati",
        "model": "facebook/mms-tts-guj"
    },
    "9": {
        "name": "Punjabi",
        "model": "facebook/mms-tts-pan"
    },
    "10": {
        "name": "Odia",
        "model": "facebook/mms-tts-ory"
    },
    "11": {
        "name": "Assamese",
        "model": "facebook/mms-tts-asm"
    }
}


def select_language():
    print("\n========================================")
    print("             MISTI TTS")
    print("========================================")
    print("Normal Indian Text-to-Speech\n")

    for key, language in LANGUAGES.items():
        print(f"{key}. {language['name']}")

    print()

    choice = input("Select language: ").strip()

    if choice not in LANGUAGES:
        print("[!] Invalid language selection.")
        return None

    return LANGUAGES[choice]


def generate_speech(language):
    selected_lang = language["name"]
    model_id = language["model"]

    print(f"\n[*] Selected language: {selected_lang}")
    print(f"[*] Model: {model_id}")

    text = input("\nEnter text:\n> ").strip()

    if not text:
        print("[!] Text cannot be empty.")
        return

    # --------------------------------------------------------
    # Device
    # --------------------------------------------------------

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("\nLoading TTS model...")
    print(f"[*] Using device: {device}")

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    print(f"[*] Loading model: {model_id}")

    try:
        model = VitsModel.from_pretrained(model_id).to(device)
        tokenizer = AutoTokenizer.from_pretrained(model_id)

        model.eval()

        print("[*] Model loaded successfully.")

    except Exception as e:
        print("\n[!] Failed to load model.")
        print(f"Error: {type(e).__name__}: {e}")
        return

    # --------------------------------------------------------
    # Tokenization
    # --------------------------------------------------------

    print("\nGenerating speech...")

    try:
        inputs = tokenizer(
            text,
            return_tensors="pt"
        )

        # Make sure input IDs exist
        if "input_ids" not in inputs:
            print("[!] Tokenizer did not produce input IDs.")
            return

        # Make sure text produced tokens
        if inputs["input_ids"].shape[1] == 0:
            print("[!] The entered text produced zero tokens.")
            print("[!] Please enter text using the selected language/script.")
            return

        inputs["input_ids"] = inputs["input_ids"].long()

        inputs = {
            key: value.to(device)
            for key, value in inputs.items()
        }

        print(f"[*] Input IDs dtype: {inputs['input_ids'].dtype}")
        print(f"[*] Input shape: {tuple(inputs['input_ids'].shape)}")

        # ----------------------------------------------------
        # TTS generation
        # ----------------------------------------------------

        with torch.inference_mode():
            output = model(**inputs).waveform

        waveform = output.cpu().numpy().squeeze()

        sample_rate = model.config.sampling_rate

        print(f"[*] Sample rate: {sample_rate} Hz")

        # ----------------------------------------------------
        # Output directory
        # ----------------------------------------------------

        lang_out_dir = os.path.join(
            OUT_DIR,
            selected_lang.lower()
        )

        os.makedirs(
            lang_out_dir,
            exist_ok=True
        )

        # ----------------------------------------------------
        # WAV filename
        # ----------------------------------------------------

        timestamp = time.strftime("%Y%m%d_%H%M%S")

        wav_path = os.path.join(
            lang_out_dir,
            f"{selected_lang.lower()}_{timestamp}.wav"
        )

        # ----------------------------------------------------
        # Save WAV
        # ----------------------------------------------------

        sf.write(
            wav_path,
            waveform,
            sample_rate
        )

        print(f"\n[✓] Speech generated successfully!")
        print(f"[✓] WAV saved: {wav_path}")

        # ----------------------------------------------------
        # Play through laptop speaker
        # ----------------------------------------------------

        print("[*] Playing speech...")

        try:
            winsound.PlaySound(
                wav_path,
                winsound.SND_FILENAME
            )

            print("[✓] Playback finished.")

        except Exception as e:
            print("[!] Could not play audio automatically.")
            print(f"Error: {e}")
            print(f"[*] You can manually open: {wav_path}")

    except Exception as e:
        print("\n[!] Failed during generation.")
        print(f"Error: {type(e).__name__}: {e}")


def main():
    while True:

        print("\n========================================")
        print("             MISTI TTS")
        print("========================================")
        print("1. Generate Speech")
        print("2. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":

            language = select_language()

            if language:
                generate_speech(language)

        elif choice == "2":
            print("\nExiting MISTI...")
            break

        else:
            print("[!] Invalid option.")


if __name__ == "__main__":
    main()