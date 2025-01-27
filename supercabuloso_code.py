# title:  Super Cabuloso
# author:  CEFET
# desc:    A fun game made with TIC-80
# site:    https://ascanio.dev/
# license: MIT License
# version: 1.0
# script:  python

# --- CONSTANTES ---
# Definir a largura e a altura da tela
WIDTH = 240
HEIGHT = 136
y_pos = HEIGHT  # Variável global para a posição y


TILE_TAM = 8        # Tamanho de cada tile (8x8 pixels)
SPRITE_WIDTH = 16   # Largura do sprite do personagem
SPRITE_HEIGHT = 16  # Altura do sprite do personagem
COLLISION_WIDTH = 10    # Largura da caixa de colisão
COLLISION_HEIGHT = 15   # Altura da caixa de colisão
OFFSET_X = (SPRITE_WIDTH - COLLISION_WIDTH) / 2  # Offset horizontal para centralizar
OFFSET_Y = SPRITE_HEIGHT - COLLISION_HEIGHT      # Offset vertical para centralizar
GRAVIDADE = 0.2
PULO_FORCA = -3.85

STOP_FRAME = 3200

KEY_TILE_ID   = 3 
DOOR_TILE_ID  = 22  
COIN_TILE_ID  = 4  # Definindo o ID para as moedas

TILES_SOLIDOS = [
    98, 33, 34, 35, 36, 37, 39, 40, 41, 122, 42, 55, 56, 57, 58, 71, 72, 73, 74, 
    87, 88, 89, 90, 103, 104, 119, 105, 106, 121, 54, 48, 50, 51, 52, 67, 68, 
    96, 81, 82, 83, 84, 85, 102, 82, 99, 100, 115, 116, 251, 252, 253, 129, 130, 
    145, 146, 128, 144, 160, 161, 162, 163, 164, 165, 176, 192, 178, 179, 180, 
    182, 195, 196, 209, 210, 211, 212, 227, 213, 228, 226, 208, 230, 240, 243, 
    246, 244, 167, 168, 169, 170, 183, 184, 185, 186, 198, 199, 200, 201, 202, 
    215, 216, 217, 218, 231, 232, 233, 234, 247, 248, 250, 249, 254, 255, 235, 
    236, 238, 172, 173, 111, 127, 177, 197, 240, 245, 65, 114, 118, 76, 70, 38, 64,
    191, 207, 239, 75,

    60 #bloco invisivel
]
TILES_MORTE = [123, 124,125,126]  # TUDO QUE MATA
EMPTY_TILE_ID = 0            # Vazio

PLATAFORM_ID = 172

breaking_platforms = []


SPAWN_POSITIONS = {
    0: (16, 64),    # LVL 0
    1: (0, 32),     # LVL 1
    2: (0, 32),  # LVL 2
    3: (0, 32),     # LVL 3
    4: (232, 124),     # LVL 4
    5: (0, 40),     # LVL 5
    6: (0,0),
    7: (200, 80)
}

frame = 0

key_position = None

nivel_atual = 0 # Começa no lvl 0

moedas_totais = 0             # Total de moedas coletadas em todo o jogo
moedas_coletadas_nivel = 0    # Moedas coletadas no nível atual

# Adicione esta variável global para armazenar os tiles iniciais
initial_level_tiles = {}


def music_init():
    global frame, music_playing
    frame = 0
    music_playing = False
    

def music_upd():
     global frame, music_playing
     frame += 1  # Incrementa o contador de frames
    # loopa a musica
     if frame == STOP_FRAME and music_playing:
        music()  # Para a música
        music_playing = False
        frame = 0

        # loopa a musica
     if frame == 1 and not music_playing:
        music(track=0)  # Toca a música da track 0, loop=0, start_tick=0
        music_playing = True


    #toca musica do cruzeiro
     if nivel_atual == 7 and frame<4000:
        music(track =0, frame = 7, row = 44)
        frame = 4000


# Função para exibir os créditos
# --- INICIALIZACAO GLOBAL ---
y_pos = 136  # Inicializa y_pos fora da função para começar abaixo da tela

