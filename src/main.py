import os
from pdf_to_images import convert_pdf_to_images
from vision_extractor import extract_page
from merge_html import merge_html_pages
from structuralhtml_chunker import chunk_html
from graph_processor import process_chunks

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PDF_PATH = os.path.join(BASE_DIR, "data", "sbc.pdf")
IMAGE_DIR = os.path.join(BASE_DIR, "output", "pages")
RAW_DIR = os.path.join(BASE_DIR, "output", "raw_llm")
FINAL_JSON = os.path.join(BASE_DIR, "output", "final_json", "sbc.json")
HTML_DIR = os.path.join(BASE_DIR, "output", "html")
COMBINED_HTML = os.path.join(BASE_DIR, "output", "combined.html")

#  FIXED PATHS
output_dir = os.path.join(BASE_DIR, "output")
chunk_path = os.path.join(output_dir, "chunksforllm2.json")


def main():
    print(" Converting PDF to images...")
   # images = convert_pdf_to_images(PDF_PATH, IMAGE_DIR)

    print(" Extracting with Vision LLM...")
    os.makedirs(HTML_DIR, exist_ok=True)

#    # for i, img in enumerate(images):
#         print(f"Processing page {i+1}...")
#         result = extract_page(img, i + 1)

#         html_path = os.path.join(HTML_DIR, f"page_{i+1}.html")
#         with open(html_path, "w", encoding="utf-8") as f:
#             f.write(result)

    print(" Merging JSON output...")
   # merge_pages(RAW_DIR, FINAL_JSON)

    #  STEP 1: Merge HTML
    print(" Merging HTML pages...")
   # merge_html_pages(HTML_DIR, COMBINED_HTML)

    #  STEP 2: Chunk combined HTML
    print("Chunking HTML...")
    # chunk_html(COMBINED_HTML, chunk_path)

    #  STEP 3: Process graph
    print(" Extracting Graph + Storing in Neo4j...")
    process_chunks(chunk_path, output_dir)

    print("\n PIPELINE COMPLETED")


if __name__ == "__main__":
    main()