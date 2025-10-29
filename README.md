# Natural Language to SQL Autonomous Agent Dashboard 🤖📊

This project is a web-based BI dashboard that lets non-technical users query a database using plain English. An autonomous AI agent, built with **LangGraph** and **Google Gemini**, translates these questions into SQL, executes them, and intelligently self-corrects if the SQL fails.

---

## ✨ Features
* **Natural Language Querying:** Ask questions like "Show top 5 customers by revenue."
* **AI-Powered SQL Generation:** Uses Google Gemini to convert natural language into SQL.
* **Autonomous Execution:** The agent runs the generated SQL against a SQLite database.
* **Self-Correction Loop:** If a query fails, the agent rewrites it and tries again.
* **(Planned) Web Interface:** A Streamlit front-end (`app.py`) for user interaction.

---

## 🛠️ Tech Stack
* **AI Agent:** LangGraph, LangChain
* **LLM:** Google Gemini (e.g., `gemini-2.0-flash-001`)
* **Database:** SQLite
* **Data Handling:** Pandas
* **Web (Planned):** Streamlit

---

## 🚀 Setup
1.  **Clone the repository:**
    ```bash
    git clone the repo
    cd autonomous-sql-analyst
    ```

3.  **Set up API Key:**
    * Create a `.env` file (you can rename `.env.example`).
    * Add your Google API key: `GOOGLE_API_KEY="YOUR_API_KEY_HERE"`
    * (For Colab, use the Secrets tab to add `GEMINI_KEY`).
4.  **Prepare Your Database:**
    * This project requires **your own** dataset (e.g., CSV).
    * You must create a SQLite database file named `business_data.sqlite3` from your data.
    * The `data_setup.py` script is **just an example** for a specific Kaggle dataset. You must modify it or write your own script to process **your data** into **your schema**.

---

## 📜 Database Schema (Example Only)

**⚠️ IMPORTANT:** The schema below is **only an example** from the `data_setup.py` script. It **is not** your schema.

 Agents will use the tools to fetch the datails about your schemas from your database provided.

<details>
<summary>Click to see the example schema (for reference only)</summary>

```sql
-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    city TEXT
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id INTEGER,
    order_date TIMESTAMP NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order Items table (Bridge Table)
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    line_total REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Indexes for performance:
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);

```
</details>
 Future Work

* **Robust Streamlit Frontend:** Build out `app.py` with `st.status`, `st.dataframe`, and charts.
* **Business Insight Visualization:** Automatically generate charts (KPIs, bar charts) from results.
* **Improved Agent Responses:** Handle complex queries (trends, comparisons) and ask clarifying questions.
* **Advanced Error Handling:** Try different SQL dialects or query strategies on repeated failure.
* **Query Caching/History:** Save successful queries and show user history in the UI.
* **Schema Discovery Tool:** Give the agent a tool to fetch the DB schema dynamically.
