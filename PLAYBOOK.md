# PLAYBOOK — Arena de Leilão

Referência interna para os 4 tipos de pedido recorrentes. Objetivo: eu ir direto
ao trecho certo com `grep`/`view -view_range` em vez de reler o arquivo inteiro.

Convenção de anchors: `arquivo :: função/const` — sempre `grep -n "^const NOME\|^function nome"`
pra achar a linha atual, porque edições deslocam número de linha mas não o texto-âncora.

---

## 1. Adicionar personagem

**Isso mudou.** Os dados de personagem não ficam mais no `index.html` —
ficam em **`characters.py`**, um objeto `Character` por personagem
(nome, stats, ataques, tudo junto, sem listas paralelas pra desalinhar).

1. Abra `characters.py`, copie um dos dois exemplos comentados no fim do
   arquivo (`_EXEMPLO_SIMPLES` ou `_EXEMPLO_COM_QUARTO_ATAQUE_E_ULTIMATE`).
2. Cole dentro da lista `CHARACTERS`, edite os valores.
3. Rode `python build_characters.py` — isso gera `characters.generated.js`
   (o `index.html` já carrega esse arquivo sozinho, não precisa editar HTML).
4. Se `build_characters.py` reclamar de algo (nome duplicado, style/level
   inválido, número errado de ataques, lendário sem ultimate...), ele NÃO
   gera o arquivo — corrija o erro apontado e rode de novo.

**Rank/raridade** agora é um campo (`rank=`) direto no `Character`, não uma
tabela separada. Só `"lendario"` e `"mitico"` usam `ultimate=` de verdade
em batalha (`ULT_TIERS` no `index.html` continua controlando isso).

**Ataques** usam `Attack(nome, tipo, power=, cooldown=, effects=[...])`.
Pra efeitos, use os helpers em `characters.py` (`heal()`, `shield()`,
`stun()`, `dot()`, `buff()`, `debuff()`, `confuse()`, `cleanse()`,
`dispel()`, `revive()`) em vez de escrever o dict na mão — cobrem os casos
comuns. Pra algo fora desses, passe o dict direto seguindo o formato
documentado no topo de `characters.py`.

**Não precisa tocar:** motor de batalha, leilão, UI, `index.html`. Um
personagem novo em `characters.py` + rodar o build já aparece no Anidex,
no leilão e é jogável.

---

## 1b. Como o `characters.generated.js` se encaixa (referência técnica)

`build_characters.py` lê `CHARACTERS` (lista de `Character`) e monta, na
mesma ordem, as estruturas que o motor de batalha sempre esperou: `RAW`,
`CHAR_KIT`, `APPEARANCE`, `CLASS_TYPE`, `FOURTH_ATTACK`, `ULTIMATES`,
`RANK_OVERRIDE`, `ART`, `ANIMES`. O alinhamento por posição entre essas
listas (que antes era responsabilidade de quem editava o HTML) agora é
responsabilidade do script — ele monta tudo no mesmo loop, então não tem
como desalinhar.

`index.html` carrega `characters.generated.js` num `<script src>` antes
do script principal. **Nunca edite `characters.generated.js` na mão** —
qualquer mudança lá se perde no próximo `python build_characters.py`.

Dois ajustes pequenos foram feitos no motor pra isso funcionar bem:
- `FOURTH_ATTACK` agora é de verdade opcional (`attacks: fourthAtk ? [...] : [...]`) —
  antes todo personagem precisava ter um 4º ataque, mesmo que undefined.
- `describeEffect()` agora entende o formato moderno de efeito (lista de
  `{kind:...}`), não só o formato antigo (`{type:...}`) — sem isso, os
  efeitos de personagens novos apareceriam sem descrição na tela.

---

## 2. Adicionar animação de transformação (arte + Ultimate tipo "transform")

**Pré-requisito:** personagem já existe (seção 1) e tem entrada em `ULTIMATES` com
`kind` omitido/`"transform"` (não `"meteor"`).

### 2.1 — Preparar a arte (fora do HTML)
```bash
python3 prepare_sprite.py --slug <slug> --state front        arte.png
python3 prepare_sprite.py --slug <slug> --state back         arte.png
python3 prepare_sprite.py --slug <slug> --state charge-front arte.png   # opcional
python3 prepare_sprite.py --slug <slug> --state charge-back  arte.png   # opcional
python3 prepare_sprite.py --slug <slug> --state ssj-front    arte.png
python3 prepare_sprite.py --slug <slug> --state ssj-back     arte.png
python3 prepare_sprite.py --check <slug>          # SEMPRE — ver COMO-ADICIONAR-ARTE.md
```

### 2.2 — Uma entrada em characters.py (não mais no HTML)
No `Character` correspondente, em `characters.py`, preencha:
```python
sprite=dict(slug="slug-da-pasta", states=["front","back","chargeFront","chargeBack","ssjFront","ssjBack"]),
```
`states` lista só o que existe de verdade — sem `charge*`, o jogo pula direto pro clarão.
Depois rode `python build_characters.py` — ele monta a entrada em `ART` sozinho.