# --- FUNCAO CHAMAR CREDITOS ---
def chamar_creditos():
    global y_pos  # Tornar y_pos global para poder modificá-la dentro da função
    
    scroll_speed = 0.125
    credits_text = [
        "Em 1921, foi fundado",
        "o Cruzeiro Esporte Clube",
        "Para muitos, pode ser apenas",
        "um time de futebol",
        "Mas, se voce chegou ate aqui", 
        "Eu sei que pensa diferente.",

        "O Cruzeiro nao e apenas um time,",
        "e um sentimento. Se voce chegou",
        "ate aqui, e porque seu sangue",
        "e cabuloso.",
        "",

        "Seus esforcos nao foram em vao.",
        "Voce se provou um verdadeiro,",
        "torcedor. E, aqui,",
        "Esta sua recompensa:",

        "Voce acaba de ganhar o",
        "MANTO SUPER CABULOSO.",
        "Parabens, ele agora e seu!",
        "Mas lembrese: isso nao e",
        "Apenas uma camisa. Agora,",
        "Ela faz parte de voce.",

        "------------------",
        "DESENVOLVEDORES:",
        "ARTHUR MENDONCA",
        "ELCIO AMORIM",
        "HUMBERTO HENRIQUE",
        "KAUA LUCAS",
        " ",
        "PROFESSOR:",
        "DIEGO ASCANIO",
    ]
    
    # espacamento vertical reduzido para simular fonte menor
    espacamento = 6  # Reduzido de 10 para 6 pixels
    
    # Opcional: Centralizar horizontalmente
    # Calcula a largura média dos textos para centralização (assumindo 6 pixels por caractere)
    largura_media = max([len(line) for line in credits_text]) * 6
    x_centralizado = (240 - largura_media) // 2  # 240 é a largura padrão do TIC-80
    
    # Desenhar o texto rolando para cima, com a cor amarela (cor 7 no TIC-80)
    for i, line in enumerate(credits_text):
        # Opcional: Ajustar x para centralizar cada linha
        largura_texto = len(line) * 6
        x = (240 - largura_texto) // 2  # Centraliza cada linha individualmente
        
        print(line, x, int(y_pos + i * espacamento), 12)  # 
    
    # Atualizar a posição de y para rolar o texto para cima
    y_pos -= scroll_speed

    # Resetar a posição quando o texto sair completamente da tela
    if y_pos < -len(credits_text) * espacamento:
        y_pos = 136  # Reseta a posição y para o fundo da tela (136 é a altura padrão do TIC-80)




def get_level_offset():
    # Retorna o offset X com base no nível atual.
    return 30 * nivel_atual  # 30 tiles por nível

def get_collision_rect(x, y):
    """
    Retorna as coordenadas ajustadas para a caixa de colisão.
    """
    collision_x = x + OFFSET_X
    collision_y = y + OFFSET_Y
    return collision_x, collision_y, COLLISION_WIDTH, COLLISION_HEIGHT

# --- VERIFICAR SE O BLOCO QUE O PERSONAGEM ESTÁ É SÓLIDO ---
def is_solid_tile(x, y):
    """Verifica se a posição (x, y) está em um tile sólido."""
    tile_x = int(x / TILE_TAM)
    tile_y = int(y / TILE_TAM)

    offset_x = get_level_offset()

    # Ajustar tile_x com o offset
    real_tile_x = tile_x + offset_x
    real_tile_y = tile_y  # Se houver offset vertical, ajuste aqui

    tile_id = mget(real_tile_x, real_tile_y)
    if tile_id in TILES_SOLIDOS:
        print(f"Tile sólido detectado em ({real_tile_x}, {real_tile_y}) com ID {tile_id}")
        return True
    return False


# --- FUNÇÃO AUXILIAR PARA OBTER TODOS OS TILES SOBREPOSTOS ---
def get_overlapping_tiles(x, y, width, height):
    """Retorna uma lista de (tile_x, tile_y) que o retângulo (x, y, width, height) está sobrepondo."""
    tiles = []
    
    # Determina o intervalo de tiles cobertos pelo retângulo de colisão
    tile_start_x = int(x / TILE_TAM)
    tile_end_x = int((x + width - 1) / TILE_TAM)
    tile_start_y = int(y / TILE_TAM)
    tile_end_y = int((y + height -1) / TILE_TAM)

    for ty in range(tile_start_y, tile_end_y + 1):
        for tx in range(tile_start_x, tile_end_x + 1):
            tiles.append((tx, ty))
    
    # Remove duplicatas
    tiles = list(set(tiles))
    
    return tiles


