# src/query_pipeline.py
from query_to_cypher import question_to_cypher
#from neo4j_handler import Neo4jHandler
from answer_generator import generate_answer
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from neo4j_handler import Neo4jHandler
MODEL_CONTEXT_LIMIT = 128000


def ask_question(question):

    start_time = time.time()
    print(f"\nQuestion: {question}")

    # ==========================================
    # STEP 1: QUESTION -> CYPHER
    # ==========================================
    cypher_result = question_to_cypher(question)

    cypher = cypher_result["cypher"]

    print(f"\nGenerated Cypher:\n{cypher}")

    # ==========================================
    # STEP 2: RUN NEO4J QUERY
    # ==========================================
    neo4j = Neo4jHandler()

    result = neo4j.run_query(cypher)

    neo4j.close()

    print(f"\nDB Result:\n{result}")

    # ==========================================
    # STEP 3: ANSWER GENERATION
    # ==========================================
    answer_result = generate_answer(question, result)

    answer = answer_result["answer"]

    print(f"\nThis is the answer retrieved from the Neo4j database:\n{answer}")

    # ==========================================
    # FINAL TOKEN + COST SUMMARY
    # ==========================================
    total_prompt_tokens = (
        cypher_result["prompt_tokens"]
        + answer_result["prompt_tokens"]
    )

    total_completion_tokens = (
        cypher_result["completion_tokens"]
        + answer_result["completion_tokens"]
    )

    final_total_tokens = (
        cypher_result["total_tokens"]
        + answer_result["total_tokens"]
    )

    final_total_cost = (
        cypher_result["total_cost"]
        + answer_result["total_cost"]
    )

    remaining_tokens = MODEL_CONTEXT_LIMIT - final_total_tokens

    # ==========================================
    # PRINT FINAL SUMMARY
    # ==========================================
    print("\n========== FINAL LLM USAGE ==========")

    print(f"Total Prompt Tokens      : {total_prompt_tokens}")
    print(f"Total Completion Tokens  : {total_completion_tokens}")
    print(f"Final Total Tokens       : {final_total_tokens}")
    #print(f"Remaining Context Tokens : {remaining_tokens}")

    print("\n========== FINAL LLM COST ==========")

    print(f"Final Total Cost         : ${final_total_cost:.6f}")


    end_time = time.time()

    total_time = end_time - start_time

    print("\n========== RESPONSE TIME ==========")
    print(f"Total Retrieval Time : {total_time:.2f} seconds")


   
   # return answer
    return {
    "answer": answer,
    "prompt_tokens": total_prompt_tokens,
    "completion_tokens": total_completion_tokens,
    "total_tokens": final_total_tokens,
    "total_time": round(total_time, 2),
    "total_cost": round(final_total_cost, 6)
}