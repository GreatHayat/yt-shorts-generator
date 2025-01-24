import os
import json
import asyncio
from typing import List
from pydantic import BaseModel, Field
from dataclasses import dataclass
from crawl4ai import AsyncWebCrawler
from pydantic_ai import Agent, RunContext

# import from utils folder
from utils.subtitles_generator import generate_audio_and_subtitle
from utils.image_downloader import download_image
from utils.image_generator import generate_image
from utils.video_generator import preprocess_images, create_video_with_audio_and_subtitles


class Scene(BaseModel):
    scene_number: int = Field(...,
                              description="The sequential number of the scene.")
    text: str = Field(...,
                      description="The narration or on-screen text for the scene.")
    image_prompt: str = Field(
        ..., description="A detailed prompt to generate the image or visual for the scene.")
    timeframe: int = Field(...,
                           description="The duration of the scene in seconds.")


class YouTubeShortsScript(BaseModel):
    scenes: List[Scene] = Field(
        ..., description="A list of scenes, each containing the script and related metadata.")


system_prompt = """You are an advanced language model tasked with analyzing news articles and generating a YouTube Shorts video script. You will be provided with a tool to scrape web pages, primarily news articles. Here's your job:

1. **Focus on Relevant Content**:  
   Analyze the webpage content and extract only the main article text. Ignore headers, footers, navigation bars, advertisements, and any other irrelevant content.

2. **Script Creation**:  
   Based on the extracted content, generate a compelling script for a YouTube Shorts video. Divide the script into scenes, ensuring the flow is engaging and concise.

3. **Scene Structure**:  
   Each scene should include:  
   - **Text**: The script or narration for the scene.  
   - **Image Description Prompt**: An effective prompt for generating a relevant and visually engaging image or video background for the scene. This will be used with an image-generation AI.  
   - **Timeframe**: A duration (in seconds) for each scene to guide video editors.

4. **Output Format**:  
   The output should be in valid JSON format. Each scene should be a separate object in the JSON array, containing the following fields:  
   - `scene_number`: The sequential number of the scene.  
   - `text`: The narration or on-screen text for the scene.  
   - `image_prompt`: A detailed prompt to generate the image or visual for the scene.  
   - `timeframe`: The duration of the scene in seconds.

5. **Ensure Creativity and Clarity**:  
   Make the script engaging, audience-focused, and easy to follow. Use persuasive and emotionally appealing language where appropriate.

Focus on creating a visually appealing and engaging experience for the audience while maintaining accuracy and relevance to the article.
"""


@dataclass
class Deps:
    client: AsyncWebCrawler
    url: str


agent = Agent(
    # model='google-gla:gemini-1.5-pro',
    model='openai:gpt-4o-mini',
    system_prompt=system_prompt,
    result_type=YouTubeShortsScript,
    deps_type=Deps,
    name="YouTube Shorts Script Generator",
)


@agent.tool
async def web_crawler(ctx: RunContext[Deps]) -> str:
    """Use this tool to scrap the webpage and return content as markdown"""
    result = await ctx.deps.client.arun(
        url=ctx.deps.url,
    )

    # return the content of the webpage as markdown
    return result.markdown


async def main(url: str):
    async with AsyncWebCrawler() as crawler:
        deps = Deps(
            client=crawler,
            url=url
        )

        result = await agent.run('Crawl the webpage of a given URL and do your job', deps=deps)

        scenes = result.data.scenes

        json_output = json.dumps([scene.model_dump()
                                  for scene in scenes], indent=2)

        print(json_output)

        urls = []

        for item in json.loads(json_output):
            print(f"Generating image for scene {item['scene_number']}")
            url = generate_image(item['image_prompt'])
            urls.append({"url": url, "scene": item['scene_number']})

        generate_audio_and_subtitle(json.loads(json_output))

        for item in urls:
            print(f"Downloading image for scene {item['scene']}")
            download_image(item['url'], f"image{item['scene']}")

    input_dir = "images"
    output_dir = "images_processed"
    audio_dir = "audios"
    output_video = "output_video.mp4"

    os.makedirs('images_processed', exist_ok=True)
    # Process images
    preprocess_images(input_dir, output_dir)

    # Create video with synchronized audio and subtitles
    create_video_with_audio_and_subtitles(output_dir, audio_dir, output_video)

if __name__ == "__main__":
    url = 'https://www.bbc.com/future/article/20250122-expert-tips-on-how-to-keep-exercising-during-cold-winter-weather'
    asyncio.run(main(url))

# https://www.bbc.com/future/article/20250122-expert-tips-on-how-to-keep-exercising-during-cold-winter-weather