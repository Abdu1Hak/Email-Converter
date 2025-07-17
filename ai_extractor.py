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
            continue 
        
        instruction = """
        You are a parser. Your task is to extract key information from the email body below and return it as a JSON object in the structure below.

        IMPORTANT:
        - If ALL values in the output would be null, empty, or missing, DO NOT return the JSON structure. INSTEAD, return ONLY the string "0" (without quotes or formatting).
        - If at least one value can be filled, return the JSON object as specified below.
        - Do NOT return any explanation, commentary, or formatting—only the JSON or "EMPTY".

        All values must be in lowercase (except for file names and URLs). The 'category' field must match exactly one from the provided list. The scheduling fields may be null if not specified. If attachments are mentioned or included, add them in the 'attachments' array, each with a filename, filetype, url, and optional notes. If no attachments are present, use an empty array. If any value is not found, use null.

        Output format (ONLY if at least one value is present):
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

        ---
        Email Body:
        """ + mail[i]

        response = client.chat.completions.create(
            model="Meta-Llama-3.1-8B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                }
            ]
        )

        response_content = response.choices[0].message.content.strip()
    
        try:
            parsed_json = json.loads(response_content)
            required_fields = ["client name", "property address", "project title", "service description"]
            all_required_present = True
            
            for field in required_fields:
                value = parsed_json.get(field)
                if not value or value == "null" or not value.strip():
                    all_required_present = False
                    break
            
            if all_required_present:
                with open(f"parsed_email_{i}.json", "w") as f:
                    json.dump(parsed_json, f, indent=4)
                    
        except json.JSONDecodeError:
            pass
                


