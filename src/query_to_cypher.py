# this is main code
# # src/query_to_cypher.py
# from groq import Groq
# import os
# from dotenv import load_dotenv
# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def question_to_cypher(question):
#     """
#     Improved Cypher generator specialized for SBC (Summary of Benefits and Coverage) documents.
#     """
#     prompt = f"""
# You are an expert Neo4j Cypher query generator for health insurance Summary of Benefits and Coverage (SBC) documents.

# ### Graph Schema:
# - All nodes have label `:Entity`
# - Every node has a `name` property (very important)
# - Some nodes also have properties like: `network_cost`, `out_of_network_cost`, `answer`, `value`, `limitations`, `medical_event`
# - Relationships connect entities with various types (EXCLUDES, OFFERS, HAS_ANSWER, etc.)

# ### STRICT INSTRUCTIONS:
# - Return **ONLY** valid Cypher code. No explanations, no markdown, no extra text.
# - Use `toLower(e.name)` for case-insensitive matching.
# - Prefer `OPTIONAL MATCH` to avoid empty results.
# - Use `coalesce()` to return the most useful value (network_cost, answer, value, name).
# - Always include at least: entity name, relationship type, and value/result.

# ### Good Query Patterns:

# 1. For "Out-of-Pocket Limit" questions:
# ```cypher
# MATCH (e:Entity)
# WHERE toLower(e.name) CONTAINS "out-of-pocket limit" OR toLower(e.name) CONTAINS "oop limit"
# OPTIONAL MATCH (e)-[r]-(v)
# RETURN e.name AS entity,
#        type(r) AS relationship,
#        coalesce(e.answer, e.value, v.name, e.network_cost) AS result
# ORDER BY type(r)

# ---

# EXAMPLES:

# Q: What is the copayment for preferred brand drugs?
# A:
# MATCH (e:Entity)-[r]->(v:Value)
# WHERE toLower(e.name) CONTAINS "preferred brand drugs"
# AND type(r) IN ["COPAY", "COPAYMENT"]
# RETURN e.name, type(r), v.name

# Q: What is the cost of prescription?
# A:
# MATCH (e:Entity)-[r]->(v:Value)
# WHERE toLower(e.name) CONTAINS "prescription"
# AND type(r) = "COST"
# RETURN e.name, type(r), v.name

# Q: What is the deductible?
# A: MATCH (e:Entity)
# WHERE toLower(e.name) CONTAINS "deductible"

# OPTIONAL MATCH (e)-[r]-(v)
# RETURN
#     e.name AS deductible_type,
#     type(r) AS relationship,
#     coalesce( e.value, v.name, e.network_cost) AS deductible_info,
#     e.answer AS full_answer
# ORDER BY type(r)


# ---

# QUESTION:
# {question}
# """
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0,
#          stop=["\n\n"]
#     )
#     return response.choices[0].message.content.strip()







# from groq import Groq
# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def question_to_cypher(question):
#     """
#     Robust Cypher generator for SBC (Summary of Benefits and Coverage).
#     """

#     prompt = f"""
# You are an expert Neo4j Cypher query generator for health insurance SBC documents.

# ----------------------------------
# GRAPH SCHEMA
# ----------------------------------
# - Nodes: (:Entity)
# - Properties:
#   - name (always present)
#   - value, answer, network_cost, out_of_network_cost, limitations, medical_event
# - Relationships: dynamic (e.g., COST, COPAY, NOT_COVERED, COVERED, LIMIT, DEDUCTIBLE)

# ----------------------------------
# STRICT RULES (MUST FOLLOW)
# ----------------------------------
# 1. Return ONLY Cypher query (no explanation, no markdown).
# 2. Always use case-insensitive matching:
#    toLower(e.name) CONTAINS "<keyword>"
# 3. Prefer OPTIONAL MATCH unless relationship is निश्चित.
# 4. Always return:
#    - entity
#    - relationship
#    - result
# 5. Always use coalesce in this priority:
#    coalesce(e.answer, e.value, e.network_cost, e.out_of_network_cost, v.name)
# 6. Use directed relationship when intent is clear:
#    (e)-[r:TYPE]->(v)
# 7. Always include ORDER BY relationship

# ----------------------------------
# QUERY TEMPLATES
# ----------------------------------

