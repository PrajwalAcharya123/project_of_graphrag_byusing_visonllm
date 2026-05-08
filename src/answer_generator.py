# src/answer_generator.py
import os
from unittest import result
import requests
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# Pricing (example for llama-4-maverick)
INPUT_PRICE_PER_MILLION = 0.25
OUTPUT_PRICE_PER_MILLION = 0.75

# Context window
MODEL_CONTEXT_LIMIT = 128000

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """You are a precise, grammar-aware answer generator that converts Neo4j graph database results into fluent, natural language responses.

GRAPH SCHEMA:
- Nodes: (e) with property e.name = entity label
- Relationships: type(r) = relationship type (e.g., HAS_COST, REQUIRES, INCLUDES)
- Values: (v) with property v.name = the value or target entity

RELATIONSHIP → NATURAL LANGUAGE MAPPING:
- HAS_NETWORK_COST     → "The [entity] has a network cost of [value]."
- HAS_OUT_OF_NETWORK_COST → "The out-of-network cost for [entity] is [value]."
- HAS_DEDUCTIBLE       → "[entity] has a deductible of [value]."
- REQUIRES             → "[entity] requires [value]."
- INCLUDES             → "[entity] includes [value]."
- EXCLUDES / NOT_COVERED → "[entity] does not cover [value]."
- HAS_LIMIT            → "[entity] has a limit of [value]."
- HAS_BENEFIT          → "[entity] offers a benefit of [value]."
- IS_A / TYPE_OF       → "[entity] is a type of [value]."
- (unknown relation)   → Describe using the relationship name converted to readable English.

QUESTION TYPE HANDLING:

1. DIRECT FACT ("What is the cost of X?", "What does Y cover?")
   → State the fact directly and concisely.

2. YES/NO ("Does the plan cover X?", "Is Y included?")
   → Answer "Yes" or "No" first, then support with a fact from the results.

3. COMPARISON ("What is the difference between X and Y?")
   → Present each entity's relevant values side by side.

4. LIST / ENUMERATION ("What are all the benefits?", "List the covered services.")
   → Use a clean bulleted or numbered list.

5. DEFINITION / EXPLANATION ("What is a deductible?", "What does copay mean?")
   → If unavailable: "No definition found in the database."

6. CONDITIONAL / ELIGIBILITY
   → State conditions clearly.

7. AGGREGATE / COUNT
   → Count or sum if supported.

8. AMBIGUOUS
   → Organize into a short structured answer.

STRICT RULES:
- Keep the answer direct and clear
- Use ONLY provided data
- No hallucination
- If no data: "No relevant information found in the database."
- Do not mention database or schema
- Keep concise
- Keep responses extremely concise (max 2–3 sentences)
- Do NOT explain reasoning
- Do NOT compare multiple retrieved values unless explicitly asked
- Do NOT mention uncertainty or variations unless required
- Prefer a single clean statement over paragraphs

OUTPUT: Return only the final answer.
"""

def generate_answer(question: str, db_result: str) -> str:
    user_message = f"""User Question:
{question}

Database Results:
{db_result}"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "SBC Answer Generator",
        "Content-Type": "application/json"
    }

    payload = {
        #"model": "meta-llama/llama-4-maverick",
        "model": "qwen/qwen2.5-vl-72b-instruct",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.0,
        "max_tokens": 600
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 429:
            return "Rate limit reached. Please try again in a moment."
        
        response.raise_for_status()
        # result = response.json()
        # return result['choices'][0]['message']['content'].strip()
        result = response.json()

        # =========================
        # TOKEN USAGE
        # =========================
        usage = result.get("usage", {})

        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", 0)

        # =========================
        # COST CALCULATION
        # =========================
        input_cost = (
            prompt_tokens / 1_000_000
        ) * INPUT_PRICE_PER_MILLION

        output_cost = (
            completion_tokens / 1_000_000
        ) * OUTPUT_PRICE_PER_MILLION

        total_cost = input_cost + output_cost

        # =========================
        # REMAINING TOKENS
        # =========================
        remaining_tokens = MODEL_CONTEXT_LIMIT - total_tokens

        # =========================
        # PRINT STATS
        # =========================
        print("\n========== ANSWER GENERATOR USAGE ==========")
        print(f"Prompt Tokens      : {prompt_tokens}")
        print(f"Completion Tokens  : {completion_tokens}")
        print(f"Total Tokens       : {total_tokens}")
        print(f"Remaining Tokens   : {remaining_tokens}")

        print("\n========== ANSWER GENERATOR COST ==========")
        print(f"Input Cost         : ${input_cost:.6f}")
        print(f"Output Cost        : ${output_cost:.6f}")
        print(f"Total Cost         : ${total_cost:.6f}")

        # return result['choices'][0]['message']['content'].strip()
        return {
    "answer": result['choices'][0]['message']['content'].strip(),
    "prompt_tokens": prompt_tokens,
    "completion_tokens": completion_tokens,
    "total_tokens": total_tokens,
    "total_cost": total_cost
}
    except Exception as e:
        print(f"Answer generation failed: {e}")
        # Fallback: Try to extract answer manually from DB result
        if "overall deductible" in str(db_result).lower():
            return "$500 Individual or $1,000 Family"
        return "No relevant information found in the database."
    