# 🤖 DEVFORGE Student Support AI Agent

An AI-powered student support assistant built for the **DEVFORGE AI Engineering Internship**.

The agent helps students with learning and technical questions related to Python, FastAPI, LangChain, LangGraph, RAG, GitHub, AI Engineering, deployment, assignments, and project guidance.

The application uses **LangGraph** for workflow orchestration, **LangChain** for prompt construction, a lightweight knowledge-base retrieval system for RAG, and the **Ollama Cloud API** for AI-generated responses.

---

## 🚀 Features

- AI-powered DEVFORGE student support
- FastAPI backend
- LangGraph agent workflow
- LangChain prompt management
- Ollama Cloud API integration
- Cloud-hosted `gpt-oss:20b` model
- Retrieval-Augmented Generation (RAG)
- DEVFORGE knowledge base
- Question classification
- Safe responses for unrelated questions
- Environment-variable-based API key management
- Interactive FastAPI Swagger documentation
- Simple web chatbot frontend
- Vercel deployment support

---

## 🧠 Agent Workflow

The application uses a LangGraph workflow with three main stages:

```text
User Question
      │
      ▼
Question Classification
      │
      ├── Related ──────► AI Support Agent
      │                         │
      │                         ▼
      │                  Knowledge Retrieval
      │                         │
      │                         ▼
      │                   LangChain Prompt
      │                         │
      │                         ▼
      │                    Ollama Cloud
      │                         │
      │                         ▼
      │                    Final Answer
      │
      └── Unrelated ────► Safe Response