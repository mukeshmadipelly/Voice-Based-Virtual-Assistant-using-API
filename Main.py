from Frontend.GUI import ( 
    GraphicalUserInterface, 
    SetAssistantStatus, 
    ShowTextToScreen, 
    TempDirectoryPath, 
    SetMicrophoneStatus, 
    AnswerModifier, 
    QueryModifier, 
    GetMicrophoneStatus, 
    GetAssistantStatus 
) 
from Backend.Model import FirstLayerDMM 
from Backend.RealTimeSearchEngine import RealtimeSearchEngine 
from Backend.Automation import Automation 
from Backend.SpeechToText import SpeechRecognition 
from Backend.Chatbot import ChatBot 
from Backend.TextToSpeech import TextToSpeech 
from dotenv import dotenv_values 
from asyncio import run 
from time import sleep 
import subprocess 
import threading 
import json 
import time
import os
from PIL import Image, ImageDraw, ImageFont

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname") 
DefaultMessage = f'''{Username}: Hello {Assistantname}, How are you? 
{Assistantname}: Welcome {Username}. I am doing well. How may i help you?''' 
subprocesses = [] 
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"] 

def ShowDefaultChatIfNoChats(): 
    File = open(r'Data\ChatLog.json',"r", encoding='utf-8') 
    if len(File.read())<5: 
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file: 
            file.write("") 
        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file: 
            file.write(DefaultMessage)

def ReadChatLogJson():
    chatlog_path = TempDirectoryPath('ChatLog.data')
    if not os.path.exists(chatlog_path):
        with open(chatlog_path, 'w', encoding='utf-8') as file:
            json.dump([], file)
    with open(chatlog_path, 'r', encoding='utf-8') as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
            if entry["role"] == "user":
               formatted_chatlog += f"User: {entry['content']}\n"
            elif entry["role"] == "assistant":
                formatted_chatlog += f"Assistant: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")

    with open(TempDirectoryPath('Database.data'),"w",encoding='utf-8') as file:
         file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI(): 
    File = open(TempDirectoryPath('Database.data'), "r+", encoding='utf-8') 
    Data = File.read() 
    if len(str(Data))>0: 
        lines = Data.split('\n') 
        result = '\n'.join(lines) 
        File.close() 
        File = open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') 
        File.write(result) 
        File.close() 

def InitialExecution():
     SetMicrophoneStatus("False") 
     ShowTextToScreen("") 
     ShowDefaultChatIfNoChats() 
     ChatLogIntegration() 
     ShowChatsOnGUI() 
        
InitialExecution()

def MainExecution(): 
    try:
        TaskExecution = False 
        ImageExecution = False 
        ImageGenerationQuery = ""

        SetAssistantStatus("Listening...") 
        Query = SpeechRecognition()
        
        if not Query:  # If no speech detected
            SetAssistantStatus("Available...")
            return False
            
        ShowTextToScreen(f" {Username} : {Query}") 
        SetAssistantStatus("Thinking...") 
        Decision = FirstLayerDMM(Query)  

        print(f"Decision: {Decision}") 

        G = any([i for i in Decision if i.startswith("general")]) 
        R = any([i for i in Decision if i.startswith("realtime")])

        mearged_query = " and ".join(
            [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
        )

        for queries in Decision:
            if "generate" in queries:
                ImageGenerationQuery = str(queries)
                ImageExecution = True
        
        for queries in Decision:
            if TaskExecution == False:
                if any(queries.startswith(func) for func in Functions):
                    run(Automation(list(Decision)))
                    TaskExecution = True

        if ImageExecution == True:
            print(f"🔹 Generating Image for prompt: {ImageGenerationQuery}")
            with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
                file.write(f"{ImageGenerationQuery}, True")

            try:
                python_executable = r"C:\Users\mukes\Desktop\JarvisAI\.venv\Scripts\python.exe"
                p1 = subprocess.Popen(
                    [python_executable, r'Backend\ImageGeneration.py'],
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    stdin=subprocess.PIPE, 
                    shell=False
                )
                subprocesses.append(p1)
                stdout, stderr = p1.communicate()
                # Handle output as before
            except Exception as e:
                print(f"Error: {e}")
            return True

        if R:
            SetAssistantStatus("Searching...")
            Answer = RealtimeSearchEngine(QueryModifier(mearged_query))
            ShowTextToScreen(f"{Assistantname} : {Answer}")
            SetAssistantStatus("Answering...")
            TextToSpeech(Answer)
            return True
            
        elif G:
            for Queries in Decision:
                if "general" in Queries:
                    SetAssistantStatus("Thinking...")
                    QueryFinal = Queries.replace("general ","")
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname} : {Answer}")
                    TextToSpeech(Answer)
                    return True
                    
        else:
            # Handle other cases
            return True
            
    except Exception as e:
        print(f"Error in MainExecution: {e}")
        return False
    finally:
        SetMicrophoneStatus("True")  # Reset microphone status
        SetAssistantStatus("Available...")
         
def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()

        if CurrentStatus == "True":
            MainExecution()
        else:
            AIStatus = GetAssistantStatus()

            if "Available..." in AIStatus:
                sleep(0.1)
            else:
                SetAssistantStatus("Available...")

def secondThread():
     GraphicalUserInterface()
     

if __name__ == "__main__":
     thread2 = threading.Thread(target=FirstThread,daemon=True)
     thread2.start()
     secondThread()