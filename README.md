# Ontologia Minecraft — Java Edition 1.21.11

Projeto desenvolvido no âmbito da unidade curricular de **Representação e Processamento de Conhecimento na Web (RPCW)** da Universidade do Minho, 2025/2026.

## Objetivo

O objetivo deste projeto é especificar uma ontologia para o domínio do **Minecraft Java Edition 1.21.11**, cobrindo elementos e mecânicas de sobrevivência, como blocos, items, entidades, mobs, biomas, dimensões, estruturas, crafting, encantamentos, efeitos e progressão de jogo.

A ontologia é explorável através de uma aplicação web desenvolvida em Flask, com ligação a um repositório GraphDB. A aplicação permite consultar classes, indivíduos, propriedades, relações diretas e inversas, executar queries de competência e aumentar a ontologia ao nível da ABox, criando novos recursos, adicionando conhecimento guiado e inserindo triples validadas no repositório.

## Stack Tecnológica

- **Protégé** — modelação da TBox: classes, propriedades, restrições e hierarquia ontológica;
- **Python + rdflib** — geração da ABox a partir de dados JSON;
- **GraphDB** — armazenamento RDF e endpoint SPARQL;
- **Flask** — aplicação web para exploração e extensão da ontologia;
- **SPARQL** — consulta e atualização da ontologia.

## Fonte de Dados

A ontologia é construída a partir de duas fontes principais:

1. **PrismarineJS/minecraft-data**, versão `1.21.11`, usado como fonte primária para:

   - blocos;
   - items;
   - entidades;
   - biomas;
   - foods;
   - enchantments;
   - recipes;
   - effects.

2. **Dados manuais complementares**, usados para informação que não está suficientemente explícita no dataset principal:

   - drops de mobs;
   - spawns de mobs em biomas;
   - tiers de materiais;
   - requisitos mínimos de mineração;
   - dimensões;
   - estruturas;
   - items necessários para aceder a dimensões;
   - propriedades específicas de mobs;
   - blocos afetados pela gravidade.

Os dados manuais encontram-se em:

```text
data/manual/
```

A geração automática da ontologia junta os dados do PrismarineJS com estes dados manuais.

---

## Perguntas de Competência

A ontologia e a aplicação web foram desenhadas para responder às seguintes perguntas de competência:

1. Que ingredientes são necessários para craftar um item?
2. Que mobs dropam determinado item?
3. Em que biomas pode aparecer determinado mob?
4. Que ferramenta ou tier mínimo é necessário para minerar um bloco?
5. Que items podem receber determinado encantamento?
6. Que estruturas geram num determinado bioma?
7. Qual é a progressão dos tiers de material?
8. Que mobs são imunes ao fogo?
9. Que mobs ardem à luz do sol?
10. Que items são necessários para aceder a uma dimensão?
11. Que blocos são afetados pela gravidade?
12. Que alimentos têm maior saturação?
13. Que encantamentos são incompatíveis entre si?

Estas perguntas são respondidas através de queries SPARQL integradas na página **Queries de Competência** da aplicação web.

---

## Estrutura da Ontologia

A ontologia está dividida em duas partes principais:

- **TBox**: classes, hierarquias, object properties, data properties e restrições;
- **ABox**: indivíduos gerados automaticamente a partir dos datasets e dos dados manuais.

A TBox principal encontra-se em:

```text
ontology/classes.ttl
```

A ontologia final, com TBox e ABox combinadas, é gerada em:

```text
ontology/minecraft.ttl
```

---

## Classes de Topo

A ontologia organiza o domínio em seis classes principais:

| Classe | Papel no domínio | Descrição |
|---|---|---|
| `GameObject` | O quê? | Objetos tangíveis do jogo, como blocos, items e entidades |
| `Environment` | Onde? | Contextos espaciais, como dimensões, biomas e estruturas |
| `Recipe` | Como se faz? | Processos de produção ou transformação de items |
| `Enchantment` | Que melhoria? | Modificadores aplicáveis a items |
| `Effect` | Que estado? | Estados temporários aplicáveis a entidades |
| `MaterialTier` | Que nível? | Tiers de progressão e qualidade de materiais |

---

