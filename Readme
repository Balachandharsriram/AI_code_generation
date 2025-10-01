⚡ PLC Code Genius: AI-Powered Industrial Automation Assistant 🤖

From plain English to PLC code in seconds

<p align="center"> <img src="https://img.shields.io/badge/AI-Powered-Gemini%201.5%20Flash-blue?style=for-the-badge&logo=google" /> <img src="https://img.shields.io/badge/Backend-FastAPI%20%7C%20Python-green?style=for-the-badge&logo=fastapi" /> <img src="https://img.shields.io/badge/Database-PostgreSQL-orange?style=for-the-badge&logo=postgresql" /> <img src="https://img.shields.io/badge/Vector%20DB-ChromaDB%20%7C%20Transformers-purple?style=for-the-badge&logo=opensearch" /> </p>

PLC Code Genius is an AI-powered backend platform that helps automation engineers and PLC programmers generate production-ready code instantly.
It supports both Structured Text (ST) and Ladder Diagram (LD) formats, enriched with RAG-driven contextual knowledge for accuracy and reliability.

✨ Highlights

🔀 Dual-Format Output → Structured Text (ST) + Ladder Diagram (LD)

🧠 Smarter with RAG → Integrates ChromaDB + Transformers for domain-specific accuracy

✅ Built-in Validation → Catches common ST syntax errors before deployment

⚡ Fast & Lightweight → Powered by FastAPI & Uvicorn

📜 Persistent History → Every generation logged in PostgreSQL for traceability

🛠️ Tech Stack
🔧 Component	🚀 Technology	🎯 Purpose
LLM Engine	Google Gemini 1.5 Flash	Core AI for PLC code generation
RAG/Vector DB	ChromaDB + Sentence Transformers	Contextual knowledge retrieval
Backend	FastAPI + Python	High-performance API services
Database	PostgreSQL + SQLAlchemy	Persistent request history
Runtime	Uvicorn	Async server execution
🗺️ System Architecture
<p align="center"> <img src="architecture-diagram.png" alt="PLC Code Genius Architecture" width="700"/> </p>

User → Gemini (LLM) → RAG Pipeline → FastAPI Backend → PostgreSQL → ST/LD Output

🔍 Example

Input (Natural Language):

“When the start button is pressed, run the conveyor motor for 15 seconds, stop on overload.”

Structured Text (ST):

IF Start_PB AND NOT Stop_PB THEN
    Motor_1 := TRUE;
    TON_1(IN := TRUE, PT := T#10s);
END_IF;

IF TON_1.Q THEN
    Motor_1 := FALSE;
END_IF;


Ladder Diagram (LD):

---[Start_PB]----[Stop_NC]----[Timer_1]----
                                | T4:1.DN |
---[Motor_1]-------------------|         |----(Motor_1)---

---[Timer_1]------------------[TON T4:1 10.0]----

🧩 Use Cases

⚡ Rapid prototyping of PLC logic

📚 Learning aid for engineers new to ST & LD

🛠️ Reduce repetitive coding tasks

🤝 Integrate into HMI/SCADA pipelines

📌 Notes

Works even without RAG (falls back to Gemini).

Syntax checks to reduce debugging time.

Database schema auto-syncs at startup.

🎯 Vision

PLC Code Genius is built to empower automation engineers by:

Reducing manual coding effort 🕒

Minimizing errors with AI validation 🛡️

Accelerating industrial automation projects 🚀
