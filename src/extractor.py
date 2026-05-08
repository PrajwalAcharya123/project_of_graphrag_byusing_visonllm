
# # src/extractor.py

# from groq import Groq
# import os
# import json
# import re
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# # =========================
# # CLEAN LLM OUTPUT
# # =========================
# def clean_llm_output(text):
#     text = re.sub(r"```json", "", text)
#     text = re.sub(r"```", "", text)

#     match = re.search(r"\{.*\}", text, re.DOTALL)
#     return match.group(0).strip() if match else text.strip()


# # =========================
# # 🔥 CONVERT CHUNK → TEXT
# # =========================
# def chunk_to_text(chunk):
#     if chunk["type"] == "table_row":
#         data = chunk["data"]

#         # Convert structured row into readable sentence
#         parts = []
#         for key, value in data.items():
#             if value:
#                 parts.append(f"{key}: {value}")

#         return ". ".join(parts)

#     elif chunk["type"] == "section":
#         return f"{chunk.get('title', '')}. {chunk.get('content', '')}"

#     elif chunk["type"] == "list":
#         return " ".join(chunk.get("items", []))

#     return ""


# def extract_graph(text):
#     prompt = f"""
            
#             You are an expert system for extracting COMPLETE structured knowledge graphs from health insurance SBC documents.

#             Your goal is to extract ALL meaningful structured data from the document, including:
#             - entities
#             - relationships
#             - attributes
#             - numeric values
#             - conditions
#             - limits
#             - coverage rules

#             Output ONLY valid JSON in this format:

#             {{
#             "entities": [],
#             "relationships": [],
#             "attributes": [],
#             "tables": [],
#             "rules": []
#             }}

#             ----------------------
#             EXTRACTION GUIDELINES:
#             ----------------------

#             1. ENTITIES:
#             Extract ALL important entities including:
#             - Plans (e.g., "Plan Option 1")
#             - Services (e.g., "Primary care visit", "Emergency room care")
#             - Medical events (e.g., "Pregnancy", "Hospital stay")
#             - Cost types (e.g., "Copay", "Coinsurance", "Deductible")
#             - Coverage types (e.g., "Preventive care", "Out-of-network provider")
#             - Conditions (e.g., "Preauthorization")

#             2. RELATIONSHIPS:
#             Extract structured relationships:
#             - HAS_COPAY
#             - HAS_COINSURANCE
#             - HAS_DEDUCTIBLE
#             - HAS_LIMIT
#             - REQUIRES
#             - COVERS
#             - NOT_COVERED
#             - APPLIES_TO
#             - REDUCES_BENEFIT

#             Example:
#             ["Specialist visit", "HAS_COPAY", "$50"]

#             3. ATTRIBUTES:
#             Extract ALL numeric and descriptive values:
#             - dollar amounts ($500, $35)
#             - percentages (20%, 40%)
#             - counts (60 visits/year)
#             - coverage limits
#             - plan details

#             Example:
#             ["Deductible", "individual", "$500"]

#             4. TABLE EXTRACTION:
#             Convert table rows into structured triples:
#             Each row should produce:
#             - entity (service)
#             - attributes (costs)
#             - relationships

#             Example:
#             {{
#             "service": "Primary care visit",
#             "network_cost": "$35 copay",
#             "out_of_network_cost": "40% coinsurance",
#             "conditions": "deductible does not apply"
#             }}

#             5. RULES & CONDITIONS:
#             Extract rules like:
#             - "Preauthorization is required"
#             - "Failure results in 50% reduction"

#             Example:
#             ["Specialist visit", "REQUIRES", "Preauthorization"]
#             ["No preauthorization", "REDUCES_BENEFIT", "50%"]

#             6. COVERAGE:
#             Capture:
#             - covered services
#             - excluded services
#             - limitations

#             Example:
#             ["Cosmetic surgery", "NOT_COVERED", "Plan"]
#             ["Home health care", "HAS_LIMIT", "60 visits/year"]

#             7. SCENARIOS:
#             Extract example cost breakdowns:

#             Example:
#             {{
#             "scenario": "Pregnancy",
#             "total_cost": "$12,800",
#             "patient_pays": "$3,160"
#             }}

