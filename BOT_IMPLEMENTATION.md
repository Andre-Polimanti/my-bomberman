# Bot Implementation — My Bomberman

## Visão geral

O sistema de bots adiciona jogadores controlados por IA ao jogo. Por padrão, **P3 (Yellowy)** e **P4 (Cyany)** são bots; **P1 (Bluey)** e **P2 (Redy)** continuam sendo controlados pelo teclado.

Cada bot toma uma decisão por tick de jogo (~200ms), seguindo uma máquina de estados com três prioridades ordenadas: fugir, atacar, perseguir.

---

## Arquivos criados

```
src/game/bot/
├── bot_player.py   — lógica de IA de um bot individual
└── bot_manager.py  — gerencia a lista de bots e repassa ações ao App
```

### Arquivos modificados

| Arquivo | Mudança |
|---|---|
| `src/game/app.py` | Import de `BotManager`; instanciação em `setup()`; chamada em `on_loop()` |

---

## Fluxo de execução

```
on_loop() [app.py]
  └─ bot_manager.update(app)
       └─ para cada bot:
            bot_player.update(app)
              ├─ [prioridade 1] fugir   → player.face_to_dir() + player.walk()
              ├─ [prioridade 2] atacar  → retorna dict de ação de bomba
              └─ [prioridade 3] perseguir → player.face_to_dir() + player.walk()
  └─ para cada ação de bomba retornada:
       bomb_manager.create_bomb(...)
```

O bot não interage com o sistema de teclado. Ele chama `player.face_to_dir()` e `player.walk()` diretamente para movimento, e retorna um dicionário `{"type": "PLAY", "action": "BOMBING", ...}` para o `App` criar a bomba — o mesmo formato usado pelo sistema de teclado.

---

## Máquina de estados (prioridades)

### Prioridade 1 — Fuga

**Quando:** o tile atual do bot está no conjunto de `danger_tiles`.

**Como funciona:**

1. `_get_danger_tiles()` percorre todas as bombas ativas:
   - Se a bomba está **TICKING** e tem menos de `1500ms` restantes: calcula a área de explosão prevista com `_predicted_blast()` e a adiciona ao conjunto de perigo.
   - Se está **EXPLODING** ou **LINGERING**: adiciona as `fire_coords` já calculadas pela própria bomba.

2. `_bfs_find_safe()` faz um BFS a partir da posição atual, expandindo pelos tiles livres, e retorna o **primeiro tile fora do perigo** encontrado.

3. `_bfs_next_step()` calcula o **primeiro passo do caminho** até esse tile seguro.

4. O bot executa esse passo com `_step_to()`.

> O bot não age sobre mais nada neste tick enquanto estiver fugindo — a fuga é sempre a decisão de maior prioridade.

---

### Prioridade 2 — Bombing

**Quando:** o bot não está em perigo e não tem nenhuma bomba ativa no mapa (verificado por `b.team == player.team`).

**Como funciona (`_can_bomb_enemy`):**

Para que o bot possa bombear um inimigo, três condições precisam ser satisfeitas simultaneamente:

1. **Alinhamento:** bot e inimigo estão na **mesma linha (y igual)** ou **mesma coluna (x igual)**.

2. **Alcance:** a distância entre eles é `≤ BOMB_RANGE + 1` (6 tiles). A bomba é colocada um tile à frente do bot, então a distância real da bomba ao inimigo é `dist - 1`, que precisa estar dentro do `BOMB_RANGE = 5`.

3. **Linha de visão (`_clear_line`):** não há nenhum tile obstruído entre o bot e o inimigo (tiles do índice 2 até `dist - 1` são verificados — o tile imediatamente à frente do bot e o tile do inimigo são excluídos da checagem).

Se tudo for válido, o bot se vira na direção do inimigo e chama `player.get_valid_target()`. Esse método já verifica se o tile à frente está livre (não obstruído e não ocupado). Se retornar uma posição válida, ela é retornada como alvo da bomba.