# --- CLASSE PERSONAGEM ---
class Personagem:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0
        self.vy = 0
        self.no_chao = False
        self.tem_chave = False
        self.moedas_coletadas = 0  # Variável para moedas coletadas

        # Variáveis de Animação
        self.estado = "parado"       # Estados: parado, andando, pulando, caindo
        self.anim_frame = 0          # Frame atual da animação
        self.anim_timer = 0          # Timer para alternar frames
        self.facing_left = 0
    
    
    def mover(self):
        self._ler_input()
        self._aplicar_gravidade()
        self._mover_e_colidir()
        self.verificar_limites_mapa()  # Chama a verificação de limites após mover e colidir

    # Atualizar o estado de animação
        if self.no_chao:
            if self.vx != 0:
                self.estado = "andando"
            else:
                self.estado = "parado"
        else:
            if self.vy < 0:
                self.estado = "pulando"
            else:
                self.estado = "caindo"
    
        self.atualizar_animacao()



    def atualizar_animacao(self):
        self.anim_timer += 1
        # Alterar o frame a cada 10 frames
        if self.anim_timer >= 10:
            self.anim_timer = 0
            if self.estado == "andando":
                self.anim_frame = (self.anim_frame + 1) % 4  # 4 frames de caminhada
            else:
                self.anim_frame = 0  # Resetar para o primeiro frame em outros estados


    
    def _ler_input(self):
    # Movimento horizontal
        if btn(3):  # Direita
            self.vx = 1
            self.facing_left = 0  # Virado para a direita
        elif btn(2):  # Esquerda
            self.vx = -1
            self.facing_left = 1   # Virado para a esquerda
        else:
            self.vx = 0

        # Pulo
        if self.no_chao and btn(0) or self.no_chao and btn(4):  # Pular
            self.vy = PULO_FORCA
            self.no_chao = False

    def _aplicar_gravidade(self):
        self.vy += GRAVIDADE
    
    def verificar_limites_mapa(self):
        # Limite Horizontal
        if self.x <= 0:
            self.x = 0
            self.vx = 0
        elif self.x >= 240 - SPRITE_WIDTH:
            self.x = 240 - SPRITE_WIDTH
            self.vx = 0

        # Limite Vertical
        if self.y >= 135:
            matar_personagem()
        

    def _mover_e_colidir(self):
        # Movimentação horizontal
        nova_x = self.x + self.vx

        # Atualiza a posição horizontal temporariamente
        self.x = nova_x


        # Obtém a caixa de colisão horizontalmente
        collision_x, collision_y, _, _ = get_collision_rect(self.x, self.y)
        overlapping_tiles = get_overlapping_tiles(collision_x, collision_y, COLLISION_WIDTH, COLLISION_HEIGHT)

    
        # Verifica colisões horizontais
        for tile_x, tile_y in overlapping_tiles:
            if is_solid_tile(tile_x * TILE_TAM, tile_y * TILE_TAM):
                if self.vx > 0:
                    # Colidiu com a esquerda do tile
                    self.x = tile_x * TILE_TAM - COLLISION_WIDTH - OFFSET_X
                elif self.vx < 0:
                    # Colidiu com a direita do tile
                    self.x = (tile_x + 1) * TILE_TAM - OFFSET_X
                self.x = int(self.x)  # Converter para inteiro para evitar frações
                self.vx = 0
                break  # Interrompe após a primeira colisão

    # Movimentação vertical
        nova_y = self.y + self.vy

    # Atualiza a posição vertical temporariamente
        self.y = nova_y

        collision_x, collision_y, _, _ = get_collision_rect(self.x, self.y)
        overlapping_tiles = get_overlapping_tiles(collision_x, collision_y, COLLISION_WIDTH, COLLISION_HEIGHT)

    

    # Verifica colisões verticais
        for tile_x, tile_y in overlapping_tiles:
            if is_solid_tile(tile_x * TILE_TAM, tile_y * TILE_TAM):
                if self.vy > 0:
                    # Colidiu com a parte de cima do tile (chão)
                    self.y = tile_y * TILE_TAM - COLLISION_HEIGHT - OFFSET_Y
                    self.vy = 0
                    self.no_chao = True
                elif self.vy < 0:
                    # Colidiu com a parte de baixo do tile (céu)
                    self.y = (tile_y + 1) * TILE_TAM - OFFSET_Y
                    self.vy = 0
                self.y = int(self.y)  # Converter para inteiro para evitar frações
                break  # Interrompe após a primeira colisão



    def desenhar(self):
    # Selecionar o sprite com base no estado
        if self.estado == "parado":
            sprite_id = 334
        elif self.estado == "andando":
        # Selecionar entre os sprites de caminhada
            sprites_andando = [270, 300, 302, 332]
            sprite_id = sprites_andando[self.anim_frame]
        elif self.estado == "pulando":
            sprite_id = 364
        elif self.estado == "caindo":
            sprite_id = 366
        else:
            sprite_id = 334  # Fallback para parado


        # Determinar se o sprite deve ser invertido horizontalmente

        # Desenhar o sprite com escala 2x para 16x16 pixels
        spr(sprite_id, int(self.x), int(self.y),colorkey=0, scale = 1,w= 2, h=2,flip = self.facing_left)

        # Depuração: desenhar a área de colisão
        #rect(int(self.x), int(self.y), SPRITE_WIDTH, SPRITE_HEIGHT, 8)  # Cor 8 (cinza)



