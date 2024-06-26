from openai import OpenAI
import os



api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an expert text summarizer."},
        {"role": "user", "content": f"Summarize the following text in a concise manner: {text}"}
    ],
    max_tokens=150,
    temperature=0.2,
    )

    return completion.choices[0].message