#             ----------------------
#             CRITICAL RULES:
#             ----------------------

#             - Extract EVERYTHING meaningful (not just costs)
#             - Include ALL numeric values
#             - Normalize entity names
#             - Do NOT miss tables
#             - Do NOT summarize
#             - Do NOT explain
#             - Output ONLY JSON

#             ----------------------
#             TEXT:
#             {text}
#             """


#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0
#     )

#     raw_output = response.choices[0].message.content

#     print("\n🔍 RAW LLM OUTPUT:\n", raw_output)

#     cleaned = clean_llm_output(raw_output)

#     try:
#         parsed = json.loads(cleaned)
#     except Exception as e:
#         print("❌ JSON parse failed:", e)
#         parsed = {"entities": [], "relationships": [], "attributes": []}

#     return parsed


# # =========================
# # 🔥 MAIN DRIVER (IMPORTANT)
# # =========================
# def process_chunks(input_file, output_dir="output/llm_graph"):
#     with open(input_file, "r", encoding="utf-8") as f:
#         chunks = json.load(f)

#     os.makedirs(output_dir, exist_ok=True)

#     for chunk in chunks:
#         chunk_id = chunk.get("chunk_id", "unknown")

#         text = chunk_to_text(chunk)
#         print(f"\n📄 Chunk {chunk_id} text:\n{text[:500]}...")  # Print first 500 chars
#         if not text.strip():
#             continue

#         print(f"\n🚀 Processing: {chunk_id}")

#         graph = extract_graph(text)
#         print(f"\n✅ Extracted graph for chunk {chunk_id}:\n{json.dumps(graph, indent=2)}") 
#         # Save per chunk
#         file_path = os.path.join(output_dir, f"{chunk_id}.json")

#         with open(file_path, "w", encoding="utf-8") as f:
#             json.dump(graph, f, indent=2)

#         print(f"💾 Saved: {file_path}")








# extractor.py

from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# =========================
# CLEAN LLM OUTPUT
# =========================
def clean_llm_output(text):
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0).strip() if match else text.strip()


# =========================
# CONVERT CHUNK → TEXT
# =========================
def chunk_to_text(chunk):
    """Convert any structured chunk dict into a plain text string for the LLM."""
    chunk_type = chunk.get("type", "")

    if chunk_type == "table_row":
        data = chunk.get("data", {})
        parts = [f"{key}: {value}" for key, value in data.items() if value]
        return ". ".join(parts)

    elif chunk_type == "section":
        return f"{chunk.get('title', '')}. {chunk.get('content', '')}"

    elif chunk_type == "list":
        return " ".join(chunk.get("items", []))

    elif chunk_type == "benefit_service":
        # Serialize structured benefit chunks into readable text
        parts = []
        for key in ["medical_event", "service", "network_cost",
                    "out_of_network_cost", "limitations"]:
            val = chunk.get(key)
            if val:
                parts.append(f"{key.replace('_', ' ')}: {val}")
        if chunk.get("requires_preauth"):
            parts.append("requires preauthorization: yes")
        return ". ".join(parts)

    elif chunk_type == "coverage_example":
        parts = [f"example: {chunk.get('name', '')}"]
        if chunk.get("total_cost"):
            parts.append(f"total cost: {chunk['total_cost']}")
        if chunk.get("patient_total"):
            parts.append(f"patient pays: {chunk['patient_total']}")
        for k, v in (chunk.get("plan_parameters") or {}).items():
            parts.append(f"{k}: {v}")
        for k, v in (chunk.get("cost_breakdown") or {}).items():
            parts.append(f"{k}: {v}")
        return ". ".join(parts)

    elif chunk_type in ("preamble", "footnote"):
        return chunk.get("content", "")

    elif chunk_type == "plan_metadata":
        parts = []
        if chunk.get("coverage_for"):
            parts.append(f"covers: {chunk['coverage_for']}")
        if chunk.get("plan_type"):
            parts.append(f"plan type: {chunk['plan_type']}")
        return ". ".join(parts)

    elif chunk_type == "excluded_service":
        svc = chunk.get("service", "")
        return f"excluded service: {svc}" if svc else ""

    elif chunk_type == "other_covered_service":
        svc = chunk.get("service", "")
        return f"covered service: {svc}" if svc else ""

    elif chunk_type == "important_question":
        q = chunk.get("question", "")
        a = chunk.get("answer", "")
        return f"question: {q}. answer: {a}"

    # Fallback: dump all string values
    return " ".join(str(v) for v in chunk.values() if isinstance(v, str) and v)


