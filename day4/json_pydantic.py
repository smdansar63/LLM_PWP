import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"

from pydantic import BaseModel

class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema=Ticket.model_json_schema()

response_format={
    "type": "json_object"
}

system_prompt = f"""
Extract the personal information from the ticket strictly based on this schema and give a json output.
{schema}. after one info , the next info should be in a new line. Do not add any extra text or explanation. Only give the json output.
"""

system_message = {
    "role": "system",
    "content": system_prompt
}

text = "My name is John Doe, my email is john.doe@example.com and I have an issue with my i Phone not charging properly."

user_prompt=f"""
This is a customer ticket. Please extract the personal information from this.
{text}
"""

user_message = {
    "role": "user",
    "content": user_prompt
}

messages = [system_message, user_message]  

response = client.chat.completions.create(model = model, messages=messages, response_format=response_format)

print(response.choices[0].message.content)

import json
raw_json=response.choices[0].message.content
data_file=json.loads(raw_json)
ticket=Ticket(**data_file)


# inko pass kr sakte hai aage!
print(ticket.name)
print(ticket.email)
print(ticket.issue)
