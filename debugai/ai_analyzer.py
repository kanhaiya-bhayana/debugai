from openai import OpenAI
import os

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)


import json 
import re

def parse_ai_json(text):

    try:
        return json.loads(text)

    except:
        # try extracting JSON block
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            return json.loads(match.group())

        raise
def analyze_with_ai(log: str):

    prompt = f"""
You are a senior software engineer debugging a production issue.

Return STRICT JSON in this format:

{{
 "root_cause": "...",
 "fix": "...",
 "prevention": "..."
}}

Stack trace:
{log}
"""

    try:
        completion = client.chat.completions.create(
            model="z-ai/glm4.7",
            messages=[
                {"role": "system", "content": "You are an expert debugging assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )

        content = completion.choices[0].message.content
        ai_result = parse_ai_json(content)

        return ai_result

    except Exception as e:
        return {
            "root_cause": "AI analysis failed",
            "fix": str(e),
            "prevention": "Check API configuration"
        }