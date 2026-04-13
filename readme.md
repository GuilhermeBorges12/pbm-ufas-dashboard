# Tratamento de Leads para Projeto de BI

## Descrição do Projeto
Este projeto tem como objetivo realizar o tratamento de dados provenientes de um arquivo `.csv` contendo leads, com foco na preparação para análise em ferramentas de Business Intelligence (BI).

Os dados originais apresentavam inconsistências, principalmente em uma coluna com estrutura semelhante a JSON, porém mal formatada. Foi desenvolvido um processo de limpeza, padronização e modelagem dos dados utilizando Python e a biblioteca Pandas.

---

## Problema Encontrado

A base de dados demonstrava diversos problemas de formatação, apresentando dados semi-estruturados em formato incorreto e sem padronização.
Além de uma coluna (`payload_json_banco_dados`) com json incorreto, exemplo: 

                mensagem {
                            sexo : ""masculino""
                         }

---

##  Etapas do Tratamento (ETL)

###  1. Leitura do CSV
- Utilização do `pandas.read_csv`
- Separador `;`
- Codificação `utf-8`

---

###  2. Tratamento da coluna JSON (semi-estruturada)
- Correção de aspas duplicadas
- Uso de expressões regulares (Regex) para extração de campos específicos:
  - `source_platform`
  - `interesse_curso`
  - `nome_contato`
  - `email_contato`

---

### 3. Conversão de Datas
- Conversão da coluna `data_hora_interacao` para o tipo datetime utilizando:

```python
pd.to_datetime(df['data_hora_interacao'])
```
---

### 4. Limpeza e Padronização
- Substituição de valores inválidos:
  - `''` e `','` → `"Não Informado"`
- Padronização dos canais de origem:
  
| Valor Original | Valor Padronizado |
|---------------|------------------|
| site          | Site Institucional |
| ig            | Instagram |
| fb            | Facebook |
| landing_page  | Landing Page / Google |

---

### 5. Enriquecimento dos Dados
Criação de novas colunas derivadas:

- `mes_ano`
- `mes_num`
- `hora_dia`
- `dia_semana`
- `tem_mensagem` (Com/Sem mensagem)
- `tipo_lead`:
  - **Novo** → primeira ocorrência do email
  - **Retorno** → email repetido

---

###  6. Modelagem de Dados 

####  Tabela Fato (`fato_interacoes.csv`)
Contém os eventos/interações:

- ID da transação (Pode ser considerado como atributo identificador primário)
- Data e hora
- Canal
- Tipo de lead
- Interesse no curso

---

####  Tabela Dimensão (`dim_pessoas.csv`)
Contém informações únicas por lead:

- Email
- Nome
- Primeiro contato
- Canal
- Interesse

---

#### Tabela Agregada (`agg_mes.csv`)
Resumo mensal para análise:

- Total de interações
- Pessoas únicas
- Distribuição por tipo de curso:
  - Mestrado
  - Doutorado
  - Indeciso
  - Não informado

---

##  Arquivos Gerados

- `fato_interacoes.csv`
- `dim_pessoas.csv`
- `agg_mes.csv`

---

## Tecnologias Utilizadas

- Python
- Pandas
- Regex (re)
- Power BI 
