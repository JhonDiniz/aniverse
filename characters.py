"""
characters.py
=============
TODOS os dados de personagens do jogo moram AQUI, num objeto Python por
personagem. Nada de JS pra editar, nada de listas paralelas pra manter
alinhadas na mesma posição -- isso foi removido de propósito (era uma fonte
constante de bug: mexer em CHAR_KIT sem mexer em APPEARANCE/CLASS_TYPE na
mesma posição desalinhava todo mundo depois).

COMO ADICIONAR UM PERSONAGEM
-----------------------------
Copie um dos exemplos comentados no fim do arquivo, cole dentro da lista
CHARACTERS, preencha os campos. Depois rode:

    python build_characters.py

Isso gera `characters.generated.js`, que o index.html já carrega sozinho.
Não precisa editar o HTML.

CAMPOS OBRIGATÓRIOS de Character: name, anime, style, level, hp, atk,
def_fis, def_mag, vel, attacks (uma lista com 2 a 3 objetos Attack).
Tudo o resto é opcional (tem valor padrão sensato).

SISTEMA DE RANK
----------------
Escala oficial: D < C < B < A < S < Z (D é o mais fraco, Z o mais forte).
Todo personagem tem um `rank` nesses 6 valores. Rank é só uma classificação
de força/raridade -- NÃO tem relação nenhuma com transformação (ver Form
mais abaixo). Um personagem rank D pode ter uma transformação; um rank Z
pode não ter nenhuma.

SISTEMA DE LINHAS DE BATALHA (dianteira/traseira)
---------------------------------------------------
Cada time em campo tem 3 personagens na DIANTEIRA e 2 na TRASEIRA (isso já
existia como "combate"/"suporte" -- mesma ideia, só que agora a traseira
também pode ser atacada, não só usar uma habilidade de carga própria).

Regra padrão: um ataque só pode mirar a dianteira enquanto ela tiver algum
sobrevivente. Só quando os 3 da dianteira caem é que a traseira passa a
poder ser atingida por ataques comuns.

Em Attack, isso é controlado por:
    target_type       "single" (padrão) | "all_frontline" | "all_backline"
                       | "nearest_line_all" | "mixed"
    ignore_frontline   True = esse ataque específico pode mirar a traseira
                       mesmo com a dianteira viva (ex: Rasen-Shuriken)
    frontline_count / backline_count   só usados com target_type="mixed",
                       pra ataques que acertam N da dianteira + M da traseira
                       numa tacada só (ex: Mini Bijuudama = 2 dianteira + 1 traseira)

"nearest_line_all" acerta TODOS os vivos da linha mais exposta no momento
(dianteira se ela tiver alguém vivo, senão a traseira inteira) -- é a
mecânica de "ataque em área que sempre pega quem está na frente".

SISTEMA DE CARGA
-----------------
Cada personagem em batalha tem uma carga de 0 a 5 (não é inteira -- anda de
0.75 em 0.75). Toda vez que ele ataca OU é atacado, ganha +0.75 de carga,
até o teto de 5. Ataques podem ter um `cost` (0 a 5): só podem ser usados se
a carga atual for >= cost, e ao usar, a carga é debitada nesse valor. Ataque
de cost=0 pode ser usado a qualquer momento (e ainda gera os +0.75 de carga
normalmente, como qualquer outro).

TRANSFORMAÇÃO (Form)
----------------------
Uma transformação é um Attack com `transforms_into="chave"` apontando pra um
Form dentro de Character.forms. NÃO é dano -- ao ser usado, troca os
atributos e os 4 ataques do personagem pelos da forma indicada, mantendo o
mesmo ID/vaga na equipe (não é um personagem novo, nunca aparece separado
no pool/leilão/draft/Anidex). Custuma ter cost alto (ex: 5), porque é uma
virada de jogo.

O MODELO DE EFEITOS (pra usar em Attack.effects)
--------------------------------------------------
Cada efeito é um dict com:
    kind    "stat" | "heal" | "shield" | "stun" | "dot" | "cleanse" | "dispel"
            | "revive1" | "taunt" | "confuse" | "recoil" | "absorb"
    target  "self" | "enemy" | "allies" | "team"
    stat    "atk" | "def" | "vel" | "eva" | "acc" | "all"   (só kind="stat")
    pct     modificador percentual (ex.: -20)
    flat    valor fixo (cura, escudo, dano contínuo)
    pctHp   valor como % da vida máxima (cura/escudo alternativos)
    turns   duração; sem isso, dura até ser atingido
    chance  0-100, chance de aplicar (padrão 100)

Só que você não precisa escrever esses dicts na mão -- use as funções
heal(), shield(), stun(), dot(), buff(), debuff(), confuse(), cleanse(),
dispel(), revive() lá embaixo. Elas cobrem os casos comuns; pra algo mais
exótico, passe o dict direto em `effects=[...]`.
"""

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------
# HELPERS DE EFEITO -- use dentro de Attack(effects=[...])
# ---------------------------------------------------------------------
def heal(amount, target="self"):
    return {"kind": "heal", "target": target, "flat": amount}


