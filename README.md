# Ontologia Minecraft — Java Edition 1.21.11

Projeto desenvolvido no âmbito da unidade curricular de **Representação e Processamento de Conhecimento na Web (RPCW)** da Universidade do Minho, 2025/2026.

## Objetivo

Especificação de uma ontologia para o domínio do Minecraft Java Edition 1.21.11, cobrindo mecânicas de sobrevivência: blocos, items, mobs, biomas, dimensões, estruturas, crafting, encantamentos, efeitos e progressão de jogo. A ontologia é explorável e extensível através de uma aplicação web.

## Stack Tecnológica

- **Protégé** — modelação da TBox (classes, propriedades, restrições)
- **Python + rdflib** — geração da ABox a partir dos dados do PrismarineJS
- **GraphDB** — triplestore com endpoint SPARQL

## Fonte de Dados

- **PrismarineJS/minecraft-data** (versão 1.21.11) — fonte primária para blocos, items, entidades, biomas, foods, enchantments, recipes e effects
- **Dados manuais** — spawns mob↔bioma, drops de mobs, damage de armas/armaduras, dimensões e estruturas

## Perguntas de Competência

A ontologia foi desenhada para responder a estas perguntas via SPARQL:

1. Que materiais preciso para craftar o item X?
2. Que mobs dropam o item Y?
3. Em que biomas spawna o mob Z?
4. Que ferramenta mínima é necessária para minerar o bloco W?
5. Que items posso encantar com Fortune? E com Sharpness?
6. Que estruturas geram em cada bioma?
7. Qual o caminho de progressão Wood → Stone → Iron → Diamond → Netherite?
8. Que mobs são imunes a fogo? Que mobs ardem à luz do sol?
9. Que items são necessários para abrir um portal para a Nether/End?
10. Que blocos são afetados pela gravidade?
11. Que food items dão mais saturation?
12. Que encantamentos são incompatíveis entre si?

---

## Estrutura da Ontologia (TBox)

### Classes de Topo

A ontologia tem 6 classes de topo, conceptualmente ortogonais:

| Classe | Responde a... | Descrição |
|--------|---------------|-----------|
| `GameObject` | "O quê?" | Objetos tangíveis do jogo (blocos, items, entidades) |
| `Environment` | "Onde?" | Localizações e contextos (dimensões, biomas, estruturas) |
| `Recipe` | "Como se faz?" | Processos de produção |
| `Enchantment` | "Que melhoria?" | Modificadores aplicáveis a items |
| `Effect` | "Que estado?" | Estados temporários de entidades |
| `MaterialTier` | "De que qualidade?" | Enumeração fechada de tiers de material |

### Hierarquia Completa de Classes

```
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
│   │   ├── LightEmittingBlock       [≡ Block ⊓ emitLight > 0]
│   │   ├── TransparentBlock          [≡ Block ⊓ isTransparent = true]
│   │   └── IndestructibleBlock       [≡ Block ⊓ hardness = -1.0]
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
│   │   ├── StackableItem             [≡ Item ⊓ stackSize > 1]
│   │   └── NonStackableItem          [≡ Item ⊓ stackSize = 1]
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
│   ├── PlaceableBlock                [≡ Block ⊓ Item]
│   ├── RenewableResource             [≡ GameObject ⊓ isRenewable = true]
│   └── NonRenewableResource          [≡ GameObject ⊓ isRenewable = false]
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
└── MaterialTier                      [enumeração: Wood, Stone, Copper, Iron,
                                       Gold, Diamond, Netherite, Leather,
                                       Chainmail, Turtle]
```

### Decisões de Modelação Relevantes

#### Dualidade Block↔Item (Opção C — Multi-classificação)

Em Minecraft, muitos objetos existem simultaneamente como bloco no mundo e como item no inventário (ex: `stone`, `oak_planks`). Em vez de duplicar indivíduos ou forçar disjunção, usamos multi-classificação:

- Um indivíduo `:Stone` pode ser `a :Block` **e** `a :Item` ao mesmo tempo
- `Block` e `Item` **não** são declaradas como disjuntas
- A classe definida `PlaceableBlock ≡ Block ⊓ Item` é inferida automaticamente pelo reasoner
- Isto resulta em ~1013 indivíduos com dupla classificação, ~492 items puros e ~153 blocos não-coletáveis

