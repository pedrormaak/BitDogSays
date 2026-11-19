# Lista de materiais e componentes

## Por arena (1 placa mestra + 2 equipes)

| Qtd. | Item | Função |
|---|---|---|
| 1 | BitDogLab com OLED 128×128 (SH1107) | Placa mestra |
| 4 | BitDogLab com OLED 128×64 (SSD1306) | Placas secundárias (2 por equipe) |
| 5 | Cabo USB | Gravação e alimentação |
| 5 | Fonte USB, powerbank ou bateria da própria placa | Alimentação durante o jogo |

Com as **duas arenas** (`SIMON_LAB_1` e `SIMON_LAB_2`), o total fica em **2 mestras e 8 secundárias**.

> A mestra e as secundárias usam drivers de display diferentes porque as placas têm telas diferentes. Se a sua placa tiver outra tela, troque o driver e a inicialização do `oled` no `main.py`.

## Recursos da BitDogLab usados

| Recurso | Pino (Pico W) | Uso no jogo |
|---|---|---|
| Botão A | GP5 | Mestra: iniciar jogo · Secundária: cor do botão A |
| Botão B | GP6 | Mestra: reiniciar · Secundária: cor do botão B |
| Matriz de LEDs 5×5 (WS2812 / NeoPixel) | GP7 | Mostra as cores |
| Buzzer | GP21 | Notas das cores, bipes e música da vitória (só na mestra) |
| Display OLED (I2C1) | SDA GP2 · SCL GP3 · end. `0x3C` | Rodada, placar e mensagens |
| Wi-Fi (CYW43439, 2,4 GHz) | interno | Rede entre as placas |
