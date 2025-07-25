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

def clean_ai_response(response_text: str) -> str:
    text = response_text.strip()
    if text.startswith("```"):
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1:]
        if text.endswith("```"):
            text = text[:-3]
    return text.strip()

def extract_with_ai(mail, counter):
    print("no mail is here")
    if not mail:
        return
    
    for i in range(len(mail)):
        if not mail[i]:
            continue 
        
        instruction = """
                    
        Parse this email and return JSON. Do your best to figure out each field from the email content.

        IMPORTANT: Return ONLY the JSON object. No explanations, no additional text, no commentary, no formatting, no reasoning.

        This email may not be a request, evaluvate this email and if it appearse to be a service request mark is_a_request to true

        Rules:
        - All text lowercase except names, file names, URLs
        - Use your best judgment to infer missing information from context
        - Match category to the closest option from the list
        - If email is NOT asking for repair/maintenance work, set "is_a_request" to null
        - Make reasonable assumptions about property type, service type, and timing based on the email content

        JSON Format:
        {
        "is_a_request": true or null,
        "client_name": "person's name",
        "management_name": "company being contacted", 
        "project_title": "what needs to be fixed",
        "service_description": "description of the problem",
        "budget": null,
        "category": "pick from category list",
        "preferred_time": null,
        "preferred_day": "day name or null",
        "alternate_day": "day name or null",
        "preferred_arrival_time": "time or null",
        "address": {
            "unit_number": "apartment/unit number",
            "street_number": "building number", 
            "street_name": "street name",
            "city": "city name",
            "province": "province",
            "country": "country", 
            "postal_code": "postal code"
        },
        "attachments": [],
        "property_details": {
            "property_type": "residential or commercial",
            "type_of_service": "installing, repairing, or replacing",
            "budget": null,
            "desired_start_time": "asap, within a month, within a few months, or within a year"
        }
        }

        Categories:
        ["roofing", "flooring", "electrical work", "decks & balconies", "transportation", "windows", "handyman", "painting & wall finishes", "foundation", "doors", "masonry", "drainage", "smart home", "basement", "demolition", "excavation", "plumbing", "commercial cleaning", "garage", "energy advisors", "kitchen", "residential cleaning", "snow removal", "bathroom", "landscaping", "hvac", "general contractor", "siding"]

        Email Body:
                
        """ + mail[i]

        response = client.chat.completions.create(
            model="Llama-3.3-Swallow-70B-Instruct-v0.4",
            messages=[
                {
                    "role": "user",
                    "content": instruction
                }
            ]
        )

        response_content = response.choices[0].message.content.strip()

        response_content = clean_ai_response(response_content)

        print(f"Response for email {i+counter}: {response_content}")
    
        try:
            parsed_json = json.loads(response_content)
            required_fields = ["client_name", "project_title", "address", "service_description",]
            all_required_present = True
            if (parsed_json.get("is_a_request")) == None:
                all_required_present = False
            
            for field in required_fields:
                value = parsed_json.get(field)
                if value in [None, "", "null"]:
                    print(f"Missing required field '{field}' in email {i+counter}. Skipping this email.")
                    all_required_present = False
                    break

            
            if all_required_present:
                with open(f"parsed_email_{i+counter}.json", "w") as f:
                    json.dump(parsed_json, f, indent=4)
                    
        except json.JSONDecodeError:
            pass
                


