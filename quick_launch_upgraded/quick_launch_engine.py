
import openai
import os

def generate_quick_launch_ideas(prompt):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a startup strategist trained in monetization and current social trends."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2200,
        temperature=0.85
    )
    return response.choices[0].message.content
