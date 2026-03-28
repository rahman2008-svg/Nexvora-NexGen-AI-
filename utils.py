import json, os
from rapidfuzz import process

MEMORY_FILE = "ai_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def teach_ai(question, answer):
    memory = load_memory()
    memory.append({"question": question, "answer": answer})
    save_memory(memory)

def ask_ai(user_question):
    memory = load_memory()
    if not memory:
        return "এখনো কিছু শেখানো হয়নি।"
    questions = [item["question"] for item in memory]
    best_match = process.extractOne(user_question, questions)
    if best_match and best_match[1] > 60:
        idx = questions.index(best_match[0])
        return memory[idx]["answer"]
    return "মাফ করবেন, আমি এখনো সেই তথ্য শিখিনি।"