# # General Template
# MATCH (e:Entity)
# WHERE toLower(e.name) CONTAINS "<keyword>"
# OPTIONAL MATCH (e)-[r]-(v)
# RETURN 
#     e.name AS entity,
#     type(r) AS relationship,
#     coalesce(e.answer, e.value, e.network_cost, e.out_of_network_cost, v.name) AS result
# ORDER BY relationship

# ----------------------------------
# EXAMPLES
# ----------------------------------

# # 1. Copayment
# Q: What is the copayment for preferred brand drugs?
# MATCH (e:Entity)-[r:COPAY|COPAYMENT]->(v)
# WHERE toLower(e.name) CONTAINS "preferred brand drugs"
# RETURN 
#     e.name AS entity,
#     type(r) AS relationship,
#     v.name AS result
# ORDER BY relationship

# # 2. Cost
# Q: What is the cost of prescription?
# MATCH (e:Entity)-[r:COST]->(v)
# WHERE toLower(e.name) CONTAINS "prescription"
# RETURN 
#     e.name AS entity,
#     type(r) AS relationship,
#     v.name AS result
# ORDER BY relationship

# # 3. Deductible
# Q: What is the deductible?
# MATCH (e:Entity)
# WHERE toLower(e.name) CONTAINS "deductible"
# OPTIONAL MATCH (e)-[r]-(v)
# RETURN 
#     e.name AS entity,
#     type(r) AS relationship,
#     coalesce(e.value, v.name, e.network_cost, e.answer) AS result
# ORDER BY relationship

# # 4. Out-of-pocket limit
# Q: What is the out-of-pocket limit?
# MATCH (e:Entity)
# WHERE toLower(e.name) CONTAINS "out-of-pocket limit"
#    OR toLower(e.name) CONTAINS "oop limit"
# OPTIONAL MATCH (e)-[r]-(v)
# RETURN 
#     e.name AS entity,
#     type(r) AS relationship,
#     coalesce(e.answer, e.value, e.network_cost, e.out_of_network_cost, v.name) AS result
# ORDER BY relationship

# # 5. NOT COVERED (IMPORTANT)
# Q: What items are not covered under durable medical equipment?
# MATCH (e:Entity)-[r:NOT_COVERED]->(v)
# WHERE toLower(e.name) CONTAINS "durable medical equipment"
# RETURN 
#     e.name AS entity,
#     type(r) AS relationship,
#     v.name AS result
# ORDER BY result

# # 6. Validation
# Q: Is exercise equipment covered under durable medical equipment?
# MATCH (e:Entity)-[r]->(v:Entity)
# WHERE toLower(e.name) CONTAINS "durable medical equipment"
# AND toLower(v.name) CONTAINS "exercise equipment"
# RETURN 
#     e.name AS entity,
#     type(r) AS relationship,
#     v.name AS result

# ----------------------------------
# QUESTION:
# {question}
# """

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0,
#         stop=["\n\n"]
#     )

#     return response.choices[0].message.content.strip()


