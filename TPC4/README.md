# Biblioteca Temporal – Ontologia e Queries SPARQL

## Descrição do Trabalho

Este trabalho consistiu na criação, povoamento e exploração de uma ontologia relativa a uma **biblioteca temporal**, utilizando tecnologias da Web Semântica.

### Modelação da Ontologia

Numa primeira fase foi realizada a **modelação da ontologia utilizando a ferramenta Protégé** de acordo com a ontologia dada pelo professor ([ ./bibliotecatemporal.ttl](bibliotecatemporal.ttl/))

Estas definições permitiram representar as relações entre **livros, autores, eventos históricos/futuros e diferentes linhas temporais**.

### Povoamento da Ontologia

Após a definição da estrutura da ontologia, procedeu-se ao seu **povoamento com instâncias**.

Para tal, foi desenvolvido um **script em Python**, recorrendo à biblioteca **rdflib**, que permitiu:

1. Ler a ontologia em formato **Turtle (.ttl)**.
2. Processar dois conjuntos de dados fornecidos em formato **JSON** ([ ./dataset_temporal_100.json](dataset_temporal_100.json/) e [ ./dataset_temporal_v2_100.json](dataset_temporal_v2_100.json/)
3. Criar automaticamente **indivíduos das classes definidas na ontologia**.
4. Estabelecer as respetivas **relações entre os indivíduos**, como:

   * associação de livros aos seus autores,
   * associação de livros às linhas temporais,
   * referência a eventos históricos ou futuros,
   * associação de bibliotecários às bibliotecas onde trabalham.

No final, o script gerou uma nova versão da ontologia já **povoada com dados**, que foi posteriormente carregada no **GraphDB** para permitir a execução de consultas SPARQL ([./bibliotecaTemporalFinal.ttl](bibliotecaTemporalFinal.ttl/))


# Exercícios SPARQL – Biblioteca Temporal

## 1. Liste todos os livros que existem na linha temporal original (`LinhaOriginal`) (LIVROS POR LINHA TEMPORAL)

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT DISTINCT ?nomeLivro WHERE {
    ?nomeLivro :existeEm ?nomeLinhaT .
    ?nomeLinhaT a :LinhaOriginal .
}
ORDER BY ?nomeLivro 
```

---

## 2. Identifique os livros que existem em mais do que uma linha temporal (LIVROS EM MÚLTIPLAS LINHAS TEMPORAIS)

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?nomeLivro (COUNT(?nomeLinhaT) AS ?numLinhasT) WHERE {
    ?nomeLivro :existeEm ?nomeLinhaT .
}
GROUP BY ?nomeLivro 
HAVING (COUNT(?nomeLinhaT) > 1)   
```

---

## 3. Liste todos os livros classificados como `LivroParadoxal` (LIVROS PARADOXAIS)

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?nomeLivro WHERE {
    ?nomeLivro a :LivroParadoxal .
}
```

---

## 4. Para cada `LivroHistórico`, indique os eventos históricos que esse livro refere (LIVROS HISTÓRICOS E EVENTOS)

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?nomeLivro ?nomeEventoHistorico WHERE {
    ?nomeLivro a :LivroHistórico .
    ?nomeLivro :refere ?nomeEventoHistorico .
    ?nomeEventoHistorico a :EventoHistórico .
}
ORDER BY ?nomeLivro
```

---

## 5. Identifique livros classificados como LivroHistorico que referem eventos futuros (INCONSISTÊNCIAS SEMÂNTICAS)

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?nomeLivro WHERE {
    ?nomeLivro a :LivroHistórico ;
               :refere ?nomeEvento .
    ?nomeEvento a :EventoFuturo .
}
```

---

## 6. Liste os autores e o número de livros que escreveram, ordenando o resultado por número de livros em ordem decrescente (AUTORES MAIS PROLÍFICOS)

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?nomeAutor (COUNT(?livro) AS ?numLivros) WHERE {
    ?livro :escritoPor ?autor .
    ?autor :nome ?nomeAutor .
}
GROUP BY ?nomeAutor
ORDER BY DESC(?numLivros)
```

---

## 7. Identifique os autores que escreveram pelo menos um livro paradoxal (AUTORES DE LIVROS PARADOXAIS)

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?nomeAutor WHERE {
    ?livro a :LivroParadoxal ;
             :escritoPor ?autor .
    ?autor :nome ?nomeAutor
}
GROUP BY ?nomeAutor
```

---

## 8. Liste todos os livros que existem em pelo menos uma linha temporal alternativa (`LinhaAlternativa`).

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?livro WHERE {
    ?livro :existeEm ?nomeLinhaT .
    ?nomeLinhaT a :LinhaAlternativa .
}
ORDER BY ?livro
```

---

## 9. Indique todos os bibliotecários e a biblioteca onde trabalham (BIBLIOTECÁRIOS)

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?nome ?biblioteca WHERE {
    ?nome a :Bibliotecário ;
          :trabalhaEm ?biblioteca .
    ?biblioteca a :Biblioteca .
}
```

---

## 10. Liste todos os livros escritos por Cronos e indique em que linhas temporais esses livros existem (LIVROS ESCRITOS POR CRONOS)

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?livro ?linhaTemporal ?tipoLinhaTemporal WHERE {
    ?livro :escritoPor :Cronos ;
           :existeEm ?linhaTemporal .
    ?linhaTemporal a ?tipoLinhaTemporal
    
    FILTER(?tipoLinhaTemporal != owl:NamedIndividual)
    FILTER(?tipoLinhaTemporal IN (:LinhaOriginal, :LinhaAlternativa))
}
ORDER BY ?livro
```

# Questões Bónus (Opcionais)

## 11. Identifique livros que não referem nenhum evento

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?livro WHERE {
    ?livro a :Livro .
    FILTER NOT EXISTS {
        ?livro :refere ?evento .
    }
}
ORDER BY ?livro
```

---

## 12. Verifique se existe algum livro sem linha temporal associada

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?livro WHERE {
    ?livro a :Livro .
    FILTER NOT EXISTS {
        ?livro :existeEm ?linhaTemporal .
    }
}
ORDER BY ?livro
```

---

## 13. Identifique autores que sejam também leitores (caso essa propriedade esteja modelada)

```sparql
PREFIX : <http://rpcw.di.uminho.pt/2026/untitled-ontology-13/>
SELECT ?pessoa WHERE {
    ?pessoa a :Autor ;
            a :Leitor .
}
```

---
