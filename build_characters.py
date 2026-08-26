#!/usr/bin/env python3
"""
build_characters.py
====================
Lê characters.py e gera characters.generated.js -- o arquivo que o
index.html carrega de verdade. Rode isso toda vez que editar characters.py:

    python build_characters.py

NÃO edite characters.generated.js na mão -- ele é sobrescrito toda vez.

O QUE ESSE SCRIPT FAZ
----------------------
O motor de batalha (dentro do index.html) espera os dados divididos em
várias estruturas (RAW, CHAR_KIT, APPEARANCE, CLASS_TYPE, FOURTH_ATTACK,
CHAR_FORMS, RANK_OVERRIDE, ART, ANIMES) alinhadas por POSIÇÃO ou por NOME
exato. Isso não mudou -- mudar o motor de batalha seria arriscado demais.

O que mudou é que você não precisa mais alinhar isso na mão: você escreve
UM objeto Character por personagem em characters.py, e este script monta
todas essas estruturas sozinho, na ordem certa, sem chance de desalinhar.

Este script também VALIDA os atributos de cada personagem antes de gerar
qualquer coisa (ver RANK_TOTALS/STAT_LIMITS abaixo) -- um personagem com
soma errada ou atributo fora do limite trava o build com um erro claro,
em vez de virar um bug silencioso dentro da batalha.
"""

import json
import sys
from characters import CHARACTERS, Attack, Character, Form

RANKS = ("D", "C", "B", "A", "S", "Z")
TARGET_TYPES = ("single", "all_frontline", "all_backline", "nearest_line_all", "mixed")

# Soma EXATA dos 5 atributos (vida, ataque, defesa física, defesa mágica,
# velocidade) que cada rank exige. Isso é checado pra todo Character -- não
# pras Forms (transformação), que não são personagens do pool/leilão/draft.
RANK_TOTALS = {"D": 450, "C": 500, "B": 550, "A": 600, "S": 650, "Z": 750}

# Faixa permitida de cada atributo, individualmente (além da soma bater
# exato com o rank).
STAT_LIMITS = {
    "hp":     (50, 300),
    "atk":    (40, 200),
    "defFis": (40, 200),
    "defMag": (40, 200),
    "vel":    (50, 150),
}



def attack_to_js(a: Attack | None):
    """Espelha exatamente o formato que a função A() do JS produzia, mais os
    campos novos de carga/alvo/transformação."""
    if a is None:
        return None
    obj = {
        "name": a.name,
        "dmgType": a.dmg_type,
        "category": "melee" if a.cooldown == 0 else "special",
        "power": a.power,
        "cooldown": a.cooldown,
        "effect": a.effects if a.effects else None,
        "effects": a.effects if a.effects else [],
        "onceOnly": bool(a.once_only),
        "precision": a.precision,
        "cost": a.cost,
        "targetType": a.target_type,
    }
    # campos raros só entram se realmente usados, pra não poluir o JSON
    extras = {
        "hits": a.hits,
        "ignoreDef": a.ignore_def,
        "crit": a.crit,
        "minDmg": a.min_dmg,
        "maxDmg": a.max_dmg,
        "onlyBelowHp": a.only_below_hp,
        "recoilPct": a.recoil_pct,
        "frontlineCount": a.frontline_count,
        "backlineCount": a.backline_count,
        "transformsInto": a.transforms_into,
    }
    for k, v in extras.items():
        if v is not None:
            obj[k] = v
    if a.scales_with_def:
        obj["scalesWithDef"] = True
    if a.ignore_frontline:
        obj["ignoreFrontline"] = True
    return obj


def form_to_js(key: str, f: Form):
    return {
        "key": key,
        "name": f.name,
        "vida": f.hp, "atk": f.atk,
        "defFis": f.def_fis, "defMag": f.def_mag, "vel": f.vel,
        "attacks": [attack_to_js(a) for a in f.attacks],
    }


def validate_stats(name: str, rank: str, stats: dict):
    """Checa os 3 requisitos do sistema de rank:
    1. cada atributo dentro do min/máx (STAT_LIMITS);
    2. a soma dos 5 bate EXATO com o orçamento do rank (RANK_TOTALS);
    Só vale pra Character -- Form (transformação) não entra no pool/leilão,
    então não tem orçamento de rank pra respeitar."""
    errs = []
    for stat, valor in stats.items():
        lo, hi = STAT_LIMITS[stat]
        if not (lo <= valor <= hi):
            errs.append(f'"{name}": {stat}={valor} fora do limite permitido ({lo}-{hi})')
    total = sum(stats.values())
    esperado = RANK_TOTALS[rank]
    if total != esperado:
        errs.append(f'"{name}" é rank {rank} (orçamento {esperado}) mas a soma dos 5 atributos deu {total} '
                     f'(diferença de {total-esperado:+d}) -- vida+atk+defFis+defMag+vel tem que bater exato')
    return errs


