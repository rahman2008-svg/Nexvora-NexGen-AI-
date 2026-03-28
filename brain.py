from memory import find_answer, random_qa, save_qa
from context import save_context, get_context
from nlp import detect_intent, extract_keywords, build_sentence
import random

def clean_text(text):
    return text.strip().lower()


def match_by_keywords(question):
    data = random_qa()
    return data


def smart_generate(question, context):
    q = question.lower()

    # 🔥 follow-up understanding
    if "আগেরটা" in q:
        if context:
            return "আগের প্রশ্ন ছিল: " + context[-1]['q']

    if "বাংলাদেশ" in q and "জেলা" in q:
        return "৬৪"

    if "রাজধানী" in q:
        return "ঢাকা"

    return None


def generate_smart_answer(question):
    intent = detect_intent(question)
    keywords = extract_keywords(question)

    item = random_qa()

    if not item:
        return "আমি এখনো শিখছি, আমাকে Teach করো 😊"

    base = item['answer']

    final = build_sentence(base, intent)

    return final


def learn_clean(question, answer):
    if len(question) > 5 and len(answer) > 3:
        save_qa(clean_text(question), answer)


def chat_ai(user, question):
    context = get_context(user)

    # 1. direct memory
    ans = find_answer(question)
    if ans:
        final = ans
        save_context(user, question, final)
        return final

    # 2. smart rule
    smart = smart_generate(question, context)
    if smart:
        intent = detect_intent(question)
        final = build_sentence(smart, intent)

        save_context(user, question, final)
        return final

    # 3. AI generate
    final = generate_smart_answer(question)

    # 4. learn
    learn_clean(question, final)

    save_context(user, question, final)

    return final
