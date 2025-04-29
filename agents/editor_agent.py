import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def edit_content(draft: str) -> str:
    prompt = f"""
    You are a professional content editor. Take the following draft and improve it by:
    - Fixing grammar and punctuation
    - Improving readability and tone
    - Making it more engaging and conversational
    - Enhancing SEO (without keyword stuffing)
    - Keeping structure intact

    Draft:
    {draft}

    Return the polished version.
    """
    try:
        response = client.chat.completions.create(
            model = "gpt-4",
            messages=[{"role":"user","content":prompt}],
            temperature=0.5,
            max_tokens=1200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error] {str(e)}" 