import openai
import os

# Make sure to set your OpenAI API key here or in the environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert text summarizer."},
            {"role": "user", "content": f"Summarize the following text in a concise manner: {text}"}
        ],
        max_tokens=150,
        temperature=0.2,
    )
    return response.choices[0].message['content'].strip()