def shield(amount, target="self"):
    return {"kind": "shield", "target": target, "flat": amount}


def stun(chance=100, target="enemy", turns=1):
    return {"kind": "stun", "target": target, "turns": turns, "chance": chance}


def dot(amount, turns=2, target="enemy"):
    return {"kind": "dot", "target": target, "flat": amount, "turns": turns}


def buff(stat, pct, target="self", turns=3):
    """stat: 'atk' | 'def' | 'vel' | 'eva' | 'acc' | 'all'"""
    return {"kind": "stat", "target": target, "stat": stat, "pct": pct, "turns": turns}


def debuff(stat, pct, target="enemy", turns=None):
    e = {"kind": "stat", "target": target, "stat": stat, "pct": -abs(pct)}
    if turns:
        e["turns"] = turns
    return e


def confuse(turns=2, target="enemy"):
    return {"kind": "confuse", "target": target, "turns": turns}


def cleanse(target="self"):
    return {"kind": "cleanse", "target": target}


def dispel(target="enemy"):
    return {"kind": "dispel", "target": target}


def revive(turns=2, target="self"):
    return {"kind": "revive1", "target": target, "turns": turns}


def next_dodge(pct, target="self"):
    """Bônus de evasão só pro PRÓXIMO ataque recebido -- consumido depois de
    um golpe (acerte ou erre), não soma turno a turno como buff/debuff normal."""
    return {"kind": "nextDodge", "target": target, "pct": pct}


# ---------------------------------------------------------------------
# ATAQUE
# ---------------------------------------------------------------------
@dataclass
class Attack:
    name: str
    dmg_type: str          # "physical" | "magic"
    power: int = 0          # 0-160 -- dano vem do ATK do personagem × isso. 0 = só efeito, sem dano
    cooldown: int = 0       # 0 = corpo a corpo, sem espera. 2-5 = ataque especial
    effects: list = field(default_factory=list)   # veja heal()/shield()/stun()/etc acima
    once_only: bool = False   # só pode ser usado 1x na batalha inteira
    precision: int = 100      # % de acerto -- ataques fortes costumam ter menos

    # --- carga (ver seção "SISTEMA DE CARGA" no topo do arquivo) ---
    cost: float = 0          # 0 a 5 -- quanto de carga o ataque consome. 0 = sempre disponível

    # --- alvo (ver seção "SISTEMA DE LINHAS DE BATALHA" no topo do arquivo) ---
    target_type: str = "single"   # "single" | "all_frontline" | "all_backline" | "nearest_line_all" | "mixed"
    ignore_frontline: bool = False    # só importa pra "single"/"all_backline": mira a traseira mesmo com dianteira viva
    frontline_count: Optional[int] = None   # só pra target_type="mixed": quantos da dianteira
    backline_count: Optional[int] = None    # só pra target_type="mixed": quantos da traseira

    # --- transformação (troca de forma, ver classe Form) ---
    transforms_into: Optional[str] = None   # chave de um Form em Character.forms -- vira o personagem transformado

    # Campos raros -- só preencha se o personagem realmente precisar:
    hits: Optional[int] = None            # múltiplos golpes no mesmo ataque
    ignore_def: Optional[float] = None    # 0 a 1 -- fração da defesa do alvo ignorada
    crit: Optional[int] = None            # % de chance de crítico (x1.5), além do padrão do jogo
    min_dmg: Optional[int] = None         # dano fixo aleatório, ignora a fórmula normal
    max_dmg: Optional[int] = None
    only_below_hp: Optional[float] = None # só pode usar com vida abaixo dessa fração (0-1)
    scales_with_def: bool = False         # usa a DEFESA do personagem em vez do ataque
    recoil_pct: Optional[float] = None    # % da vida do próprio atacante perdida ao usar


