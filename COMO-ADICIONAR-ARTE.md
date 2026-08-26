# Como adicionar arte de um personagem

Existem DOIS tipos de arte no jogo:

- **Frente/costas**: duas artes desenhadas separadamente, uma pra quando o
  personagem é visto de costas (seu time) e outra de frente (time inimigo).
  Precisa de arte dupla pra cada estado. Nenhum personagem usa isso hoje
  (Son Goku usava, mas a arte dele foi removida — ele caiu de volta pro
  gerador procedural, que continua existindo em `SPRITES` no index.html).
- **Pose única espelhável** (Naruto e todo personagem novo daqui pra frente):
  UMA arte por pose (base/dash/block...), desenhada olhando pra direita. O
  jogo espelha sozinho com CSS quando o personagem está no campo inimigo —
  não precisa desenhar nem processar a versão "olhando pra esquerda". E
  TODAS as poses de um personagem moram num **sheet.png único** — não é
  1 arquivo por pose, é 1 arquivo pro personagem inteiro.

Use pose única sempre que puder: é metade do trabalho de desenhar, e um
arquivo só pra versionar.

## Estrutura

```
index.html
prepare_sprite.py
slice_poses.py            (opcional -- só se a arte vier numa folha só)
characters.py             (é AQUI que a arte se liga ao personagem, não no HTML)
assets/sprites/
    naruto/                (pose única espelhável -- UM arquivo só)
        sheet.png            (base + dash + block, um do lado do outro)
```

O `assets/` fica **ao lado** do HTML. Funciona no GitHub Pages e abrindo o
arquivo direto no navegador.

## Pose única espelhável (o caminho recomendado)

**0. Se a arte vier numa folha só (3 poses lado a lado), corte primeiro**

Fontes de arte costumam mandar base/dash/block juntas numa imagem só. Em vez
de cortar na mão (frágil — qualquer reespaçamento futuro corta errado), use:

```bash
python3 slice_poses.py folha.png ./recortes base dash block
```

Isso ACHA os vãos de fundo vazio entre as poses sozinho e corta cada uma no
próprio tamanho, não importa o espaçamento usado na folha original. Se a
contagem de poses encontradas não bater com a de nomes dados, ele avisa em
vez de cortar errado. Gera `./recortes/base.png`, `dash.png`, `block.png`.

**1. Processe cada pose com o prepare_sprite.py**

```bash
python3 prepare_sprite.py recortes/base.png  --slug naruto --state base
python3 prepare_sprite.py recortes/dash.png  --slug naruto --state dash
python3 prepare_sprite.py recortes/block.png --slug naruto --state block
```

Isso ainda gera um PNG por estado, temporariamente — vira 1 arquivo só no
passo 3. Poses bem mais LARGAS que altas (dash, corpo inteiro deitado numa
corrida) costumam estourar a largura do canvas quando escaladas pela altura
do corpo. Se aparecer `AVISO: a arte transborda o canvas (lateral)`,
reprocesse com `--scale` menor até o aviso sumir:

```bash
python3 prepare_sprite.py recortes/dash.png --slug naruto --state dash --scale 0.58
```

Isso deixa a pose um pouco mais "recuada" que as outras (é o preço de uma
pose larga caber num canvas retrato) — mas nada fica cortado, que é o que
importa. Ajuste o número até o aviso sumir, sem exagerar pra baixo.

**2. Confira o alinhamento — este passo não é opcional**

```bash
python3 prepare_sprite.py --check naruto
```

Abra `assets/sprites/naruto/_contato.png` (esse arquivo é só conferência —
apague antes de subir pro jogo de verdade, ele não é usado em nada):

- **Linha dourada** = chão. Todos os pés precisam pisar nela.
- **Linha verde** = topo do corpo. Não precisa bater exatamente entre poses
  muito diferentes (dash agachado vs base em pé), mas ninguém pode ficar
  flutuando ou cortado.

**3. Junte tudo num sheet.png só e apague os arquivos individuais**

```bash
python3 prepare_sprite.py --sheet naruto --states base dash block
```

Isso lê `base.png`/`dash.png`/`block.png` (já processados e do mesmo
tamanho), gera `assets/sprites/naruto/sheet.png` com as três lado a lado
NA ORDEM DADA, e apaga os três arquivos individuais — só o `sheet.png` fica
na pasta. A ordem de `--states` aqui **precisa ser a mesma** que vai em
`states=[...]` no characters.py (é essa ordem que decide qual "fatia" do
sheet é cada pose).

**4. Ligue ao personagem em `characters.py`** (não no HTML)

```python
Character(
    name="Naruto Uzumaki",
    ...
    sprite=dict(slug="naruto", states=["base", "dash", "block"]),
),
```

