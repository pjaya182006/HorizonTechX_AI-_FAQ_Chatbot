# HorizonTechX_AI-_FAQ_Chatbot
# AI FAQ Conversational SaaS Engine

A production-quality, responsive AI-powered FAQ Chatbot web application platform built with Python Flask, SQLite, and an NLP text-matching engine utilizing scikit-learn (TF-IDF vectorization) and NLTK.

Designed with a modern, high-fidelity WhatsApp-style interface, this platform serves as an enterprise-grade SaaS product template capable of parsing natural language customer queries and matching them securely with relevant solutions.

---

## 🚀 Key Features Matrix

* **Intelligent NLP Processing Engine:** Tokenizes and vectorizes data dynamically using a TF-IDF implementation to handle query intent and semantic tracking.
* **Modern WhatsApp-Inspired Chat View:** Full Light/Dark mode responsiveness, custom sender bubbles, automated smooth scrolling, and dynamic chat animations.
* **Automated Suggestion Vectors:** Displays alternative fallback questions if a user's input falls below the specified confidence threshold engine limits.
* **Administrative Metrics Control Console:** Secure management environment featuring analytics overview charts, live message logging history tracking, and manual CRUD capability for the FAQ knowledge registry.
* **SaaS Productivity Toolkits:** Text-to-Speech (TTS) voice modulation responses and historical thread session downloads exported directly as clean `.csv` schemas.

---

## 🛠️ Project Directory Tree

```text
faq_chatbot/
│
├── config.py
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── faq.json
│
├── database/
│   └── chatbot.db         # Auto-generated at initialization
│
├── utils/
│   ├── __init__.py
│   ├── nlp_engine.py
│   └── db_manager.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
└── templates/
    ├── base.html
    ├── index.html
    ├── chatbot.html
    ├── admin.html
    ├── about.html
    └── contact.html