# =========================
# EXTRACT GRAPH VIA LLM
# =========================
def extract_graph(text: str) -> dict:
    """
    Send text to the LLM and get back a structured graph dict with keys:
    entities, relationships, attributes, tables, rules.
    """
    prompt = f"""
You are an expert system for extracting COMPLETE structured knowledge graphs
from health insurance plan documents.

Extract ALL meaningful structured data. Output ONLY valid JSON in this format:

{{
  "entities": [],
  "relationships": [],
  "attributes": [],
  "tables": [],
  "rules": []
}}

----------------------
EXTRACTION GUIDELINES:
----------------------

1. ENTITIES — extract all important named things:
   Plans, Services, Medical events, Cost types, Coverage types, Conditions

2. RELATIONSHIPS — structured triples as arrays ["subject", "REL_TYPE", "object"]:
   HAS_COPAY, HAS_COINSURANCE, HAS_DEDUCTIBLE, HAS_LIMIT,
   REQUIRES, COVERS, NOT_COVERED, APPLIES_TO, REDUCES_BENEFIT,
   HAS_NETWORK_COST, HAS_OUT_OF_NETWORK_COST, HAS_LIMITATION,
   HAS_MEDICAL_EVENT, INCLUDES_SERVICE, EXCLUDES_SERVICE

   Example: ["Specialist visit", "HAS_COPAY", "$50"]

3. ATTRIBUTES — named value triples as arrays ["entity", "attribute_key", "value"]:
   Dollar amounts, percentages, counts, coverage limits, plan details
   Example: ["Deductible", "individual_amount", "$500"]

4. TABLES — one object per service row:
   {{
     "service": "Primary care visit",
     "network_cost": "$35 copay",
     "out_of_network_cost": "40% coinsurance",
     "limitations": "none",
     "requires_preauth": false
   }}

5. RULES — conditions and consequences:
   Example: ["Specialist visit", "REQUIRES", "Preauthorization"]
   Example: ["No preauthorization", "REDUCES_BENEFIT", "50%"]

----------------------
CRITICAL RULES:
----------------------
- Extract EVERYTHING meaningful
- Include ALL numeric values
- Normalize entity names (consistent casing)
- Do NOT miss tables
- Do NOT summarize or explain
- Output ONLY JSON

----------------------
TEXT:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    raw_output = response.choices[0].message.content
    print("\n  RAW LLM OUTPUT:\n", raw_output[:300], "...")

    cleaned = clean_llm_output(raw_output)

    try:
        parsed = json.loads(cleaned)
    except Exception as e:
        print(f"  JSON parse failed: {e}")
        parsed = {
            "entities": [], "relationships": [],
            "attributes": [], "tables": [], "rules": []
        }

    return parsed







# def extract_graph(text: str, chunk_type: str = "unknown", chunk_id: str = "unknown") -> dict:
#     """
#     Chunk-type-aware extraction. The prompt changes based on what kind of
#     chunk is being processed so the LLM knows exactly what to look for.
#     """

#     # ── TYPE-SPECIFIC INSTRUCTIONS ──────────────────────────────────────────

#     type_instructions = {

#         "important_question": """
# You are processing a QUESTION-ANSWER chunk from a health insurance plan.

# This chunk contains:
# - question: a question a plan member would ask
# - answer: the direct answer (often has dollar amounts, limits, thresholds)
# - why_it_matters: a longer explanation of the real-world impact

# Your job:
# 1. Extract the question node with its FULL text preserved
# 2. Extract every numeric value, threshold, rule mentioned in the answer
# 3. Extract every real-world consequence mentioned in why_it_matters
# 4. Link every extracted fact back to the question node

