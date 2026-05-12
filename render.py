import pygame
from game import draw_grid, draw_ships, can_place_ship, count_remaining_ships
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


def draw_ships_list(screen, ships_dict, position, show_zero=True):
    font = pygame.font.Font(None, 30)  # Стандартный шрифт
    x, y = position
    line_height = 30
    ship_sizes = sorted(ships_dict.keys(), reverse=True)
    for ship_size in ship_sizes:
        count = ships_dict.get(ship_size, 0)
        if count == 0 and show_zero == False:
            continue
        text = f"{ship_size}-палубный: {count}"
        color = (255, 100, 100) if count == 0 else (255, 255, 255)
        label = font.render(text, True, color)
        screen.blit(label, (x, y))
        y += line_height

def render_game(screen, left_grid_x, left_grid_y, right_grid_x, right_grid_y,grid_size,
                cell_size, player_grid, computer_grid, current_cells, ships_to_place,
                animations, game_phase, show_enemy_ships):
    # здесь позже будет игровая логикa
    # Рисуем сетки
    draw_grid(screen, left_grid_x, left_grid_y, grid_size=10, player="Игрок")
    draw_grid(screen, right_grid_x, right_grid_y, grid_size=10, player="Компьютер")
    draw_ships(screen, player_grid, left_grid_x, left_grid_y, grid_size, cell_size, show_ships=True)
    draw_ships(screen, computer_grid, right_grid_x, right_grid_y, grid_size, cell_size, show_ships=show_enemy_ships)
    # draw_ships_list(screen, ships_to_place, (left_grid_x, left_grid_y + grid_size * cell_size + 20))

    # выбор данных для списка кораблей
    if game_phase == 'placing':
        # фаза расстановки: показываем что осталось поставить игроку
        ships_info = ships_to_place
        list_title = 'Осталось поставить:'
        list_pos = (left_grid_x, left_grid_y + grid_size * cell_size + 20)
    else:
        # фаза боя: показываем кол-во кораблей противника
        ships_info = count_remaining_ships(computer_grid)
        list_title = 'Корабли противника:'
        list_pos = (right_grid_x, right_grid_y + grid_size * cell_size + 20)

    # рисуем заголовок списка
    font = pygame.font.Font(None, 30)
    title_label = font.render(list_title, True, (255, 255, 0))
    screen.blit(title_label, list_pos)
    # рисуем список
    draw_ships_list(screen, ships_info, (list_pos[0], list_pos[1] + 30), show_zero=True)

    intersect = any(player_grid[r][c] == 1 for (r, c) in current_cells)

    if intersect or (current_cells and not can_place_ship(player_grid, current_cells)):
        highlight_color = (255, 0, 0)
    else:
        highlight_color = (255, 255, 0)

    if not all(count==0 for count in ships_to_place.values()) and game_phase == 'placing':
        btn_rect = pygame.Rect(50, 50, 300, 50)
        mouse_pos = pygame.mouse.get_pos()
        if btn_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (150, 220, 150), btn_rect)
        else:
            pygame.draw.rect(screen, (100, 200, 100), btn_rect)

        font = pygame.font.Font(None, 36)
        text = font.render('Случайная расстановка', True, (255, 255, 255))
        screen.blit(text, (60, 55))

    if game_phase == 'placing' and all(count==0 for count in ships_to_place.values()):
        btn_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 50, 300, 50)
        mouse_pos = pygame.mouse.get_pos()
        if btn_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (150, 220, 150), btn_rect)
        else:
            pygame.draw.rect(screen, (100, 200, 100), btn_rect)
        font = pygame.font.Font(None, 36)
        text = font.render('Начать бой!', True, (255, 255, 255))
        screen.blit(text, (btn_rect.x + 10, btn_rect.y + 5))

    # Кнопка "Показать/Скрыть корабли"
    toggle_btn_rect = pygame.Rect(SCREEN_WIDTH - 250, 50, 200, 40)
    mouse_pos = pygame.mouse.get_pos()
    toggle_color = (200, 100, 100) if show_enemy_ships else (100, 100, 200)
    pygame.draw.rect(screen, toggle_color, toggle_btn_rect)
    font = pygame.font.Font(None, 30)
    toggle_text = font.render('Скрыть' if show_enemy_ships else 'Показать', True, (255, 255, 255))
    screen.blit(toggle_text, (toggle_btn_rect.x + 30, toggle_btn_rect.y + 8))

    # подсвечиваем current_cells
    for (r, c) in current_cells:
        rect_x = left_grid_x + c * cell_size
        rect_y = left_grid_y + r * cell_size

        rect = pygame.Rect(rect_x, rect_y, cell_size, cell_size)
        pygame.draw.rect(screen, highlight_color, rect, 2)

    # кнопка выхода в меню
    menu_button = pygame.Rect(SCREEN_WIDTH - 175, 10, 165, 40)
    mouse_pos = pygame.mouse.get_pos()
    b_color = (255, 0, 0) if menu_button.collidepoint(mouse_pos) else (200, 0, 0)
    pygame.draw.rect(screen, b_color, menu_button, border_radius=8)
    font = pygame.font.Font(None, 30)
    btn_text = font.render('Выйти в меню.', True, (255, 255, 255))
    screen.blit(btn_text, (menu_button.x + 10, menu_button.y + 12))

    for anim in animations:
        anim.draw(screen)
        anim.update()


def draw_game_over(screen, player_wins):
    font = pygame.font.Font(None, 74)
    text = 'ВЫ ПОБЕДИЛИ!' if player_wins else 'КОМПЬЮТЕР ПОБЕДИЛ!'
    color = (0, 255, 0) if player_wins else (255, 0, 0)
    label = font.render(text, True, color)
    screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2))

def draw_exit_confirm(screen, message = 'Выйти в главное меню?'):
    # рисует полупрозрачное окно подтверждения
    # будем писать полупрозрачный фон
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    # создадим окно
    box_w = 400
    box_h = 200
    box_y = SCREEN_HEIGHT // 2 - box_h // 2
    box_x = SCREEN_WIDTH // 2 - box_w // 2
    pygame.draw.rect(screen, (50, 50, 70), (box_x, box_y, box_w, box_h), border_radius=15)
    pygame.draw.rect(screen, (150, 150, 200), (box_x, box_y, box_w, box_h), 3, border_radius=15)
    font_b = pygame.font.Font(None, 50)
    font_s = pygame.font.Font(None, 35)
    text = font_b.render(message, True, (255, 255, 255))
    screen.blit(text, (box_x + box_w//2 - text.get_width()//2, box_y + 40))


    # кнопки
    mouse = pygame.mouse.get_pos()


    yes_rect = pygame.Rect(box_x + 50, box_y + 120, 120, 50)
    yes_color = (255, 100, 100) if yes_rect.collidepoint(mouse) else (200, 50, 50)
    yes_text = font_s.render('Да.', True, (255, 255, 255))
    pygame.draw.rect(screen, yes_color, yes_rect, border_radius=10)
    screen.blit(yes_text, (yes_rect.x + 45, yes_rect.y + 12))

    no_rect = pygame.Rect(box_x + 230, box_y + 120, 120, 50)
    no_color = (100, 255, 100) if no_rect.collidepoint(mouse) else (50, 200, 50)
    no_text = font_s.render('Нет!', True, (255, 255, 255))
    pygame.draw.rect(screen, no_color, no_rect, border_radius=10)
    screen.blit(no_text, (no_rect.x + 40, no_rect.y + 12))


    return yes_rect, no_rect