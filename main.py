import sqlite3
from datetime import datetime
from typing import List, Dict
from fastmcp import FastMCP
import asyncio
import os

mcp = FastMCP(name="expense-db-server")

# Global connection
conn = None
DB_FILE = "expenses.db"


async def init_db():
    """Initialize SQLite database for expenses"""
    global conn
    if conn is not None:
        return
    
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()


@mcp.tool
async def add_expense(amount: float, category: str, description: str = "") -> int:
    """
    Add a new expense
    
    Args:
        amount: Expense amount
        category: Expense category (e.g., 'food', 'transport', 'utilities')
        description: Optional description
    
    Returns:
        ID of the added expense
    """
    await init_db()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, description, date))
    conn.commit()
    return cursor.lastrowid


@mcp.tool
async def get_total() -> float:
    """Get total of all expenses"""
    await init_db()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) as total FROM expenses')
    result = cursor.fetchone()
    return result['total'] or 0.0


@mcp.tool
async def get_all_expenses() -> List[Dict]:
    """Get all expenses"""
    await init_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    return [dict(row) for row in cursor.fetchall()]


if __name__ == "__main__":
    asyncio.run(init_db())
    mcp.run()