# EXAMPLE INPUT:
#   question: "What is the overall deductible?"
#   answer: "$500/Individual or $1,000/family"
#   why_it_matters: "You must pay all costs up to the deductible before the plan
#                    pays. Family members meet individual deductibles until the
#                    family deductible is met."

# EXAMPLE OUTPUT:
#   important_questions: [
#     {
#       "question": "What is the overall deductible?",
#       "answer": "$500/Individual or $1,000/family",
#       "why_it_matters": "You must pay all costs up to the deductible before..."
#     }
#   ]
#   entities: ["Deductible", "Individual Deductible", "Family Deductible"]
#   relationships: [
#     ["Individual Deductible", "HAS_AMOUNT", "$500"],
#     ["Family Deductible", "HAS_AMOUNT", "$1000"],
#     ["Deductible", "APPLIES_BEFORE", "Plan Payment"]
#   ]
#   attributes: [
#     ["Individual Deductible", "amount", "$500"],
#     ["Family Deductible", "amount", "$1000"],
#     ["Deductible", "rule", "must be met before plan pays"]
#   ]
# """,

#         "benefit_service": """
# You are processing a BENEFIT SERVICE chunk from a health insurance plan.

# This chunk contains:
# - medical_event: the situation (e.g. "visiting a specialist")
# - service: the specific service being covered
# - network_cost: what the member pays IN-network
# - out_of_network_cost: what the member pays OUT-of-network
# - limitations: rules, preauth requirements, penalties
# - requires_preauth: true/false

# Your job:
# 1. Create a node for the service
# 2. Create separate cost nodes for in-network and out-of-network
# 3. Extract copay/coinsurance amounts as individual attributes
# 4. Extract EVERY limitation and penalty as its own relationship
# 5. If preauth is required, create a Preauthorization node and link it
# 6. If there is a penalty for missing preauth, extract the penalty amount

# EXAMPLE INPUT:
#   service: "Specialist visit"
#   network_cost: "$50 copay/visit"
#   out_of_network_cost: "40% coinsurance"
#   limitations: "Preauthorization required. Failure to obtain may reduce
#                 benefits by 50% of total cost."
#   requires_preauth: true

# EXAMPLE OUTPUT:
#   entities: ["Specialist visit", "Specialist visit | Network",
#              "Specialist visit | OutOfNetwork", "Preauthorization",
#              "No Preauthorization Penalty"]
#   relationships: [
#     ["Specialist visit", "HAS_NETWORK_COST", "Specialist visit | Network"],
#     ["Specialist visit", "HAS_OUT_OF_NETWORK_COST", "Specialist visit | OutOfNetwork"],
#     ["Specialist visit", "REQUIRES", "Preauthorization"],
#     ["No Preauthorization Penalty", "REDUCES_BENEFIT", "50%"]
#   ]
#   attributes: [
#     ["Specialist visit | Network", "copay", "$50"],
#     ["Specialist visit | Network", "frequency", "per visit"],
#     ["Specialist visit | OutOfNetwork", "coinsurance", "40%"],
#     ["No Preauthorization Penalty", "reduction", "50% of total cost"]
#   ]
#   rules: [
#     ["Specialist visit", "REQUIRES", "Preauthorization"],
#     ["No Preauthorization Penalty", "REDUCES_BENEFIT", "50%"]
#   ]
# """,

#         "other_covered_service": """
# You are processing an OTHER COVERED SERVICE chunk from a health insurance plan.

# This chunk contains a service that is covered but may have special conditions
# or limitations. The section field tells you which part of the plan it belongs to.

# Your job:
# 1. Create a node for the service
# 2. Link it to the plan as a covered service
# 3. Extract any conditions or limitations mentioned in the service name or section
# 4. Note that limitations may apply even if not fully listed here

# EXAMPLE INPUT:
#   service: "Acupuncture (if prescribed for rehabilitation)"
#   section: "Other Covered Services"