## Hierarquia de Classes

Resumo da hierarquia principal:

```text
owl:Thing
│
├── GameObject
│   ├── Block
│   │   ├── NaturalBlock
│   │   │   ├── Ore
│   │   │   │   ├── MetalOre
│   │   │   │   └── GemOre
│   │   │   ├── Stone
│   │   │   ├── Dirt
│   │   │   ├── Sand
│   │   │   └── Terrain
│   │   ├── Plant
│   │   │   ├── Log
│   │   │   ├── Leaves
│   │   │   ├── Sapling
│   │   │   ├── Flower
│   │   │   ├── Crop
│   │   │   └── Fungus
│   │   ├── CraftedBlock
│   │   │   ├── Planks
│   │   │   ├── Slab
│   │   │   ├── Stairs
│   │   │   ├── Wall
│   │   │   ├── Fence
│   │   │   ├── Door
│   │   │   ├── Bed
│   │   │   ├── Sign
│   │   │   ├── Wool
│   │   │   └── GlassBlock
│   │   ├── FunctionalBlock
│   │   │   ├── Furnace
│   │   │   ├── CraftingStation
│   │   │   ├── BrewingStand
│   │   │   ├── EnchantingTable
│   │   │   ├── Beacon
│   │   │   ├── Anvil
│   │   │   └── StorageBlock
│   │   ├── LightSource
│   │   ├── FluidBlock
│   │   ├── GravityBlock
│   │   ├── RedstoneBlock
│   │   ├── LightEmittingBlock
│   │   ├── TransparentBlock
│   │   └── IndestructibleBlock
│   │
│   ├── Item
│   │   ├── Tool
│   │   │   ├── Pickaxe
│   │   │   ├── Axe
│   │   │   ├── Shovel
│   │   │   ├── Hoe
│   │   │   ├── Shears
│   │   │   ├── FishingRod
│   │   │   ├── FlintAndSteel
│   │   │   └── SpecialTool
│   │   ├── Weapon
│   │   │   ├── Sword
│   │   │   ├── Bow
│   │   │   ├── Crossbow
│   │   │   ├── Trident
│   │   │   ├── Mace
│   │   │   └── Shield
│   │   ├── Armor
│   │   │   ├── Helmet
│   │   │   ├── Chestplate
│   │   │   ├── Leggings
│   │   │   ├── Boots
│   │   │   ├── Elytra
│   │   │   └── WolfArmor
│   │   ├── Food
│   │   │   ├── RawFood
│   │   │   ├── CookedFood
│   │   │   └── SpecialFood
│   │   ├── Material
│   │   │   ├── Ingot
│   │   │   ├── Gem
│   │   │   ├── RawMineral
│   │   │   ├── Nugget
│   │   │   └── OrganicMaterial
│   │   ├── Potion
│   │   ├── Projectile
│   │   ├── Bucket
│   │   ├── Container
│   │   ├── Vehicle
│   │   │   ├── Boat
│   │   │   └── Minecart
│   │   ├── MobEquipment
│   │   ├── Decoration
│   │   ├── SpawnEgg
│   │   ├── MusicDisc
│   │   ├── Dye
│   │   ├── Book
│   │   ├── SmithingTemplate
│   │   ├── UtilityItem
│   │   ├── StackableItem
│   │   └── NonStackableItem
│   │
│   ├── Entity
│   │   ├── Mob
│   │   │   ├── HostileMob
│   │   │   │   ├── UndeadMob
│   │   │   │   ├── ArthropodMob
│   │   │   │   └── NetherMob
│   │   │   ├── PassiveMob
│   │   │   │   ├── Animal
│   │   │   │   └── Villager
│   │   │   ├── NeutralMob
│   │   │   ├── TameableMob
│   │   │   ├── BossMob
│   │   │   └── AmbientMob
│   │   └── ProjectileEntity
│   │
│   ├── PlaceableBlock
│   ├── RenewableResource
│   └── NonRenewableResource
│
├── Environment
│   ├── Dimension
│   ├── Biome
│   │   ├── OverworldBiome
│   │   ├── NetherBiome
│   │   └── EndBiome
│   └── Structure
│       ├── NaturalStructure
│       └── DimensionalStructure
│
├── Recipe
│   ├── CraftingRecipe
│   │   ├── ShapedRecipe
│   │   └── ShapelessRecipe
│   ├── SmeltingRecipe
│   ├── BrewingRecipe
│   └── SmithingRecipe
│
├── Enchantment
│   ├── WeaponEnchantment
│   ├── ArmorEnchantment
│   ├── ToolEnchantment
│   ├── BowEnchantment
│   ├── CrossbowEnchantment
│   ├── TridentEnchantment
│   ├── MaceEnchantment
│   └── CurseEnchantment
│
├── Effect
│   ├── BeneficialEffect
│   └── HarmfulEffect
│
└── MaterialTier
```