#### Enchantments — sem disjunção entre subclasses

As subclasses de `Enchantment` (WeaponEnchantment, ArmorEnchantment, etc.) **não** são mutuamente disjuntas porque encantamentos como `Unbreaking` e `Mending` aplicam-se a múltiplos tipos de item simultaneamente. A classificação é feita pela relação `applicableTo`.

#### Proveniência de items — relação, não subclasse

A origem de um item (animal, mineral, mob drop) é modelada pela hierarquia de object properties `obtainedFrom` e não por subclasses tipo "AnimalDerivedItem", evitando classificações transversais artificiais.

---

## Object Properties (38 total)

### Hierarquia de obtenção

```
obtainedFrom : Item → GameObject
├── droppedBy    : Item → Mob          [inversa: drops]
├── minedFrom    : Item → Block        [inversa: minedDrops]
├── shearedFrom  : Item → GameObject
├── milkableFrom : Item → Mob
├── craftedBy    : Item → Recipe       [inversa: produces]
└── smeltedFrom  : Item → Item         [inversa: smeltsInto]
```

### Ferramentas e materiais

| Property | Domain → Range | Características |
|----------|---------------|-----------------|
| `minedWith` | Block → Tool | inversa: `canMine` |
| `requiresMinTier` | Block → MaterialTier | Functional |
| `madeOfMaterial` | Item → MaterialTier | Functional |

### Localização e spawn

| Property | Domain → Range | Características |
|----------|---------------|-----------------|
| `spawnsIn` | Mob → Biome | inversa: `hasSpawn` |
| `locatedIn` | GameObject → Environment | **Transitive**, inversa: `contains` |
| `generatesIn` | Structure → Biome | inversa: `hasStructure` |
| `foundIn` | GameObject → Environment | — |

### Encantamentos

| Property | Domain → Range | Características |
|----------|---------------|-----------------|
| `applicableTo` | Enchantment → Item | inversa: `canBeEnchantedWith` |
| `incompatibleWith` | Enchantment → Enchantment | **Symmetric** |

### Receitas

| Property | Domain → Range | Características |
|----------|---------------|-----------------|
| `hasIngredient` | Recipe → Item | inversa: `usedIn` |
| `produces` | Recipe → Item | **Functional** |

### Outras relações

| Property | Domain → Range |
|----------|---------------|
| `weakAgainst` | Mob → Item |
| `immuneTo` | Mob → Effect |
| `tamedWith` | TameableMob → Item |
| `breedsWith` | PassiveMob → Item |
| `ridesOn` | Entity → Vehicle |
| `hasEffect` | Item → Effect |
| `usesFuel` / `canBurnIn` | FunctionalBlock ↔ Item |
| `requiredToEnter` / `opensAccess` | Dimension ↔ Item |
| `storedIn` / `containsItem` | Item ↔ Container |

---

## Data Properties (40 total)

### Comuns a GameObjects

`hasName` (string), `hasDisplayName` (string), `hasID` (integer), `stackSize` (integer), `isRenewable` (boolean)

### Blocos

`hardness` (float), `blastResistance` (float), `isTransparent` (boolean), `emitLight` (integer 0-15), `filterLight` (integer 0-15), `isDiggable` (boolean), `affectedByGravity` (boolean)

### Items com durabilidade

`maxDurability` (integer), `attackDamage` (float), `attackSpeed` (float), `armorPoints` (integer), `armorToughness` (float), `knockbackResistance` (float)

### Food

`foodPoints` (float), `saturation` (float), `effectiveQuality` (float), `saturationRatio` (float)

### Mobs

`health` (float), `mobAttackDamage` (float), `experienceDrop` (integer), `entityWidth` (float), `entityHeight` (float), `isBurnableInSunlight` (boolean), `isImmuneToFire` (boolean)

### Enchantments

`maxLevel` (integer), `enchantmentWeight` (integer), `isTreasureOnly` (boolean), `isCurse` (boolean), `isTradeable` (boolean), `isDiscoverable` (boolean)