Depois rode `python3 build_characters.py` como sempre. O nome da chave em
`ART` (gerado automaticamente a partir disso) é o `name` do Character —
não precisa bater com mais nada.

**Como o jogo troca de pose sozinho durante a batalha:** `base` é o repouso;
quando o personagem ataca, a arte "desliza" pro quadro `dash` do sheet por
meio segundo e volta; quando é atingido, desliza pro quadro `block` por um
instante e volta. Isso já está pronto no motor (`swapPoseTemporarily`,
chamado em `playFxEvent`) — você só precisa fornecer o `sheet.png`, não
precisa mexer em lógica nenhuma.

**Adicionando transformação depois:** quando tiver as 3 artes de
transformação, reprocesse tudo junto com uma pose a mais em `--states`:

```bash
python3 prepare_sprite.py t1.png --slug naruto --state transform1
python3 prepare_sprite.py t2.png --slug naruto --state transform2
python3 prepare_sprite.py t3.png --slug naruto --state transform3
python3 prepare_sprite.py --sheet naruto --states base dash block transform1 transform2 transform3
```

E atualize `states=[...]` em characters.py pra bater com a mesma lista, na
mesma ordem. Continua sendo 1 arquivo só (`sheet.png`), só que com mais
quadros dentro.

## Frente/costas (o caminho antigo, ainda válido pra quem já usa)

**1. Processe cada estado**

```bash
python3 prepare_sprite.py --slug vegeta --state front       frente.png
python3 prepare_sprite.py --slug vegeta --state back        costas.png
python3 prepare_sprite.py --slug vegeta --state charge-front carga-frente.png
python3 prepare_sprite.py --slug vegeta --state ssj-front    ssj-frente.png
```

**2. Confira o alinhamento** (mesmo `--check` de cima)

Se algum estado estiver fora, reprocesse **só ele**:

```bash
python3 prepare_sprite.py --slug vegeta --state ssj-front ssj-frente.png --scale 1.06
python3 prepare_sprite.py --slug vegeta --state charge-front carga.png --dy -4
```

`--scale 1.06` deixa 6% maior. `--dy -4` sobe 4px.

**3. Ligue ao personagem em `characters.py`**

```python
sprite=dict(slug="vegeta", states=["front","back","chargeFront","chargeBack","ssjFront","ssjBack"]),
```

Em `states`, liste só o que existe de verdade na pasta.

**4. Nome da transformação**

O texto da faixa que cruza a tela vem do campo `ultimate.name` do Character,
em `characters.py`. Só personagens com `ultimate=` definido mostram a faixa.

## Por que o alinhamento importa tanto

A animação de transformação é só uma troca de `src` na mesma `<img>`. Isso só
funciona porque todas as artes de um personagem compartilham o mesmo canvas,
com a sola dos pés e o centro do corpo no mesmo ponto.

Arte solta, no recorte que veio da fonte, faz o personagem pular de tamanho e
desgrudar do chão na hora da troca. O `prepare_sprite.py` existe por causa
disso — e o `slice_poses.py` existe pra a etapa ANTES dele (separar poses que
vieram juntas numa folha só) não depender de coordenadas fixas frágeis.

## Regras que o jogo segue sozinho

- Personagem sem `sprite=` em `characters.py` → stick figure (a menos que
  tenha uma entrada procedural em `SPRITES` no index.html, como o Son Goku).
- Estado não declarado em `states` → o jogo nunca pede aquele quadro.
- Sem `charge-*` (frente/costas) → pula a fase de carga de ki e transforma
  direto, mas a faixa com o nome ainda aparece.
- Frente/costas: arquivo faltando ou com erro de carregamento → cai no stick
  figure em vez de mostrar ícone de imagem quebrada (é o `onerror` da `<img>`).
- Pose única (sheet.png): se o arquivo não existir ou falhar, hoje só avisa
  no console do navegador — não troca pro stick figure sozinho ainda, porque
  background-image não dispara `onerror` como `<img>` dispara. Se isso for
  um problema no seu uso, é um ponto pra melhorar depois.
- Só entram na pré-carga os personagens em campo na formação atual.
- Pose única (base/dash/block/...) é espelhada automaticamente (`mirror-x`)
  quando o personagem está no campo inimigo — nunca desenhe a versão
  invertida à mão.

## Se mudar o tamanho do canvas

`CANVAS_W`, `CANVAS_H`, `BODY_H`, `ANCHOR_X` e `ANCHOR_Y` no
`prepare_sprite.py` são um contrato com o `SPRITE_CANVAS` do `index.html`.
Mudar um exige mudar o outro **e reprocessar todas as artes de todos os
personagens**.
