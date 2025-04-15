import socket
import pickle
import pygame
import sys

WIDTH, HEIGHT = 800, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP do servidor
server_ip = input("Digite o IP do servidor: ")
client_socket.connect((server_ip, 5555))
player_id = pickle.loads(client_socket.recv(1024))
ready = input("Digite 'ready' quando estiver pronto: ").strip().lower()
while ready != "ready":
    ready = input("Digite 'ready' quando estiver pronto: ").strip().lower()
client_socket.sendall(pickle.dumps("READY"))


print(f"Você é o player {player_id}")

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Pong - Jogador {player_id}")
font = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()

def draw(state):
    win.fill(BLACK)

    # Desenha raquetes
    pygame.draw.rect(win, WHITE, (10, state["players"][0]["y"], 10, 100))
    pygame.draw.rect(win, WHITE, (WIDTH - 20, state["players"][1]["y"], 10, 100))

    # Desenha bola
    pygame.draw.ellipse(win, WHITE, (state["ball"]["x"], state["ball"]["y"], 10, 10))

    # Desenha placar
    score_text = font.render(f"{state['score'][0]}   x   {state['score'][1]}", True, WHITE)
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.update()

while True:
    clock.tick(60)

    keys = pygame.key.get_pressed()
    direction = 0
    if keys[pygame.K_UP]:
        direction = -1
    elif keys[pygame.K_DOWN]:
        direction = 1
    client_socket.sendall(pickle.dumps(direction))

    try:
        data = client_socket.recv(4096)
        if not data:
            break
        state = pickle.loads(data)
        draw(state)
    except:
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
