import network
import socket
from machine import Pin, I2C, PWM
from sh1107_bitdoglab import SH1107_I2C
import neopixel
import time
import random

# ==========================================
# 1. CONFIGURAÇÕES DA ARENA (AJUSTE AQUI)
# ==========================================
SSID_REDE = "SIMON_LAB_1"    # Mestra 1 usa "SIMON_LAB_1", Mestra 2 usa "SIMON_LAB_2"
TIME_1 = "AZUL"              # Mestra 1 usa "AZUL", Mestra 2 usa "ROXO"
TIME_2 = "VERMELHO"           # Mestra 1 usa "VERMELHO", Mestra 2 usa "LARANJA"
SENHA_REDE = "simon123"

# ==========================================
# 2. CONFIGURAÇÃO DE HARDWARE E WI-FI
# ==========================================
ap = network.WLAN(network.AP_IF)
ap.config(essid=SSID_REDE, password=SENHA_REDE, channel=1) #Mestra 1 usa channel 1, Mestra 2 usa channel 11
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
oled = SH1107_I2C(128, 128, i2c, addr=0x3C, rotate_180=False)

btn_a = Pin(5, Pin.IN, Pin.PULL_UP)
btn_b = Pin(6, Pin.IN, Pin.PULL_UP)
np = neopixel.NeoPixel(Pin(7), 25)

buzzer = PWM(Pin(21))
buzzer.duty_u16(0)

ap = network.WLAN(network.AP_IF)
ap.config(essid=SSID_REDE, password=SENHA_REDE)
ap.active(True)

while ap.active() == False:
    pass

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('0.0.0.0', 8080))
udp.setblocking(False) 

# ==========================================
# 3. LÓGICA DO JOGO
# ==========================================
CONFIG_CORES = {
    "VERDE":    {"rgb": (0, 50, 0),   "freq": 415},
    "VERMELHO": {"rgb": (50, 0, 0),   "freq": 311},
    "AMARELO":  {"rgb": (50, 50, 0),  "freq": 252},
    "AZUL":     {"rgb": (0, 0, 50),   "freq": 209}
}

CORES = list(CONFIG_CORES.keys())
sequencia_mestra = []
rodada_atual = 1
placar_geral = {TIME_1: 0, TIME_2: 0}

def atualizar_display(titulo, linha1="", linha2="", linha3="", linha4=""):
    oled.fill(0)
    oled.rect(0, 0, 128, 128, 1)
    oled.text(titulo, 10, 10)
    oled.hline(0, 25, 128, 1)
    oled.text(linha1, 10, 40)
    oled.text(linha2, 10, 60)
    oled.text(linha3, 10, 80)
    oled.text(linha4, 10, 100)
    oled.show()

def set_cor_matriz(rgb):
    for i in range(25):
        np[i] = rgb
    np.write()

def tocar_nota(freq, volume=32768):
    if freq > 0:
        buzzer.freq(freq)
        buzzer.duty_u16(volume)
    else:
        buzzer.duty_u16(0)

def acionar_cor_e_som(cor_nome, tempo):
    cfg = CONFIG_CORES[cor_nome]
    set_cor_matriz(cfg["rgb"])
    tocar_nota(cfg["freq"])
    time.sleep(tempo)
    set_cor_matriz((0, 0, 0))
    tocar_nota(0)

def som_erro():
    set_cor_matriz((50, 0, 0))
    tocar_nota(150)
    time.sleep(1.5)
    tocar_nota(0)
    set_cor_matriz((0, 0, 0))

def tocar_musica_mario():
    """ Toca o arpejo classico de 'Level Clear' do Super Mario Bros """
    # Formato: (Frequência em Hz, Duração em segundos)
    notas = [
        (392, 0.15),  # G4
        (523, 0.15),  # C5
        (659, 0.15),  # E5
        (784, 0.15),  # G5
        (1047, 0.15), # C6
        (1319, 0.15), # E6
        (1568, 0.35), # G6 (Nota longa)
        (1319, 0.4)   # E6 (Final longa)
    ]
    
    for freq, duracao in notas:
        tocar_nota(freq, 30000)
        time.sleep(duracao)
        tocar_nota(0) # Breve silêncio para separar as notas
        time.sleep(0.02)

