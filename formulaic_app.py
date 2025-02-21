import requests
import json
import os
from dotenv import load_dotenv
import aiohttp
import asyncio


load_dotenv(".env")
FORMULAIC_API_KEY = os.getenv("FORMULAIC_API_KEY")
# public formulaic templates
RECIPE_ID = "1b849022-f2f2-44ac-bc06-c8f642f64b00"
SCRIPT_ID = "954a2728-5be8-4706-843f-cbe3eded3307"
# BODY = """{
#   "models": [
#     {
#       "id": "gpt-4o-mini",
#       "name": "GPT-4o mini",
#       "config": {
#         "deprecation_date": "2029-10-09T00:00:00Z"
#       },
#       "vendor": "OpenAI",
#       "provider": "OpenAI",
#       "description": "A smaller, more efficient version of GPT-4o, suitable for tasks that don't require the full power of the larger model."
#     }
#   ],
#   "variables": [
#     {
#       "id": "602528a6-80e4-48a8-aac4-9ef854bd82d7",
#       "name": "question",
#       "type": "string",
#       "value": "emergency! emergency! stuff is wayyyy on fire, yo! help, please lord god. i need help."
#     }
#   ]
# }"""


BODY = """{
"variables": [
    {
        "id": "602528a6-80e4-48a8-aac4-9ef854bd82d7",
        "name": "question",
        "type": "string",
        "value": {event_message}
    }
],
"models": ["gemini-1.5-flash-001"]
}"""


# Example: Retrieve Formula Metadata
async def get_formula_metadata():
    url = f"https://formulaic.app/api/recipes/{RECIPE_ID}/scripts"
    headers = {
        "Authorization": f"Bearer {FORMULAIC_API_KEY}",
        "Accept": "*/*",
        "Content-Type": "application/json",
    }
    print(f"{headers=}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(data)
            else:
                print(f"Error: {response.status_code}")
                print(f"Response: {response.text}")
            return response


# Example: do something that i'm not exactly sure what it is for /artifacts
# fix this and figure it out later
# async def get_llm_response(event_message, formula_options={}):
#     recipe_id, script_id = formula_options
#     url = f"https://formulaic.app/api/recipes/{recipe_id}/scripts/{script_id}/artifacts"
#     headers = {
#         "Authorization": f"Bearer {FORMULAIC_API_KEY}",
#         "Accept": "*/*",
#         "Content-Type": "application/json",
#         "name": "value",
#     }

#     # Safely format the body as a dictionary, then serialize it as JSON
#     body_data = {
#         "variables": [
#             {
#                 "id": "23c0c57f-2c1a-483b-b94f-0638b5221853",
#                 "name": "question",
#                 "type": "string",
#                 "value": event_message,
#             }
#         ],
#         "models": ["meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"],
#     }
#     print(body_data)
#     # Serialize the body to JSON
#     new_body = json.dumps(body_data)


#     print(f"{new_body=}")
async def get_llm_response(event_message, formula_options={}):
    recipe_id = formula_options["recipe_id"]
    url = f"https://formulaic.app/api/recipes/{recipe_id}/chats"
    headers = {
        "Authorization": f"Bearer {FORMULAIC_API_KEY}",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "name": "value",
    }

    # Safely format the body as a dictionary, then serialize it as JSON
    body_data = {
        "messages": [
            {"role": "assistant", "content": "Welcome to Formulaic! Ask me anything."},
            {
                "role": "user",
                "content": 'please respond with only the word "High" in plain text format',
            },
        ]
    }
    print(body_data)
    # Serialize the body to JSON
    new_body = json.dumps(body_data)

    print(f"{new_body=}")

    async with aiohttp.ClientSession() as session:  # Use aiohttp instead of asyncio
        async with session.post(url, headers=headers, data=new_body) as response:
            if response.status == 200:
                data = await response.json()  # Await the response to get the data
                print(f"Message: {event_message}")
                print(data)
                response = data["chat"]["messages"][-1]["content"]
                print(f"last response -1: {response}")
                return response  # Return the LLM response
            else:
                print(f"Error: {response.status}")
                print(f"Response Body: {await response.text()}")
                print(f"Response: {response}")
                return response


async def add_to_chat_session(event_message):
    url = f"https://formulaic.app/api/recipes/{RECIPE_ID}/chats"
    headers = {
        "Authorization": f"Bearer {FORMULAIC_API_KEY}",
        "Accept": "*/*",
        "Content-Type": "application/json",
    }

    # Safely format the body as a dictionary, then serialize it as JSON
    body_data = {
        "variables": [
            {
                "id": "23c0c57f-2c1a-483b-b94f-0638b5221853",
                "name": "question",
                "type": "string",
                "value": event_message,
            }
        ],
        "models": ["meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"],
    }


if __name__ == "__main__":
    # Example Usage:
    asyncio.run(get_formula_metadata())
    # get_llm_response()
