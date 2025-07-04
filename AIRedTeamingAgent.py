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

# Pyrit imports 
from pyrit.prompt_target import OpenAIChatTarget, PromptChatTarget

## Using Azure AI Foundry project, example: AZURE_AI_PROJECT=https://your-account.services.ai.azure.com/api/projects/your-project
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

# Create a PyRIT PromptChatTarget for an Azure OpenAI model
# This could be any class that inherits from PromptChatTarget
chat_target = OpenAIChatTarget(
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    model_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
    endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
) 

# red_team_result = await red_team_agent.scan(target=chat_target)

# Funzione asincrona che esegue lo scan
async def run_red_team_scan():
    red_team_result =  await red_team_agent.scan(
        target=chat_target, # required
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