### 2.3 — Nada mais.
`bitmapFor`, `chargeBitmapFor`, `preloadArt`, `artFailed`, `playTransformation` e a
faixa de título (`.ult-title` em `part2.html`) já são genéricos — funcionam pra
qualquer personagem que tenha entrada em `ART` + `ULTIMATES`. **Não duplicar
código de animação por personagem.**

**Se a transformação tiver custo especial** (ex.: Might Guy perde vida por rodada,
Edward perde escudo permanente) — isso já é dado, não código: ver campos
`selfRecoil`, `upfrontToll`, `permanentShieldCost`, `growPerHit/growCap/explodeOnDeath`
em `ULTIMATES` (`part4.html`) e a lógica que já os lê em `useUltimate()` (`part8.html`).
Não escrever `if(nome==="X")` em lugar nenhum — sempre generalizar por campo de dado.

---

## 3. Personagem com arte de pose (base / dash / block) — já implementado

Existem DOIS jeitos de dar arte de verdade a um personagem — escolha um por
personagem, não misture os dois:

**A) Front/back desenhados separados** (padrão antigo, ex. Son Goku) — dois
desenhos por estado (de frente e de costas), porque o jogo olha o personagem
de ângulos diferentes conforme o lado. Ver seção 2 acima.

**B) Uma pose só, espelhada pelo jogo** (padrão novo, ex. Naruto) — você
manda UMA arte por pose (olhando/avançando pra DIREITA), e o jogo mesmo
inverte com CSS (`scaleX(-1)`, classe `.mirror-x`) quando o personagem está
no campo inimigo. Metade do trabalho de arte do método A, e é o que vale
pra qualquer personagem novo daqui pra frente — front/back manual só
continua existindo pelo Son Goku, que já estava pronto antes desse sistema.

### 3.1 — Preparar a arte
```bash
python3 prepare_sprite.py --slug <slug> --state base   arte-parada.png
python3 prepare_sprite.py --slug <slug> --state dash    arte-avancando.png
python3 prepare_sprite.py --slug <slug> --state block  arte-bloqueando.png
python3 prepare_sprite.py --check <slug>
```
Preciso da arte olhando pra DIREITA (é a orientação "campo do jogador" —
o espelho automático só cobre o campo inimigo). Se a arte de referência já
tiver as 3 poses juntas numa folha só, recorte cada uma antes (ver o que foi
feito pro Naruto: `naruto_crop_base.py`-style, colunas isoladas por conteúdo
de alpha — não precisou de chroma-key porque a arte já veio com fundo
transparente).

### 3.2 — Uma entrada em characters.py
```python
sprite=dict(slug="<slug>", states=["base","dash","block"]),
```
`build_characters.py` monta a entrada em `ART` sozinho — não editar `ART` na mão.

### 3.3 — Nada mais.
`usesPoseArt(c)` detecta sozinho que esse personagem usa o padrão novo (basta
ter `"base"` em `states`). A partir daí:
- **Pose parada:** sempre "base", nos dois lados do campo — só espelha.
- **No turno de ataque:** `swapPoseTemporarily()` troca pra "dash" durante a
  animação de avanço (`.anim-attack-player`/`.anim-attack-enemy`) e volta pra
  "base" sozinho quando ela termina.
- **Ao ser atingido:** o mesmo troca pra "block" durante o `.anim-hit` e volta.
- **Espelhamento:** `fighterArt(c, {..., side:"enemy"})` aplica `.mirror-x`;
  `side:"player"` não aplica nada.

**Não escrever `if(c.name==="Naruto")` em lugar nenhum** — tudo isso é
genérico por cima de `usesPoseArt()`/`ART`, então o próximo personagem com
essas 3 poses funciona só preenchendo `sprite=` em `characters.py`.

### 3.4 — Transformação com esse padrão (3 frames formando uma sequência)
Ainda não implementado o GATILHO (a troca automática durante `playTransformation`),
mas o registro já está pronto: `STATE_FILE` já tem `transform1`/`transform2`/`transform3`
reservados. Quando pedir pra um personagem desse padrão: preparar as 3 artes com
esses estados, e adaptar `playTransformation()` (hoje pensada pro par
`chargeFront`→`ssjFront` do Son Goku) pra tocar os 3 frames em sequência antes
de resolver na pose final. Avisar antes de implementar — o timing exato
(quanto tempo por frame) muda com a arte em mãos.

---

## 4. Adicionar nova mecânica (efeito de ataque, status, regra de batalha)

**Efeitos de ataque existentes:** `shield`, `heal`, `debuff`, `stun`, `dot`.
Todos seguem o mesmo padrão em 3 pontos que SEMPRE precisam mudar juntos:

1. **Criação do efeito nos dados** — `E(type, value)` (`part3.html`, perto de `function E`).
   Usado em `A(nome, tipo, dano, cooldown, E("novoTipo", valor), onceOnly)`.
