from googlesearch import search 
from groq import Groq 
from json import load, dump 
import datetime 
from dotenv import dotenv_values # 

#Load environment variables from the env file. 
env_vars = dotenv_values(".env") 

#Retrieve environment variables for the chatbot 
Username = env_vars.get("Username") 
Assistantname = env_vars.get("Assistantname") 
GroqAPIKey  = env_vars.get("GroqAPIKey") 

# Initialize the Groq client with the provided AP 
client  = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

try: 
    with open(r"Data\ChatLog.json", "r") as f: 
        messages = load(f) 
except: 
    with open(r"Data\ChatLog.json", "w") as f: 
        dump([], f)

def GoogleSearch(query): 
    results = list(search(query, advanced=True, num_results=5)) 
    Answer = f"The search results for '{query}' are:\n[start]\n"

    for i in results: 
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

    Answer += "[end]" 
    return Answer 

#Function to clean up the answer by removing empty Lines. 
def AnswerModifier (Answer): 
    lines = Answer.split('\n') 
    non_empty_lines = [line for line in lines if line.strip()] 
    modified_answer = '\n'.join(non_empty_lines) 
    return modified_answer
 
#Predefined chatbot conversation system message and an initial user message. 
SystemChatBot = [ 
    {"role": "system", "content": System}, 
    {"role": "user", "content": "Hi"}, 
    {"role": "assistant", "content": "Hello, how can I help you?"} 
]

def information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")  # Fix incorrect format "%8"
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    return (f"Use this real-time information if needed:\n"
            f"Day: {day}\n"
            f"Date: {date}\n"
            f"Month: {month}\n"
            f"Year: {year}\n"
            f"Time: {hour} hours, {minute} minutes, {second} seconds.\n")

def RealtimeSearchEngine(prompt):
    global messages

    if not prompt.strip():  # Handle empty input
        return "It seems like you didn't type anything. Please ask a question!"

    with open(r"Data\ChatLog.json", "r") as f:
        try:
            messages = load(f)
        except:
            messages = []

    messages.append({"role": "user", "content": prompt})

    system_messages = [
        {"role": "system", "content": System},
        {"role": "system", "content": information()},  # Fetch real-time info
        {"role": "system", "content": GoogleSearch(prompt)}
    ]

    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=system_messages + messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.strip().replace("</s>", "")

        if not Answer:
            Answer = "I'm sorry, but I couldn't retrieve information about that. Please try asking in a different way."

        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"Error: {e}")
        return "Oops! Something went wrong. Please try again."



if __name__ == "__main__":
    while True:
        prompt = input("Enter your Query: ")
        print(RealtimeSearchEngine(prompt))



