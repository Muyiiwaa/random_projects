import random
import time
from google.genai import types
from google import genai

client = genai.Client()

def response_generator(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    )
    response = response.text

    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Streamed response emulator
def response_model():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

if __name__== "__main__":
    model_result = model_response(prompt=input("Enter your prompt: "))
    print(model_result)