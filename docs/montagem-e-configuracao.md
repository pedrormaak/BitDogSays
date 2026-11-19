# Montagem e configuração

Não é preciso montar nenhum circuito: o jogo usa só os recursos que já vêm na BitDogLab. A configuração é toda feita no código.

## Esquema da arena

```
                 Wi-Fi "SIMON_LAB_1"  (canal 1)
                ┌────────────────────────────┐
                │      PLACA MESTRA 1        │
                │   IP 192.168.4.1 : 8080    │
                └──────────────┬─────────────┘
          UDP "EQUIPE,COR"     │     UDP "EQUIPE,COR"
     ┌────────────┬────────────┴───────────┬────────────┐
 Secundária    Secundária             Secundária    Secundária
 AZUL          AZUL                   VERMELHO      VERMELHO
 A=VERMELHO    A=VERDE                A=VERMELHO    A=VERDE
 B=AZUL        B=AMARELO              B=AZUL        B=AMARELO
 └──── equipe AZUL ────┘              └─── equipe VERMELHO ───┘
```

A arena 2 é igual, com `SIMON_LAB_2`, canal 11 e as equipes ROXO e LARANJA.

## 1. Placa mestra

Copie para a placa os arquivos de [`codigo/mestra/`](../codigo/mestra/):

- `main.py`
- `sh1107_bitdoglab.py`

No início do `main.py`, ajuste:

| Variável | Mestra 1 | Mestra 2 |
|---|---|---|
| `SSID_REDE` | `"SIMON_LAB_1"` | `"SIMON_LAB_2"` |
| `TIME_1` | `"AZUL"` | `"ROXO"` |
| `TIME_2` | `"VERMELHO"` | `"LARANJA"` |
| `channel=` (linha do `ap.config`) | `1` | `11` |

A senha da rede é `simon123` e precisa ser a mesma nas secundárias.

## 2. Placas secundárias

Copie para cada placa os arquivos de [`codigo/secundaria/`](../codigo/secundaria/):

- `main.py`
- `ssd1306.py`

No início do `main.py`, ajuste cada placa conforme a tabela:

| Placa | `WIFI_SSID` | `EQUIPE` | `COR_BOTAO_A` | `COR_BOTAO_B` |
|---|---|---|---|---|
| 1 | `SIMON_LAB_1` | `AZUL` | `VERMELHO` | `AZUL` |
| 2 | `SIMON_LAB_1` | `AZUL` | `VERDE` | `AMARELO` |
| 3 | `SIMON_LAB_1` | `VERMELHO` | `VERMELHO` | `AZUL` |
| 4 | `SIMON_LAB_1` | `VERMELHO` | `VERDE` | `AMARELO` |
| 5 | `SIMON_LAB_2` | `ROXO` | `VERMELHO` | `AZUL` |
| 6 | `SIMON_LAB_2` | `ROXO` | `VERDE` | `AMARELO` |
| 7 | `SIMON_LAB_2` | `LARANJA` | `VERMELHO` | `AZUL` |
| 8 | `SIMON_LAB_2` | `LARANJA` | `VERDE` | `AMARELO` |

> O nome da `EQUIPE` precisa ser **exatamente igual** ao `TIME_1` ou ao `TIME_2` da mestra. Caso contrário, a mestra ignora os toques dessa placa.

## 3. Ligando a arena

1. Ligue a **mestra** primeiro. O display mostra "NOVO JOGO" e o placar.
2. Ligue as **secundárias**. A matriz pisca em branco enquanto procura a rede. Quando conecta, mostra as duas cores dos botões, uma de cada lado.
3. Aperte o **botão A da mestra** para começar.

O arquivo se chama `main.py` para rodar sozinho quando a placa é ligada, sem precisar do computador.

## Problemas comuns

| Sintoma | Causa provável |
|---|---|
| A secundária fica piscando branco | A mestra está desligada, o `WIFI_SSID` está errado ou a senha está diferente |
| A mestra não reage aos botões de uma equipe | O nome da `EQUIPE` na secundária não bate com o `TIME_1`/`TIME_2` da mestra |
| A tela da mestra fica em branco | O arquivo `sh1107_bitdoglab.py` não foi copiado para a placa |
| As duas arenas se atrapalham | As mestras estão no mesmo canal: use 1 e 11 |