---

## Decisões de Modelação

### Dualidade entre `Block` e `Item`

Em Minecraft, muitos recursos existem simultaneamente como bloco no mundo e como item no inventário. Por exemplo, `stone`, `oak_planks` ou `diamond_ore` podem ser tratados como recursos do jogo e, em alguns casos, como objetos manipuláveis.

Por isso, `Block` e `Item` não foram modeladas como classes disjuntas. A ontologia permite multi-classificação, ou seja, o mesmo indivíduo pode pertencer simultaneamente a mais do que uma classe.

A classe `PlaceableBlock` representa esta interseção:

```text
PlaceableBlock ≡ Block ⊓ Item
```

### Encantamentos

As subclasses de `Enchantment` não são necessariamente disjuntas, porque há encantamentos que se aplicam a vários tipos de item. Por exemplo, `unbreaking` e `mending` aplicam-se a vários equipamentos.

A aplicabilidade é representada através das propriedades:

```text
applicableTo
canBeEnchantedWith
```

### Receitas

As receitas são modeladas como indivíduos da classe `Recipe`, com subclasses para receitas shaped e shapeless.

As relações principais são:

```text
produces
craftedBy
hasIngredient
usedIn
hasSlot
slotItem
slotRow
slotColumn
outputQuantity
```

A representação com `RecipeSlot` permite preservar a estrutura de receitas shaped e calcular quantidades de ingredientes.

### Material tiers

Os tiers de material são representados como indivíduos da classe `MaterialTier`.

Exemplos:

```text
Wood
Stone
Copper
Iron
Gold
Diamond
Netherite
Leather
Chainmail
Turtle
```

A propriedade `tierOrder` permite ordenar os tiers e responder a perguntas sobre progressão de jogo.

---

## Object Properties

A ontologia define relações entre indivíduos, incluindo:

| Property | Domínio → Alcance | Descrição |
|---|---|---|
| `obtainedFrom` | `Item → GameObject` | Origem genérica de um item |
| `droppedBy` | `Item → Mob` | Mob que pode dropar o item |
| `drops` | `Mob → Item` | Items que um mob pode dropar |
| `minedFrom` | `Item → Block` | Bloco de onde um item pode ser obtido |
| `minedDrops` | `Block → Item` | Item obtido ao minerar um bloco |
| `minedWith` | `Block → Tool` | Ferramenta que pode minerar um bloco |
| `canMine` | `Tool → Block` | Blocos que uma ferramenta pode minerar |
| `requiresMinTier` | `Block → MaterialTier` | Tier mínimo necessário para minerar um bloco |
| `madeOfMaterial` | `Item → MaterialTier` | Tier ou material principal de um item |
| `spawnsIn` | `Mob → Biome` | Biomas onde um mob pode aparecer |
| `hasSpawn` | `Biome → Mob` | Mobs que aparecem num bioma |
| `locatedIn` | `GameObject → Environment` | Localização de um recurso |
| `contains` | `Environment → GameObject` | Relação inversa de localização |
| `generatesIn` | `Structure → Biome` | Biomas onde uma estrutura gera |
| `hasStructure` | `Biome → Structure` | Estruturas existentes num bioma |
| `applicableTo` | `Enchantment → Item` | Items aos quais um encantamento se aplica |
| `canBeEnchantedWith` | `Item → Enchantment` | Encantamentos aplicáveis a um item |
| `incompatibleWith` | `Enchantment → Enchantment` | Encantamentos incompatíveis |
| `hasIngredient` | `Recipe → Item` | Ingrediente usado numa receita |
| `usedIn` | `Item → Recipe` | Receitas onde um item é usado |
| `produces` | `Recipe → Item` | Item produzido por uma receita |
| `craftedBy` | `Item → Recipe` | Receita que produz o item |
| `requiredToEnter` | `Dimension → Item` | Items necessários para aceder a uma dimensão |
| `opensAccess` | `Item → Dimension` | Dimensão acessível através de um item |
| `hasSlot` | `Recipe → RecipeSlot` | Slots associados a uma receita |
| `slotItem` | `RecipeSlot → Item` | Item colocado num slot de crafting |

