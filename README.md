# 🧠 GraphRAG — PDF to Knowledge Graph QA System

> Transform PDFs into a structured Neo4j knowledge graph and answer questions using LLM-generated Cypher queries.

---

## 📌 Overview

**GraphRAG** is an end-to-end Retrieval-Augmented Generation (RAG) pipeline that ingests PDF documents, extracts structured knowledge using Vision LLMs, builds a Neo4j knowledge graph, and answers natural language questions by generating and executing Cypher queries.

The system is split into two major stages:

| Stage | Description |
|---|---|
| **Stage 1 — Ingestion** | PDF → HTML extraction → chunking → entity/relation extraction → Neo4j |
| **Stage 2 — Retrieval & QA** | Natural language question → Cypher query → Neo4j → answer |

---

## 🗂️ Project Structure

```
GRAPHRAGFINAL/
│
├── src/                         # Stage 1: Ingestion pipeline
│   ├── main.py                  # Entry point for the ingestion pipeline
│   ├── pdf_to_images.py         # Splits PDF into per-page images
│   ├── vision_extractor.py      # Extracts HTML from images using Vision LLM
│   ├── merge_html.py            # Merges per-page HTML into a single document
│   ├── structuralhtml_chunker.py# Chunks HTML by section headers and tables
│   ├── graph_processor.py       # Orchestrates chunk-to-graph pipeline
│   ├── chunk_to_graph.py        # Extracts entities, relations, values via LLM
│   ├── neo4j_handler.py         # Inserts extracted graph data into Neo4j
│   ├── extractor.py             # Utility extraction helpers
│   ├── prompt.txt               # Prompts used for LLM graph extraction
│   └── neo4j_inserted_output.json  # Log of inserted graph data
│
├── QA_Section/                  # Stage 2: Question answering
│   ├── app.py                   # Streamlit UI — ask questions interactively
│   ├── ask.py                   # Terminal-based single question answering
│   ├── query_pipeline.py        # End-to-end QA orchestration
│   ├── query_to_cypher.py       # Converts natural language to Cypher via LLM
│   └── answer_generator.py      # Generates final answer from Cypher results
│
├── csvfile_test/                # Bulk evaluation & benchmarking
│   ├── evaluate.py              # Runs QA over a CSV of questions
│   └── evaluator.py             # Scores answers, calculates cost/tokens/time
│
├── data/                        # Input PDF documents
├── output/                      # Intermediate outputs (images, merged HTML, etc.)
├── .env                         # API keys and configuration
└── requirements.txt             # Python dependencies
```

---

