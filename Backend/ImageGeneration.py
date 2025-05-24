import asyncio
from random import randint
from PIL import Image
import requests
import os
from dotenv import get_key
from time import sleep

# Ensure the 'Data' folder exists
if not os.path.exists("Data"):
    os.makedirs("Data")

def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    # Generate file names
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

async def generate_images(prompt: str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes:
            with open(fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
                f.write(image_bytes)
        else:
            print(f"Failed to generate image {i + 1}")

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

def main():
    while True:
        try:
            with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
                data: str = f.read()

            prompt, status = data.split(",")

            if status.strip() == "True":
                print("Generating Images...")
                GenerateImages(prompt=prompt)

                # Reset the status
                with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                    f.write("False,False")
                break
            else:
                sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            sleep(1)

if __name__ == "__main__":
    main()