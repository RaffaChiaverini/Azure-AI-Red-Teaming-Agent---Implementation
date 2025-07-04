from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    RedTeam,
    AzureOpenAIModelConfiguration,
    AttackStrategy,
    RiskCategory,
    TargetConfig
)
# from azure.ai.evaluation.red_team import AttackStrategy

import os
from dotenv import load_dotenv

# Load environmental variables from .env file
load_dotenv()

# Reuse the naming convention from your previous code
endpoint = os.environ["AZURE_AI_PROJECT"]  # e.g., https://<account>.services.ai.azure.com/api/projects/<project-name>
model_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]  # e.g., https://<account>.openai.azure.com
model_api_key = os.environ["AZURE_OPENAI_KEY"]
model_deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT"]  # e.g., gpt-4

# Create the Azure OpenAI model configuration
model_config = AzureOpenAIModelConfiguration(
    model_deployment_name=model_deployment_name
)

# Create the target configuration for the Azure OpenAI model
target_config = AzureOpenAIModelConfiguration(
    model_deployment_name=model_deployment_name
)

# Set the attack strategies
agent_attack_strategies = [
            AttackStrategy.ASCII_SMUGGLER,        # Inserisce caratteri ASCII invisibili o speciali per confondere i filtri.
            AttackStrategy.BASE64,                # Codifica il testo in Base64 per aggirare i controlli.
            AttackStrategy.CAESAR,                # Applica una cifratura classica a rotazione (es. sposta lettere di 3 posizioni).
            AttackStrategy.CHARACTER_SPACE,       # Aggiunge spazi tra i caratteri per eludere rilevamenti (es: "v i o l e n t").
            AttackStrategy.UNICODE_CONFUSABLE,    # Usa caratteri Unicode simili ma diversi (es: `а` cirillica invece di `a` latina).
            AttackStrategy.LEETSPEAK,             # Sostituisce lettere con numeri o simboli (es: `k1ll`, `h4ck`).
            AttackStrategy.JAILBREAK,             # Utilizza prompt costruiti per aggirare le restrizioni del modello.
            AttackStrategy.ROT13,                 # Codifica semplice che ruota ogni lettera di 13 posizioni nell’alfabeto.
            AttackStrategy.DIACRITIC              # Aggiunge accenti e segni diacritici per mascherare parole (es: "vïölënt").
        ]

# Set the risk categories 
agent_risk_categories = [
            RiskCategory.VIOLENCE,
            RiskCategory.HATE_UNFAIRNESS,
            RiskCategory.SEXUAL,
            RiskCategory.SELF_HARM
        ],

# Create the AI Project client
with AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
) as project_client:

    # Configure the target model
    target_config = AzureOpenAIModelConfiguration(model_deployment_name=model_deployment_name)

    # Create the Red Team agent
    red_team_agent = RedTeam(
        attack_strategies = [AttackStrategy.BASE64],
        risk_categories = [RiskCategory.VIOLENCE],
        display_name="red-team-cloud-run2",
        target=target_config
    )

    # Launch the red team run
    red_team_response = project_client.red_teams.create(
        red_team=red_team_agent,
        headers={
            "model-endpoint": model_endpoint, 
            "api-key": model_api_key},
    )

    # Get and print the scan result
    get_red_team_response = project_client.red_teams.get(name=red_team_response.name)
    print(f"Red Team scan status: {get_red_team_response.status}")

