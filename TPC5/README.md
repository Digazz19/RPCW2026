# Biblioteca Temporal — Aplicação Web

Aplicação web desenvolvida em Flask que permite navegar e consultar uma ontologia OWL de uma biblioteca temporal, armazenada num repositório GraphDB e acedida via queries SPARQL.

---

## Estrutura do Projeto

```
bibapp/
├── app.py              # Rotas Flask e lógica de queries SPARQL
├── mquery.py           # Módulo auxiliar para execução de queries SPARQL
└── templates/
    ├── layout.html     # Template base com navbar e footer
    ├── lista.html      # Lista de todos os livros (catálogo)
    ├── livro.html      # Página de detalhe de um livro
    ├── eventos.html    # Lista de todos os eventos
    └── evento.html     # Página de detalhe de um evento
```

---

## Ontologia

A ontologia (`bib_temp.ttl`) modela uma biblioteca de ficção científica com dimensão temporal. As principais classes são:

- **Livro** — com subclasses `LivroHistorico`, `LivroFiccional` e `LivroParadoxal`
- **Autor** — com nome e país de origem
- **Evento** — com subclasses `EventoHistorico` e `EventoFuturo`
- **LinhaTemporal** — com subclasses `LinhaOriginal` e `LinhaAlternativa`
- **Biblioteca** — local onde os livros se encontram
- **Bibliotecario** / **Leitor** — agentes que interagem com a biblioteca

Relações relevantes:
- `:escritoPor` — livro → autor
- `:refereEvento` — livro → evento
- `:existeEm` — livro → linha temporal
- `:pertenceA` — livro → biblioteca

---

## Rotas Implementadas

### `GET /` ou `GET /livros`
Lista todos os livros do catálogo (LivroParadoxal, LivroFiccional, LivroHistorico), ordenados por título. Para cada livro mostra o título (com link para a página de detalhe), tipo, autor e país.

### `GET /livro/<id_livro>`
Página de detalhe de um livro específico. Apresenta:
- ID, título, tipo, autor, país de origem do autor
- Linhas temporais em que o livro existe (pode ser mais do que uma)
- Eventos referenciados pelo livro, com link para a página de cada evento

### `GET /eventos`
Lista todos os eventos registados na ontologia, ordenados por designação. Para cada evento mostra a designação, descrição e os livros que o referenciam, com links para as páginas dos livros.

### `GET /evento/<id_evento>`
Página de detalhe de um evento específico. Apresenta:
- ID, designação e descrição do evento
- Lista de livros que referenciam o evento, com links para as páginas dos livros

---

## Como Executar

1. Garantir que o GraphDB está a correr localmente na porta `7200` com um repositório chamado `biblioteca_temporal` e a ontologia `bib_temp.ttl` carregada.

2. Instalar as dependências Python:
```bash
pip install flask SPARQLWrapper
```

3. Iniciar a aplicação:
```bash
python app.py
```

4. Aceder em: [http://localhost:5000](http://localhost:5000)

---

## Notas

- A navbar contém links para o **Catálogo** (`/livros`) e para os **Eventos** (`/eventos`).
- A rota raiz `/` e `/livros` apontam para a mesma função, garantindo que ambos os URLs funcionam.