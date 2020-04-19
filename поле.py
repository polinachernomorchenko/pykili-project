import pygame
import sys


def prevent_win(field):
    for i in range(3):  # строка
        if field[i].count('o') == 2:
            for j in range(3):
                if field[i][j] == 0:
                    field[i][j] = 'x'
                    return field

    for i in range(3):  # столбец
        if field[0][i] == field[1][i] == 'o' \
                or field[0][i] == field[2][i] == 'o' \
                or field[1][i] == field[2][i] == 'o':
            stl = i
            for j in range(3):
                if field[j][stl] == 0:
                    field[j][stl] = 'x'
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

    return field


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
                if pole[i][j] == 'o' and (i != laststr or j != laststl):
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
            
    return field


def chek_win(field, sign):
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
    pygame.time.wait(500)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if move == 0:
            pygame.time.wait(250)
            pole = game_agent(field, move, laststr, laststl)
            move += 1
        if event.type == pygame.MOUSEBUTTONDOWN and not game_end and move % 2 == 1:
            pygame.time.wait(250)
            xm, ym = pygame.mouse.get_pos()
            stl = int(xm // (block + space))
            str = int(ym // (block + space))
            pygame.time.wait(300)
            if field[str][stl] == 0:
                field[str][stl] = 'o'
            move += 1
            pygame.time.wait(250)

        if move % 2 == 0 and not game_end:
            laststr = str
            laststl = stl
            field = game_agent(field, move, laststr, laststl)
            move += 1
            pygame.time.wait(150)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_end = False
            move = 0
            field = [[0] * 3 for i in range(3)]
            screen.fill(beige)
            pygame.display.update()

        if game_end == False:
            for str in range(3):
                for stl in range(3):
                    if field[str][stl] == 'x':
                        color = cross
                        pygame.time.wait(1000)
                    elif field[str][stl] == 'o':
                        color = zero
                    else:
                        color = super_pink

                    x = block * stl + (stl + 1) * space
                    y = block * str + (str + 1) * space
                    pygame.draw.rect(screen, color, (x, y, block, block))
                    pygame.display.update()

            if (move - 1) % 2 == 0:
                sign = 'x'
            if (move - 1) % 2 == 1:
                sign = 'o'

            game_end = chek_win(field, sign)

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
