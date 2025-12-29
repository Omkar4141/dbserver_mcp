

# 💰 Expense Tracker using MCP (FastMCP + LangChain + Ollama)- Sample Project for understanding MCP 

This project demonstrates a **simple end-to-end MCP (Model Context Protocol)** example where:

* A **FastMCP server** exposes tools to manage expenses stored in **SQLite**
* A **LangChain client** connects to the MCP server
* An **LLM (Llama 3.2 via Ollama)** decides when to call tools
* Natural language queries like

  > *"Add my expense 500 to groceries"*
  > automatically trigger backend database operations


## 📌 Architecture Overview

```
User (CLI)
   │
   ▼
LangChain Client (client.py)
   │
   │  MCP (stdio)
   ▼
FastMCP Server (main.py)
   │
   ▼
SQLite Database (expenses.db)
```

### Key Components

| Component                 | Description                            |
| ------------------------- | -------------------------------------- |
| **FastMCP**               | Exposes database operations as tools   |
| **LangChain MCP Adapter** | Connects LLM to MCP tools              |
| **Ollama (Llama 3.2:3b)** | Interprets user intent and calls tools |
| **SQLite**                | Persistent expense storage             |

---

## 📂 Project Structure

```
.
├── main.py        # FastMCP expense database server
├── client.py      # LangChain MCP client with LLM
├── expenses.db    # SQLite database (auto-created)
└── README.md
```

## 🚀 Features

* ✅ Add expenses using natural language
* ✅ View total expenses
* ✅ List all expenses
* ✅ Automatic tool selection by LLM
* ✅ Persistent storage using SQLite
* ✅ MCP-compliant architecture


## 🛠️ Tools Exposed by MCP Server

The FastMCP server exposes the following tools:

### `add_expense`

Adds a new expense entry.

```json
{
  "amount": 500,
  "category": "groceries",
  "description": "weekly shopping"
}
```

### `get_total`

Returns the total sum of all expenses.


### `get_all_expenses`

Returns a list of all recorded expenses.


## ⚙️ Prerequisites

Make sure you have the following installed:

* **Python 3.10+**
* **Ollama**
* **Llama 3.2 model**
* **uv** (Python package runner)

```bash
ollama pull llama3.2:3b
```

## 📦 Install Dependencies

```bash
uv add fastmcp langchain langchain-mcp-adapters langchain-ollama
```

## ▶️ Running the Client

Update paths inside `client.py`:

```python
"command": "/home/omkar/.local/bin/uv",
"args": [
    "run",
    "fastmcp",
    "run",
    "/full/path/to/main.py"
]
```

Then run:

```bash
uv run client.py
```

## 🧠 How It Works (Step-by-Step)

1. User enters a natural language query
2. LLM decides whether a tool is needed
3. If required:

   * Tool name + arguments are generated
4. LangChain invokes MCP tool
5. Result is returned to LLM
6. LLM generates final user-friendly respons




Just tell me 👍
