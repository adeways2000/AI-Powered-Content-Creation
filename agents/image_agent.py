import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(topic: str) -> str:
    prompt = f"A High Quality, Professional, AI-generated Illustration for: {topic}"

    try:
        response = client.chat.completions.create(
            model = "dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"

        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        return f"[Error] {str(e)}"    