import random

from user_manager import find_user_profile
from datetime import datetime
from user_manager import create_user, create_guest_user


def extract_name(message):

    message = message.strip()

    phrases = [
        "my name is",
        "i'm",
        "i am",
        "call me",
        "i go by",
        "my first name is",
        "people call me",
        "it's",
    ]

    lowered = message.lower()

    for phrase in phrases:

        if lowered.startswith(phrase):

            return message[len(phrase):].strip().title()

    return message.title()

def confirm_name(message):

    name = extract_name(message)
    confirmation_prompts = [
        f"You said your name is {name}. Did I get that right?",
        f"I heard {name}. Is that what you'd like me to call you?",
        f"Just to make sure I understood correctly, is your name {name}?",
        f"Did you say {name}?",
        f"I believe you said {name}. Is that right?",
        f"I heard the name {name}. Did I catch that correctly?",
        f"Before we continue, did I get your name right as {name}?",
        f"I want to make sure I understood you correctly. Is your name {name}?",
        f"You said {name}. Is that what you'd like me to call you?",
        f"Did I hear {name} correctly?",
        f"Just checking, should I call you {name}?",
        f"To be sure I understood, is your name {name}?",
        f"Have I got your name right as {name}?",
        f"I think I heard {name}. Is that correct?",
        f"Would you like me to call you {name}?"
]

    return random.choice(confirmation_prompts)


def greet_user(user_id):
    profile = find_user_profile(user_id)
    current_hour = datetime.now().hour


    if 5 <= current_hour < 12:
        time_greeting = "Good morning"
    elif 12 <= current_hour < 18:
        time_greeting = "Good afternoon"
    else:
        time_greeting = "Good evening"



    if profile:
        name = profile['name'].title()

        greetings = [
        f"Welcome back, {name}. How are you doing today?",
        f"Hello, {name}. What would you like to explore today?",
        f"Hi {name}, it's nice to see you again.",
        f"Welcome back, {name}. What can I help you with today?",
        f"Hello {name}. I hope you're doing well.",
        f"Hi {name}. What would you like to work on today?",
        f"It's great to see you again, {name}.",
        f"Welcome back, {name}. What's on your mind today?",
        f"Hello {name}. How can I assist you today?",
        f"Hi {name}. Ready to learn something new today?",
        f"Welcome back, {name}. What are we tackling today?",
        f"Good to have you here, {name}.",
        f"Hello again, {name}. How are things going?",
        f"Hi {name}. What would you like to discuss today?",
        f"Welcome back, {name}. I'm ready whenever you are.",
        f"Hello {name}. What can I help you understand today?",
        f"It's nice to see you again, {name}.",
        f"Welcome back, {name}. How may I assist you today?",
        f"Hi {name}. Let's make today productive.",
        f"{time_greeting}, {name}. How are you doing today?",
        f"{time_greeting}, {name}. What would you like to work on today?",
        f"{time_greeting}, {name}. It's good to see you again.",
        f"Welcome back, {name}. How has your day been?",
        f"Hello, {name}. What can I help you learn today?",
    ]

        return random.choice(greetings)
    guest_greetings = [
            "Hello. I don't think we've met before. What would you like me to call you?",
            "Hi there. I don't recognize you yet. What name would you like me to go by?",
            "Hello. This appears to be a new face. What should I call you?",
            "Hi. I don't believe we've met before. May I know your name?",
            "Hey there. I don't recognize you yet. What would you like me to be called?",
            "Hello. It's nice to meet you. What should I call you?",
            "Hi there. You seem new to me. What name would you like to use?",
            "Welcome. I don't think we've spoken before. What would you like me to call you?",
            "Hello. I haven't seen you before. How would you like to introduce yourself?",
            "Hey. I don't recognize you just yet. What should I call you?"
    ]

    return random.choice(guest_greetings)



def handle_name_confirmation(message, extracted_name):
    yes_words = [
        "yes",
        "yeah",
        "yep",
        "correct",
        "that's right",
        "exactly",
        "right",
        "yes that's correct",
        "that's my name"
    ]
    no_words = [
        "no",
        "nope",
        "incorrect",
        "that's wrong",
        "not quite",
        "you got it wrong",
        "wrong"
    ]
    if message.lower() in yes_words:
        user_id = create_user(extracted_name)
        return {
            "status": "created",
            "user_id": user_id,
            "response": welcome_new_user(extracted_name)
        }


    elif message.lower() in no_words:
        return "retry"

    else:
        return "unclear"


def welcome_new_user(name):

    welcome_prompts = [
        f"Nice to meet you, {name}. How can I help you today?",
        f"It's a pleasure to meet you, {name}.",
        f"Great. I'll call you {name} from now on.",
        f"Thanks, {name}. It's nice to meet you.",
        f"Welcome, {name}. What would you like to explore today?",
        f"Glad to meet you, {name}. How can I assist you?",
        f"Perfect. I'll remember your name as {name}.",
        f"It's great to meet you, {name}.",
        f"Thank you, {name}. How may I help you today?",
        f"Good to meet you, {name}. What would you like to work on today?"
    ]

    return random.choice(welcome_prompts)
