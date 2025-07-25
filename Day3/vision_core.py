from mss import mss
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from google import genai

load_dotenv()

def screenshot():
    with mss() as sct:
        file_path = 'screenshots/screenshot.png'
        sct.shot(output=file_path)
        print(f"Screenshot taken and saved as '{file_path}'")
        return file_path

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def ask_gpt(base64_image, question):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": question },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )

    return response.output_text

def ask_gemini(image_path, question):
    client = genai.Client()

    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=[
            genai.types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/png"
            ),
            question
        ]
    )
    return response.text