def validate(c: Character, seen_names: set):
    errs = []
    if not c.name or not c.name.strip():
        errs.append("personagem sem `name`")
    elif c.name in seen_names:
        errs.append(f'nome duplicado: "{c.name}" (tem que ser único, é a chave de ULTIMATES/ART/RANK_OVERRIDE/FORMS)')
    if c.style not in ("physical", "magic", "hybrid"):
        errs.append(f'"{c.name}": style inválido "{c.style}" (use physical/magic/hybrid)')
    if c.level not in ("weak", "medium", "strong"):
        errs.append(f'"{c.name}": level inválido "{c.level}" (use weak/medium/strong)')
    if c.rank not in RANKS:
        errs.append(f'"{c.name}": rank inválido "{c.rank}" (use um de {RANKS})')
    else:
        errs += validate_stats(c.name, c.rank, {"hp": c.hp, "atk": c.atk, "defFis": c.def_fis, "defMag": c.def_mag, "vel": c.vel})
    if not (2 <= len(c.attacks) <= 3):
        errs.append(f'"{c.name}": precisa ter 2 ou 3 ataques em `attacks` (tem {len(c.attacks)})')

    all_attacks = list(c.attacks)
    if c.fourth_attack:
        all_attacks.append(c.fourth_attack)
    for a in all_attacks:
        errs += validate_attack(c.name, a)
    for key, form in (c.forms or {}).items():
        if not (1 <= len(form.attacks) <= 4):
            errs.append(f'"{c.name}" forma "{key}": precisa ter de 1 a 4 ataques (tem {len(form.attacks)})')
        for a in form.attacks:
            errs += validate_attack(f'{c.name} ({key})', a)
    return errs


def validate_attack(owner_label: str, a: Attack):
    errs = []
    if a.target_type not in TARGET_TYPES:
        errs.append(f'"{owner_label}" / ataque "{a.name}": target_type inválido "{a.target_type}" (use um de {TARGET_TYPES})')
    if not (0 <= a.cost <= 5):
        errs.append(f'"{owner_label}" / ataque "{a.name}": cost {a.cost} fora do intervalo 0-5')
    if a.target_type == "mixed" and not (a.frontline_count or a.backline_count):
        errs.append(f'"{owner_label}" / ataque "{a.name}": target_type="mixed" precisa de frontline_count e/ou backline_count')
    return errs


def build():
    if not CHARACTERS:
        print("Aviso: CHARACTERS está vazia em characters.py -- gerando um jogo sem nenhum personagem.")

    raw = {}          # anime -> [[name, level, style], ...]
    char_kit = []      # flat, mesma ordem de raw
    appearance = []
    class_type = []
    fourth_attack = []
    rank_override = {}
    forms = {}         # nome do personagem -> {chave_da_forma: form_js}
    art = {}
    animes_order = []

    seen_names = set()
    all_errors = []

    for c in CHARACTERS:
        all_errors += validate(c, seen_names)
        seen_names.add(c.name)

        if c.anime not in raw:
            raw[c.anime] = []
            animes_order.append(c.anime)
        raw[c.anime].append([c.name, c.level, c.style])

        char_kit.append({
            "vida": c.hp, "atk": c.atk,
            "defFis": c.def_fis, "defMag": c.def_mag, "vel": c.vel,
            "attacks": [attack_to_js(a) for a in c.attacks],
        })
        appearance.append(c.appearance if c.appearance else None)
        class_type.append([c.class_, c.element])
        fourth_attack.append(attack_to_js(c.fourth_attack))

        if c.rank != "D":
            rank_override[c.name] = c.rank
        if c.forms:
            forms[c.name] = {key: form_to_js(key, f) for key, f in c.forms.items()}
        if c.sprite is not None:
            art[c.name] = {"slug": c.sprite["slug"], "states": c.sprite["states"], "facing": c.sprite.get("facing", "right")}

    if all_errors:
        print(f"\n❌ {len(all_errors)} problema(s) em characters.py -- nada foi gerado:\n")
        for e in all_errors:
            print("  -", e)
        print()
        sys.exit(1)

    def js_const(name, value):
        return f"const {name} = {json.dumps(value, ensure_ascii=False, indent=2)};"

    parts = [
        "// ARQUIVO GERADO AUTOMATICAMENTE por build_characters.py -- não edite na mão.",
        "// Fonte: characters.py. Pra mudar personagens, edite lá e rode o script de novo.",
        "",
        js_const("ANIMES", animes_order),
        js_const("RAW", raw),
        js_const("CHAR_KIT", char_kit),
        js_const("APPEARANCE", appearance),
        js_const("CLASS_TYPE", class_type),
        js_const("FOURTH_ATTACK", fourth_attack),
        js_const("RANK_OVERRIDE", rank_override),
        js_const("CHAR_FORMS", forms),
        js_const("ART", art),
        "",
    ]

    with open("characters.generated.js", "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    print(f"✅ characters.generated.js gerado com {len(CHARACTERS)} personagem(ns), "
          f"{len(animes_order)} anime(s), {len(forms)} personagem(ns) com transformação.")


if __name__ == "__main__":
    build()
