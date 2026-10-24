import os 
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

client = Groq(api_key = my_api_key)

model = "openai/gpt-oss-120b"

role = "user"
prompt = "What are the topics I should learn to become an AI Engineer? just give names of the topics, no explanation needed."

#System 

sys_message = {
    "role": "system",
    "content": "You are a Senior AI Engineer with extensive experience in the field and also my mentor."
}

message = {
    "role": role,
    "content": prompt
}
messages = [ sys_message, message ]

response = client.chat.completions.create(model=model,messages=messages, temperature=0.7)

print(response.choices[0].message.content)