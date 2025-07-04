
# Azure AI Red Teaming Agent – EvaluationSDK & FoundrySDK Implementations

Questo repository offre un'implementazione completa e funzionante di un **AI Red Teaming Agent** costruito con le tecnologie Microsoft Azure. Sono incluse due versioni operative:

- Una che sfrutta l’**Azure AI Evaluation SDK** in locale (con supporto a PyRIT)
- Una che utilizza l’**Azure AI Foundry SDK** per eseguire test direttamente in cloud

Entrambe sono pronte all’uso. È sufficiente **personalizzare il file `.env` con le proprie credenziali e configurazioni Azure** per eseguire subito i test.

> ✅ Ottimo punto di partenza per testare la robustezza dei modelli LLM e la risposta ai tentativi di prompt injection o contenuti sensibili.

---

## 🚀 Cosa contiene

| File                      | Descrizione                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `Agent_EvaluationSDK.py` | Red teaming locale con [Azure AI Evaluation SDK][eval-sdk] e callback personalizzati. |
| `Agent_FoundrySDK.py`    | Red teaming via cloud con [Azure AI Foundry SDK][foundry-sdk].              |

Questa repo è pensata per team di sicurezza, ricercatori o prompt engineer interessati a valutare la resilienza dei modelli AI rispetto a strategie comuni di attacco testuale.

---

## ⚙️ Setup & Configurazione

### 1. Clona la repo

```bash
git clone https://github.com/your-org/azure-red-teaming-agent.git
cd azure-red-teaming-agent
````

### 2. Installa le dipendenze

> Richiede Python 3.9+

```bash
pip install -r requirements.txt
```

Dipendenze principali:

* `azure-ai-evaluation[redteam]`
* `azure-ai-projects`
* `pyrit`
* `openai`
* `python-dotenv`
* `azure-identity`

### 3. Configura il file `.env`

```env
# Endpoint del progetto Foundry (solo per Agent_FoundrySDK.py)
AZURE_AI_PROJECT=https://<account>.services.ai.azure.com/api/projects/<nome-progetto>

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<tuo-openai>.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_KEY=your-azure-openai-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

---

## 🧠 Come funziona

### ✅ Evaluation SDK (locale)

* Usa la classe `RedTeam` da `azure.ai.evaluation.red_team`.
* Include callback statici o dinamici con Azure OpenAI.
* Supporta strategie di attacco avanzate e categorie di rischio multiple.
* Esecuzione asincrona e altamente personalizzabile.

### ☁️ Foundry SDK (cloud)

* Usa `AIProjectClient` per eseguire i test da remoto.
* Configura target e strategie tramite oggetti modello.
* Perfetto per integrazione in pipeline automatizzate.

---

## 🧪 Prompt Shield e Filtri di Sicurezza

> ⚠️ **IMPORTANTE:** per osservare in modo più evidente le funzionalità dell’agente e valutare le reali risposte del modello, **si consiglia di impostare al minimo le configurazioni di filtering e contenuto sensibile** sul proprio endpoint Azure OpenAI.

Durante i test, Microsoft può bloccare alcune richieste tramite **Prompt Shield** (un livello di protezione che agisce *prima* dell’inferenza del modello). Questo comportamento è parte integrante delle difese Azure, ma può interferire con i risultati se non gestito.

Alcuni attacchi che possono essere bloccati in anticipo:

* `ROT13`
* `UNICODE_CONFUSABLE`
* `JAILBREAK`
* `LEETSPEAK`

---

## 🎯 Strategie di Attacco Supportate

* `Base64`
* `ROT13`
* `Caesar`
* `ASCII_Smuggler`
* `CharacterSpace`
* `Leetspeak`
* `UnicodeConfusable`
* `Diacritic`
* `Jailbreak`
* `Compose` (es. `Base64 + ROT13`)

### Categorie di rischio testate:

* `VIOLENCE`
* `HATE_UNFAIRNESS`
* `SEXUAL`
* `SELF_HARM`

---

## 📌 Use Case

* Validazione e tuning delle policy di sicurezza
* Analisi del comportamento dei modelli sotto attacco
* Ricerca su difese AI e content filtering
* Testing automatizzato di modelli LLM

---

## 📚 Documentazione Ufficiale

* [AI Red Teaming con Evaluation SDK][eval-sdk]
* [AI Red Teaming con Foundry SDK][foundry-sdk]
* [Azure AI Evaluation SDK su PyPI](https://pypi.org/project/azure-ai-evaluation/)
* [Microsoft PyRIT GitHub](https://github.com/Azure/PyRIT)

---

## 📝 Licenza

Distribuito sotto licenza MIT — vedi [LICENSE](./LICENSE)

---

## 🙋‍♀️ Contribuisci

Pull request, segnalazioni e suggerimenti sono benvenuti!

---

[eval-sdk]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/run-scans-ai-red-teaming-agent
[foundry-sdk]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/run-ai-red-teaming-cloud

```

### Attack risk category

![Attack risk category](.venv\img\Screenshot 2025-07-04 182816.png)

### Attack Complexity

![Attack Complexity](.venv\img\Screenshot 2025-07-04 182839.png)