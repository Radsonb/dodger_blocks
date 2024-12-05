import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonte
font = pygame.font.SysFont("Arial", 30)
game_over_font = pygame.font.SysFont("Arial", 60)

# Jogador
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10

# Blocos
block_size = 50
block_list = [{"pos": [random.randint(0, WIDTH - block_size), 0], "speed": 5}]

# Pontuação
score = 0

# Relógio
clock = pygame.time.Clock()

# Detectar colisão
def detect_collision(player_pos, block_pos):
    px, py = player_pos
    bx, by = block_pos
    return (bx < px < bx + block_size or bx < px + player_size < bx + block_size) and (by < py < by + block_size)

# Tela de Game Over
def show_game_over():
    screen.fill(WHITE)
    game_over_text = game_over_font.render("GAME OVER", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    button_text = font.render("TRY AGAIN", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, GRAY, button_rect)
    screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    main()

# Função principal
def main():
    global player_pos, block_list, score
    player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
    block_list = [{"pos": [random.randint(0, WIDTH - block_size), 0], "speed": 5}]
    score = 0

    game_over = False
    while not game_over:
        screen.fill(WHITE)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimento do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed

        # Movimento dos blocos e aumento de dificuldade
        for block in block_list:
            block["pos"][1] += block["speed"]
            if block["pos"][1] > HEIGHT:
                block["pos"] = [random.randint(0, WIDTH - block_size), 0]
                score += 1

                # Aumentar dificuldade com a pontuação
                if score % 5 == 0:  # A cada 5 pontos, aumentar dificuldade
                    block["speed"] += 1
                    block_list.append({"pos": [random.randint(0, WIDTH - block_size), 0], "speed": block["speed"]})

        # Desenhar jogador e blocos
        pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
        for block in block_list:
            pygame.draw.rect(screen, RED, (block["pos"][0], block["pos"][1], block_size, block_size))

        # Verificar colisão
        for block in block_list:
            if detect_collision(player_pos, block["pos"]):
                game_over = True

        # Exibir pontuação
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Atualizar a tela
        pygame.display.update()
        clock.tick(30)

    show_game_over()

# Iniciar o jogo
main()
