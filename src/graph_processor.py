
import json
import os
from chunk_to_graph import chunks_to_graph_data
from neo4j_handler import Neo4jHandler

def process_chunks(chunk_path, output_dir, batch_size=20):
    """
    Process chunks using the reliable rule-based approach.
    batch_size is kept for compatibility and future-proofing, 
    but not really needed for performance.
    """

    print(f" Loading chunks from: {chunk_path}")
    with open(chunk_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    print(f" Processing {len(chunks)} chunks using rule-based transformer...")

    # Process in batches
    all_graphs = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"   Processing batch {i//batch_size + 1} ({len(batch)} chunks)")

        graph_data = chunks_to_graph_data(batch)   # rule-based
        all_graphs.append(graph_data)

    # Merge all batches
    final_graph = {
        "entities": [],
        "relationships": [],
        "attributes": []
    }

    for g in all_graphs:
        final_graph["entities"].extend(g.get("entities", []))
        final_graph["relationships"].extend(g.get("relationships", []))
        final_graph["attributes"].extend(g.get("attributes", []))

    # Remove duplicates (simple way)
    final_graph["entities"] = list(dict.fromkeys(final_graph["entities"]))

    print(f" Final Stats - Entities: {len(final_graph['entities'])} | "
          f"Relationships: {len(final_graph['relationships'])} | "
          f"Attributes: {len(final_graph['attributes'])}")

    # Save final graph
    output_file = os.path.join(output_dir, "final_graph.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_graph, f, indent=2)
    print(f" Saved final graph: {output_file}")

    # Insert into Neo4j
    print("  Inserting into Neo4j...")
    neo4j = Neo4jHandler()
    neo4j.insert_graph_data(final_graph)
    neo4j.close()

    print(" Rule-based processing completed successfully!")
    return final_graph




# # graph_processor.py

# import json
# import os
# from extractor import extract_graph_from_chunks   # replaces chunk_to_graph import
# from neo4j_handler import Neo4jHandler


# def process_chunks(chunk_path: str, output_dir: str, batch_size: int = 10):
#     """
#     Load chunks from a JSON file, extract a knowledge graph using the LLM
#     extractor, merge all batches, save to disk, and insert into Neo4j.

#     batch_size is smaller than the old rule-based version (was 20) because
#     LLM calls are rate-limited. Tune this to your Groq tier.
#     """

#     print(f"  Loading chunks from: {chunk_path}")
#     with open(chunk_path, "r", encoding="utf-8") as f:
#         chunks = json.load(f)

#     os.makedirs(output_dir, exist_ok=True)

#     total = len(chunks)
#     print(f"  Processing {total} chunks via LLM extractor (batch_size={batch_size})...")

#     all_entities = set()
#     all_relationships = []
#     all_attributes = []

#     for i in range(0, total, batch_size):
#         batch = chunks[i : i + batch_size]
#         batch_num = i // batch_size + 1
#         print(f"\n  Batch {batch_num} ({len(batch)} chunks, "
#               f"chunks {i+1}–{min(i+batch_size, total)} of {total})")

#         # LLM-based extraction (replaces chunks_to_graph_data)
#         graph_data = extract_graph_from_chunks(batch)

#         all_entities.update(graph_data.get("entities", []))
#         all_relationships.extend(graph_data.get("relationships", []))
#         all_attributes.extend(graph_data.get("attributes", []))

#         print(f"    Batch result — entities: {len(graph_data['entities'])} | "
#               f"relationships: {len(graph_data['relationships'])} | "
#               f"attributes: {len(graph_data['attributes'])}")

#     # De-duplicate relationships and attributes
#     # (entities is already a set so no duplicates there)
#     seen_rels = set()
#     unique_rels = []
#     for rel in all_relationships:
#         key = tuple(rel)
#         if key not in seen_rels:
#             seen_rels.add(key)
#             unique_rels.append(rel)

#     seen_attrs = set()
#     unique_attrs = []
#     for attr in all_attributes:
#         key = tuple(attr)
#         if key not in seen_attrs:
#             seen_attrs.add(key)
#             unique_attrs.append(attr)

#     final_graph = {
#         "entities": sorted(all_entities),
#         "relationships": unique_rels,
#         "attributes": unique_attrs,
#     }

#     print(f"\n  Final stats — "
#           f"entities: {len(final_graph['entities'])} | "
#           f"relationships: {len(final_graph['relationships'])} | "
#           f"attributes: {len(final_graph['attributes'])}")

#     # Save final merged graph to disk
#     output_file = os.path.join(output_dir, "final_graph.json")
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(final_graph, f, indent=2)
#     print(f"  Saved final graph: {output_file}")

#     # Insert into Neo4j (neo4j_handler is unchanged)
#     print("  Inserting into Neo4j...")
#     neo4j = Neo4jHandler()
#     neo4j.insert_graph_data(final_graph)
#     neo4j.close()

#     print("  LLM-based processing completed successfully!")
#     return final_graph