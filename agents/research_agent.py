import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def research_topic(topic: str) -> str:
    prompt = f"""
    You are a research assistant. Provide a detailed overview of the topic: "{topic}".
    Include current trends, background, and important points to include in a blog or content.
    Make it factual and helpful for content creation.
    """
    try:
        response = client.chat.completions.create(
            model = "gpt-4",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7,
            max_tokens=700
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error] {str(e)}"   
# test

# if __name__ == '__main__':
#    topic_summary = research_topic("generative ai")
#    print(topic_summary)
