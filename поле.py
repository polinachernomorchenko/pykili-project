import pygame
import sys
import random

def draw_field(field, super_pink, cross, zero, block, space):

        for str in range(3):
            for stl in range(3):
                if field[str][stl] == 'x':
                    color = cross
                elif field[str][stl] == 'o':
                    color = zero
                else:
                    color = super_pink

                x = block * stl + (stl + 1) * space
                y = block * str + (str + 1) * space
                pygame.draw.rect(screen, color, (x, y, block, block))
                pygame.display.update()


def prevent_win(field):

    for str in field:  # строка
        if str.count('o') == 2:
            for j in range(3):
                if str[j] == 0:
                    str[j] = 'x'
                    return field

    for i in range(3):  # столбец
        if field[0][i] == field[1][i] == 'o' \
        or field[0][i] == field[2][i] == 'o' \
        or field[1][i] == field[2][i] == 'o':
            stl = i
            for str in field:
                if str[stl] == 0:
                    str[stl] = 'x'
                    return field

    return False


def able_to_win(field):

    for i in range(3):  # строка
        if field[i].count('x') == 2:
            for j in range(3):
                if field[i][j] == 0:
                    field[i][j] = 'x'
                    return field

    for i in range(3):  # столбец
        if field[0][i] == field[1][i] == 'x' \
                or field[0][i] == field[2][i] == 'x' \
                or field[1][i] == field[2][i] == 'x':
            stl = i
            for j in range(3):
                if field[j][stl] == 0:
                    field[j][stl] = 'x'
                    return field

    if field[0][0] == 'x':
        if field[2][2] == 0:
            field[2][2] = 'x'
            return field

    if field[2][2] == 'x':
        if field[0][0] == 0:
            field[0][0] = 'x'
            return field

    if field[0][2] == 'x':
        if field[2][0] == 0:
            field[2][0] = 'x'
            return field

    if field[2][0] == 'x':
        if field[0][2] == 0:
            field[0][2] = 'x'
            return field

    return False


def game_agent(field, move, laststr, laststl):

    if move == 0:  # cтавим крест в центр поля
        field[1][1] = 'x'
        return field

    if move == 2:  # узнаем ход противника и выбираем желаемый угол
        for str in range(3):
            for stl in range(3):
                if field[str][stl] == 'o':
                    i = str
                    j = stl
                    break

        if j == 0:
            stl = 2
        else:
            stl = 0
        if i == 0:
            str = 2
        else:
            str = 0

        field[str][stl] = 'x'
        return field

    if move == 4:  # б = первый ход ноликов в углу, а = второй ход ноликов в углу

        if laststr == 0 and laststl == 0 \
        or laststr == 0 and laststl == 2 \
        or laststr == 2 and laststl == 0 \
        or laststr == 2 and laststl == 2:
            a = True
        else:
            a = False

        for i in range(3):
            for j in range(3):
                if field[i][j] == 'o' and (i != laststr or j != laststl):
                    fstr = i
                    fstl = j
                    if i == 0 and j == 0 \
                            or i == 0 and j == 2 \
                            or i == 2 and j == 0 \
                            or i == 2 and j == 2:
                        b = True
                    else:
                        b = False

        field_able = able_to_win(field)
        if not field_able:
            field_prevent = prevent_win(field)

        if field_able:
            field = field_able

        elif field_prevent:
            field = field_prevent

        elif b and not a:
            pygame.time.wait(500)

            if fstr == 2 and laststr == 1:
                if fstl == 0:
                    field[0][0] = 'x'
                    return field  # 1
                else:
                    field[0][2] = 'x'
                    return field  # 2

            elif fstr == 0 and laststr == 1:
                if fstl == 0:
                    field[2][0] = 'x'
                    return field  # 3
                else:
                    field[2][2] = 'x'
                    return field  # 4

            elif fstr == 0 and laststr == 2:
                if fstl == 0:
                    field[0][2] = 'x'
                    return field  # 5
                else:
                    field[0][0] = 'x'  # 6

            elif fstr == 2 and laststr == 0:
                if fstl == 0:
                    field[2][2] = 'x'
                    return field  # 7
                else:
                    field[2][0] = 'x'
                    return field  # 8

    if move == 6:

        field_able = able_to_win(field)
        if not field_able:
            field_prevent = prevent_win(field)

        if field_able:
            field = field_able

        elif field_prevent:
            field = field_prevent

        else:
            free_sq = []
            for i in range(3):
                for j in range(3):
                    if field[i][j] == 0:
                        free_sq.append((i, j))
            goal = random.choice(free_sq)
            field[goal[0]][goal[1]] = 'x'
            return field

    if move == 8:

        free_sq = []
        for i in range(3):
            for j in range(3):
                if field[i][j] == 0:
                    free_sq.append((i, j))
        goal = random.choice(free_sq)
        field[goal[0]][goal[1]] = 'x'
        return field

    return field


