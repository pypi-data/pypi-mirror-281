import pandas as pd
import logging
import typer
from colorama import Fore, Style
from emotion_detective.data.inference.data_ingestion import mov_to_mp3_audio
from emotion_detective.data.inference.data_preprocessing import transcribe_translate
from emotion_detective.models.model_predict import get_predictions

app = typer.Typer()

def show_instructions():
    instructions = (
        f"{Fore.YELLOW}🕵️ Welcome to the Emotion Detective CLI! 🕵️{Style.RESET_ALL}\n\n"
        f"{Fore.CYAN}This tool processes 🎥 video and 🎵 audio files to detect"
        f"emotions.{Style.RESET_ALL}\n\n"
        f"{Fore.GREEN}🚀 Instructions: {Style.RESET_ALL}\n"
        f"1. {Fore.BLUE}input_media_path: {Style.RESET_ALL} Path to input audio (mp3)"
        f"or video file (mp4). {Fore.RED}[required]{Style.RESET_ALL}\n"
        f"2. {Fore.BLUE}model_path: {Style.RESET_ALL} Path to the saved NLP model. "
        f"{Fore.RED}[required]{Style.RESET_ALL}\n"
        f"3. {Fore.BLUE}model_type: {Style.RESET_ALL} Type of NLP model "
        f"('roberta' or 'rnn'). {Fore.RED}[required]{Style.RESET_ALL}\n"
        f"4. {Fore.BLUE}emotion_mapping_path: {Style.RESET_ALL} Path to the "
        f"emotion mapping file. {Fore.RED}[required]{Style.RESET_ALL}\n"
        f"\n{Fore.MAGENTA}🔔 Please provide the necessary inputs when prompted. "
        f"🔔{Style.RESET_ALL}\n"
    )
    print(instructions)

@app.command()
def main(
    input_media_path: str = typer.Option(
        None, help="Path to the input audio (mp3) or video file (mp4)."
    ),
    model_path: str = typer.Option(
        None, help="Path to the saved NLP model."
    ),
    model_type: str = typer.Option(
        None, help="Type of NLP model ('roberta' or 'rnn')."
    ),
    emotion_mapping_path: str = typer.Option(
        None, help="Path to the emotion mapping file."
    )
) -> pd.DataFrame:
    """Inference pipeline for emotion detection from video and audio files.

    Args:
        input_media_path (str): Path to input audio (mp3) or video file (mp4).
        model_path (str): Path to the saved NLP model.
        model_type (str): Type of NLP model ('roberta' or 'rnn').
        emotion_mapping_path (str): Path to the emotion mapping file.

    Returns:
        pd.DataFrame: DataFrame containing transcribed sentences, predicted emotions,
        their values, and probability.
    """
    show_instructions()

    if input_media_path is None:
        input_media_path = input(
            "Please enter the path to the input audio (mp3) or video file (mp4): "
            )
    if model_path is None:
        model_path = input("Please enter the path to the saved NLP model: ")
    if model_type is None:
        model_type = input("Please enter the model type ('roberta' or 'rnn'): ")
    if emotion_mapping_path is None:
        emotion_mapping_path = input(
            "Please enter the path to the emotion mapping file: "
            )

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("logs/emotion_detective.txt")
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info('Starting program...')

    if input_media_path.endswith(".mp4"):
        logger.info("Converting video to audio...")
        output_path = mov_to_mp3_audio(input_media_path)
        logger.info("Transcribing and translating audio...")
        transcribed_df = transcribe_translate(output_path)
    else:
        transcribed_df = transcribe_translate(input_media_path)

    logger.info("Getting predictions...")
    logger.info(f"Using model type: {model_type}")
    predictions_df = get_predictions(model_path, transcribed_df, emotion_mapping_path,
                                     model_type=model_type)

    logger.info("Program finished.")
    print(predictions_df)
    return predictions_df

if __name__ == "__main__":
    app()
