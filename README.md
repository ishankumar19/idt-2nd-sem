# LIGHT 🤖 — Adaptive Quiz Generator

LIGHT is a Flask-based adaptive quiz application that generates personalized MCQ quizzes using the Google Gemini API. It focuses more questions on your weak topics and fewer on your strong ones, helping you study smarter.

---

## Features

- 🎯 **Adaptive questioning** — 65% of questions target weak topics, 35% target strong topics
- 📄 **PDF support** — Upload study material and generate questions directly from it
- 🌙 **Dark-themed UI** — Clean chat-style interface
- ✅ **Instant review** — See your score, correct answers, and explanations after each quiz

---

## Tech Stack

- **Backend**: Python, Flask
- **AI**: Google Gemini API (`gemini-3-flash-preview`)
- **Frontend**: HTML, CSS, JavaScript

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/light-quiz.git
cd light-quiz
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

You can get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Run the app

```bash
python light.py
```

Open your browser and go to `http://localhost:5000`.

---

## Usage

1. Type your **weak topics** (comma separated) in the chat input — e.g. `Thermodynamics, Fluid Mechanics`
2. LIGHT generates 10 adaptive MCQs instantly
3. Answer all questions and click **Submit All Answers**
4. Review your score and explanations

---

## Project Structure

```
light-quiz/
├── light.py              # Flask backend, Gemini API integration
└── templates/
    └── index.html        # Frontend UI
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Your API key |

---
