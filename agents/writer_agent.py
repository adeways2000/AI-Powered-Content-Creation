import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def write_draft(topic: str, outline: str) -> str:
    prompt = f"""
    You are a professional content writer. Based on the topic and outline below, write a full-length content draft

    Make the tone engaging and informative. Add transitions and make sure it flows well.
    
    Topic: {topic}

    outline:
    {outline}

    Begin writing:
    """

    try:
        response = client.chat.completions.create(
            model = "gpt-4",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7,
            max_tokens=1200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error] {str(e)}" 