# Generic imports
from dotenv import load_dotenv
import os
import asyncio

# Load environmental variables from .env file
load_dotenv()

# Azure imports
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.evaluation.red_team import RedTeam, RiskCategory
from azure.ai.evaluation.red_team import AttackStrategy
from openai import AzureOpenAI

# Pyrit imports 
from pyrit.prompt_target import OpenAIChatTarget, PromptChatTarget




"""# Azure AI Project Hub information
azure_ai_project = {
    "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
    "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP_NAME"),
    "project_name": os.environ.get("AZURE_PROJECT_NAME"),
}"""

## Using Azure AI Foundry project, example: AZURE_AI_PROJECT=https://your-account.services.ai.azure.com/api/projects/your-project
azure_ai_project = os.environ.get("AZURE_AI_PROJECT")

# Azure OpenAI deployment information
azure_openai_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")  # e.g., "gpt-4"
azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")  # e.g., "https://endpoint-name.openai.azure.com/openai/deployments/deployment-name/chat/completions"
azure_openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY")  # e.g., "your-api-key"
azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION")  # Use the latest API version


########################################################################################################################################################
########################################################################################################################################################
# Basic Example: Fixed Response Callback

# Define a simple callback function that always returns a fixed response
def financial_advisor_callback(query: str) -> str:  # noqa: ARG001
    return "I'm a financial advisor assistant. I can help with investment advice and financial planning within legal and ethical guidelines."

########################################################################################################################################################
# Intermediary Example: Using a Model Configuration as Target

# Define a model configuration to test
azure_oai_model_config = {
    "azure_endpoint": azure_openai_endpoint,
    "azure_deployment": azure_openai_deployment,
    "api_key": azure_openai_api_key,
}

########################################################################################################################################################
# Advanced Example: Using an Azure Open AI Model Endpoint in a Callback Function


token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

# Define a callback that uses Azure OpenAI API to generate responses
async def azure_openai_callback(messages: list, stream=False, session_state=None, context=None) -> dict[str, list[dict[str, str]]]:

    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
        azure_ad_token_provider=token_provider,
        api_version="2024-10-21"
    )


    ## Extract the latest message from the conversation history
    messages_list = [{"role": message.role, "content": message.content} for message in messages]
    latest_message = messages_list[-1]["content"]

    try:
        # Call the model
        response = client.chat.completions.create(
            model=azure_openai_deployment,
            messages=[
                {"role": "user", 
                 "content": latest_message},
            ],
        )

        # Format the response to follow the expected chat protocol format
        formatted_response = {
            "content": response.choices[0].message.content, 
            "role": "assistant"
        }

    except Exception as e:
        print(f"Error calling Azure OpenAI: {e!s}")
        formatted_response = {"content": "I encountered an error and couldn't process your request.", "role": "assistant"}

    return {"messages": [formatted_response]}

########################################################################################################################################################
########################################################################################################################################################

# Create the `RedTeam` instance with minimal configurations
red_team = RedTeam(
    azure_ai_project=azure_ai_project,
    credential=DefaultAzureCredential(),
    risk_categories=[
        RiskCategory.Violence, 
        RiskCategory.HateUnfairness, 
        RiskCategory.Sexual, 
        RiskCategory.SelfHarm
    ],
    num_objectives=1,
)

# Run the red team scan called "Basic-Callback-Scan" with limited scope for this basic example
# This will test 1 objective prompt for each of Violence and HateUnfairness categories with the Flip strategy
async def main():
    # Run the red team scan called "Intermediary-Model-Target-Scan"
    result = await red_team.scan(
        target=azure_openai_callback,
        scan_name="Advanced-Callback-Scan",
        attack_strategies=[
            AttackStrategy.EASY,  # Group of easy complexity attacks
            AttackStrategy.MODERATE,  # Group of moderate complexity attacks
            AttackStrategy.CharacterSpace,  # Add character spaces
            AttackStrategy.ROT13,  # Use ROT13 encoding
            AttackStrategy.UnicodeConfusable,  # Use confusable Unicode characters
            AttackStrategy.CharSwap,  # Swap characters in prompts
            AttackStrategy.Morse,  # Encode prompts in Morse code
            AttackStrategy.Leetspeak,  # Use Leetspeak
            AttackStrategy.Url,  # Use URLs in prompts
            AttackStrategy.Binary,  # Encode prompts in binary
            AttackStrategy.Compose([AttackStrategy.Base64, AttackStrategy.ROT13]),  # Use two strategies in one attack
        ],
    )
    return result

result = asyncio.run(main())