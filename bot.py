
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from json_gen import make_json

sys_prompt = """
    You are a helpful customer support assistant for the TOCTOC site. Use the supplied tool to assist the user efficiently.  
    Your main goal is to identify the customer's intent, which can be one of the following:  
    - **Buscar propiedad**: The customer is interested in searching for a property to buy or rent.  
    - **Tasar propiedad**: The customer wants to estimate the value of their property.  
    - **Financiar**: The customer is interested in obtaining financial assistance, like a mortgage.  

    After identifying the intent, use the single tool, `get_properties`, to assist the user by filling in the appropriate parameters based on the context of the conversation.  

    ### Tool Functionality Breakdown:  
    1. **`intent` and `workflow`**:  
    - Define the overall purpose of the customer's request.  
    - Use `intent` for the high-level intent (`Buscar propiedad`, `Tasar propiedad`, `Financiar`).  
    - Use `workflow` for simplified versions (`Buscar`, `Tasar`, `Hipotecario`).

    2. **Search and Responses**:  
    - Use the **`search`** parameter to input the customer's most recent message.  
    - Use **`customResponse`** for the bot's latest message in response to the customer.  

    3. **Region and Commune**:  
    - Populate the **`region`** and **`city`** parameters based on the customer's inputs.  
    - If the user mentions only the **commune**, infer the **region** using your knowledge of Chilean geography.

    4. **Attributes for Property Search**:  
    - For `Buscar propiedad`, filter as much as possible based on the customer's preferences, using the `response` attribute to capture values such as:  
        - **`commune`, `region`, `typeOfProperty`, `bedrooms`, `bathrooms`, `priceMin`, `priceMax`, etc.**  

    5. **Clarifying Missing Information**:  
    - Use the `questions` attribute to identify missing fields where further clarification is needed.  
    - For example, if `commune` is missing in the `response`, set `questions` with `{'key': 'commune', 'value': false}`.

    6. **Finalizing the Interaction**:  
    - Use the **`isFinished`** parameter:  
        - Set it to `True` when the conversation is complete (e.g., when all necessary inputs for `Buscar propiedad`, `Tasar propiedad`, or `Financiar` have been provided).  
        - Otherwise, keep it `False` to continue the dialogue.

    ### Guidelines for Usage:  
    - Always aim to narrow down the customer's request as much as possible, particularly for **Buscar propiedad**.  
    - If the user mentions a **commune** or a **region**, ensure these fields are reflected in the tool.  
    - When enough information has been gathered, finalize the workflow and confirm the conversation is finished (`isFinished: True`).  

    ### Examples of Interaction:  
    1. **For Buscar propiedad**:  
    - Customer: "Quiero buscar una casa en Ñuñoa."  
    - Tool Call:  
        ```json
        {
        "city": "Ñuñoa",
        "region": "Región Metropolitana de Santiago",
        "search": "Quiero buscar una casa en Ñuñoa.",
        "customResponse": "Entendido, estoy buscando propiedades en Ñuñoa.",
        "intent": "Buscar propiedad",
        "workflow": "Buscar",
        "response": [
            {"key": "commune", "value": "Ñuñoa"},
            {"key": "region", "value": "Región Metropolitana de Santiago"}
        ],
        "questions": [
            {"key": "typeOfProperty", "value": false},
            {"key": "priceMax", "value": false}
        ],
        "isFinished": false
        }
        ```

    2. **When the conversation ends**:  
    - If all fields have been clarified and the intent fulfilled:  
        ```json
        {
        "city": "Ñuñoa",
        "region": "Región Metropolitana de Santiago",
        "search": "Quiero buscar una casa en Ñuñoa.",
        "customResponse": "Perfecto, he encontrado propiedades que cumplen con tus requisitos.",
        "intent": "Buscar propiedad",
        "workflow": "Buscar",
        "response": [
            {"key": "commune", "value": "Ñuñoa"},
            {"key": "region", "value": "Región Metropolitana de Santiago"},
            {"key": "typeOfProperty", "value": "Casa"},
            {"key": "priceMax", "value": "200000000"}
        ],
        "questions": [],
        "isFinished": true
        }
        ```

    By following these instructions, the tool should streamline the process of identifying customer needs and generating precise responses.

        """

