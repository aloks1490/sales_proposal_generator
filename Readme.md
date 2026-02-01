# AI Proposal Generator  
**Local RAG-powered business proposal writer**  
(using Ollama + Chroma + LangChain)

Generate structured, professional sales proposals from your company documents + meeting notes — **completely offline** and **private**.

https://github.com/yourusername/ai-proposal-generator  
*(replace with your actual repo link)*

## ✨ Features

- Fully **local** execution (no OpenAI / Anthropic / cloud dependency)
- Uses lightweight **Ollama** model (`granite4:1b` or any model you prefer)
- Embeds documents with fast & compact **all-MiniLM-L6-v2**
- Persistent vector storage with **Chroma**
- Supports **PDF, DOCX, TXT** company files
- Streamlit interface — simple drag & drop + paste meeting notes
- Custom instructions field (e.g. "emphasize ROI", "focus on sustainability")
- Outputs clean **Markdown** proposal with standard B2B structure
- One-click download of generated proposal

## Proposal Structure (fixed)

```markdown
# Proposal

## 1. Executive Summary

## 2. Understanding Your Needs

## 3. Proposed Solution

## 4. Pricing & Packages

## 5. Next Steps
```

## Tech Stack

| Component          | Technology                                   | Notes                              |
|--------------------|----------------------------------------------|------------------------------------|
| UI                 | Streamlit                                    | Simple & fast                      |
| LLM                | Ollama                                       | granite4:1b (default)              |
| Embeddings         | sentence-transformers/all-MiniLM-L6-v2       | ~80 MB, very fast                  |
| Vector Database    | Chroma                                       | persistent on disk                 |
| Document loading   | LangChain loaders                            | PDF, DOCX, TXT                     |
| RAG Framework      | LangChain (LCEL)                             | clean chain composition            |

## Quick Start

### 1. Prerequisites

- Python 3.11
- [Ollama](https://ollama.com/) installed and running
- At least 8 GB RAM recommended

```bash
# Pull the model once (or choose another small model)
ollama pull granite4:1b
# or try: llama3.2:3b, phi3:3.8b, gemma2:2b, etc.