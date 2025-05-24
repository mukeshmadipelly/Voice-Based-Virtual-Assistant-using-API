from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

def RealtimeInformation():
    now = datetime.datetime.now()
    return f"""Current Date and Time:
- Day: {now.strftime('%A')}
- Date: {now.strftime('%d %B %Y')}
- Time: {now.strftime('%H:%M:%S')}
(Use this information as the real-time date and time)"""

def load_chat_log():
    """Load chat history from file."""
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
            if not isinstance(messages, list):  # Ensure it's a valid list
                return []
            return messages
    except FileNotFoundError:
        return []

def save_chat_log(messages):
    """Save chat history to file."""
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

def ChatBot(Query):
    messages = load_chat_log()

    # System instruction + Real-time information (always updated)
    System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname}.
You always have access to the latest date and time.

(IMPORTANT: Do not say 'I don’t know the time or date' because you have access to the following real-time data.)
{RealtimeInformation()} 

*** Do not tell time unless I ask. Do not talk too much, just answer the question. ***
*** Reply only in English, even if the question is in Hindi. ***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

    # Always update system instructions with real-time data
    SystemChatBot = [{"role": "system", "content": System}]    
    # Append user query
    messages.append({"role": "user", "content": Query})
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + messages,  # Always use updated real-time data
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        save_chat_log(messages)  # Save conversation history

        return Answer
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, an error occurred."
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))
