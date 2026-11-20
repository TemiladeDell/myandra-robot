from myandradb_link import (
    load_user,
    load_learning,
    get_context,
    get_recent_dialogue
)

from known_facts import get_facts
from web_search import search_web


def get_user_profile(user_id):
    return load_user(user_id)


def build_context(user_id, current_message):

    PERSONAL_PHRASES = [
        "my favorite",
        "my age",
        "my name"
    ]

    FOLLOWUP_WORDS = {
        "he", "she", "they",
        "him", "her", "them",
        "it",
        "his", "hers",
        "their", "its"
    }

    FRESHNESS_WORDS = {
        "latest",
        "newest",
        "current",
        "today",
        "recent",
        "now"
    }

    is_personal_question = any(
        phrase in current_message.lower()
        for phrase in PERSONAL_PHRASES
    )

    words = [
        word.strip(".,?!")
        for word in current_message.lower().split()
    ]

    is_followup = any(
        word in FOLLOWUP_WORDS
        for word in words
    )

    needs_freshness = any(
        word in current_message.lower()
        for word in FRESHNESS_WORDS
    )

    web_context = "[No web results found]"
    response = None

    if not is_personal_question and not is_followup:

        search_query = current_message

        if needs_freshness:
            search_query += " current latest"

        response = search_web(search_query)

    if response:

        answer = response.get(
        "answer",
        ""
    )

        web_context = f"""
AUTHORITATIVE WEB ANSWER:

{answer}
"""
    recent_conversation = get_context(user_id)[-3:]
    dialogue = get_recent_dialogue(user_id)

    LOW_VALUE_MESSAGES = {
        "ok",
        "okay",
        "yes",
        "yeah",
        "yep",
        "clear",
        "thanks",
        "thank you"
    }

    filtered = []

    for item in recent_conversation:

        if item["message"].lower().strip() not in LOW_VALUE_MESSAGES:
            filtered.append(item)

    profile = get_user_profile(user_id)

    if profile:

        return {
            "name": profile["name"] or "Unknown",
            "education": profile["education_level"] or "Unknown",
            "learning": load_learning(user_id),
            "known_facts": get_facts(user_id),
            "recent_conversation": filtered,
            "recent_dialogue": dialogue,
            "web_knowledge": web_context,
            "user_mode": "registered"
        }

    return {
        "recent_conversation": filtered,
        "recent_dialogue": dialogue,
        "web_knowledge": web_context,
        "user_mode": "guest"
    }