# EXAMPLE OUTPUT:
#   entities: ["Acupuncture", "Rehabilitation"]
#   relationships: [
#     ["HealthPlan", "COVERS_SERVICE", "Acupuncture"],
#     ["Acupuncture", "REQUIRES_CONDITION", "Prescribed for rehabilitation"]
#   ]
#   attributes: [
#     ["Acupuncture", "coverage_condition", "must be prescribed for rehabilitation"],
#     ["Acupuncture", "section", "Other Covered Services"]
#   ]
# """,

#         "excluded_service": """
# You are processing an EXCLUDED SERVICE chunk from a health insurance plan.

# This chunk describes something the plan does NOT cover.

# Your job:
# 1. Create a node for the excluded service
# 2. Link it to the plan as explicitly excluded
# 3. Extract any exceptions (sometimes excluded services have partial exceptions)
# 4. Preserve the exact reason for exclusion if given

# EXAMPLE INPUT:
#   service: "Cosmetic surgery"

# EXAMPLE OUTPUT:
#   entities: ["Cosmetic surgery"]
#   relationships: [
#     ["HealthPlan", "EXCLUDES_SERVICE", "Cosmetic surgery"]
#   ]
#   attributes: [
#     ["Cosmetic surgery", "coverage_status", "not covered"]
#   ]
# """,

#         "coverage_example": """
# You are processing a COVERAGE EXAMPLE chunk from a health insurance plan.

# This chunk contains a real-world cost scenario showing how the plan works
# in practice — total costs, what the patient pays, and a cost breakdown.

# Your job:
# 1. Create a node for the example scenario
# 2. Extract every cost figure with its label
# 3. Extract the plan parameters used in the example (deductible, OOP max, etc.)
# 4. Link the services involved in the example
# 5. The goal is that someone asking "how much would X cost?" can find this node

# EXAMPLE INPUT:
#   name: "Having a Baby"
#   total_cost: "$12,800"
#   patient_total: "$3,160"
#   plan_parameters: {"deductible": "$500", "oop_max": "$5,000"}
#   cost_breakdown: {"hospital_fees": "$9,000", "physician_fees": "$3,800"}

# EXAMPLE OUTPUT:
#   entities: ["Having a Baby Example", "Having a Baby Example | Deductible",
#              "Having a Baby Example | OOP Max"]
#   relationships: [
#     ["HealthPlan", "HAS_EXAMPLE", "Having a Baby Example"],
#     ["Having a Baby Example", "HAS_PARAMETER", "Having a Baby Example | Deductible"],
#     ["Having a Baby Example", "HAS_COST_ITEM", "Having a Baby | Hospital Fees"]
#   ]
#   attributes: [
#     ["Having a Baby Example", "total_cost", "$12,800"],
#     ["Having a Baby Example", "patient_pays", "$3,160"],
#     ["Having a Baby Example | Deductible", "value", "$500"]
#   ]
# """,

#         "section": """
# You are processing a SECTION chunk from a health insurance plan.

# This is a block of policy text from a named section of the document.

# Your job:
# 1. Extract every rule, condition, limit, and threshold stated in the text
# 2. Extract every service or benefit mentioned
# 3. Extract every dollar amount, percentage, or time limit
# 4. Create relationships between rules and the services they apply to
# 5. Preserve important policy language as attributes

# Focus on: what does this section ALLOW, REQUIRE, LIMIT, or EXCLUDE?
# """,
#     }

#     # Default instructions for unknown types
#     default_instructions = """
# You are processing a chunk from a health insurance plan document.
# Extract all entities, relationships, attributes, rules, and important
# questions you can find. Preserve all numeric values and policy language.
# """

#     specific_instructions = type_instructions.get(chunk_type, default_instructions)

#     # ── FULL PROMPT ──────────────────────────────────────────────────────────

#     prompt = f"""
# {specific_instructions}

# ----------------------
# OUTPUT FORMAT — return ONLY valid JSON with exactly these keys:
# ----------------------

# {{
#   "entities": [],
#   "relationships": [],
#   "attributes": [],
#   "tables": [],
#   "rules": [],
#   "important_questions": []
# }}

# FIELD RULES:

# entities:
#   - List of string node names
#   - Short but descriptive: "Specialist visit", "Individual Deductible"
#   - Never just "Plan" or "Service" — always be specific

