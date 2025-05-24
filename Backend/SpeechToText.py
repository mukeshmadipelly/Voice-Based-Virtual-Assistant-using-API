from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time

env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage")

# Generate HTML file for speech recognition
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;
        let isListening = false;

        function startRecognition() {
            if (isListening) return; // Prevent multiple starts
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = false; // Stop after a single utterance
            recognition.interimResults = false; // Only final results

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                output.textContent = transcript; // Update the output
                stopRecognition(); // Stop recognition after getting a result
            };

            recognition.onend = function() {
                isListening = false;
            };

            recognition.start();
            isListening = true;
        }

        function stopRecognition() {
            if (recognition && isListening) {
                recognition.stop();
                isListening = false;
            }
        }
    </script>
</body>
</html>'''

HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Save HTML file
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

current_dir = os.getcwd()
Link = f"file:///{current_dir}/Data/Voice.html"

# Configure Chrome options
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
# chrome_options.add_argument("--headless=new")  # Uncomment for headless mode

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

TempDirPath = rf"{current_dir}/Frontend/Files"

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what is", "what's", "how's", "can you"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognition():
    driver.get(Link)
    driver.find_element(by=By.ID, value="start").click()

    start_time = time.time()
    while True:
        try:
            Text = driver.find_element(by=By.ID, value="output").text
            print("Recognized Text:", Text)  # Debugging line

            if Text:
                driver.find_element(by=By.ID, value="end").click()
                
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))

            # Timeout after 10 seconds of no speech
            if time.time() - start_time > 10:
                print("No speech detected. Stopping recognition.")
                driver.find_element(by=By.ID, value="end").click()
                return None

        except Exception as e:
            print(f"Error: {e}")  # Debugging line
            pass

if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        if Text:
            print(Text)