def heal_pct_atk(pct, target="self"):
    """Cura como % do ATAQUE ATUAL do personagem (não da vida máxima) --
    recalculado no momento em que o ataque é usado, então reflete buffs e
    transformações em vigor naquela hora. Ex.: Manto Protetor do Naruto."""
    return {"kind": "healPctAtk", "target": target, "pct": pct}


# ---------------------------------------------------------------------
# FORM -- uma forma alternativa (transformação) do MESMO personagem.
# Não é um personagem selecionável: nunca aparece no pool/leilão/draft/Anidex
# por conta própria. Só existe pendurada em Character.forms, e só é alcançada
# através de um Attack com transforms_into="chave_da_forma".
# ---------------------------------------------------------------------
@dataclass
class Form:
    name: str            # nome mostrado em batalha (ex: "Manto 4 Caudas A")
    hp: int
    atk: int              # ver nota em Character.atk -- um valor só, sem físico/mágico
    def_fis: int
    def_mag: int
    vel: int
    attacks: list        # até 4 objetos Attack -- SUBSTITUEM os ataques normais enquanto transformado


# ---------------------------------------------------------------------
# PERSONAGEM
# ---------------------------------------------------------------------
@dataclass
class Character:
    name: str
    anime: str
    style: str        # "physical" | "magic" | "hybrid" -- estilo predominante
    level: str        # "weak" | "medium" | "strong" -- usado só pra exibição/agrupamento

    hp: int
    atk: int           # UM atributo só de ataque -- não existe mais divisão entre
                        # Ataque Físico/Ataque Mágico no personagem. O tipo de dano
                        # (físico/mágico) é propriedade do ATAQUE (Attack.dmg_type),
                        # não do personagem.
    def_fis: int
    def_mag: int
    vel: int

    attacks: list       # 2 a 3 objetos Attack (o "kit base" do personagem)
    fourth_attack: Optional[Attack] = None   # ataque extra opcional, desbloqueado sempre disponível

    class_: str = "Lutador"     # Guerreiro, Mago, Tanque, Assassino, Espadachim, Atirador, Estrategista, Suporte, Atleta...
    element: str = "Normal"     # Fogo, Gelo, Elétrico, Sombrio, Sagrado, Venenoso, Espiritual, Psíquico, Vento, Terra, Água, Metal, Natureza, Normal

    rank: str = "D"    # "D" | "C" | "B" | "A" | "S" | "Z" -- D é o mais fraco, Z o mais forte

    forms: dict = field(default_factory=dict)   # {"chave": Form(...)} -- transformações deste personagem

    appearance: Optional[dict] = None  # {"skin":"#...", "hairColor":"#...", "hairStyle":"...", "outfit":"#...", "outfit2":"#..."}
    sprite: Optional[dict] = None      # {"slug":"nome-da-pasta", "states":["front","back",...], "facing":"right"|"left"} -- ver COMO-ADICIONAR-ARTE.md



