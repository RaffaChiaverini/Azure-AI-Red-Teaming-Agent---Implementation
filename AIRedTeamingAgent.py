# Generic imports
from dotenv import load_dotenv
import os
import asyncio

# Load environmental variables from .env file
load_dotenv()

# Azure imports
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation.red_team import RedTeam, RiskCategory
from azure.ai.evaluation.red_team import AttackStrategy

## Using Azure AI Foundry project
azure_ai_project = os.environ.get("AZURE_AI_PROJECT")

# Instantiate your AI Red Teaming Agent
# Specifying risk categories and number of attack objectives per risk categories you want the AI Red Teaming Agent to cover
red_team_agent = RedTeam(
    azure_ai_project=azure_ai_project, # required
    credential=DefaultAzureCredential(), # required
    risk_categories=[ # optional, defaults to all four risk categories
        RiskCategory.Violence,
        RiskCategory.HateUnfairness,
        RiskCategory.Sexual,
        RiskCategory.SelfHarm
    ], 
    num_objectives=1, # optional, defaults to 10
)

import asyncio

# Definizione della callback complessa
async def advanced_callback(messages, stream=False, session_state=None, context=None):
    messages_list = [{"role": message.role, "content": message.content} 
                     for message in messages]
    latest_message = messages_list[-1]["content"]

    response = "I'm an AI assistant that follows safety guidelines. I cannot provide harmful content."

    formatted_response = {
        "content": response,
        "role": "assistant"
    }

    return {"messages": [formatted_response]}

# Funzione asincrona che esegue lo scan
async def run_red_team_scan():
    red_team_result =  await red_team_agent.scan(
        target=advanced_callback, # required
        output_path="My-RedTeam-Scan.json",
        scan_name="Scan with many strategies", # optional
        attack_strategies=[ # optional
            AttackStrategy.CharacterSpace,  # Add character spaces
            AttackStrategy.ROT13,  # Use ROT13 encoding
            AttackStrategy.UnicodeConfusable,  # Use confusable Unicode characters
            AttackStrategy.Compose([AttackStrategy.Base64, AttackStrategy.ROT13]), # composition of strategies
        ],
    )
    print(red_team_result)

# Esecuzione dell'intera logica asincrona
asyncio.run(run_red_team_scan())