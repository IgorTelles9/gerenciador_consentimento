## Documentação: Módulo de Gerenciamento de Consentimento (MGC)

### 1\. Visão Geral

O Módulo de Gerenciamento de Consentimento (MGC) é o componente central e a "fonte única da verdade" para todas as questões de privacidade dentro do arcabouço de software de conformidade com a LGPD.

Ele é implementado como um microsserviço de API RESTful, desacoplado dos demais componentes (como o Gateway de Privacidade e o Painel de Controle do Titular), permitindo manutenibilidade e escalabilidade independentes.

Seu propósito principal é:

  * **Centralizar** o registro e a gestão do ciclo de vida do consentimento do titular dos dados.
  * **Garantir** a conformidade com os princípios da LGPD, como Finalidade, Transparência e Prestação de Contas (*Accountability*).
  * **Fornecer** as políticas de privacidade ativas para o Gateway de Privacidade (GP) de forma eficiente.
  * **Receber** e processar as escolhas de privacidade feitas pelo usuário no Painel de Controle do Titular (PCPT).

### 2\. Arquitetura e Tecnologias

O MGC foi construído utilizando um stack de tecnologias Python modernas, com foco em performance e melhores práticas de engenharia de software:

  * **Framework Web:** **FastAPI**, pela sua alta performance, digitação de dados (typing) nativa e geração automática de documentação de API (Swagger/OpenAPI).
  * **Banco de Dados:** **PostgreSQL**, por sua robustez, confiabilidade e suporte nativo a tipos de dados avançados como `ENUM`.
  * **ORM (Mapeamento Objeto-Relacional):** **SQLAlchemy**, para uma interação segura e "Pythônica" com o banco de dados.
  * **Validação de Dados:** **Pydantic**, usado pelo FastAPI para definir, validar e serializar "schemas" de dados de entrada e saída da API.
  * **Migrações de Banco:** **Alembic**, para gerenciar a evolução do esquema do banco de dados de forma segura e versionada.
  * **Mensageria (Publisher):** **Paho-MQTT**, utilizado para publicar notificações de invalidação de cache em tempo real para o Gateway de Privacidade.
  * **Configuração:** Leitura de variáveis de ambiente a partir de um arquivo `.env` (ex: `python-dotenv`).

A arquitetura do código-fonte é estritamente organizada por responsabilidade para promover baixo acoplamento e alta coesão:

