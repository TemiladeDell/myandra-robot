import os

from ollama import Client

client = Client(
    host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
)

def generate_response(system_prompt, user_message):

    try:

        response = client.chat(
            model="qwen2.5:1.5b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            options={
                "num_predict": 48,
                "temperature": 0.7
            }
        )

        return response["message"]["content"]

    except Exception as e:

        print("OLLAMA ERROR:", e)

        return "I'm sorry, my language model is currently unavailable."
