import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Carica variabili d'ambiente
load_dotenv()

# Recupera le variabili
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_KEY")
deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")

# Stampa di controllo
print("🔍 Verifica variabili d'ambiente:")
print("AZURE_OPENAI_ENDPOINT:", endpoint)
print("AZURE_OPENAI_KEY:", "✔️" if api_key else "❌ Manca")
print("AZURE_OPENAI_DEPLOYMENT:", deployment)

# Istanzia il client AzureOpenAI
client = AzureOpenAI(
    api_key=api_key,
    api_version = "2024-12-01-preview",
    azure_endpoint=endpoint
)

# Test di chiamata
try:
    print("\n🚀 Eseguo chiamata di test...")
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": "Ciao!"}],
    )
    print("✅ Risposta ricevuta:", response.choices[0].message.content)
except Exception as e:
    print("❌ Errore nella chiamata:", e)