## 🔄 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     STAGE 1 — INGESTION                      │
│                                                             │
│  PDF ──► pdf_to_images.py ──► vision_extractor.py           │
│          (page images)         (Gemini Pro Vision)          │
│                                      │                      │
│                               HTML per page                 │
│                                      │                      │
│                           merge_html.py                     │
│                         (single HTML file)                  │
│                                      │                      │
│                    structuralhtml_chunker.py                 │
│               (chunks by headers, tables, sections)         │
│                                      │                      │
│                         graph_processor.py                  │
│                                      │                      │
│                    chunk_to_graph.py (LLaMA 4 Maverick)     │
│                  (entities, relations, values)              │
│                                      │                      │
│                         neo4j_handler.py                    │
│                          (→ Neo4j DB)                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   STAGE 2 — RETRIEVAL & QA                   │
│                                                             │
│  Question ──► query_to_cypher.py ──► Cypher Query           │
│              (LLaMA 4 Maverick / Groq)                      │
│                                      │                      │
│                              Neo4j Execution                │
│                                      │                      │
│                         answer_generator.py                 │
│                           (Final Answer)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Technologies Used

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Vision LLM (PDF extraction) | `google/gemini-pro-vision` via **OpenRouter API** |
| Graph extraction LLM | `meta-llama/llama-4-maverick` via **OpenRouter API** |
| QA / Cypher generation | **Groq API** (LLaMA model) as primary or alternative |
| Knowledge Graph DB | **Neo4j** |
| Interactive UI | **Streamlit** |
| Environment Management | **python-dotenv** |
| Evaluation & Benchmarking | Custom CSV-based evaluator |

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- A running **Neo4j** instance (local or cloud via [Neo4j Aura](https://neo4j.com/cloud/aura/))
- API keys for **OpenRouter** and **Groq**

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/project_of_graphrag_byusing_visonllm.git
cd project_of_graphrag_byusing_visonllm
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following keys (this file is git-ignored and should **never** be committed):

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
GROQ_API_KEY=your_groq_api_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password_here
```

> **Get your API keys:**
> - OpenRouter: [https://openrouter.ai](https://openrouter.ai)
> - Groq: [https://console.groq.com](https://console.groq.com)
> - Neo4j Aura (free cloud): [https://neo4j.com/cloud/aura/](https://neo4j.com/cloud/aura/)

> ⚠️ **Never share or commit your `.env` file.** It is already listed in `.gitignore`.

---

### `.gitignore`

The following are excluded from version control:

```gitignore
# Environment variables
.env

# Python cache
__pycache__/
*.pyc

# Virtual environment
venv/

# System files
.DS_Store
```

---

## 🏃 Running the Project

### Stage 1 — Ingest a PDF into Neo4j

Place your PDF file in the `data/` folder, then run:

```bash
cd src
python main.py
```

This will execute the full ingestion pipeline:
1. Converts each PDF page into an image
2. Sends each image to Gemini Pro Vision (via OpenRouter) to extract HTML
3. Merges all HTML pages into one document
4. Chunks the HTML structurally by sections, headers, and tables
5. Extracts entities, relations, and values from each chunk using LLaMA 4 Maverick
6. Inserts the knowledge graph into Neo4j

---

### Stage 2 — Answer Questions

#### Option A: Interactive UI (Streamlit)

```bash
cd QA_Section
streamlit run app.py
```

Opens a web interface in your browser where you can type questions and get answers interactively.

#### Option B: Terminal (Single Question)

```bash
cd QA_Section
python ask.py
```

Prompts you to type a question in the terminal and prints the answer directly.

---

### Bulk Evaluation (CSV Mode)

If you have a CSV file of questions with expected answers, use the evaluation module to test in bulk:

```bash
cd csvfile_test
python evaluate.py
```

Your input CSV should have columns for the question and the expected/reference answer.

The evaluator will generate a **new output CSV** with the following added columns:

| Column | Description |
|---|---|
| `generated_answer` | The answer produced by the pipeline |
| `score` | `1` if correct, `0` if incorrect |
| `input_tokens` | Number of input tokens consumed |
| `output_tokens` | Number of output tokens produced |
| `time_taken` | Response time in seconds |
| `cost` | Estimated API cost |

---

## 🔑 API Key Summary

| Key | Used For | Required |
|---|---|---|
| `OPENROUTER_API_KEY` | Vision extraction (Gemini Pro Vision) + Graph extraction (LLaMA 4 Maverick) | ✅ Yes |
| `GROQ_API_KEY` | Cypher query generation and answer generation | ✅ Yes (or OpenRouter as fallback) |
| `NEO4J_URI` + credentials | Storing and querying the knowledge graph | ✅ Yes |

---

## 🧩 Module Details

### `src/pdf_to_images.py`
Splits every page of a PDF into individual image files for Vision LLM processing.

### `src/vision_extractor.py`
Sends each page image to **Gemini Pro Vision** via OpenRouter and returns the page content as structured HTML, preserving tables, headings, and text layout.

### `src/merge_html.py`
Concatenates all per-page HTML outputs into a single unified HTML document.

### `src/structuralhtml_chunker.py`
Parses the merged HTML and splits it into semantic chunks based on structural elements — section headers (`<h1>`, `<h2>`, etc.), table boundaries, and logical document sections. Ensures each chunk is self-contained and contextually meaningful.

### `src/chunk_to_graph.py`
Uses **LLaMA 4 Maverick** (via OpenRouter) to process each chunk and extract:
- **Entities** — Named concepts, objects, people, organizations
- **Relations** — Connections between entities
- **Values** — Attributes and properties

### `src/neo4j_handler.py`
Takes extracted graph data and writes nodes and relationships into the **Neo4j** database using the Bolt protocol.

### `QA_Section/query_to_cypher.py`
Takes a natural language question and uses an LLM (Groq / OpenRouter) to generate a valid **Cypher query** tailored to the graph schema in Neo4j.

### `QA_Section/answer_generator.py`
Executes the Cypher query against Neo4j, retrieves results, and synthesizes a coherent natural language answer.

### `csvfile_test/evaluator.py`
Evaluates generated answers against reference answers, assigning a binary score (`1`/`0`), and tracks token usage, latency, and cost per question.

---

## 📋 Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

Full `requirements.txt`:

```
neo4j
groq
python-dotenv
pdfplumber
langchain
langchain-text-splitters
langchain-community
langchain-core
tiktoken
openai
pdf2image
pillow
tqdm
bs4
streamlit
```

| Package | Purpose |
|---|---|
| `neo4j` | Neo4j Python driver for graph DB operations |
| `groq` | Groq API client for LLM inference |
| `python-dotenv` | Loads environment variables from `.env` |
| `pdfplumber` | PDF text and table extraction |
| `langchain` + `langchain-*` | LLM orchestration, text splitting, and chaining |
| `tiktoken` | Token counting for OpenAI-compatible models |
| `openai` | OpenAI-compatible client (used with OpenRouter) |
| `pdf2image` | Converts PDF pages to images for Vision LLM |
| `pillow` | Image processing library |
| `tqdm` | Progress bars for long-running pipelines |
| `bs4` | BeautifulSoup — HTML parsing and chunking |
| `streamlit` | Interactive web UI for QA |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---
