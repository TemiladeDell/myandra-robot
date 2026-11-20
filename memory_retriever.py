from myandradb_link import search_conversation

STOP_WORDS = {
    "what",
    "is",
    "the",
    "a",
    "an",
    "how",
    "can",
    "you",
    "tell",
    "me",
    "about",
    "please",
    "explain"
}



def retrieve_relevant_memories(user_id, message):

    words = message.lower().split()

    keywords = []

    for word in words:

        word = word.strip(".,?!")

        if word not in STOP_WORDS:
            keywords.append(word)

    memories = []
    seen = set()

    for keyword in keywords:

        results = search_conversation(
            user_id,
            keyword
        )

        for item in results:

            key = (
                item["role"],
                item["message"]
            )

            if key not in seen:

                seen.add(key)

                memories.append(item)

    return memories
