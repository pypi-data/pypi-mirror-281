from emotion_detective.logger.logger import setup_logging
from moviepy.editor import VideoFileClip


def mov_to_mp3_audio(input_file: str) -> str:
    """
    Extracts audio from a video file and saves it as an mp3 file.

    Args:
        input_file (str): Path to the input video file.

    Returns:
        str: Path to the saved mp3 file.

    Raises:
        ValueError: If the input file does not have a .mp4 extension.
        Exception: Any exceptions encountered during the conversion process.

    Author: Kacper Janczyk
    """
    # Setting up logging
    logger = setup_logging()

    try:
        logger.info("Converting video to audio...")

        # Deriving output file path by replacing .mp4 with .mp3
        if input_file.lower().endswith('.mp4'):
            output_file = input_file[:-4] + '.mp3'
        else:
            logger.debug("Input file must have a .mp4 extension")
            raise ValueError("Input file must have a .mp4 extension")

        # Extracting audio from the video clip
        video_clip = VideoFileClip(input_file)
        audio_clip = video_clip.audio

        # Saving the extracted audio as an mp3 file
        logger.info(f"Saving audio file to {output_file}...")
        audio_clip.write_audiofile(output_file, codec='mp3')

        # Closing audio and video clips
        audio_clip.close()
        video_clip.close()

        # Returning the output file path
        return output_file

    except Exception as e:
        # Logging any errors encountered during the conversion process
        logger.error(f"Error in converting video to audio: {e}")
        raise
