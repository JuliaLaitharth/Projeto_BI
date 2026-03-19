## 1. Plano do Projeto: Data Warehouse de Gestão Financeira

### 1.1. Objetivo do Projeto
O objetivo principal deste projeto é consolidar 12 meses de transações de cartões de crédito de diferentes titulares num único ambiente analítico (Data Warehouse). O foco é transformar dados brutos e desestruturados (arquivos CSV) em informações organizadas que permitam identificar padrões de consumo, gastos por categoria e gestão de parcelamentos.

### 1.2. Justificação 
Os dados originais apresentam inconsistências que impedem uma análise direta:

Nomes de estabelecimentos poluídos: Presença de códigos de máquinas de cartão.

Dados não numéricos: Informação de parcelas misturada com texto.

Dispersão de ficheiros: Dados espalhados por 12 ficheiros mensais independentes.

### 1.3. Escopo Técnico 
Para a execução, foi definida a seguinte stack:

Linguagem: Python 3.9.

Bibliotecas de Dados: Pandas e SQLAlchemy.

Base de Dados: PostgreSQL.

Controlo de Versão: Github.

### 1.4. Arquitetura da Solução
A solução foi desenhada seguindo o ciclo ETL (Extract, Transform, Load):

Extração: Leitura em lote de todos os arquivos .csv na pasta do projeto.

Transformação: Higienização de strings via Regex, conversão de tipos monetários e cálculo de parcelas.

Carga: Distribuição dos dados no modelo Star Schema.


## 2. Arquitetura do Data Warehouse

### 2.1. Modelo Dimensional 
A arquitetura de dados foi desenhada seguindo o padrão Star Schema. Esta escolha justifica-se pela necessidade de performance em consultas analíticas e pela clareza na separação de responsabilidades entre tabelas de métricas e tabelas de contexto.

O modelo é composto por uma Tabela de Fato centralizada, que se relaciona com múltiplas Tabelas de Dimensão;

* **Tabela de Fato (`fato_transacao`):** Armazena os eventos quantitativos (as compras). Contém as chaves estrangeiras (FKs) que ligam às dimensões e as métricas principais, como `valor_brl`, `valor_usd` e o controle de parcelas (`num_parcela` e `total_parcelas`).
* **Tabelas de Dimensão (Contexto):**
    * **`dim_data`:** Permite a análise temporal detalhada (ano, mês, trimestre, dia da semana).
    * **`dim_titular`:** Identifica quem realizou o gasto (Vin Diesel, Eva Mendes, etc.).
    * **`dim_categoria`:** Classifica a natureza do gasto (Alimentação, Lazer, etc.).
    * **`dim_estabelecimento`:** Armazena o local da transação de forma higienizada.



### 2.2. Diagrama de Entidade-Relacionamento (ERD)
Abaixo, apresenta-se a visualização técnica das tabelas e suas conexões (Chaves Primárias e Estrangeiras) conforme implementado no servidor **PostgreSQL**:

<img src="docs/bipst.png" alt="Diagrama BI" width="600">

### 2.3. Vantagens da Arquitetura Adotada
1.  **Redução de Redundância:** Os nomes dos titulares e categorias são armazenados apenas uma vez em suas respectivas dimensões.
2.  **Facilidade de Uso:** Permite que ferramentas de BI (como Power BI ou Looker) criem filtros (Slicers) de forma nativa e rápida.
3.  **Escalabilidade:** Novos titulares ou novos meses de dados podem ser adicionados sem alterar a estrutura das tabelas existentes.

---

### O que falta agora para fechar o trabalho?

Agora que você já tem o **Plano** e a **Arquitetura**, falta apenas o último tópico:
* **Tópico 3: Processo ETL e Resultados:** Onde você explica o código Python e mostra os prints das tabelas preenchidas no banco de dados.

**Gostaria que eu preparasse o texto do Tópico 3 e as Queries SQL para você gerar os últimos prints de resultados?**