# =======================================================================
# ELENCO -- adicione seus personagens aqui embaixo
# =======================================================================
CHARACTERS: list[Character] = [
    Character(
        name="Son Goku",
        anime="Dragon Ball",
        style="physical",
        level="strong",
        hp=234, atk=129, def_fis=99, def_mag=74, vel=114,
        class_="Guerreiro", element="Normal",
        rank="S",
        attacks=[
            Attack("Soco Direto", "physical", power=50, cooldown=0),
            Attack("Kamehameha", "physical", power=110, cooldown=2, precision=95),
            Attack("Kaio-ken", "physical", power=0, cooldown=3, effects=[buff("atk", 25, turns=3)]),
        ],
        fourth_attack=Attack("Genki Dama", "physical", power=135, cooldown=4, precision=80),
    ),
    Character(
        name="Vegeta",
        anime="Dragon Ball",
        style="physical",
        level="strong",
        hp=231, atk=134, def_fis=104, def_mag=69, vel=112,
        class_="Guerreiro", element="Normal",
        rank="S",
        attacks=[
            Attack("Soco do Orgulho Saiyajin", "physical", power=52, cooldown=0),
            Attack("Big Bang Attack", "physical", power=115, cooldown=2, precision=93),
            Attack("Investida Furiosa", "physical", power=0, cooldown=3, effects=[buff("atk", 28, turns=3)]),
        ],
        fourth_attack=Attack("Final Flash", "physical", power=140, cooldown=4, precision=82),
    ),
    Character(
        name="Freeza",
        anime="Dragon Ball",
        style="magic",
        level="strong",
        hp=208, atk=143, def_fis=78, def_mag=118, vel=103,
        class_="Mago", element="Sombrio",
        rank="S",
        attacks=[
            Attack("Golpe com a Cauda", "physical", power=45, cooldown=0),
            Attack("Disco da Morte", "magic", power=115, cooldown=2, precision=90, effects=[dot(15, turns=2)]),
            Attack("Rajada de Energia Roxa", "magic", power=100, cooldown=2, precision=95),
        ],
        fourth_attack=Attack("Explosão Supernova", "magic", power=130, cooldown=4, precision=80,
                              effects=[debuff("def", 30)]),
    ),
    Character(
        name="Broly",
        anime="Dragon Ball",
        style="physical",
        level="strong",
        hp=269, atk=144, def_fis=109, def_mag=49, vel=79,
        class_="Tanque", element="Normal",
        rank="S",
        attacks=[
            Attack("Soco Bruto", "physical", power=58, cooldown=0),
            Attack("Investida Selvagem", "physical", power=120, cooldown=2, precision=88),
            Attack("Fúria Descontrolada", "physical", power=0, cooldown=3, effects=[buff("atk", 35, turns=3)]),
        ],
        fourth_attack=Attack("Explosão de Energia Bruta", "physical", power=145, cooldown=4, precision=78,
                              effects=[stun(chance=30)]),
    ),
    Character(
        name="Bills",
        anime="Dragon Ball",
        style="hybrid",
        level="strong",
        hp=210, atk=130, def_fis=90, def_mag=100, vel=120,
        class_="Estrategista", element="Sagrado",
        rank="S",
        attacks=[
            Attack("Tapa Divino", "physical", power=60, cooldown=0, precision=97),
            Attack("Esfera de Destruição", "magic", power=125, cooldown=2, precision=90),
            Attack("Fúria Comedida", "physical", power=0, cooldown=3, effects=[debuff("def", 35)]),
        ],
        fourth_attack=Attack("Julgamento do Destruidor", "magic", power=140, cooldown=4, precision=85),
    ),
    Character(
        name="Vegito",
        anime="Dragon Ball",
        style="hybrid",
        level="strong",
        hp=239, atk=129, def_fis=99, def_mag=79, vel=104,
        class_="Guerreiro", element="Sagrado",
        rank="S",
        attacks=[
            Attack("Soco Fusionado", "physical", power=56, cooldown=0),
            Attack("Final Kamehameha", "physical", power=125, cooldown=2, precision=92),
            Attack("Provocação Confiante", "physical", power=0, cooldown=3, effects=[debuff("atk", 30)]),
        ],
        fourth_attack=Attack("Big Bang Kamehameha", "magic", power=145, cooldown=4, precision=83),
    ),
    Character(
        name="Monkey D. Luffy",
        anime="One Piece",
        style="physical",
        level="strong",
        hp=235, atk=140, def_fis=105, def_mag=60, vel=110,
        class_="Lutador", element="Normal",
        rank="S",
        attacks=[
            Attack("Soco de Borracha", "physical", power=52, cooldown=0),
            Attack("Gomu Gomu no Pistol", "physical", power=110, cooldown=2, precision=95),
            Attack("Gear Second: Rajada", "physical", power=0, cooldown=3, effects=[buff("vel", 30, turns=3)]),
        ],
        fourth_attack=Attack("Gomu Gomu no Elephant Gun", "physical", power=135, cooldown=4, precision=85),
    ),
    Character(
        name="Roronoa Zoro",
        anime="One Piece",
        style="physical",
        level="strong",
        hp=229, atk=149, def_fis=114, def_mag=54, vel=104,
        class_="Espadachim", element="Normal",
        rank="S",
        attacks=[
            Attack("Corte Rápido", "physical", power=54, cooldown=0),
            Attack("Oni Giri", "physical", power=115, cooldown=2, precision=93),
            Attack("Concentração: Ashura", "physical", power=0, cooldown=3, effects=[buff("atk", 30, turns=3)]),
        ],
        fourth_attack=Attack("Santoryu: Rashomon", "physical", power=140, cooldown=4, precision=82),
    ),
    Character(
        name="Trafalgar Law",
        anime="One Piece",
        style="magic",
        level="strong",
        hp=214, atk=139, def_fis=84, def_mag=114, vel=99,
        class_="Mago", element="Espiritual",
        rank="S",
        attacks=[
            Attack("Corte com Nodachi", "physical", power=48, cooldown=0),
            Attack("ROOM: Shambles", "magic", power=100, cooldown=2, precision=92, effects=[debuff("def", 30)]),
            Attack("Counter Shock", "magic", power=0, cooldown=3, effects=[stun(chance=45)]),
        ],
        fourth_attack=Attack("Gamma Knife", "magic", power=125, cooldown=4, precision=85, effects=[dot(18, turns=2)]),
    ),
    Character(
        name="Tony Tony Chopper",
        anime="One Piece",
        style="hybrid",
        level="medium",
        hp=211, atk=111, def_fis=101, def_mag=111, vel=116,
        class_="Suporte", element="Natureza",
        rank="S",
        attacks=[
            Attack("Chute de Rena", "physical", power=35, cooldown=0),
            Attack("Rumble Ball: Guard Point", "physical", power=0, cooldown=3, effects=[shield(55)]),
            Attack("Kung-Fu Point: Investida", "physical", power=70, cooldown=2),
        ],
        fourth_attack=Attack("Cura de Emergência", "magic", power=0, cooldown=3, effects=[heal(60)]),
    ),
    Character(
        name="Barba Branca",
        anime="One Piece",
        style="physical",
        level="strong",
        hp=272, atk=142, def_fis=112, def_mag=72, vel=52,
        class_="Tanque", element="Terra",
        rank="S",
        attacks=[
            Attack("Soco Pesado", "physical", power=58, cooldown=0),
            Attack("Gura Gura no Mi: Onda de Choque", "physical", power=125, cooldown=2, precision=88,
                   effects=[debuff("def", 35)]),
            Attack("Presença Intimidadora", "physical", power=0, cooldown=3, effects=[stun(chance=25)]),
        ],
        fourth_attack=Attack("Terremoto Absoluto", "physical", power=150, cooldown=5, precision=75,
                              effects=[dot(20, turns=2)]),
    ),
    Character(
        name="Barba Negra",
        anime="One Piece",
        style="hybrid",
        level="strong",
        hp=247, atk=127, def_fis=97, def_mag=102, vel=77,
        class_="Mago", element="Sombrio",
        rank="S",
        attacks=[
            Attack("Soco das Trevas", "physical", power=50, cooldown=0),
            Attack("Yami Yami no Mi: Black Hole", "magic", power=110, cooldown=2, precision=90,
                   effects=[debuff("def", 35)]),
            Attack("Onda de Choque Sombria", "magic", power=0, cooldown=3, effects=[stun(chance=35)]),
        ],
        fourth_attack=Attack("Trevas Absolutas", "magic", power=135, cooldown=4, precision=82,
                              effects=[dot(18, turns=2)]),
    ),
    Character(
        name="Naruto Shippuden B",
        anime="Naruto",
        style="hybrid",
        level="strong",
        hp=150, atk=125, def_fis=95, def_mag=90, vel=90,
        class_="Guerreiro", element="Vento",
        rank="B",
        attacks=[
            Attack("Clone das Sombras", "physical", power=40, cooldown=0, precision=95, cost=0,
                   effects=[next_dodge(10)]),
            Attack("Rasengan", "magic", power=60, cooldown=0, precision=85, cost=2,
                   effects=[stun(chance=20, turns=1)]),
            Attack("Rasen-Shuriken", "magic", power=70, cooldown=0, precision=75, cost=3,
                   ignore_frontline=True),
        ],
        fourth_attack=Attack("Transformação — Manto 4 Caudas", "physical", power=0, cooldown=0,
                              precision=100, cost=5, transforms_into="manto_4_caudas"),
        forms={
            "manto_4_caudas": Form(
                name="Manto 4 Caudas A",
                hp=170, atk=150, def_fis=90, def_mag=90, vel=100,
                attacks=[
                    Attack("Força Bruta", "physical", power=45, cooldown=0, precision=95, cost=0),
                    Attack("Manto Protetor", "physical", power=0, cooldown=0, precision=100, cost=2,
                           effects=[heal_pct_atk(30)]),
                    Attack("Onda de Choque", "magic", power=70, cooldown=0, precision=70, cost=3,
                           target_type="nearest_line_all"),
                    Attack("Mini Bijuudama", "magic", power=110, cooldown=0, precision=60, cost=5,
                           target_type="mixed", frontline_count=2, backline_count=1),
                ],
            ),
        },
        # Arte real (não procedural): uma pose por estado, espelhada
        # automaticamente pelo jogo quando ele está no campo inimigo.
        sprite=dict(slug="naruto", states=["base", "dash", "block"], facing="left"),
    ),
]


