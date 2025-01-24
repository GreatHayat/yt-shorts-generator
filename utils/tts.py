import os
import requests
import subprocess

url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en"
headers = {
    'Authorization': f'Token {os.environ.get("DEEPGRAM_API_KEY")}',
    'Content-Type': 'text/plain'
}


def get_audio_length(audio_path):
    """
    Get the duration of an audio file using FFmpeg
    """
    try:
        command = [
            "ffprobe", "-i", audio_path,
            "-show_entries", "format=duration",
            "-v", "quiet", "-of", "csv=p=0"
        ]
        result = subprocess.run(
            command, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting audio duration: {e}")
        return 0


def generate_audio(text, scene):
    if not text or not scene:
        return None
    
    # Create audios directory if it doesn't exist
    os.makedirs('audios', exist_ok=True)
    
    # Make the request
    response = requests.request("POST", url, headers=headers, data=text)
    
    if response.status_code == 200:
        # Save the content as an MP3 file
        audio_path = f'audios/scene{scene}.mp3'
        with open(audio_path, 'wb') as f:
            f.write(response.content)
        print(f"Audio file saved successfully as '{audio_path}'")
        
        # Get the length of the audio
        duration = get_audio_length(audio_path)
        return duration
    else:
        print(f"Error: {response.text}")
        return None