tools = [
  {
      "type": "function",
      "function": {
          "name": "get_properties",
          "parameters": {
              "type": "object",
              "properties": {
                  "city": {"type": "string",
                                           "description": "commune specified by customer."},
                  "region":{"type": "string",
                            "enum":[
                                 "Región de Arica y Parinacota",
                                "Región de Tarapacá",
                                "Región de Antofagasta",
                                "Región de Atacama",
                                "Región de Coquimbo",
                                "Región de Valparaíso",
                                "Región Metropolitana de Santiago",
                                "Región del Libertador Gral. Bernardo O'Higgins",
                                "Región del Maule",
                                "Región de Ñuble",
                                "Región del Biobío",
                                "Región de La Araucanía",
                                "Región de Los Ríos",
                                "Región de Los Lagos",
                                "Región Aysén del G. Carlos Ibáñez del Campo",
                                "Región de Magallanes y de la Antártica Chilena"
                            ],
                                      "description": "Geographical Region, if not specified provide the region that you think the customer is refferring to. Remeber, regions of Chile"},
                  "search": {"type": "string",
                                           "description": "Is the lattest message submited by the user"},
                  "customResponse": {
                      "type": "string",
                      "description": "Latest message sent by the bot."
                  },
                  "intent":{
                      "type": "string",
                      "description": "The intent of the customer in this conversation, it can be 'Buscar propiedad', 'Financiar' or 'Tasar propiedad"
                  },
                  "workflow": {
                      "type":"string",
                      "description": "Simpler version of intent, for the intent 'Buscar propiedad' is 'Buscar', for 'Financiar' is 'Hipotecario and for 'Tasar propiedad' is 'Tasar'."
                  },
                  "response":{
                      "type": "array",
                      "items":{ "type":  "object",
                              "properties":{
                                  "key":{"type":"string",
                                         "enum": [
                                            "commune",
                                            "region",
                                            "typeOfProperty",
                                            "typeOfOperation",
                                            "bedrooms",
                                            "bathrooms",
                                            "parking",
                                            "storage",
                                            "area",
                                            "priceMax",
                                            "priceMin",
                                            "petFriendly",
                                            ]},
                                  "value":{"type":"string"}}},
                      "description": "Each element has a dictionary with a 'key' as an attribute and a 'value' parameter, that is the value for the key. For example: \
                          {'key': 'commune', 'value': 'Huechuraba'}"
                      },
                  "questions":{
                      "type": "array",
                      "items":{ "type":  "object",
                              "properties":{
                                  "key":{"type":"string",
                                         "enum": [
                                            "commune",
                                            "region",
                                            "typeOfProperty",
                                            "typeOfOperation",
                                            "bedrooms",
                                            "bathrooms",
                                            "parking",
                                            "storage",
                                            "area",
                                            "priceMax",
                                            "priceMin",
                                            "petFriendly",
                                            ]},
                                  "value":{"type":"boolean"}}},
                      "description": "Each element has a dictionary with a 'key' as an attribute and a 'value' parameter is true if the response has a value o either \
                          is false if it has an empty string. For example: \
                          {'key': 'commune', 'value': true} \
                          or if in response does not have a value for commune,h it would be:\
                          {'key': 'commune', 'value': false}"
                  },
                  "isFinished": {
                        "type": "boolean",
                        "description": "True if the conversation is finished, False otherwise."
                    }
              },
              "additionalProperties": False,
          },
      },
  },
]

load_dotenv()

api_key_openai = os.getenv('API_KEY_OPENAI')
client = OpenAI(api_key=api_key_openai)

while True:
    message = input("send a message for our bot >:)")
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "system",
        "content": sys_prompt,
    },
        {"role": "user", "content": message}],

    tools=tools,
    )
    calls = completion.choices[0].message.tool_calls
    arguments = json.loads(calls[0].function.arguments)
    if arguments["isFinished"]:
        print("The conversation is finished")
        break
    
