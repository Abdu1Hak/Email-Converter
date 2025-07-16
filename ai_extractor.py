from openai import OpenAI
from dotenv import load_dotenv
import os
import json


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.sambanova.ai/v1"
)

def extract_with_ai(mail):
    if not mail:
        return
    
    for i in range(len(mail)):
        if not mail[i]:
            continue  # Skip this email, process next one
        
        instruction = """
        You are a parser. Your task is to extract key information from the email body below and return it as a JSON object in the structure below.

        All values must be in lowercase (except for file names and URLs). The 'category' field must match exactly one from the provided list. The scheduling fields may be null if not specified. If attachments are mentioned or included, add them in the 'attachments' array, each with a filename, filetype, url, and optional notes. If no attachments are present, use an empty array. If any value is not found, use null.

        Return ONLY a valid JSON object, with no extra commentary or explanation, unless you may return nothing.

        **if there is no email attached do not return anything at all**.

        ---
        Output format:
        {
        "client name": "string",
        "property address": "string",
        "project title": "string",
        "service description": "string",
        "budget": "tbd",
        "category": "one of the categories listed below",
        "preferred time": "any time | morning | afternoon | evening | null",
        "preferred day": "string or null",
        "alternate day": "string or null",
        "preferred arrival time": "string or null",
        "attachments": [
            {
            "filename": "string",
            "filetype": "string (e.g. image/jpeg)",
            "url": "string",
            "notes": "string or null"
            }
        ]
        }

        Valid categories:
        [
        "roofing", "flooring", "electrical work", "decks & balconies", "transportation",
        "windows", "handyman", "painting & wall finishes", "foundation", "doors",
        "masonry", "drainage", "smart home", "basement", "demolition", "excavation",
        "plumbing", "commercial cleaning", "garage", "energy advisors", "kitchen",
        "residential cleaning", "snow removal", "bathroom", "landscaping", "hvac",
        "general contractor", "siding"
        ]


        **IF YOU THINK THIS IS AN EMAIL AND NOT SOMETHING THAT NEEDS TO BE CONVERTED INTO A REQUEST RETRURN 0**

        --- 
        Email Body:
        """ + mail[i]

        try:
            response = client.chat.completions.create(
                model="Meta-Llama-3.1-8B-Instruct",
                messages=[
                    {
                        "role": "user",
                        "content": instruction
                    }
                ]
            )

            if response.choices[0].message.content.strip() != "0":
                parsed_json = json.loads(response.choices[0].message.content)
                filename = f"parsed_email_{i}.json"
                with open(filename, "w") as f:
                    json.dump(parsed_json, f, indent=4)


        except Exception as e:
            pass