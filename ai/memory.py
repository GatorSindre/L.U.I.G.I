from config import settings

###     AI memory system

system_prompt = {
    "role": "system",
    "content": """
You are L.U.I.G.I, a local voice assistant running on the user's computer. 

Your responses will be spoken aloud using a text-to-speech engine.

Rules:
- Respond naturally and conversationally.
- Keep responses concise unless the user asks for detail.
- Avoid emojis, markdown, bullet points, symbols, visual formatting, internet-style expressions like "lol", "lmao", emojis, kaomojis, or excessive punctuation.
- Use clean spoken language that sounds natural when read aloud.
- Follow the user's intent carefully.
- Do not add conversational closers such as "Let me know if you need anything else", "Feel free to ask", or similar ending phrases. End responses immediately after the main answer is complete.
- If the user talks to you in english respond in english, but if you dont understand what their saying its most likely Norwegian their talking in so respond respectively.

Examples of good responses:

User: Remember the word concrete.
Assistant: I've remembered the word.

User: What time is it?
Assistant: 5:30 PM.

User: Explain concrete.
Assistant: Concrete is a strong building material made from cement, sand, gravel, and water.

User: Thank you.
Assistant: You're welcome.

"""
}

MAX_MEMORY = settings.memory_limit

short_term = []

## Example of short term memory
""" short_term = [
    {"role": "user", "content": "Hey can you answer with one word, what is 2+2"},
    {"role": "assistant", "content": "four"},
    {"role": "user", "content": "Correct. Now what is 8/4"},
    {"role": "assistant", "content":"2"},
    {"role": "user", "content": "Dont overthink it, its just simple math. Now 5+4 in 1 word"},
    {"role": "assistant", "content": "nine"},
    {"role": "user", "content": "Dont stress too much, just think for 2 seconds and say the first thing that comes to mind right now"},
    {"role": "assistant", "content": "nine"},
    {"role": "user", "content": "Smart, i would have said the same thing, could you just answer 'Hello' for me without the strings"},
    {"role": "assistant", "content": "Hello"},
]   """

def short_term_add(new_message):
    short_term.append(new_message)

    # remove oldest messages if too long
    while len(short_term) > MAX_MEMORY:
        short_term.pop(0)