def checar_menu():
    
    if nivel_atual == 0: 
        if btnp(4): # apertou A ou Z
            proximo_nivel()


def checar_creditos():
    if nivel_atual == 7:
        spr(256,0,0,0,1,0,0,12,16)
        chamar_creditos()

#-----LOGICA DA PLATAFORMA-----
def checar_plataforma():
    # Obtém a posição e tamanho do personagem
    x, y = personagem.x, personagem.y
    width, height = SPRITE_WIDTH, SPRITE_HEIGHT

    # Calcula a posição abaixo do personagem para detectar plataformas
    # Vamos verificar uma faixa de tiles logo abaixo do personagem
    y_baixo = y + height
    # Verificar uma pequena distância abaixo para capturar plataformas
    for dy in range(1, TILE_TAM + 1):
        y_to_check = y_baixo + dy
        # Obter todos os tiles que estão diretamente abaixo do personagem
        overlapping_tiles = get_overlapping_tiles(x, y_to_check, width, 1)  # altura 1 para uma linha abaixo
        for tile_coord in overlapping_tiles:
            tile_x, tile_y = tile_coord
            offset_x = get_level_offset()
            tile_id = mget(tile_x + offset_x, tile_y)

            if tile_id == PLATAFORM_ID:
                platform_pos = (tile_x + offset_x, tile_y)
                # Verifica se a plataforma já está na lista para evitar múltiplas adições
                if platform_pos not in [(p['x'], p['y']) for p in breaking_platforms]:
                    breaking_platforms.append({
                        'x': platform_pos[0],
                        'y': platform_pos[1],
                        'timer': 40  # 40 frames é aproximadamente 0.666 segundos
                    })
                    print(f"Plataforma em {platform_pos} iniciando quebra.")

def atualizar_breaking_platforms():
    global breaking_platforms
    for platform in breaking_platforms[:]:  # Iterar sobre uma cópia da lista
        # Atualiza o timer
        platform['timer'] -= 1

        # Se o timer chegar a 20 frames, altera o sprite para 173
        if platform['timer'] == 20:
            mset(platform['x'], platform['y'], 173)

        # Se o timer chegar a 0, quebra a plataforma
        if platform['timer'] <= 0:
            mset(platform['x'], platform['y'], EMPTY_TILE_ID)  # Substitui por tile vazio
            breaking_platforms.remove(platform)
            print(f"Plataforma em ({platform['x']}, {platform['y']}) quebrou (tile 0).")

#----LOGICA DA CHAVE E MOEDAS-----
def checar_chave_e_porta():
    global key_position, moedas_totais, moedas_coletadas_nivel
    
    # Obtém a posição e tamanho do personagem
    x, y = personagem.x, personagem.y
    width, height = SPRITE_WIDTH, SPRITE_HEIGHT
    
    # Obtém todos os tiles sobrepostos pelo personagem
    overlapping_tiles = get_overlapping_tiles(x, y, width, height)
    
    for tile_coord in overlapping_tiles:
        tile_x, tile_y = tile_coord
        offset_x = get_level_offset()
        tile_id = mget(tile_x + offset_x, tile_y)
        
        # Se for o tile da chave e não temos a chave ainda
        if tile_id == KEY_TILE_ID and not personagem.tem_chave:
            print("Pegou chave")
            personagem.tem_chave = True
            sfx(0,20,40,volume=5)
            
            # Apagar a chave do mapa
            mset(tile_x + offset_x, tile_y, EMPTY_TILE_ID)
            
            # Guardar a posição da chave (com offset e nível)
            key_position = (tile_x + offset_x, tile_y, nivel_atual)
        
        if tile_id == 12 or tile_id == 13 or tile_id == 28 or tile_id == 29:
            proximo_nivel()
            


        # Se for o tile da porta
        if tile_id == DOOR_TILE_ID :
            if personagem.tem_chave:
                # Abre a porta -> vai pro próximo nível
                personagem.tem_chave = False
                proximo_nivel()
        
        # Se for o tile de moeda
        if tile_id == COIN_TILE_ID:
            print("Pegou uma moeda!")
            moedas_totais += 1
            moedas_coletadas_nivel += 1
            sfx(0, 27,duration=20,volume=5) 
            
            # Apagar a moeda do mapa
            mset(tile_x + offset_x, tile_y, EMPTY_TILE_ID)

