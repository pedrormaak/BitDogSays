# Softwares, bibliotecas e ferramentas

## Ferramentas

| Ferramenta | Para quê |
|---|---|
| [MicroPython para Raspberry Pi Pico W](https://micropython.org/download/RPI_PICO_W/) | Firmware gravado em cada placa (arquivo `.uf2`) |
| [Thonny](https://thonny.org/) | IDE usada para editar os códigos, copiar os arquivos e ver o console da placa |

## Bibliotecas

| Biblioteca | Origem | Onde é usada |
|---|---|---|
| `network` | nativa do MicroPython | Wi-Fi: ponto de acesso na mestra e cliente nas secundárias |
| `socket` | nativa | Envio e recebimento de pacotes UDP |
| `machine` (`Pin`, `I2C`, `PWM`) | nativa | Botões, display e buzzer |
| `neopixel` | nativa | Matriz de LEDs 5×5 |
| `framebuf` | nativa | Desenho de texto e formas nos displays |
| `time`, `random` | nativas | Temporização e sorteio das cores |
| [`sh1107_bitdoglab.py`](../codigo/mestra/sh1107_bitdoglab.py) | incluída neste repositório | Driver do OLED 128×128 da mestra |
| [`ssd1306.py`](../codigo/secundaria/ssd1306.py) | driver oficial do MicroPython, incluído aqui | Driver do OLED 128×64 das secundárias |

## Como gravar o MicroPython

1. Segure o botão **BOOTSEL** da Pico W e conecte o cabo USB no computador.
2. A placa aparece como um pendrive (`RPI-RP2`).
3. Arraste o arquivo `.uf2` do MicroPython para esse pendrive. A placa reinicia sozinha.
4. No Thonny, vá em *Ferramentas → Opções → Interpretador* e escolha **MicroPython (Raspberry Pi Pico)**.
