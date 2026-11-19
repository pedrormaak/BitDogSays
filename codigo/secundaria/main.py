import network
import socket
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import neopixel
import time

# ==========================================
# 1. CONFIGURAÇÃO DA PLACA (AJUSTE AQUI)
# ==========================================
WIFI_SSID = "SIMON_LAB_2"     #1 para mestra 1 ou 2 para mestra 2
EQUIPE = "ROXO"              #AZUL/VERMELHO para mestra 1 ou ROXO/LARANJA para mestra 2

COR_BOTAO_A = "VERDE"     #AZUL, VERMELHO, VERDE, AMARELO
COR_BOTAO_B = "AMARELO"   #AZUL, VERMELHO, VERDE, AMARELO

# ==========================================
# 2. CONFIGURAÇÃO DE HARDWARE
# ==========================================
btn_a = Pin(5, Pin.IN, Pin.PULL_UP)
btn_b = Pin(6, Pin.IN, Pin.PULL_UP)
np = neopixel.NeoPixel(Pin(7), 25)

# Inicialização do Display 128x64
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

CONFIG_CORES = {
    "VERDE":    (0, 50, 0),
    "VERMELHO": (50, 0, 0),
    "AMARELO":  (50, 50, 0),
    "AZUL":     (0, 0, 50)
}

RGB_A = CONFIG_CORES[COR_BOTAO_A]
RGB_B = CONFIG_CORES[COR_BOTAO_B]

# ==========================================
# 3. INTERFACE E REDE
# ==========================================
def atualizar_display_slave():
    oled.fill(0)
    oled.rect(0, 0, 128, 64, 1) # Moldura ajustada para 64 de altura
    oled.text(f"EQUIPE {EQUIPE}", 10, 10)
    oled.hline(0, 25, 128, 1)
    oled.text(f"A: {COR_BOTAO_A}", 10, 35)
    oled.text(f"B: {COR_BOTAO_B}", 10, 50)
    oled.show()

def tela_repouso():
    np.fill((0,0,0))
    for i in [4,3, 5,6, 14,13, 15,16, 24,23]:
        np[i] = RGB_A
    for i in [1,0, 8,9, 11,10, 18,19, 21,20]:
        np[i] = RGB_B
    np.write()

def piscar_feedback(rgb_base):
    brilho_max = (min(rgb_base[0]*4, 255), min(rgb_base[1]*4, 255), min(rgb_base[2]*4, 255))
    np.fill(brilho_max)
    np.write()
    time.sleep(0.15)
    tela_repouso()

atualizar_display_slave()

# Conexão Wi-Fi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(WIFI_SSID, "simon123")

while not sta.isconnected():
    np.fill((10, 10, 10))
    np.write()
    time.sleep(0.2)
    np.fill((0, 0, 0))
    np.write()
    time.sleep(0.2)

tela_repouso()

# Configuração UDP
UDP_IP = "192.168.4.1"
UDP_PORT = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ==========================================
# 4. LOOP PRINCIPAL DE GATILHOS
# ==========================================
while True:
    if btn_a.value() == 0:
        sock.sendto(f"{EQUIPE},{COR_BOTAO_A}".encode('utf-8'), (UDP_IP, UDP_PORT))
        piscar_feedback(RGB_A)
        while btn_a.value() == 0:
            time.sleep(0.05)
        time.sleep(0.1)

    elif btn_b.value() == 0:
        sock.sendto(f"{EQUIPE},{COR_BOTAO_B}".encode('utf-8'), (UDP_IP, UDP_PORT))
        piscar_feedback(RGB_B)
        while btn_b.value() == 0:
            time.sleep(0.05)
        time.sleep(0.1)

    time.sleep(0.01)