def check_win(field, sign):
    nulls = 0
    for str in field:
        nulls += str.count(0)
        if str == [sign, sign, sign]:
            return sign

    for stl in range(3):
        if field[0][stl] == field[1][stl] == field[2][stl] == sign:
            return sign

    if field[0][0] == field[1][1] == field[2][2] == sign:
        return sign

    if field[0][2] == field[1][1] == field[2][0] == sign:
        return sign

    if nulls == 0:
        return 'friendship'

    return False


pygame.init()
block = 200
space = 30
w = h = block * 3 + space * 4
field = [[0] * 3 for i in range(3)]
game_end = False
move = 0
laststr = '-'
laststl = '-'

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('крестики-нолики')

super_pink = (240, 180, 199)
dark_pink = (230, 160, 170)
beige = (234, 235, 220)
cross = (199, 180, 250)
zero = (250, 200, 180)

pygame.draw.rect(screen, beige, (0, 0, w, h))

for str in range(3):
    for stl in range(3):
        x = block * stl + (stl + 1) * space
        y = block * str + (str + 1) * space
        pygame.draw.rect(screen, super_pink, (x, y, block, block))
pygame.display.update()

while True:
    for event in pygame.event.get():
        pygame.time.wait(200)

        if event.type == pygame.QUIT:
            sys.exit(0)

        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN or move == 0:

            if move == 0:
                pygame.time.wait(250)
                field = game_agent(field, move, laststr, laststl)
                move += 1

            if event.type == pygame.MOUSEBUTTONDOWN and not game_end and move % 2 == 1:
                pygame.time.wait(100)
                xm, ym = pygame.mouse.get_pos()
                stl = int(xm // (block + space))
                str = int(ym // (block + space))
                if field[str][stl] == 0:
                    field[str][stl] = 'o'
                    if not game_end:
                        draw_field(field, super_pink, cross, zero, block, space)
                     move += 1
                pygame.time.wait(250)

            if move % 2 == 0 and not game_end:
                laststr = str
                laststl = stl
                field = game_agent(field, move, laststr, laststl)
                pygame.time.wait(300)
                if not game_end:
                    draw_field(field, super_pink, cross, zero, block, space)
                move += 1

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_end = False
                move = 0
                field = [[0] * 3 for i in range(3)]
                screen.fill(beige)
                pygame.display.update()

            if not game_end:
                draw_field(field, super_pink, cross, zero, block, space)

            if (move - 1) % 2 == 0:
                sign = 'x'
            if (move - 1) % 2 == 1:
                sign = 'o'

            game_end = check_win(field, sign)

            if game_end:
                pygame.time.wait(1700)
                screen.fill(beige)
                font = pygame.font.SysFont('lohitpunjabi', 160)
                if sign == 'x':
                    message = 'purple won'
                if sign == 'o':
                    message = 'orange won'
                if game_end == 'friendship':
                    message = 'friendship'
                text = font.render(message, True, dark_pink)
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                text_y = screen.get_height() / 2 - text_rect.height / 2
                screen.blit(text, [text_x, text_y])

                pygame.display.update()
