import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


EVALUATION_PROMPT = """
You are an expert evaluator for health insurance QA systems.

Your task:
Compare the ACTUAL ANSWER and the PREDICTED ANSWER.

Evaluation Rules:
- Return ONLY:
    1 → if both answers mean the same thing semantically
    0 → if the predicted answer is incorrect, incomplete, or misleading

IMPORTANT:
- Ignore wording differences
- Ignore grammar differences
- Focus ONLY on semantic correctness
- Numeric values must match
- Coverage meaning must match

Output ONLY:
1 or 0
"""


def evaluate_answers(question, actual_answer, predicted_answer):

    user_prompt = f"""
Question:
{question}

Actual Answer:
{actual_answer}

Predicted Answer:
{predicted_answer}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-4-maverick",
        "messages": [
            {
                "role": "system",
                "content": EVALUATION_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": 0,
        "max_tokens": 5
    }

    try:

        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        result = response.json()

        evaluation = result["choices"][0]["message"]["content"].strip()

        if "1" in evaluation:
            return 1
        else:
            return 0

    except Exception as e:

        print("Evaluation Error:", e)

        return 0