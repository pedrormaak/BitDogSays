# BitDog Says 🐶🎮

Jogo de memória no estilo **Genius** (*Simon Says*) feito com a placa **BitDogLab**, em que as placas conversam entre si pelo **Wi-Fi**.
Projeto da disciplina de extensão **EX028**, apresentado em oficina para turmas do 2º ano do ensino médio.

---

## Índice do projeto

| Item | Onde está |
|---|---|
| Repositório do projeto | este repositório |
| Fotos e registros da oficina | [`fotos/`](fotos/) |
| Lista de materiais e componentes | [`docs/materiais.md`](docs/materiais.md) |
| Softwares, bibliotecas e ferramentas | [`docs/softwares.md`](docs/softwares.md) |
| Códigos-fonte e firmware | [`codigo/`](codigo/) |
| Esquemas, montagem e configuração | [`docs/montagem-e-configuracao.md`](docs/montagem-e-configuracao.md) |
| Roteiro da oficina e materiais de apoio | [`docs/roteiro-oficina.md`](docs/roteiro-oficina.md) e [`apresentacao/`](apresentacao/) |

---

## Como o jogo funciona

### As peças

- **Placa mestra:** sorteia e mostra a sequência de cores na matriz de LEDs, com som. Também cria a rede Wi-Fi e confere as respostas.
- **Placas secundárias:** são os "controles" dos jogadores. Cada placa tem 2 botões, e cada botão vale uma cor.

### As equipes (duplas)

Cada equipe é uma **dupla**, e cada jogador fica com uma placa secundária:

| Jogador | Botão A | Botão B |
|---|---|---|
| Jogador 1 | Vermelho | Azul |
| Jogador 2 | Verde | Amarelo |

Assim, a dupla tem as 4 cores e só acerta a sequência se os dois colaborarem.

Cada placa mestra comanda **duas equipes** que jogam ao mesmo tempo:

| Rede (mestra) | Equipe 1 | Equipe 2 |
|---|---|---|
| `SIMON_LAB_1` (mestra 1) | AZUL | VERMELHO |
| `SIMON_LAB_2` (mestra 2) | ROXO | LARANJA |

> O nome da equipe é só um identificador. As cores do jogo são sempre verde, vermelho, amarelo e azul.

### Uma rodada

1. Aperte o **botão A da mestra** para começar.
2. A mestra mostra a sequência: cada cor acende na matriz com uma nota no buzzer.
3. As duas equipes repetem a sequência ao mesmo tempo, apertando os botões das suas placas.
4. A mestra confere cada toque: um bipe agudo indica acerto, e um bipe grave indica erro.

### Regras de resultado (como pênaltis alternados)

| Equipe 1 | Equipe 2 | O que acontece |
|---|---|---|
| ✅ acertou | ✅ acertou | **Próxima fase:** a sequência ganha mais uma cor |
| ❌ errou | ❌ errou | **Empate:** a mesma sequência é repetida |
| ✅ acertou | ❌ errou | **Vitória da equipe 1:** ponto no placar e música da vitória |
| ❌ errou | ✅ acertou | **Vitória da equipe 2** |

Ou seja, **só há vencedor quando um time acerta e o outro erra**. Depois de uma vitória, o placar é atualizado e um novo jogo começa do zero.

O **botão B da mestra** reinicia o jogo a qualquer momento.

---

## Como as placas conversam

![Como as placas conversam]

- A mestra funciona como **ponto de acesso Wi-Fi** (como um roteador) e cria a rede `SIMON_LAB_1` ou `SIMON_LAB_2`, com IP `192.168.4.1`.
- As secundárias se conectam a essa rede. Enquanto procuram, a matriz pisca em branco.
- A cada toque de botão, a secundária envia um pacote **UDP** para a mestra na porta `8080`, com o texto:

  ```
  EQUIPE,COR      ex.: AZUL,VERDE
  ```

- A mestra lê o pacote, identifica a equipe e compara a cor com o próximo item da sequência.
- As duas mestras usam **canais de Wi-Fi diferentes** (1 e 11), para uma rede não atrapalhar a outra.

---

## ⚠️ Antes de gravar: ajuste os parâmetros de cada placa

O **mesmo código** vai em todas as placas do mesmo tipo, mas **cada placa precisa de parâmetros diferentes**. Eles ficam no bloco `CONFIGURAÇÃO (AJUSTE AQUI)`, no início de cada `main.py`.

**Placa mestra** ([`codigo/mestra/main.py`](codigo/mestra/main.py)):

```python
SSID_REDE = "SIMON_LAB_1"   # Mestra 1: "SIMON_LAB_1" | Mestra 2: "SIMON_LAB_2"
TIME_1    = "AZUL"          # Mestra 1: "AZUL"        | Mestra 2: "ROXO"
TIME_2    = "VERMELHO"      # Mestra 1: "VERMELHO"    | Mestra 2: "LARANJA"
ap.config(..., channel=1)   # Mestra 1: 1             | Mestra 2: 11
```

**Placas secundárias** ([`codigo/secundaria/main.py`](codigo/secundaria/main.py)):

```python
WIFI_SSID   = "SIMON_LAB_2" # rede da mestra a que a placa pertence
EQUIPE      = "ROXO"        # igual ao TIME_1 ou TIME_2 dessa mestra
COR_BOTAO_A = "VERDE"       # jogador 1: "VERMELHO" | jogador 2: "VERDE"
COR_BOTAO_B = "AMARELO"     # jogador 1: "AZUL"     | jogador 2: "AMARELO"
```

> Se esquecer de ajustar, a secundária não entra na rede certa ou a mestra ignora os toques dela. A tabela com a configuração das 8 secundárias está em [`docs/montagem-e-configuracao.md`](docs/montagem-e-configuracao.md).

---

## Começo rápido

1. Grave o MicroPython na Pico W de cada BitDogLab ([softwares](docs/softwares.md)).
2. Copie os arquivos de [`codigo/mestra/`](codigo/mestra/) para a mestra e os de [`codigo/secundaria/`](codigo/secundaria/) para as secundárias.
3. Ajuste o bloco **"CONFIGURAÇÃO (AJUSTE AQUI)"** no início de cada `main.py` ([passo a passo](docs/montagem-e-configuracao.md)).
4. Ligue a mestra primeiro e depois as secundárias.

---

## Equipe

- *(nomes dos integrantes)*

Disciplina EX028 · Unicamp