```
/gerenciador_consentimento
|-- alembic/                  # Scripts de migração do Alembic
|-- crud/                     # Lógica de negócio (interação com o BD)
|   |-- titular.py
|   |-- consentimento.py
|   `-- ...
|-- models/                   # Definições das tabelas do BD (SQLAlchemy)
|   |-- __init__.py
|   |-- titular.py
|   |-- consentimento.py
|   `-- ...
|-- routers/                  # Lógica da API (endpoints HTTP)
|   |-- titulares.py
|   |-- consentimentos.py
|   `-- ...
|-- schemas/                  # Validação de dados da API (Pydantic)
|   |-- __init__.py
|   |-- titular.py
|   |-- consentimento.py
|   `-- ...
|-- .venv/                    # Ambiente virtual Python
|-- alembic.ini               # Configuração do Alembic
|-- database.py               # Configuração da engine e sessão do SQLAlchemy
|-- main.py                   # Ponto de entrada da aplicação FastAPI
|-- messaging.py              # Lógica de conexão e publicação MQTT
`-- .env                      # Arquivo de configuração (credenciais)
```

### 3\. Modelagem de Dados

O núcleo do MGC é seu esquema de banco de dados, que foi projetado para máxima granularidade e conformidade com a LGPD:

  * **`Titular` e `Dispositivo`:** Tabelas de cadastro básicas para identificar os atores do ecossistema.
  * **`Finalidade`:** Tabela crucial que materializa o **Princípio da Finalidade** da LGPD.
      * `nome`: Ex: "Otimização de Energia".
      * `descricao`: Explicação clara para o titular.
      * `base_legal`: Um `Enum` (ex: `CONSENTIMENTO`, `LEGITIMO_INTERESSE`) que define a justificativa legal para o tratamento, conforme o Art. 7º da LGPD.
  * **`OpcaoDeTratamento`:** O coração da granularidade. Em vez de um "sim/não", esta tabela armazena o "como" o dado pode ser tratado.
      * `chave_politica`: O "comando" legível por máquina (ex: `RAW:none:none:STREAM`, `AVG:none:10M:10M`) que o Gateway de Privacidade irá executar.
      * `titulo` e `descricao`: Explicações legíveis para o titular (ex: "Enviar média a cada 10 minutos").
  * **`RegistroConsentimento`:** A tabela de junção central que representa a escolha do titular. Ela conecta quem, o quê, por quê e como.
      * `titular_id` (Quem)
      * `dispositivo_id` (O quê)
      * `finalidade_id` (Por quê)
      * `opcao_tratamento_id` (Como)
      * `status`: Um `Enum` (ex: `ATIVO`, `REVOGADO`) que gerencia o ciclo de vida.
  * **`LogAuditoriaConsentimento`:** A tabela que garante o **Princípio da Prestação de Contas** (*Accountability*).
      * Registra um log imutável para cada alteração de estado em um `RegistroConsentimento` (ex: "CONCESSÃO INICIAL", "REVOGAÇÃO").
      * É populada automaticamente pela camada `crud` em uma transação atômica junto com a mudança de consentimento.

### 4\. Funcionalidades Principais

O MGC implementa funcionalidades críticas para o funcionamento de todo o arcabouço:

1.  **Gestão Granular de Consentimento:** O sistema permite que um titular conceda permissões diferentes para finalidades diferentes no mesmo dispositivo, e escolha *como* seus dados serão processados (a `chave_politica`), em vez de um simples "aceito tudo".

2.  **Ciclo de Vida e Auditoria (Accountability):** O MGC gerencia o ciclo de vida completo do consentimento (concessão, revogação). Cada uma dessas ações é registrada de forma automática e imutável na tabela `LogAuditoriaConsentimento`, provendo uma trilha de auditoria completa para fins de conformidade.

3.  **Sincronização Reativa com o Gateway (Push):** Esta é a funcionalidade mais crítica para a performance do sistema. Para evitar que o Gateway de Privacidade (GP) precise consultar a API do MGC a cada dado recebido (o que geraria alta latência), o MGC implementa um mecanismo de "push" reativo:

      * Quando um consentimento é criado (`POST /consentimentos`) ou revogado (`PATCH /consentimentos/{id}/revogar`), a camada `crud` faz uma chamada ao `messaging.py`.
      * O `messaging.py` publica uma mensagem leve de **invalidação de cache** em um tópico MQTT (ex: `politicas/atualizacoes`).
      * A mensagem contém `{"titular_id": X, "dispositivo_id": Y}`, sinalizando ao GP que o cache para este par deve ser apagado e a política deve ser buscada novamente na próxima requisição de dados.
      * Esta conexão MQTT é gerenciada pelos eventos de *lifespan* do FastAPI no `main.py`, garantindo que o MGC se conecte ao broker ao iniciar e se desconecte graciosamente.

4.  **Evolução Segura do Banco (Alembic):** O Alembic está configurado para ler os `models` do SQLAlchemy. Qualquer alteração no esquema (ex: adicionar uma nova coluna) é gerenciada por scripts de migração (`alembic revision --autogenerate`), e aplicada de forma segura (`alembic upgrade head`), sem perda de dados.

5.  **Configuração Segura e Modular:** Todas as configurações sensíveis (credenciais do PostgreSQL, endereço do broker MQTT) são lidas a partir de um arquivo `.env`, não estando presentes no código-fonte.

### 5\. API Endpoints (Referência Rápida)

O MGC expõe uma API RESTful para ser consumida pelos outros módulos (PCPT e GP).

#### Endpoints de Configuração (Usados pelo Admin/PCPT)

  * `POST /titulares/`: Cria um novo titular de dados.
  * `POST /dispositivos/`: Registra um novo dispositivo IoT.
  * `POST /finalidades/`: Cadastra uma nova finalidade de tratamento.
  * `POST /tipos_de_dados/`: Cadastra um novo tipo de dado (ex: "Temperatura").
  * `POST /opcoes_tratamento/`: Cadastra uma nova opção de tratamento e sua `chave_politica`.

#### Endpoints do Fluxo de Consentimento

  * **`POST /consentimentos/`**

      * **Consumidor:** Painel de Controle (PCPT).
      * **Ação:** Endpoint principal para um titular **conceder** um novo consentimento. Recebe os IDs do titular, dispositivo, finalidade e opção de tratamento.
      * **Efeito Colateral:** Dispara a publicação da mensagem de invalidação de cache no MQTT.

  * **`GET /consentimentos/titular/{titular_id}`**

      * **Consumidor:** Gateway de Privacidade (GP).
      * **Ação:** Endpoint principal para o GP **buscar** todas as políticas de consentimento *ativas* de um determinado titular. É chamado pelo GP apenas quando seu cache local (Redis) está vazio ou foi invalidado.

  * **`PATCH /consentimentos/{id}/revogar`**

      * **Consumidor:** Painel de Controle (PCPT).
      * **Ação:** Endpoint para um titular **revogar** um consentimento específico. Altera o status do registro para `REVOGADO`.
      * **Efeito Colateral:** Dispara a publicação da mensagem de invalidação de cache no MQTT.

### 6\. Configuração e Execução

1.  **Variáveis de Ambiente:** Crie um arquivo `.env` na raiz do projeto com as credenciais do PostgreSQL e do broker MQTT.
2.  **Instalação:** `uv sync`
3.  **Migrações:** Execute `uv run alembic upgrade head` para criar o esquema do banco de dados no PostgreSQL.
4.  **Execução:** Execute `uv run uvicorn main:app --reload` para iniciar o servidor da API.
5.  **Documentação:** Acesse `http://127.0.0.1:8000/docs` para ver e interagir com a documentação automática da API (Swagger UI).