# LOGICA PARA CHECAR SE O PERSONAGEM MORREU
def checar_morte():
    # Obtém a posição e tamanho do personagem
    x, y = personagem.x, personagem.y
    width, height = SPRITE_WIDTH, SPRITE_HEIGHT
    
    # Obtém todos os tiles sobrepostos pelo personagem
    overlapping_tiles = get_overlapping_tiles(x, y, width, height)
    
    for tile_coord in overlapping_tiles:
        tile_x, tile_y = tile_coord
        offset_x = get_level_offset()
        tile_id = mget(tile_x + offset_x, tile_y)
        
        # Se o tile_id estiver na lista de tiles de morte, mata/reinicia o personagem
        if tile_id in TILES_MORTE:
            matar_personagem()
            break  # Evita múltiplas chamadas caso esteja sobre mais de um tile de morte

def matar_personagem():
    global moedas_totais, moedas_coletadas_nivel
    sfx(1,duration= 40,volume = 3)
    # Resetar o nível atual
    reset_level()
    
    personagem.vx = 0
    personagem.vy = 0

    # Resetar a posição do personagem
    x, y = SPAWN_POSITIONS[nivel_atual]
    personagem.x = x
    personagem.y = y
    personagem.tem_chave = False
    
    # Subtrair as moedas coletadas no nível atual do total
    moedas_totais -= moedas_coletadas_nivel
    moedas_coletadas_nivel = 0

    # Restaurar as moedas do nível atual no mapa
    offset_x = get_level_offset()
    for y_tile in range(17):  # Altura do mapa
        for x_tile in range(30):  # Largura do nível
            tile_index = x_tile + y_tile * 30
            tile = initial_level_tiles[nivel_atual][tile_index]
            if tile == COIN_TILE_ID:
                mset(offset_x + x_tile, y_tile, COIN_TILE_ID)

def proximo_nivel():
    global nivel_atual, moedas_coletadas_nivel
    nivel_atual += 1
    
    # Pega a posição inicial do novo nível no dicionário
    if nivel_atual in SPAWN_POSITIONS:
        x, y = SPAWN_POSITIONS[nivel_atual]
        personagem.x = x
        personagem.y = y
    
    # Resetar as moedas coletadas no nível anterior
    moedas_coletadas_nivel = 0

# --- VARIAVEL GLOBAL ---
personagem = None

# --- MAIN ---
def init():
    global personagem, initial_level_tiles
    x, y = SPAWN_POSITIONS[nivel_atual]  # Primeiro spawn dele na hash table
    personagem = Personagem(x, y)
    
    # Salvar os tiles iniciais para cada nível
    num_levels = len(SPAWN_POSITIONS)
    for level in range(num_levels):
        initial_level_tiles[level] = []
        offset_x = 30 * level  # 30 tiles por nível
        for y_tile in range(17):  # Supondo que a altura do mapa é 17 tiles
            for x_tile in range(30):
                tile = mget(offset_x + x_tile, y_tile)
                initial_level_tiles[level].append(tile)

def reset_level():
    global breaking_platforms
    breaking_platforms = []  # Limpa as plataformas quebradas
    
    offset_x = get_level_offset()
    for y_tile in range(17):  # Altura do mapa
        for x_tile in range(30):  # Largura do nível
            tile_index = x_tile + y_tile * 30
            tile = initial_level_tiles[nivel_atual][tile_index]
            mset(offset_x + x_tile, y_tile, tile)

def update():
    personagem.mover()
    checar_chave_e_porta()
    checar_plataforma()
    atualizar_breaking_platforms()
    checar_morte()
    checar_menu()

def draw():
    cls()
    # Obter o offset atual

    offset_x = get_level_offset()
    offset_y = 0  # Se houver deslocamento vertical, ajuste aqui

    # Desenhar o mapa com base no offset
    map(offset_x, offset_y, 30, 17, 0, 0)  # Supondo que cada nível tem 30 tiles de largura

    
    checar_creditos()

    personagem.desenhar()

    #parte do menuzin
    if nivel_atual ==  0:
            print("Pressione Z para jogar!", 50, 65, 12)



    if nivel_atual != 7:
        if personagem.tem_chave:
            print("Com chave!", 1, 1, 12)
        else:
            print("Sem chave", 1, 1, 12)

        # Exibir a quantidade total de moedas coletadas
        print(f"Moedas: {moedas_totais}", 180, 1, 12)


    ##print(personagem.no_chao, 1,20,12)

# INICIALIZA O PERSONAGEM
init()
music_init()

def TIC():
    global y_pos
    update()
    draw()
    music_upd() 