Algumas destas propriedades têm inversas declaradas em OWL, permitindo navegação nos dois sentidos.

---

## Data Properties

A ontologia define atributos literais para vários tipos de indivíduos.

### Propriedades gerais

```text
hasName
hasDisplayName
blockID
itemID
entityID
biomeID
effectID
enchantmentID
stackSize
isRenewable
```

A propriedade genérica `hasID` foi substituída, na geração de dados, por propriedades específicas como `blockID`, `itemID`, `entityID`, `biomeID`, `effectID` e `enchantmentID`. Isto evita ambiguidades em recursos que existem simultaneamente como bloco e item, como `diamond_ore`.

### Blocos

```text
hardness
blastResistance
isTransparent
emitLight
filterLight
isDiggable
affectedByGravity
```

### Items e equipamentos

```text
maxDurability
attackDamage
attackSpeed
armorPoints
armorToughness
knockbackResistance
```

### Food

```text
foodPoints
saturation
effectiveQuality
saturationRatio
```

### Entidades e mobs

```text
health
mobAttackDamage
experienceDrop
entityWidth
entityHeight
isBurnableInSunlight
isImmuneToFire
```

### Encantamentos

```text
maxLevel
enchantmentWeight
isTreasureOnly
isCurse
isTradeable
isDiscoverable
```

### Biomas

```text
temperature
hasPrecipitation
biomeCategory
```

### Receitas e slots

```text
outputQuantity
slotRow
slotColumn
```

### Material tiers

```text
tierOrder
```

Nem todas as data properties são funcionais. As propriedades que representam um único valor por indivíduo, como `blockID`, `itemID`, `entityID`, `stackSize`, `hardness` ou `maxLevel`, podem ser funcionais. Outras propriedades não são funcionais quando representam informação repetível ou estrutural.

---

## Classes Definidas

A ontologia inclui classes que podem ser inferidas pelo reasoner:

| Classe | Definição conceptual | Descrição |
|---|---|---|
| `PlaceableBlock` | `Block ⊓ Item` | Recursos que podem existir como bloco e item |
| `LightEmittingBlock` | `Block` com `emitLight > 0` | Blocos que emitem luz |
| `TransparentBlock` | `Block` com `isTransparent = true` | Blocos transparentes |
| `IndestructibleBlock` | `Block` com `hardness = -1.0` | Blocos indestrutíveis |
| `StackableItem` | `Item` com `stackSize > 1` | Items empilháveis |
| `NonStackableItem` | `Item` com `stackSize = 1` | Items não empilháveis |
| `RenewableResource` | `GameObject` com `isRenewable = true` | Recursos renováveis |
| `NonRenewableResource` | `GameObject` com `isRenewable = false` | Recursos não renováveis |

---

## Disjunções

Foram definidas disjunções pontuais onde a distinção é segura no domínio.

Exemplos:

```text
HostileMob disjointWith PassiveMob
BeneficialEffect disjointWith HarmfulEffect
ShapedRecipe disjointWith ShapelessRecipe
```

Não foram impostas disjunções globais entre `Block` e `Item`, porque isso impediria a representação natural de recursos que têm dupla natureza no Minecraft.

---

## Geração da Ontologia

A ontologia final é gerada automaticamente a partir da TBox e dos dados.

Comando:

```bash
python scripts/build_ontology.py
```

Este script:

1. executa os exporters;
2. gera os ficheiros `data_*.ttl`;
3. junta `ontology/classes.ttl` com os ficheiros RDF gerados;
4. produz `ontology/minecraft.ttl`;
5. valida se o ficheiro Turtle final pode ser carregado;
6. imprime estatísticas básicas da ontologia.

