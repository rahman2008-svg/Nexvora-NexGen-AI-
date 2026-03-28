sessions = {}

def save_context(user, question, answer):
    if user not in sessions:
        sessions[user] = []

    sessions[user].append({
        "q": question,
        "a": answer
    })

    if len(sessions[user]) > 5:
        sessions[user].pop(0)


def get_context(user):
    return sessions.get(user, [])
