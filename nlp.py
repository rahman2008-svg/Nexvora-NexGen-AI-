# বাংলা NLP Engine

def detect_intent(text):
    t = text.lower()

    if any(x in t for x in ["কে", "what", "কি"]):
        return "definition"

    if any(x in t for x in ["কত", "how many", "number"]):
        return "quantity"

    if any(x in t for x in ["কেন", "why"]):
        return "reason"

    if any(x in t for x in ["কিভাবে", "how"]):
        return "process"

    return "general"


def extract_keywords(text):
    words = text.lower().split()

    stop_words = ["কি", "কত", "কে", "কেন", "কিভাবে", "the", "is"]

    keywords = [w for w in words if w not in stop_words]

    return keywords


def build_sentence(answer, intent):
    if intent == "definition":
        return f"{answer}"

    if intent == "quantity":
        return f"এটার সংখ্যা হলো: {answer}"

    if intent == "reason":
        return f"এর কারণ হলো: {answer}"

    if intent == "process":
        return f"এটা করার উপায়: {answer}"

    return answer
