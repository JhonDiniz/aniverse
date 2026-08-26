#!/usr/bin/env python3
"""
slice_poses.py
==============
Corta uma folha de sprites com N poses lado a lado (base / dash / bloqueio,
ou qualquer outra combinação) em arquivos PNG separados, um por pose --
SEM precisar de coordenadas fixas de corte.

Por quê: coordenadas fixas quebram toda vez que alguém reorganiza ou
reespaça a imagem original (foi exatamente o que aconteceu com o dash do
Naruto). Em vez disso, este script:

  1. Acha quais colunas da imagem são "vazias" (fundo branco ou
     transparente) e quais têm conteúdo de verdade.
  2. Agrupa colunas de conteúdo contíguas em "blocos" -- cada bloco é uma
     pose. Um vão vazio de pelo menos MIN_GAP pixels de largura é o que
     separa um bloco do outro.
  3. Pra cada bloco, corta também a margem vertical vazia (top/bottom),
     deixando cada pose bem enquadrada no seu próprio PNG.
  4. Deixa o fundo transparente (remove branco), pra combinar com o fundo
     escuro do jogo.

Uso:
    python slice_poses.py entrada.png saida_prefixo nome1 nome2 nome3 ...

    (a quantidade de nomes tem que bater com a quantidade de poses que o
    script encontrar na imagem -- se não bater, ele avisa quantas achou
    em vez de cortar errado.)

Exemplo (o caso do Naruto):
    python slice_poses.py naruto_sheet.png assets/sprites/naruto idle dash block
    -> gera assets/sprites/naruto/idle.png, dash.png, block.png
"""

import sys
import os
from PIL import Image
import numpy as np

BG_THRESHOLD = 245   # um pixel com R,G,B todos >= isso (e alpha alto) conta como "fundo branco"
MIN_GAP = 15          # colunas vazias seguidas, no mínimo, pra considerar "vão real" entre poses
PADDING = 4           # pixels de respiro deixados ao redor de cada pose depois de cortar


def is_background_column(col_pixels):
    """col_pixels: array (altura, 4) de uma coluna. True se a coluna inteira
    é fundo (transparente OU branco quase puro)."""
    alpha = col_pixels[:, 3]
    rgb = col_pixels[:, :3]
    transparente = alpha < 10
    branco = (rgb >= BG_THRESHOLD).all(axis=1) & (alpha >= 10)
    return bool((transparente | branco).all())


def find_content_blocks(arr):
    """arr: array (altura, largura, 4). Retorna lista de (x_ini, x_fim)
    -- intervalos de colunas com conteúdo, já separados pelos vãos."""
    largura = arr.shape[1]
    is_bg = np.array([is_background_column(arr[:, x, :]) for x in range(largura)])

    blocks = []
    x = 0
    while x < largura:
        if is_bg[x]:
            x += 1
            continue
        # achou início de um bloco de conteúdo -- anda até achar um vão
        # de fundo com pelo menos MIN_GAP colunas seguidas (ou o fim da imagem)
        start = x
        while x < largura:
            if is_bg[x]:
                # checa se esse vão é "real" (largo o suficiente) ou só um
                # buraco pequeno dentro do próprio desenho (ex: entre pernas)
                gap_start = x
                while x < largura and is_bg[x]:
                    x += 1
                if (x - gap_start) >= MIN_GAP or x >= largura:
                    break  # vão real, ou acabou a imagem: fecha o bloco aqui
                # vão pequeno demais -- é só espaço dentro do desenho, continua
            else:
                x += 1
        end = min(x, largura)
        # some do vão real de volta pro fim do bloco (sem incluir o vão)
        while end > start and is_bg[end-1]:
            end -= 1
        blocks.append((start, end))
    return blocks


def crop_block_tight(arr, x_ini, x_fim):
    """Corta o bloco [x_ini:x_fim] e depois aperta a margem vertical vazia."""
    sub = arr[:, x_ini:x_fim, :]
    altura = sub.shape[0]
    is_bg_row = np.array([is_background_column(sub[y, :, :]) for y in range(altura)])
    rows_with_content = np.where(~is_bg_row)[0]
    if len(rows_with_content) == 0:
        y_ini, y_fim = 0, altura
    else:
        y_ini, y_fim = rows_with_content[0], rows_with_content[-1] + 1
    y_ini = max(0, y_ini - PADDING)
    y_fim = min(altura, y_fim + PADDING)
    return sub[y_ini:y_fim, :, :]


def make_transparent(arr):
    """Troca fundo branco por transparente (mantém o que já era transparente)."""
    out = arr.copy()
    rgb = out[:, :, :3]
    alpha = out[:, :, 3]
    branco = (rgb >= BG_THRESHOLD).all(axis=2) & (alpha >= 10)
    out[branco, 3] = 0
    return out


def slice_sheet(input_path, output_dir, names):
    img = Image.open(input_path).convert("RGBA")
    arr = np.array(img)

    blocks = find_content_blocks(arr)

    if len(blocks) != len(names):
        print(f"⚠️  Encontrei {len(blocks)} pose(s) na imagem, mas você deu {len(names)} nome(s).")
        print(f"    Blocos encontrados (em pixels): {blocks}")
        print("    Ajuste a lista de nomes ou revise a imagem (algum vão ficou "
              "menor que MIN_GAP={} px e grudou duas poses?)".format(MIN_GAP))
        return False

    os.makedirs(output_dir, exist_ok=True)
    for (x_ini, x_fim), name in zip(blocks, names):
        recorte = crop_block_tight(arr, x_ini, x_fim)
        recorte = make_transparent(recorte)
        out_img = Image.fromarray(recorte, "RGBA")
        out_path = os.path.join(output_dir, f"{name}.png")
        out_img.save(out_path)
        print(f"✅ {name}.png -- {out_img.size[0]}x{out_img.size[1]}px "
              f"(bloco original: colunas {x_ini}-{x_fim})")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python slice_poses.py entrada.png pasta_saida nome1 nome2 ...")
        sys.exit(1)
    input_path = sys.argv[1]
    output_dir = sys.argv[2]
    names = sys.argv[3:]
    ok = slice_sheet(input_path, output_dir, names)
    sys.exit(0 if ok else 1)
