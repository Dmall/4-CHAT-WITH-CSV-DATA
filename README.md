# 📊 PandasAI CSV Data Explorer

This project demonstrates how to use **[PandasAI](https://github.com/gventuri/pandas-ai)** to analyze CSV data using natural language queries. With the power of **pandas** and **LLMs (Large Language Models)**, you can ask questions about your data in plain English — no need to write complex Python code!

---

## 🚀 Features

- Load and explore any CSV dataset
- Ask natural language questions (e.g., "What's the average age?" or "Show me the top 5 countries by GDP")
- Automatically interprets and executes queries using PandasAI
- Simple, interactive, and extensible

---


### Project Setup

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-folder>
```

#### 2. Create a Virtual Environment
```bash
conda create -p env python=3.10 -y
```

#### 3. Activate the Virtual Environment
```bash
conda activate env/
```

#### 4. Install Project Requirements
```bash
pip install -r requirements.txt
```

#### 5. Environment Variables
Create a .env file and add the required key-value pairs:
```bash
OPENAI_API_KEY = your_api_key
```

#### 6. How to Run the Project
```bash
streamlit run app.py
```