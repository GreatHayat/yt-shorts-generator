from .tts import generate_audio


def format_time(seconds):
    """
    Convert seconds into HH:MM:SS,mmm format
    """
    milliseconds = int((seconds - int(seconds)) * 1000)
    time_formatted = f"{int(seconds // 3600):02}:{int((seconds %
                                                       3600) // 60):02}:{int(seconds % 60):02},{milliseconds:03}"
    return time_formatted


def generate_audio_and_subtitle(json_output, output_srt_path="subtitles.srt"):
    """
    Generate an SRT file based on the text and audio durations
    """
    try:
        subtitles = []
        current_time = 0.0  # Start from 0 seconds

        # Process each item
        for item in json_output:
            scene_number = item["scene_number"]
            text = item["text"]

            print(f"Generating audio for scene {scene_number}")
            duration = generate_audio(text, scene_number)

            if duration:
                # Calculate start and end times
                start_time = current_time
                end_time = current_time + duration

                # Format times in HH:MM:SS,mmm format
                start_time_formatted = format_time(start_time)
                end_time_formatted = format_time(end_time)

                # Append the subtitle entry
                subtitles.append(f"{scene_number}")
                subtitles.append(
                    f"{start_time_formatted} --> {end_time_formatted}")
                subtitles.append(text)
                subtitles.append("")  # Blank line

                # Update current time
                current_time = end_time

        # Write to SRT file
        with open(output_srt_path, "w", encoding="utf-8") as srt_file:
            srt_file.write("\n".join(subtitles))
        print(f"SRT file generated successfully: {output_srt_path}")

    except Exception as e:
        print(f"Error generating SRT file: {e}")