### Biomes

`temperature` (float), `hasPrecipitation` (boolean), `biomeCategory` (string)

### Effects e Recipes

`effectType` (string), `outputQuantity` (integer)

> Todas as data properties são **Functional** (cada indivíduo tem no máximo um valor).

---

## Classes Definidas (Equivalent Classes)

Classes cujos membros são inferidos automaticamente pelo reasoner:

| Classe | Definição OWL | Descrição |
|--------|---------------|-----------|
| `PlaceableBlock` | `Block ⊓ Item` | Objetos que existem como bloco e como item |
| `LightEmittingBlock` | `Block ⊓ (emitLight some integer[>0])` | Blocos que emitem luz |
| `TransparentBlock` | `Block ⊓ (isTransparent value true)` | Blocos transparentes |
| `IndestructibleBlock` | `Block ⊓ (hardness value -1.0)` | Blocos indestrutíveis (bedrock) |
| `StackableItem` | `Item ⊓ (stackSize some integer[>1])` | Items empilháveis |
| `NonStackableItem` | `Item ⊓ (stackSize value 1)` | Items não empilháveis |
| `RenewableResource` | `GameObject ⊓ (isRenewable value true)` | Recursos renováveis |
| `NonRenewableResource` | `GameObject ⊓ (isRenewable value false)` | Recursos não renováveis |

---

## Disjoint Classes

Grupos de classes mutuamente exclusivas (nenhum indivíduo pode pertencer a duas delas):

- **Topo:** GameObject, Environment, Recipe, Enchantment, Effect, MaterialTier
- **Comportamento de mobs:** HostileMob ↔ PassiveMob
- **Biomas por dimensão:** OverworldBiome, NetherBiome, EndBiome
- **Tipos de receita:** CraftingRecipe, SmeltingRecipe, BrewingRecipe, SmithingRecipe
- **Shaped vs Shapeless:** ShapedRecipe ↔ ShapelessRecipe
- **Efeitos:** BeneficialEffect ↔ HarmfulEffect
- **Subclasses de Item:** Tool, Weapon, Armor, Food, Material, Potion, Projectile, Bucket, Vehicle, MobEquipment, Decoration, SpawnEgg, MusicDisc, Dye, Book, SmithingTemplate, UtilityItem, Container
- **Subclasses de Tool:** Pickaxe, Axe, Shovel, Hoe, Shears, FishingRod, FlintAndSteel, SpecialTool
- **Subclasses de Weapon:** Sword, Bow, Crossbow, Trident, Mace, Shield
- **Subclasses de Armor:** Helmet, Chestplate, Leggings, Boots, Elytra, WolfArmor
- **Subclasses de Food:** RawFood, CookedFood, SpecialFood
- **Subclasses de Material:** Ingot, Gem, RawMineral, Nugget, OrganicMaterial
- **Subclasses de Block:** NaturalBlock, CraftedBlock, FunctionalBlock, Plant, FluidBlock, GravityBlock, LightSource, RedstoneBlock
- **Subclasses de Environment:** Dimension, Biome, Structure

---

## Restrições (SubClass Of com expressões)

| Classe | Restrição | Significado |
|--------|-----------|-------------|
| `Biome` | `locatedIn some Dimension` | Todo bioma pertence a uma dimensão |
| `CraftingRecipe` | `hasIngredient max 9 Item` | Receitas de crafting têm no máximo 9 ingredientes |
| `Food` | `foodPoints some xsd:float` | Toda comida tem pontos de fome |

---

## Estrutura do Projeto

```
RPCW-Projeto/
├── data/
│   └── 1.21.11/           ← JSONs do PrismarineJS
├── scripts/
│   ├── venv/              ← ambiente Python
│   ├── explore.py         ← exploração dos dados
│   ├── explore_values.py  ← análise de valores categóricos
│   └── classify_items.py  ← validação de heurísticas de classificação
├── ontology/
│   └── minecraft.ttl ← TBox (classes, propriedades, restrições)
├── output/
│   └── ontologia com toda a info pos processamento de dados
├── webapp/                ← aplicação web (TODO)
└── README.md
```