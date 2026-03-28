from tinydb import TinyDB
from rapidfuzz import process, fuzz
import random

db = TinyDB('memory.json')

def save_qa(q, a):
    db.insert({'question': q.lower(), 'answer': a})

def get_all():
    return db.all()

def find_answer(question):
    data = get_all()
    if not data:
        return None

    questions = [i['question'] for i in data]

    result = process.extractOne(
        question.lower(),
        questions,
        scorer=fuzz.WRatio
    )

    if result:
        match, score, idx = result

        if score > 85:
            return data[idx]['answer']

    return None


def random_qa():
    data = get_all()
    if not data:
        return None
    return random.choice(data)