# relationships:
#   - Each item is a 3-element array: ["subject", "REL_TYPE", "object"]
#   - REL_TYPE must be UPPERCASE_SNAKE_CASE
#   - Allowed types: HAS_COPAY, HAS_COINSURANCE, HAS_DEDUCTIBLE, HAS_LIMIT,
#     HAS_AMOUNT, HAS_NETWORK_COST, HAS_OUT_OF_NETWORK_COST, HAS_LIMITATION,
#     HAS_MEDICAL_EVENT, HAS_IMPORTANT_QUESTION, HAS_EXAMPLE, HAS_PARAMETER,
#     HAS_COST_ITEM, INCLUDES_SERVICE, REQUIRES, REQUIRES_CONDITION,
#     COVERS, COVERS_SERVICE, EXCLUDES_SERVICE, NOT_COVERED,
#     APPLIES_TO, APPLIES_BEFORE, REDUCES_BENEFIT, SUBJECT_TO,
#     REFERENCES, OVERRIDES

# attributes:
#   - Each item is a 3-element array: ["entity", "key", "value"]
#   - Use for: dollar amounts, percentages, counts, full text, policy language
#   - Keys should be lowercase_snake_case: "copay", "amount", "rule", "condition"

# tables:
#   - Only for benefit_service rows
#   - Each item: {{"service","network_cost","out_of_network_cost","limitations","requires_preauth"}}

# rules:
#   - Condition/consequence triples: ["subject", "REL_TYPE", "object"]
#   - Focus on: preauth requirements, penalties, reduction rules, exceptions

# important_questions:
#   - CRITICAL: preserve FULL text — never shorten, summarise, or paraphrase
#   - Each item: {{"question": "...", "answer": "...", "why_it_matters": "..."}}
#   - If the chunk has no question-answer content, return empty list []

# ----------------------
# STRICT RULES:
# ----------------------
# - Output ONLY the JSON object — no explanation, no markdown, no preamble
# - For important_questions: copy the text VERBATIM from the input
# - Every dollar amount and percentage must appear in at least one attribute
# - If requires_preauth is true, ALWAYS create a REQUIRES Preauthorization relationship
# - If a penalty exists for missing preauth, ALWAYS create a REDUCES_BENEFIT rule

# ----------------------
# CHUNK TYPE: {chunk_type}
# CHUNK ID: {chunk_id}
# ----------------------
# TEXT:
# {text}
# """

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0,
#     )

#     raw_output = response.choices[0].message.content
#     print(f"\n  [{chunk_id}] RAW OUTPUT:\n", raw_output[:400], "...")

#     cleaned = clean_llm_output(raw_output)

#     try:
#         parsed = json.loads(cleaned)
#     except Exception as e:
#         print(f"  [{chunk_id}] JSON parse failed: {e}")
#         parsed = {
#             "entities": [], "relationships": [], "attributes": [],
#             "tables": [], "rules": [], "important_questions": []
#         }

#     return parsed

