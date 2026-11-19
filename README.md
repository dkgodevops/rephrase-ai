# ✍️ Smart Grammar & Tone Rewriter

A beginner-friendly AI application built in Python that demonstrates **prompt engineering**, **structured outputs (JSON schema)**, and **interactive UI development** using the Google Gemini API.

---

## 📁 Project Structure

```text
smart-tone-rewriter/
├── app.py             # Streamlit interactive web frontend
├── rewriter.py        # Core AI logic & Pydantic structured output schema
├── requirements.txt   # Dependencies
├── .env.example       # API Key configuration template
└── README.md          # Guide & instructions
```

---

## 🚀 Quickstart in VS Code

### 1. Open the Project in VS Code
Open VS Code and use `File > Open Folder...` to select:
```text
C:\Users\devel\.gemini\antigravity\scratch\smart-tone-rewriter
```

### 2. Set Up a Virtual Environment
Open the integrated terminal in VS Code (`Ctrl + ~` or ``Ctrl + ` ``) and run:

```bash
# Create virtual environment
python -m venv .venv

# Activate it (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 3. Set Your API Key
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Get your free API key from [Google AI Studio](https://aistudio.google.com/).
3. Paste it inside `.env`:
   ```env
   GEMINI_API_KEY=your_actual_key_here
   ```

### 4. Test the Core AI Logic (Terminal Test)
Run `rewriter.py` directly to see the structured output in your terminal:
```bash
python rewriter.py
```

### 5. Launch the Web UI
Run the Streamlit app:
```bash
streamlit run app.py
```
This opens the app in your browser at `http://localhost:8501`.

---

## 🧠 Key Concepts You Learn Here
1. **Pydantic Response Schemas:** Using `response_schema=RewriteResult` ensures the model returns exact types (strings, lists) rather than unpredictable unstructured text.
2. **System vs. User Instructions:** How role definitions steer tone and enforce grammar accuracy.
3. **Decoupled Architecture:** `rewriter.py` is an independent module with zero frontend code, meaning it can be plugged into a CLI, a web API (FastAPI), or a desktop tool.
