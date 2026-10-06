# ✈️ TravelBudget — Planejador de Viagem Financeiro

Aplicação desktop desenvolvida em **Python** para auxiliar no planejamento financeiro de viagens.

O TravelBudget permite definir informações básicas de uma viagem, consultar cotações de moedas e condições climáticas, calcular o orçamento disponível e manter um histórico dos planejamentos realizados.

O projeto também está sendo evoluído com a integração de um **Consultor IA**, utilizando **LangChain e LangGraph**, capaz de consultar os dados da viagem, realizar cálculos, buscar informações externas e interagir com diferentes ferramentas.

---

## 🚀 Funcionalidades

### 🧳 Planejamento de viagem

- Definição do orçamento da viagem
- Quantidade de viajantes
- Quantidade de dias
- Escolha da moeda
- Definição da cidade de destino
- Cálculo do orçamento por pessoa
- Cálculo do orçamento por dia
- Cálculo do orçamento por pessoa e por dia

### 💰 Cotação de moedas

Integração com a **AwesomeAPI** para consulta de valores atualizados de:

- 🇺🇸 Dólar
- 🇪🇺 Euro
- ₿ Bitcoin

Também está sendo implementada uma ferramenta para conversão de valores entre moedas.

### 🌤️ Clima

Integração com a **OpenWeather API** para consultar informações climáticas do destino, incluindo:

- Temperatura
- Sensação térmica
- Umidade
- Condição climática
- Ícone correspondente à condição

### 📊 Histórico

Os planejamentos realizados são armazenados em arquivo CSV, permitindo consultar viagens planejadas anteriormente.

O histórico também poderá ser utilizado pelo Consultor IA para responder perguntas relacionadas a planejamentos anteriores.

### 🤖 Consultor IA

O projeto possui um assistente de viagens integrado à aplicação.

O agente utiliza **LangChain + LangGraph** e possui ferramentas capazes de acessar diferentes informações do aplicativo.

Atualmente, o agente está sendo desenvolvido para:

- Consultar a viagem atualmente planejada
- Consultar o histórico de viagens
- Consultar cotação de moedas
- Consultar o clima de uma cidade
- Realizar cálculos de orçamento
- Converter valores entre moedas
- Utilizar múltiplas ferramentas em uma mesma conversa

A arquitetura utiliza um fluxo baseado em grafo:

```text
Usuário
   ↓
Consultor IA
   ↓
LangGraph
   ↓
┌─────────────────────┐
│      Chatbot        │
└──────────┬──────────┘
           │
       precisa de
       ferramenta?
        /       \
      sim       não
       ↓         ↓
    Tools       FIM
       ↓
    Chatbot
```

---

## 🧠 Arquitetura do projeto

O projeto foi estruturado separando a interface, regras da aplicação, serviços externos e agente de IA.

```text
TravelBudget/
│
├── data/
│   └── Historico_de_viagens.csv
│
├── models/
│   └── ...
│
├── services/
│   ├── cotacao.py
│   └── clima.py
│
├── ...
│
├── requirements.txt
├── .env
├── .gitignore
└── main.py
```

A estrutura pode ser expandida conforme novas funcionalidades forem adicionadas.

---

## 🤖 Ferramentas do agente

O Consultor IA utiliza ferramentas especializadas em vez de receber todas as informações diretamente no prompt.

### Viagem atual

Consulta os dados da viagem que está atualmente planejada no aplicativo.

### Histórico

Consulta planejamentos realizados anteriormente.

### Cotação

Consulta o valor atual de uma moeda em relação ao real.

### Clima

Consulta as condições climáticas de uma determinada cidade.

### Cálculo de orçamento

Realiza cálculos como:

```text
Orçamento por dia
Orçamento por pessoa
Orçamento por pessoa/dia
```

### Conversão de moeda

Permite realizar conversões entre valores e moedas.

---

## 💾 Memória do agente

Uma próxima etapa do projeto será utilizar **SQLite + SqliteSaver**, permitindo que o LangGraph mantenha o estado das conversas.

Essa memória será diferente do histórico de viagens:

```text
Historico_de_viagens.csv
        ↓
Dados dos planejamentos

SQLite / SqliteSaver
        ↓
Estado e histórico das conversas com o agente
```

A utilização do `thread_id` permitirá identificar uma conversa sem exigir, neste momento, um sistema de cadastro ou login.

---

## 🌐 Integração com informações da Web

Como evolução do Consultor IA, está prevista a possibilidade de utilizar ferramentas de busca na Web para obter informações que não estejam disponíveis nos dados internos da aplicação.