2. **Aplicação em batalha** — bloco `if(atk.effect){ ... }` dentro de
   `applyAction()` (`part8.html`, anchor `if(atk.effect.type===`). Acrescentar
   `else if(atk.effect.type==="novoTipo" ...)`. Ler o padrão dos 5 existentes:
   sempre loga em `b.log.unshift`, sempre empurra em `fxEffects` se tiver visual.
3. **Descrição pro jogador** — `describeEffect()` (`part6.html`). Sem isso o
   efeito não aparece no texto do botão de ataque nem no índice de personagens.

**Se o efeito precisa "tickar" turno a turno** (como `dot`), olhar o padrão já
implementado no fim de `applyAction()` (bloco `Object.keys(b.dot).forEach`) — é
o único efeito hoje com persistência multi-turno. Novo efeito assim precisa de
storage próprio em `initBattle()` — procurar a linha `hp:{}, cooldowns:{}, ...`
dentro da função, é uma lista inline de objetos por-personagem — e tick equivalente.

**Se a mecânica é de REGRA GERAL de batalha** (não efeito de ataque específico —
ex: nova condição de vitória, novo tipo de troca, novo cálculo de dano):
não existe padrão único, mas os pontos de entrada mais prováveis são:
- Fórmula de dano → `applyAction()`, linha `const dmg = Math.max(5, ...)`
- Condição de vitória → `postAction()` (`part8.html`)
- Regra de troca → `doSwitch()` (`part8.html`)
- Novo tipo de Ultimate (além de `transform`/`meteor`) → `useUltimate()` (`part8.html`),
  seguir o padrão do `if(c.ultimate.kind==="meteor"){...} else {...}`

**Sempre perguntar antes de implementar mecânica nova:** ela é POR PERSONAGEM
(vai em dado, tipo os campos de `ULTIMATES`) ou É REGRA DO JOGO (vai em código)?
Confundir os dois é o erro mais caro — mecânica de personagem hardcoded vira
`if(nome===)` espalhado; regra geral guardada como dado por personagem quebra
na primeira exceção.

---

---

## 5. Modos de jogo e sala persistente (já implementado — referência)

**Modos:** `state.mode` = `"auction"` | `"draft"`. Escolhido em `renderHome()`
(`part6.html`, `let selectedMode`) e gravado por `createRoom()`. Quem entra pelo
código herda o modo de quem criou.

| Peça | Anchor |
|---|---|
| Nome salvo no aparelho | `const NAME_KEY` — `savedName/saveName/forgetName`, tudo em try/catch |
| Tela inicial + cartões de modo | `function renderHome()`, CSS `.mode-card` |
| Constantes de tamanho | `const TEAM_SIZE`, `const DRAFT_OPTIONS` |
| Sorteio | `rollDraftOptions` / `startDraft` / `pickDraft` / `renderDraft` |
| Revanche mesma sala | `rematch(mode)` em `part8.html` |

**Para adicionar um TERCEIRO modo:** (1) cartão em `renderHome`, (2) `case` no
roteador `draw()`, (3) as funções `start<Modo>`/`render<Modo>`, (4) transição
para `phase:"ultimate"` ao fechar os times. O resto do fluxo (ultimate → ordem →
moeda → batalha) é compartilhado e não precisa ser tocado.

**Regra do sorteio:** cada jogador tem sorteio próprio (`draftOptions.p1/p2`), então
não há turno — os dois escolhem simultaneamente. A exclusão de personagens já
escolhidos é global (não existem dois Gokus em campo), revalidada dentro de
`pickDraft` contra o estado recém-carregado, porque entre desenhar a tela e clicar
o adversário pode ter levado a mesma carta.

**`rematch` monta um estado NOVO** e recoloca só sala/código/jogadores, em vez de
zerar campo a campo — assim nenhum resíduo de batalha (cooldown, dot, transformação)
vaza pra partida seguinte.

## Como validar qualquer mudança sem reler tudo

```bash
node --check game.js                    # sintaxe
node run.js                              # renderiza sprites/bitmaps isolados, se mexeu em arte
node sim.js                              # partida completa headless: leilão → ultimates → batalha até o fim
```

`sim.js`/`run.js` não fazem parte do jogo — são arneses de teste que criei
(stubs de `document`/`firebase`, harness de composição de imagem). Ficam fora
do HTML final. Recriá-los é rápido: stub de DOM + `eval` do JS extraído do
`<script>` inline do HTML (ver histórico desta conversa se precisar reconstruir).

## O que NUNCA precisa reler o arquivo inteiro para mudar
Dado (seções 1, parte de 4) = só grep pela const certa.
O que exige entender o fluxo antes de mexer = motor de batalha (`applyAction`,
`useUltimate`, `postAction`) e a máquina de fases (`draw()`/`state.phase`) —
essas duas áreas têm efeitos colaterais entre si (cooldown, stun, dot, transform
todos tickam na mesma função) e merecem leitura da função inteira, não só do trecho.