def celebrar_vitoria(equipe_vencedora):
    # Acende a matriz na cor correspondente à equipe
    if equipe_vencedora == TIME_1:
        set_cor_matriz((0, 50, 50)) 
    else:
        set_cor_matriz((50, 25, 0))
        
    # Dispara a música do Mario em vez do bipe genérico
    tocar_musica_mario()
    
    set_cor_matriz((0,0,0))

def exibir_sequencia():
    atualizar_display(f"RODADA {rodada_atual}", "Memorize a", "sequencia!")
    time.sleep(1.5)
    for cor in sequencia_mestra:
        atualizar_display("PISCA:", cor, "", "Atento...")
        acionar_cor_e_som(cor, 0.7)
        time.sleep(0.3)
    atualizar_display("VALENDO!", "Aguardando", "ambas as equipes...")

# ==========================================
# 4. VALIDAÇÃO DE REDE SIMULTÂNEA
# ==========================================
def escutar_equipes_udp():
    passos = {TIME_1: 0, TIME_2: 0}
    status = {TIME_1: "JOGANDO", TIME_2: "JOGANDO"}
    tamanho_seq = len(sequencia_mestra)
    
    while True:
        try:
            udp.recvfrom(64)
        except OSError:
            break
            
    while status[TIME_1] == "JOGANDO" or status[TIME_2] == "JOGANDO":
        if btn_b.value() == 0:
            return "RESET"

        try:
            data, addr = udp.recvfrom(64)
            mensagem = data.decode('utf-8').strip().upper()
            
            if "," in mensagem:
                equipe, cor_recebida = mensagem.split(',')
                equipe = equipe.strip()
                cor_recebida = cor_recebida.strip()
                
                if equipe in status and status[equipe] == "JOGANDO":
                    if cor_recebida == sequencia_mestra[passos[equipe]]:
                        passos[equipe] += 1
                        tocar_nota(800)
                        time.sleep(0.05)
                        tocar_nota(0)
                        
                        if passos[equipe] == tamanho_seq:
                            status[equipe] = "ACERTO"
                    else:
                        status[equipe] = "ERRO"
                        tocar_nota(150)
                        time.sleep(0.2)
                        tocar_nota(0)
                        
        except OSError:
            pass 
            
        time.sleep(0.005)
        
    return status 

# ==========================================
# 5. EXECUÇÃO PRINCIPAL
# ==========================================
def aguardar_inicio():
    atualizar_display("NOVO JOGO", "Aperte Botao A", f"{TIME_1}: {placar_geral[TIME_1]}", f"{TIME_2}: {placar_geral[TIME_2]}")
    while btn_a.value() == 1:
        time.sleep(0.1)
    time.sleep(0.5)

aguardar_inicio()

while True:
    if len(sequencia_mestra) < rodada_atual:
        sequencia_mestra.append(random.choice(CORES))
    
    exibir_sequencia()
    resultado = escutar_equipes_udp()
    
    if resultado == "RESET":
        atualizar_display("RESET", "Limpando", "sequencia...")
        som_erro()
        sequencia_mestra.clear()
        rodada_atual = 1
        aguardar_inicio()
        
    else:
        if resultado[TIME_1] == "ACERTO" and resultado[TIME_2] == "ACERTO":
            atualizar_display("RODADA FIM", "Ambas acertaram!", "Avancando...")
            tocar_nota(600)
            time.sleep(0.2)
            tocar_nota(800)
            time.sleep(0.5)
            tocar_nota(0)
            rodada_atual += 1
            
        elif resultado[TIME_1] == "ERRO" and resultado[TIME_2] == "ERRO":
            atualizar_display("EMPATE!", "Ambas erraram!", "Repetindo", "a sequencia...")
            som_erro()
            time.sleep(1.5)
            
        else:
            vencedor = TIME_1 if resultado[TIME_1] == "ACERTO" else TIME_2
            placar_geral[vencedor] += 1
            
            atualizar_display("FIM DE JOGO!", f"Venceu: {vencedor}", f"{TIME_1}: {placar_geral[TIME_1]}", f"{TIME_2}: {placar_geral[TIME_2]}")
            celebrar_vitoria(vencedor)
            time.sleep(4)
            
            sequencia_mestra.clear()
            rodada_atual = 1
            aguardar_inicio()