**Por que a bomba não pode ser colocada quando o inimigo está adjacente (dist = 1)?**

Porque o tile à frente estaria ocupado pelo próprio inimigo, e `get_valid_target()` retorna `None` nesse caso. O bot precisa estar a no mínimo 2 tiles de distância.

**Exemplo:**

```
Bot em (3, 5), inimigo em (7, 5) — mesma linha, dist = 4
Bot se vira para direita (dx=1)
Bomba colocada em (4, 5)
Explosão com range=5 alcança até (9, 5) → inimigo em (7, 5) é atingido
```

---

### Prioridade 3 — Perseguição

**Quando:** o bot não está em perigo e não pode (ou não quer) bombear agora.

**Como funciona (`_bfs_next_step`):**

BFS padrão no grid do mapa. O bot percorre os tiles adjacentes expandindo a partir da sua posição atual, respeitando as seguintes regras:

- Tiles **obstruídos** (`pixel.obstructed`) são impassáveis.
- Tiles com **bombas ativas** (`state == "TICKING"`) são impassáveis — o bot não tenta passar por cima de uma bomba.
- Tiles **ocupados por jogadores** são ignorados durante a expansão (o jogador pode ter se movido quando o bot chegar), **exceto** se o tile for o próprio objetivo (o inimigo).

O BFS carrega o **primeiro passo dado** em cada caminho (`first_step`). Assim, ao encontrar o objetivo, retorna diretamente o primeiro passo a ser dado — sem precisar reconstruir o caminho completo.

O inimigo mais próximo é selecionado por **distância de Manhattan** antes de iniciar o BFS, como heurística rápida de seleção de alvo.

---

## Throttling de ações

O bot tem um controle de frequência similar ao `MOVE_DELAY` do teclado (`150ms`). O bot usa `MOVE_DELAY = 200ms` — ligeiramente mais lento para manter o equilíbrio com jogadores humanos.

```python
self.last_move_time = -MOVE_DELAY  # inicializa negativo para garantir que o primeiro tick funcione
```

```python
now = pygame.time.get_ticks()
if now - self.last_move_time < MOVE_DELAY:
    return None  # ainda não é hora de agir
```

---

## Integração com app.py

### Em `setup()`

```python
self.bot_manager = BotManager(self.player_manager.players[2:])
```

`players[2:]` seleciona P3 e P4. P1 e P2 continuam sem entrada no `BotManager`.

### Em `on_loop()`

```python
if self.champion is None:
    bot_actions = self.bot_manager.update(self)
    for act in bot_actions:
        if act["action"] == "BOMBING":
            self.bomb_manager.create_bomb(act["player"], act["pos"], BOMB_RANGE)
```

As ações de movimento já são aplicadas diretamente dentro do `BotPlayer.update()`. Apenas o bombing precisa passar pelo `App`, pois `BombManager` vive nele — o mesmo fluxo do teclado.

---

## Constantes

| Constante | Valor | Significado |
|---|---|---|
| `MOVE_DELAY` | `200ms` | Intervalo mínimo entre ações do bot |
| `BOMB_DANGER_TIME` | `1500ms` | Tempo restante abaixo do qual a bomba é considerada perigosa |
| `BOMB_RANGE` | `5` | Alcance da explosão (igual ao definido em `app.py`) |

---

## Limitações conhecidas

- **Um bot, uma bomba:** o bot só coloca nova bomba quando não há nenhuma ativa da mesma equipe. Isso evita spam de bombas mas impede estratégias com múltiplas bombas.
- **Sem destruição de obstáculos:** o mapa atual não tem blocos destrutíveis. Se forem adicionados, o bot precisaria considerar explodir paredes para abrir caminhos.
- **Sem coordenação entre bots:** P3 e P4 agem de forma independente, sem estratégia cooperativa.
- **Seleção de alvo por Manhattan:** o inimigo mais próximo por distância em linha reta pode não ser o mais fácil de alcançar. Usar o custo real do BFS como critério seria mais preciso.
