## YouTube Shorts Generator

Generate YouTube Shorts effortlessly from any given article link using the power of `Pydantic AI`, `Crawl4 AI`, and the `DALLE 3` model for image generation.

### Prerequisites
To use this project, you must have the following API keys:
- **OpenAI API Key**
- **Deepgram API Key**

Set your API keys as environment variables:
```bash
export OPENAI_API_KEY=your_openai_api_key
export DEEPGRAM_API_KEY=your_deepgram_api_key
```

### Setup Instructions

1. **Create and Activate a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Add Your Article Link**
   - Open the `crawler.py` file.
   - Insert your desired article link in the `main` method.

3. **Run the Script**
   ```bash
   python3 crawler.py
   ```

### How It Works
The script extracts information from the provided article link and processes it using AI to generate engaging YouTube Shorts content. The `DALLE 3` model is utilized to generate visually compelling images, while OpenAI and Deepgram services handle other processing tasks. Ensure your API keys are correctly configured to enable these integrations.

### Sample Output
Below is a sample output of the generated YouTube Short:

https://github.com/user-attachments/assets/886fc835-21e2-48d6-a86c-25e6eb498b2b