Os ficheiros `scripts/ontology/data_*.ttl` são gerados automaticamente e não devem ser editados manualmente.

---

## Execução com GraphDB

Para correr o projeto:

1. Abrir o GraphDB.

2. Criar um repositório chamado:

```text
minecraft
```

3. Importar o ficheiro:

```text
ontology/minecraft.ttl
```

4. Confirmar que o endpoint SPARQL fica disponível em:

```text
http://localhost:7200/repositories/minecraft
```

5. Entrar na pasta da aplicação web:

```bash
cd webapp
```

6. Instalar dependências:

```bash
pip install -r requirements.txt
```

7. Correr a aplicação:

```bash
python app.py
```

8. Abrir no browser:

```text
http://127.0.0.1:5000
```

Sempre que `ontology/minecraft.ttl` for regenerado, deve limpar-se ou recriar-se o repositório GraphDB antes de importar novamente a ontologia, para evitar mistura entre dados antigos e dados novos.

---

## Aplicação Web

A aplicação web permite:

- visualizar a página inicial do projeto;
- listar classes da ontologia;
- consultar indivíduos de uma classe;
- abrir a página de detalhe de um recurso;
- visualizar propriedades diretas agrupadas por propriedade;
- visualizar relações inversas agrupadas por propriedade;
- executar queries de competência;
- criar novos recursos na ABox;
- adicionar conhecimento através de formulários guiados;
- inserir triples genéricas com validação de tipo, domínio e range quando possível.

Rotas principais:

```text
/
 /ontology/classes
 /ontology/classes/<class_name>
 /ontology/resource/<resource_name>
 /competency/
 /admin/add-resource
 /admin/add-knowledge
 /admin/add-relation
```

---

## Extensão da Ontologia pela Aplicação Web

A aplicação permite aumentar a ontologia ao nível da ABox, mantendo a TBox controlada nos ficheiros Turtle.

Existem três modos de extensão.

### Adicionar Recurso

A página **Adicionar Recurso** permite criar novos indivíduos na ontologia, indicando:

- nome local;
- classe OWL;
- nome legível;
- descrição opcional.

Exemplo:

```text
test_mob rdf:type HostileMob
test_mob rdfs:label "Test Mob"
test_mob rdfs:comment "Mob criado pela app"
```

Depois de criado, o recurso pode ser consultado em:

```text
/ontology/resource/test_mob
```

E passa a aparecer nas páginas das classes compatíveis, por exemplo:

```text
/ontology/classes/HostileMob
```

### Adicionar Conhecimento

A página **Adicionar Conhecimento** permite inserir padrões frequentes de conhecimento através de formulários guiados.

Exemplos de conhecimento suportado:

- drop de mob;
- spawn de mob em bioma;
- estrutura em bioma;
- item necessário para aceder a dimensão;
- tier mínimo para minerar bloco;
- bloco afetado pela gravidade;
- mob imune ao fogo;
- mob que arde à luz do sol.

Exemplo:

```text
test_mob drops gunpowder
gunpowder droppedBy test_mob
```

Neste modo, a aplicação cria automaticamente as relações inversas necessárias e valida os tipos esperados dos recursos.

### Adicionar Relação

A página **Adicionar Relação** permite inserir triples genéricas no repositório GraphDB.

Exemplos válidos:

```text
creeper spawnsIn plains
sand affectedByGravity true
diamond_ore requiresMinTier Iron
```

A aplicação valida:

- nomes locais;
- existência do predicado;
- se o predicado é `ObjectProperty` ou `DatatypeProperty`;
- se o objeto deve ser recurso ou literal;
- o tipo do literal;
- domínio e range quando essa informação existe na TBox.

Exemplo de triple rejeitada:

```text
creeper spawnsIn gunpowder
```

Esta triple é rejeitada porque `spawnsIn` espera um recurso da classe `Biome`, e `gunpowder` é um `Item`.

