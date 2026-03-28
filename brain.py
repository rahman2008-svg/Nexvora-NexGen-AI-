import memory
from rapidfuzz import fuzz

def get_answer(question):
    knowledge = memory.load_knowledge()
    best_match = None
    highest_score = 0
    for q, a in knowledge.items():
        score = fuzz.ratio(question.lower(), q.lower())
        if score > highest_score:
            highest_score = score
            best_match = a
    if best_match:
        return best_match
    else:
        return "এটি শেখানো হয়নি, তুমি Teach AI ব্যবহার করে এটি শিখাতে পারো।"
