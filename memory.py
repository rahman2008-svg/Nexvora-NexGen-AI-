import json, os

MEM_FILE = 'memory.json'

def load_knowledge():
    if os.path.exists(MEM_FILE):
        with open(MEM_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def add_knowledge(question, answer):
    knowledge = load_knowledge()
    knowledge[question] = answer
    with open(MEM_FILE, 'w', encoding='utf-8') as f:
        json.dump(knowledge, f, ensure_ascii=False, indent=2)
