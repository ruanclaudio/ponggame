import socket
import threading
import pygame
import pickle
import random

# Configurações do jogo
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 10
WHITE = (255, 255, 255)
WIN_SCORE = 10
BLACK = (0, 0, 0)
score = [0, 0]

FPS = 60
PORT = 5555
IP = "0.0.0.0"

# Estados dos jogadores
players = {
    0: {"y": HEIGHT // 2 - PADDLE_HEIGHT // 2},
    1: {"y": HEIGHT // 2 - PADDLE_HEIGHT // 2}
}

# Bola
ball = {
    "x": WIDTH // 2,
    "y": HEIGHT // 2,
    "vx": 5,
    "vy": 5
}

# Lista para armazenar flags de "pronto"
ready_flags = [False, False]

# Função para lidar com cada cliente
def handle_client(conn, player_id):
    global players
    conn.send(pickle.dumps(player_id))
    print(f"[PLAYER {player_id}] conectado. Aguardando READY...")

    # Espera o jogador enviar "READY"
    while True:
        try:
            data = conn.recv(1024)
            status = pickle.loads(data)
            if status == "READY":
                ready_flags[player_id] = True
                print(f"[PLAYER {player_id}] está pronto!")
                break
        except:
            pass

    # Loop de controle do jogador
    while True:
        try:
            data = conn.recv(1024)
            direction = pickle.loads(data)

            if direction == -1:
                players[player_id]["y"] -= 10
            elif direction == 1:
                players[player_id]["y"] += 10
        except:
            break

    conn.close()
    print(f"[PLAYER {player_id}] desconectado.")

# Inicializa o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(2)

print("[SERVIDOR] Aguardando conexões...")

clients = []
for i in range(2):
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn, i)).start()

# Aguarda todos os jogadores ficarem prontos
print("[SERVIDOR] Esperando jogadores digitarem READY...")
while not all(ready_flags):
    pass  # Espera até os dois estarem prontos

print("[SERVIDOR] Todos os jogadores estão prontos! Iniciando o jogo...")

# Inicializa pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Server")
font = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()

# Função de desenho
def draw():
    win.fill(BLACK)

    # Raquetes
    pygame.draw.rect(win, WHITE, (10, players[0]["y"], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(win, WHITE, (WIDTH - 20, players[1]["y"], PADDLE_WIDTH, PADDLE_HEIGHT))

    # Bola
    pygame.draw.ellipse(win, WHITE, (ball["x"], ball["y"], BALL_SIZE, BALL_SIZE))

    # Placar
    score_text = font.render(f"{score[0]}   x   {score[1]}", True, WHITE)
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.update()

# Loop principal do jogo
while True:
    if ball["x"] <= 0:
        score[1] += 1
        ball["x"], ball["y"] = WIDTH // 2, HEIGHT // 2
        ball["vx"] = random.choice([-5, 5])
        ball["vy"] = random.choice([-5, 5])

        if score[1] >= WIN_SCORE:
            winner_text = font.render("Player 1 venceu!", True, WHITE)
            win.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)

            score = [0, 0]
            ball.update({"x": WIDTH // 2, "y": HEIGHT // 2, "vx": 5, "vy": 5})
            players[0]["y"] = HEIGHT // 2 - PADDLE_HEIGHT // 2
            players[1]["y"] = HEIGHT // 2 - PADDLE_HEIGHT // 2

    elif ball["x"] >= WIDTH:
        score[0] += 1
        ball["x"], ball["y"] = WIDTH // 2, HEIGHT // 2
        ball["vx"] = random.choice([-5, 5])
        ball["vy"] = random.choice([-5, 5])

        if score[0] >= WIN_SCORE:
            winner_text = font.render("Player 0 venceu!", True, WHITE)
            win.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)

            score = [0, 0]
            ball.update({"x": WIDTH // 2, "y": HEIGHT // 2, "vx": 5, "vy": 5})
            players[0]["y"] = HEIGHT // 2 - PADDLE_HEIGHT // 2
            players[1]["y"] = HEIGHT // 2 - PADDLE_HEIGHT // 2

    clock.tick(FPS)

    ball["x"] += ball["vx"]
    ball["y"] += ball["vy"]

    # Colisão com topo/baixo
    if ball["y"] <= 0 or ball["y"] >= HEIGHT - BALL_SIZE:
        ball["vy"] *= -1

    # Colisão com as raquetes
    if (ball["x"] <= 20 and players[0]["y"] < ball["y"] < players[0]["y"] + PADDLE_HEIGHT):
        ball["vx"] *= -1
    elif (ball["x"] >= WIDTH - 30 and players[1]["y"] < ball["y"] < players[1]["y"] + PADDLE_HEIGHT):
        ball["vx"] *= -1

    # Envia o estado atualizado para todos os clientes
    state = {"players": players, "ball": ball, "score": score}
    for conn in clients:
        try:
            conn.sendall(pickle.dumps(state))
        except:
            pass

    draw()
