# # src/answer_generator.py
# from groq import Groq
# import os
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def generate_answer(question, db_result):
#     prompt = f"""
# You are answering a user question using ONLY Neo4j database results.

# Your job is to convert structured database output into a clear answer.

# STRICT RULES:

# 1. ONLY use the provided database results
# 2. DO NOT add any external knowledge
# 3. DO NOT guess or hallucinate

# 4. FIRST: Identify if any database entries are RELEVANT to the user question
#    - Match based on entity meaning (not exact string only)
#    - Ignore unrelated entities

# 5. IF NO relevant data is found:
#    respond exactly:
#    "No relevant information found in the database."

# 6. Interpret graph structure:
#    - e.name = entity
#    - type(r) = relationship
#    - v.name = value

# 7. Convert relationships into natural language:
#    Example:
#    ("Primary care visit", "HAS_NETWORK_COST", "$35 copay")
#    → "The network cost of primary care visit is $35 copay."

# 8. If multiple relevant results exist:
#    - Combine them clearly
#    - Group similar information
#    - Avoid repetition

# 9. Keep answer concise and factual
# 10. DO NOT include unrelated database entries

# OUTPUT:
# Return only the final answer (no explanation).

# Schema:
# (Entity)-[RELATION]->(Entity/Value)

# User Question:
# {question}

# DATABASE RESULTS:
# {db_result}
# """
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0
#     )

#     return response.choices[0].message.content.strip()





# src/answer_generator.py
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
   → Example: "The copay for a primary care visit is $35."

2. YES/NO ("Does the plan cover X?", "Is Y included?")
   → Answer "Yes" or "No" first, then support with a fact from the results.
   → Example: "Yes, the plan covers emergency services with a $150 copay."

3. COMPARISON ("What is the difference between X and Y?")
   → Present each entity's relevant values side by side.
   → Use clear labels. Avoid redundancy.

4. LIST / ENUMERATION ("What are all the benefits?", "List the covered services.")
   → Use a clean bulleted or numbered list.
   → Group similar items logically.

5. DEFINITION / EXPLANATION ("What is a deductible?", "What does copay mean?")
   → If the database has a definition or description node, use it.
   → If not, respond: "No definition found in the database."

6. CONDITIONAL / ELIGIBILITY ("When does X apply?", "Who qualifies for Y?")
   → State conditions or eligibility criteria from the results clearly.

7. AGGREGATE / COUNT ("How many services are covered?", "What is the total limit?")
   → Count or sum from the database results if the data supports it.

8. AMBIGUOUS OR MULTI-PART ("Tell me about X")
   → Extract all relevant relationships for the entity.
   → Organize them into a short paragraph or grouped list.

STRICT RULES:
- Use ONLY the data provided. Never add external knowledge.
- Never guess, infer beyond the data, or hallucinate.
- Relevance check: Match entities by meaning, not just exact string. E.g., "GP visit" matches "primary care visit".
- If no relevant data exists: respond exactly → "No relevant information found in the database."
- Correct all grammar in the final output. Write in complete, well-formed English sentences.
- Avoid robotic phrasing like "The database shows..." or "According to the results...".
- Do not mention the database, graph, or schema in your answer.
- Do not repeat the question in your answer.
- Keep the answer concise. Remove redundancy.

OUTPUT: Return only the final answer. No preamble, no explanation, no metadata."""


def generate_answer(question: str, db_result: str) -> str:
    user_message = f"""User Question:
{question}

Database Results:
{db_result}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()
