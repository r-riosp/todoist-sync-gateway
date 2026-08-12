# ⛩️ TAL Gateway (Todoist ➔ AnyType & Linear)

Um gateway assíncrono e resiliente projetado para centralizar e rotear tarefas do Todoist para plataformas de produtividade e gerenciamento de issues (AnyType e Linear).

Construído com foco em alta performance e tolerância a falhas, este projeto atua como um motor de sincronização local, permitindo que você capture ideias rapidamente pelo celular (via Todoist) e as despache automaticamente para os seus ambientes de trabalho corretos.

## 🚀 Features e Arquitetura

* **Roteamento Inteligente por Tags:** Controle total do fluxo de dados. Utilize tags nativas no Todoist (`@linear`, `@anytype`) para direcionar suas tarefas. Tarefas sem tags de roteamento são ignoradas de forma segura.
* **Outbox Pattern (Modo de Espera):** Nada se perde. Se o AnyType local estiver desligado ou a API do Linear cair, o Gateway enfileira a tarefa no SQLite com status `PENDING`. Um worker em background tenta o reenvio automaticamente sem bloquear novas requisições.
* **Desacoplamento de Estados:** Falhas isoladas. Se o sincronismo com uma plataforma falhar, a outra continua funcionando normalmente.
* **GraphQL Integration:** Comunicação direta, tipada e enxuta com a API do Linear utilizando `gql`.

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.11+
* **Framework Web:** FastAPI (com Uvicorn)
* **Banco de Dados:** SQLite (nativo, ideal para filas locais)
* **Requisições & APIs:** HTTPX, gql (GraphQL)
* **Gerenciador de Dependências:** PDM

## ⚙️ Instalação e Setup

Siga os passos abaixo para rodar o Gateway na sua máquina local:

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/tal-gateway.git
cd tal-gateway
```

### 2. Instale as dependências via PDM
```bash
pdm install
```

### 3. Configuração de Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais:
```env
TODOIST_API_KEY="sua_chave_do_todoist"

ANYTYPE_API_KEY="sua_chave_do_anytype"
ANYTYPE_BASE_URL="http://127.0.0.1:31009/v1"

LINEAR_API_KEY="sua_chave_do_linear"
LINEAR_TEAM_ID="seu_team_uuid"
LINEAR_STATE_ID="uuid_da_coluna_backlog"
```

### 4. Execute a aplicação
O banco de dados SQLite e suas tabelas serão criados automaticamente na primeira inicialização.
```bash
pdm run uvicorn main:app --reload
```

## 🧪 Testes

A suíte de testes unitários cobre o roteamento inteligente, parsing de webhooks e a resiliência das conexões. Os testes utilizam pytest e mocks completos (sem I/O de banco ou rede).
```bash
pdm run pytest tests/ -v
```

[//]: # (## 🗺️ Próximos Passos &#40;Roadmap&#41;)

[//]: # ()
[//]: # (- [ ] Substituir Webhooks pela Todoist Sync API &#40;Polling ativo&#41;.)

[//]: # (- [ ] Desenvolver um processo Daemon &#40;systemd&#41; para Linux.)

[//]: # (- [ ] Construir uma interface nativa leve em GTK4 para gerenciamento de credenciais locais.)