# ---------------------------------------------------------------------
# EXEMPLOS (copie, cole dentro de CHARACTERS, edite os valores)
# ---------------------------------------------------------------------
_EXEMPLO_SIMPLES = Character(
    name="Fulano de Tal",
    anime="Meu Anime",
    style="physical",
    level="medium",
    hp=150, atk=90, def_fis=80, def_mag=70, vel=60,  # soma = 450 = orçamento exato do rank D
    class_="Lutador", element="Normal",
    attacks=[
        Attack("Soco Básico", "physical", power=35, cooldown=0),
        Attack("Golpe Especial", "physical", power=80, cooldown=2),
        Attack("Grito de Guerra", "physical", power=0, cooldown=3, effects=[buff("atk", 25)]),
    ],
)

_EXEMPLO_COM_QUARTO_ATAQUE_E_ULTIMATE = Character(
    name="Fulana Poderosa",
    anime="Meu Anime",
    style="hybrid",
    level="strong",
    hp=200, atk=150, def_fis=100, def_mag=80, vel=120,
    class_="Guerreiro", element="Fogo",
    rank="S",   # D/C/B/A/S/Z -- rank não tem relação com transformação (isso é Form)
    attacks=[
        Attack("Corte Rápido", "physical", power=55, cooldown=0),
        Attack("Explosão Flamejante", "magic", power=120, cooldown=3, precision=90,
               effects=[dot(20, turns=2)]),
        Attack("Fúria Interior", "physical", power=0, cooldown=3, effects=[buff("atk", 30)]),
    ],
    fourth_attack=Attack("Transformação — Despertar Supremo", "physical", power=0, cooldown=0,
                          cost=5, transforms_into="despertar_supremo"),
    forms={
        "despertar_supremo": Form(
            name="Fulana Poderosa (Despertar Supremo)",
            hp=350, atk=210, def_fis=110, def_mag=100, vel=160,
            attacks=[
                Attack("Golpe Ardente", "physical", power=90, cooldown=0),
                Attack("Chama Total", "magic", power=130, cooldown=0, precision=85, cost=3),
                Attack("Fúria Absoluta", "physical", power=150, cooldown=0, precision=75, cost=5),
            ],
        ),
    },
    # sprite=dict(slug="fulana-poderosa", states=["front","back"]),  # opcional, ver COMO-ADICIONAR-ARTE.md
)