# =========================
# NORMALIZE LLM OUTPUT → GRAPH FORMAT
# =========================
def normalize_llm_graph(llm_output: dict) -> dict:
    """
    Convert the LLM's richer output format into the standard graph format
    that neo4j_handler.insert_graph_data() expects:

    {
      "entities": [str, ...],
      "relationships": [(src, REL_TYPE, dst), ...],
      "attributes": [(entity, key, value), ...]
    }

    This bridges the LLM extractor with Neo4j without changing neo4j_handler.py.
    """
    entities = set()
    relationships = []
    attributes = []

    # --- 1. Explicit entities ---
    for e in llm_output.get("entities", []):
        if isinstance(e, str) and e.strip():
            entities.add(e.strip())

    # --- 2. Relationships (expect ["src", "REL", "dst"] arrays) ---
    for rel in llm_output.get("relationships", []):
        if isinstance(rel, (list, tuple)) and len(rel) == 3:
            src, rel_type, dst = [str(x).strip() for x in rel]
            if src and rel_type and dst:
                entities.add(src)
                entities.add(dst)
                relationships.append((src, rel_type.upper().replace(" ", "_"), dst))

    # --- 3. Attributes (expect ["entity", "key", "value"] arrays) ---
    for attr in llm_output.get("attributes", []):
        if isinstance(attr, (list, tuple)) and len(attr) == 3:
            entity, key, value = [str(x).strip() for x in attr]
            if entity and key and value:
                entities.add(entity)
                attributes.append((entity, key, value))

    # --- 4. Tables → structured nodes + relationships ---
    for row in llm_output.get("tables", []):
        if not isinstance(row, dict):
            continue

        service = str(row.get("service", "")).strip()
        if not service:
            continue

        entities.add(service)

        net = str(row.get("network_cost", "")).strip()
        oon = str(row.get("out_of_network_cost", "")).strip()
        limitations = str(row.get("limitations", "")).strip()
        preauth = row.get("requires_preauth", False)

        if net:
            net_node = f"{service} | Network"
            entities.add(net_node)
            relationships.append((service, "HAS_NETWORK_COST", net_node))
            attributes.append((net_node, "raw", net))

        if oon:
            oon_node = f"{service} | OutOfNetwork"
            entities.add(oon_node)
            relationships.append((service, "HAS_OUT_OF_NETWORK_COST", oon_node))
            attributes.append((oon_node, "raw", oon))

        if limitations and limitations.lower() not in ["none", "", "-"]:
            lim_node = f"{service} | Limitation"
            entities.add(lim_node)
            relationships.append((service, "HAS_LIMITATION", lim_node))
            attributes.append((lim_node, "text", limitations))

        if preauth or (
            "preauthorization" in (net + oon + limitations).lower()
        ):
            entities.add("Preauthorization")
            relationships.append((service, "REQUIRES", "Preauthorization"))

    # --- 5. Rules → relationships (same triple format as relationships) ---
    for rule in llm_output.get("rules", []):
        if isinstance(rule, (list, tuple)) and len(rule) == 3:
            src, rel_type, dst = [str(x).strip() for x in rule]
            if src and rel_type and dst:
                entities.add(src)
                entities.add(dst)
                relationships.append((src, rel_type.upper().replace(" ", "_"), dst))

    return {
        "entities": sorted(entities),
        "relationships": relationships,
        "attributes": attributes,
    }


# =========================
# # COMBINED: chunk list → graph dict
# =========================
def extract_graph_from_chunks(chunks: list[dict]) -> dict:
    """
    Process a list of chunks through:
      chunk_to_text() → extract_graph() → normalize_llm_graph()

    Returns the standard graph dict ready for neo4j_handler.insert_graph_data().
    Skips chunks that produce empty text.
    """
    entities = set()
    relationships = []
    attributes = []

    for chunk in chunks:
        chunk_id = chunk.get("chunk_id", "unknown")
        text = chunk_to_text(chunk)

        if not text.strip():
            print(f"  Skipping empty chunk: {chunk_id}")
            continue

        print(f"  Processing chunk: {chunk_id}")

        llm_output = extract_graph(text)
        normalized = normalize_llm_graph(llm_output)

        entities.update(normalized["entities"])
        relationships.extend(normalized["relationships"])
        attributes.extend(normalized["attributes"])

    return {
        "entities": sorted(entities),
        "relationships": relationships,
        "attributes": attributes,
    }

# def extract_graph_from_chunks(chunks: list[dict]) -> dict:
#     entities = set()
#     relationships = []
#     attributes = []

#     for chunk in chunks:
#         chunk_id   = chunk.get("chunk_id", "unknown")
#         chunk_type = chunk.get("type", "unknown")        # pass type to prompt
#         text       = chunk_to_text(chunk)

#         if not text.strip():
#             print(f"  Skipping empty chunk: {chunk_id}")
#             continue

#         print(f"  Processing [{chunk_type}] chunk: {chunk_id}")

#         llm_output = extract_graph(text, chunk_type, chunk_id)  # pass both
#         normalized = normalize_llm_graph(llm_output)

#         entities.update(normalized["entities"])
#         relationships.extend(normalized["relationships"])
#         attributes.extend(normalized["attributes"])

#     return {
#         "entities": sorted(entities),
#         "relationships": relationships,
#         "attributes": attributes,
#     }