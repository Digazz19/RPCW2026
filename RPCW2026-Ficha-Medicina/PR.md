# Povoamento e Consulta de Ontologia Médica

## Descrição Geral

Este trabalho consiste no povoamento de uma ontologia OWL (`medical.ttl`) a partir de datasets em formato CSV e JSON, e na criação de queries SPARQL para consulta da ontologia resultante.

A ontologia base define as classes `:Disease`, `:Symptom`, `:Treatment` e `:Patient`, e as propriedades `:hasSymptom`, `:hasTreatment`, `:exhibitsSymptom` e `:hasDisease`.

---

## Requisitos

### Dependências Python

```bash
pip install rdflib pandas
```

### Ficheiros necessários

| Ficheiro | Descrição |
|---|---|
| `medical.ttl` | Ontologia base |
| `Disease_Syntoms.csv` | Doenças e sintomas |
| `Disease_Description.csv` | Descrições das doenças |
| `Disease_Treatment.csv` | Tratamentos por doença |
| `doentes.json` | Dados dos doentes |

Todos os ficheiros devem estar na mesma pasta que os scripts.

---

## Estrutura dos Scripts

### `generate_instances.py` → `med_doencas.ttl`

**O que faz:**
1. Corrige a propriedade `:name` → `:nome` nos pacientes já existentes na ontologia base
2. Lê `Disease_Syntoms.csv` e cria instâncias de `:Disease` e `:Symptom`
3. Associa cada doença aos seus sintomas via `:hasSymptom`
4. Lê `Disease_Description.csv` e associa uma descrição a cada doença via `:hasDescription`
5. Grava o resultado em `med_doencas.ttl`

```bash
python generate_instances.py
```

---

### `generate_treatments.py` → `med_tratamentos.ttl`

**O que faz:**
1. Parte de `med_doencas.ttl`
2. Lê `Disease_Treatment.csv` (colunas `Precaution_1` a `Precaution_4`)
3. Cria instâncias de `:Treatment` para cada tratamento único
4. Associa cada doença aos seus tratamentos via `:hasTreatment`
5. Grava o resultado em `med_tratamentos.ttl`

```bash
python generate_treatments.py
```

---

### `generate_doentes.py` → `med_doentes.ttl`

**O que faz:**
1. Parte de `med_tratamentos.ttl`
2. Lê `doentes.json` — cada entrada tem `nome` e lista de `sintomas`
3. Cria instâncias de `:Patient` com IDs do tipo `doente_00001` a `doente_10000`
4. Associa o nome via `:nome` e os sintomas via `:exhibitsSymptom`
5. Grava o resultado em `med_doentes.ttl`

```bash
python generate_doentes.py
```

---

## Execução Completa (ordem obrigatória)

```bash
python generate_instances.py
python generate_treatments.py
python generate_doentes.py
```

---

## Queries SPARQL

As queries SPARQL desenvolvidas estão documentadas no ficheiro **[sparql.txt](sparql.txt)**.