from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def question_to_cypher(question):
    """
    Final unified Cypher generator for SBC Neo4j graph.
    Covers all major question types.
    """

    prompt = f"""
You are an expert Neo4j Cypher query generator for health insurance SBC documents.

-------------------------------
GRAPH SCHEMA
-------------------------------
- Nodes: (:Entity)
- Properties:
  name (mandatory), value, answer, network_cost, out_of_network_cost, limitations, medical_event
- Relationships:
  HAS_COPAY, HAS_COINSURANCE, HAS_LIMIT, NOT_COVERED, COVERS,
  REQUIRES, NETWORK_COST, OUT_OF_NETWORK_COST, DEDUCTIBLE,
  REDUCES_BENEFIT, APPLIES_TO

-------------------------------
STRICT RULES (MUST FOLLOW)
-------------------------------
1. Return ONLY Cypher query (no explanation, no markdown).
2. Always use case-insensitive matching:
   toLower(e.name) CONTAINS "<keyword>"
3. Prefer OPTIONAL MATCH if relationship is unclear.
4. Always return:
   e.name AS entity,
   type(r) AS relationship,
   result
5. Always use:
   coalesce(e.answer, e.value, e.network_cost, e.out_of_network_cost, v.name)
6. Use correct relationship types when question implies it.
7. Always include ORDER BY relationship

-------------------------------
SMART QUERY PATTERN
-------------------------------
MATCH (e:Entity)
WHERE toLower(e.name) CONTAINS "<keyword>"
OPTIONAL MATCH (e)-[r]-(v)
RETURN 
    e.name AS entity,
    type(r) AS relationship,
    coalesce(
        e.answer,
        e.value,
        e.network_cost,
        e.out_of_network_cost,
        v.name
    ) AS result
ORDER BY relationship

-------------------------------
SPECIALIZED PATTERNS
-------------------------------

# Copay
MATCH (e:Entity)-[r:HAS_COPAY]->(v)
WHERE toLower(e.name) CONTAINS "<keyword>"
RETURN e.name AS entity, type(r) AS relationship, v.name AS result
ORDER BY relationship

# Coinsurance
MATCH (e:Entity)-[r:HAS_COINSURANCE]->(v)
WHERE toLower(e.name) CONTAINS "<keyword>"
RETURN e.name AS entity, type(r) AS relationship, v.name AS result
ORDER BY relationship

# Limit
MATCH (e:Entity)-[r:HAS_LIMIT]->(v)
WHERE toLower(e.name) CONTAINS "<keyword>"
RETURN e.name AS entity, type(r) AS relationship, v.name AS result
ORDER BY relationship

# Not Covered
MATCH (e:Entity)-[r:NOT_COVERED]->(v)
WHERE toLower(e.name) CONTAINS "<keyword>"
RETURN e.name AS entity, type(r) AS relationship, v.name AS result
ORDER BY result

# Covered Services
MATCH (e:Entity)-[r:COVERS]->(v)
WHERE toLower(e.name) CONTAINS "<keyword>"
RETURN e.name AS entity, type(r) AS relationship, v.name AS result

# Requires (Preauthorization etc.)
MATCH (e:Entity)-[r:REQUIRES]->(v)
WHERE toLower(e.name) CONTAINS "<keyword>"
RETURN e.name AS entity, type(r) AS relationship, v.name AS result

# Network Cost
MATCH (e:Entity)-[r:NETWORK_COST]->(v)
WHERE toLower(e.name) CONTAINS "<keyword>"
RETURN e.name AS entity, type(r) AS relationship, v.name AS result

# Out of Network Cost
MATCH (e:Entity)-[r:OUT_OF_NETWORK_COST]->(v)
WHERE toLower(e.name) CONTAINS "<keyword>"
RETURN e.name AS entity, type(r) AS relationship, v.name AS result

# Deductible
MATCH (e:Entity)
WHERE toLower(e.name) CONTAINS "deductible"
OPTIONAL MATCH (e)-[r]-(v)
RETURN 
    e.name AS entity,
    type(r) AS relationship,
    coalesce(e.value, v.name, e.network_cost, e.answer) AS result
ORDER BY relationship

# Out-of-pocket limit
MATCH (e:Entity)
WHERE toLower(e.name) CONTAINS "out-of-pocket limit"
   OR toLower(e.name) CONTAINS "oop limit"
OPTIONAL MATCH (e)-[r]-(v)
RETURN 
    e.name AS entity,
    type(r) AS relationship,
    coalesce(e.answer, e.value, e.network_cost, e.out_of_network_cost, v.name) AS result
ORDER BY relationship


EXAMPLES:

Q: What is the copayment for preferred brand drugs?
A:
MATCH (e:Entity)-[r]->(v:Value)
WHERE toLower(e.name) CONTAINS "preferred brand drugs"
AND type(r) IN ["COPAY", "COPAYMENT"]
RETURN e.name, type(r), v.name

Q: What is the cost of prescription?
A:
MATCH (e:Entity)-[r]->(v:Value)
WHERE toLower(e.name) CONTAINS "prescription"
AND type(r) = "COST"
RETURN e.name, type(r), v.name

Q: What is the deductible?
A: MATCH (e:Entity)
WHERE toLower(e.name) CONTAINS "deductible"

OPTIONAL MATCH (e)-[r]-(v)
RETURN
    e.name AS deductible_type,
    type(r) AS relationship,
    coalesce( e.value, v.name, e.network_cost) AS deductible_info,
    e.answer AS full_answer
ORDER BY type(r)

-------------------------------
QUESTION:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        stop=["\n\n"]
    )

    return response.choices[0].message.content.strip()