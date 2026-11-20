from known_facts import save_fact


MEMORY_TRIGGERS = [
    "favorite",
    "love",
    "enjoy",
    "enjoyable",
    "hobby",
    "passion",
    "interested in",
    "i am",
    "i study",
    "i work as",
    "my name is"
]


def extract_memory(user_id, message):


    if "?" in message:
        return

    msg = message.lower().strip()

    if not any(trigger in msg for trigger in MEMORY_TRIGGERS):
        return

    # Favorite programming language

    if "favorite programming language" in msg:

        value = message.split("is", 1)[1].strip()

        save_fact(
            user_id,
            "favorite_programming_language",
            value
        )

    # Favorite food

    elif "favorite food" in msg:

        value = message.split("is", 1)[1].strip()

        save_fact(
            user_id,
            "favorite_food",
            value
        )

    # Favorite sport

    elif "favorite sport" in msg:

        value = message.split("is", 1)[1].strip()

        save_fact(
            user_id,
            "favorite_sport",
            value
        )

    # Hobby

    elif "i enjoy" in msg:

        value = message.split("enjoy", 1)[1].strip()

        save_fact(
            user_id,
            "hobby",
            value
        )

    elif "i love" in msg:

        value = message.split("love", 1)[1].strip()

        save_fact(
            user_id,
            "interest",
            value
        )
