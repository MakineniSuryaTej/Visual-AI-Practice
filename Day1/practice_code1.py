from mss import mss
from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from google import genai

load_dotenv()
client = OpenAI()

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


if __name__ == "__main__":
    image_path = screenshot()
    image_b64 = image_to_base64(image_path)
    question = "What is in this screenshot?"
    # answer = ask_gpt(image_b64, question)
    # print("GPT-4 Vision's answer:", answer)
    gemini_answer = ask_gemini(image_path, question)
    print("Gemini's answer:", gemini_answer)