Possíveis usos:

- Pesquisa de atrações turísticas
- Informações sobre destinos
- Pesquisa de recomendações
- Consulta de informações atualizadas
- Extração de informações de páginas específicas

Essa funcionalidade será adicionada posteriormente para ampliar a capacidade do Consultor IA.

---

## 🔐 Human-in-the-Loop

Outra funcionalidade planejada é a utilização de **Human-in-the-Loop (HITL)** através do LangGraph.

A ideia é permitir que determinadas ações que alterem dados da aplicação precisem de confirmação do usuário antes de serem executadas.

Exemplo:

```text
Usuário
   ↓
"Altere minha viagem para 10 dias"
   ↓
Agente propõe alteração
   ↓
Confirmação do usuário
   ↓
Ferramenta executa alteração
```

O HITL será utilizado principalmente para operações que modificam dados, e não necessariamente para consultas simples como clima ou cotação.

---

## 🛠️ Tecnologias utilizadas

### Linguagem

- Python

### Interface

- CustomTkinter

### Inteligência Artificial

- LangChain
- LangGraph
- Groq
- LLM com suporte a tool calling

### APIs

- AwesomeAPI
- OpenWeather API

### Dados

- Pandas
- CSV
- SQLite *(em implementação)*

### Web

- Requests
- BeautifulSoup
- Tavily *(planejado para busca Web)*

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/TravelBudget.git
```

Entre na pasta:

```bash
cd TravelBudget
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

No Windows:

```bash
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
API_KEY_GROQ=sua_chave
API_KEY_OPENWEATHER=sua_chave
```

Caso outras APIs sejam utilizadas, suas respectivas chaves deverão ser adicionadas ao `.env`.

> ⚠️ Nunca envie o arquivo `.env` para o GitHub. Ele deve estar presente no `.gitignore`.

### 5. Execute a aplicação

```bash
python main.py
```

---

## 📋 Próximos passos

O projeto ainda está em desenvolvimento.

### Concluído

- [x] Interface gráfica
- [x] Planejamento financeiro
- [x] Cálculos de orçamento
- [x] Integração com cotação de moedas
- [x] Integração com clima
- [x] Persistência do histórico
- [x] Consultor IA
- [x] Integração LangChain
- [x] Integração LangGraph
- [x] Tool calling
- [x] Ferramenta de consulta da viagem atual
- [x] Ferramenta de histórico
- [x] Ferramenta de clima
- [x] Ferramenta de cotação
- [x] Ferramenta de cálculo de orçamento

### Em desenvolvimento

- [ ] Conversão de moedas
- [ ] Testes das ferramentas do agente
- [ ] Memória persistente com SQLite + SqliteSaver
- [ ] Melhor gerenciamento de conversas
- [ ] Busca de informações na Web
- [ ] Human-in-the-Loop para ações que modificam dados

### Futuramente

- [ ] Sistema de recomendação de destinos
- [ ] Utilização de Machine Learning com dados históricos
- [ ] Melhorias na personalização das recomendações
- [ ] Testes automatizados
- [ ] Melhorias de segurança e tratamento de erros

---

## 🎯 Objetivo do projeto

O TravelBudget começou como uma aplicação para praticar desenvolvimento em Python, integração com APIs e manipulação de dados.

Com sua evolução, o projeto passou a incorporar conceitos de **Inteligência Artificial, agentes, tool calling, LangGraph, memória de agentes e integração com serviços externos**.

O objetivo é construir uma aplicação capaz não apenas de realizar cálculos, mas também de **interpretar o contexto da viagem e utilizar diferentes ferramentas para auxiliar o usuário durante o planejamento**.

---

## 📚 Conceitos praticados

Durante o desenvolvimento, o projeto aborda conceitos como:

- Programação Orientada a Objetos
- APIs REST
- Requisições HTTP
- Manipulação de JSON
- Persistência de dados
- Pandas
- CSV
- Variáveis de ambiente
- Interfaces gráficas
- LLMs
- Prompt Engineering
- Tool Calling
- LangChain
- LangGraph
- StateGraph
- Agentes
- Memória de agentes
- Checkpointing
- Integração de múltiplas ferramentas
- Human-in-the-Loop
- Machine Learning *(etapa futura)*

---

## 👩‍💻 Autora

**Fernanda**

Estudante de Análise e Desenvolvimento de Sistemas, com foco em **Python, Backend, Machine Learning e Inteligência Artificial**.