As alterações feitas pela aplicação são inseridas diretamente no repositório GraphDB em tempo de execução. Para as tornar permanentes no ficheiro base da ontologia, devem ser exportadas do GraphDB ou adicionadas aos ficheiros em `data/manual/` e regeneradas com `python scripts/build_ontology.py`.

---

## Estrutura do Projeto

```text
Projeto2026/
├── README.md
├── data/
│   ├── 1.21.11/
│   │   ├── blocks.json
│   │   ├── items.json
│   │   ├── entities.json
│   │   ├── biomes.json
│   │   ├── foods.json
│   │   ├── enchantments.json
│   │   ├── recipes.json
│   │   └── effects.json
│   └── manual/
│       ├── material_tiers.json
│       ├── block_mining.json
│       ├── mob_drops.json
│       ├── mob_spawns.json
│       ├── dimensions.json
│       ├── structures.json
│       ├── portals.json
│       ├── mob_properties.json
│       └── block_properties.json
├── ontology/
│   ├── classes.ttl
│   └── minecraft.ttl
├── scripts/
│   ├── build_ontology.py
│   ├── explore.py
│   ├── explore_values.py
│   ├── classify_items.py
│   ├── exporter/
│   │   ├── common.py
│   │   ├── classifiers.py
│   │   ├── run_all.py
│   │   ├── item_exporter.py
│   │   ├── blocks_exporter.py
│   │   ├── entities_exporter.py
│   │   ├── biomes_exporter.py
│   │   ├── foods_exporter.py
│   │   ├── enchantments_exporter.py
│   │   ├── effects_exporter.py
│   │   ├── recipies_exporter.py
│   │   └── manual_exporter.py
│   └── ontology/
│       ├── data_items.ttl
│       ├── data_blocks.ttl
│       ├── data_entities.ttl
│       ├── data_biomes.ttl
│       ├── data_foods.ttl
│       ├── data_enchantments.ttl
│       ├── data_effects.ttl
│       ├── data_recipes.ttl
│       └── data_manual.ttl
└── webapp/
    ├── app.py
    ├── config.py
    ├── requirements.txt
    ├── routes/
    │   ├── admin.py
    │   ├── competency.py
    │   ├── main.py
    │   └── ontology.py
    ├── services/
    │   ├── graphdb_client.py
    │   ├── queries.py
    │   └── validation.py
    ├── static/
    └── templates/
        ├── add_resource.html
        ├── add_knowledge.html
        ├── add_relation.html
        ├── competency.html
        └── resource_detail.html
```

---

## Exemplos de Demonstração

Exemplos úteis para testar na aplicação:

| Query | Input |
|---|---|
| Ingredientes de receita | `torch` |
| Mobs que dropam item | `gunpowder` |
| Biomas de spawn de mob | `creeper` |
| Ferramenta para minerar bloco | `diamond_ore` |
| Items aplicáveis a encantamento | `fortune` |
| Estruturas por bioma | `desert` |
| Items necessários para dimensão | `nether` |
| Encantamentos incompatíveis | `fortune` |

Queries sem input:

| Query |
|---|
| Progressão de tiers |
| Mobs imunes ao fogo |
| Mobs que ardem à luz do sol |
| Blocos afetados pela gravidade |
| Alimentos com maior saturação |

### Extensão da ontologia pela aplicação

Exemplos úteis para demonstrar a extensão da ontologia:

| Funcionalidade | Exemplo |
|---|---|
| Adicionar Recurso | criar `test_mob` como `HostileMob` |
| Adicionar Conhecimento | `test_mob drops gunpowder` |
| Adicionar Relação válida | `test_mob spawnsIn plains` |
| Validação de erro | rejeitar `test_mob spawnsIn gunpowder` |

Após estas operações, os novos dados podem ser consultados nas páginas dos recursos envolvidos.

---

## Limitações

Alguma informação de domínio foi adicionada manualmente porque não está totalmente disponível ou normalizada no dataset PrismarineJS.

Os dados manuais cobrem um subconjunto representativo do domínio, suficiente para demonstrar as queries de competência e a extensibilidade da ontologia. A cobertura pode ser aumentada adicionando novas entradas aos ficheiros em `data/manual/` e regenerando a ontologia.

---

## Autoria

Projeto desenvolvido para RPCW 2025/2026.
