def build_system_prompt(context):

    web_text = context.get(
    "web_knowledge",
    ""
)
    conversation_text = ""

    dialogue_text = ""

    for item in context.get("recent_dialogue", []):
        dialogue_text += (
            f"{item['role']}: "
            f"{item['message']}\n"
        )

    for item in context["recent_conversation"]:

        if item["role"] == "user":
            conversation_text += f"user: {item['message']}\n"

    facts_text = ""

    for fact in context.get("known_facts", []):
        facts_text += f"- {fact['category']}: {fact['value']}\n"

    return f"""
You are Myandra, a friendly and intelligent AI assistant.

You are Myandra.

Creator: Temilade.

Answer clearly and briefly.

Use web facts if provided.

Known facts:
{facts_text}

Web facts:
{web_text}

Never write dialogue examples unless the user explicitly asks for one.
Never generate User: or Assistant: lines.
Answer only the user's current question.
"""
