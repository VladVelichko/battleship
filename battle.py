import pygame

'''
ВНИМАНИЕ!!!

self.board[i][j] может принимать значения:
0 - чёрное поле
1, 2, 3, 4 - единичный, 2хпалубный, 3хпалубный и 4хпалубный кораблики соответственно
5 - красная зона

Что нового:

Сделана функция удаления двойки и красной зоны вокруг неё, остался поворот двойки
Очищен код от ненужных повторов поиска номера клетки при нажатиии на клетку

Что ещё нужно сделать:
1. Написать функции для расстановки 3- и 4-хпалубных кораблей вместе с красной подсветкой
2. Написать функции для поворота больших кораблей (например, по нажатию кнопки какой-нибудь)
3. Написать функции для рандомной расстановки кораблей компьютера
0. На вторичном поле между зонами игрока и компьютера поставить стрелочку (кто ходит)
4. Написать функции игры (поочерёдные удары)
'''

class Board:
    def __init__(self):  # инициализация
        self.board = [[0] * 10 for _ in range(10)]
        self.numberofcells = 0
        self.mouse_ship = False
        self.running = False
        self.num1, self.num2, self.num3, self.num4 = '4', '3', '2', '1'
        self.stage2 = False  # при значении True ограничивает действия с кораблями во время игры

    def render1(self, s):  # рисует кораблики (справа) и поле, отвечает за кол-во корабликов
        for j in range(10):
            for i in range(10):
                pygame.draw.rect(s, ('white'), (10 + i * 40, 10 + j * 40, 40, 40), width=1)
        if int(self.num1) > 0:
            pygame.draw.rect(s, (0, 150, 150), (430, 280, 40, 40), width=1)
            font = pygame.font.Font(None, 50)
            text = font.render(self.num1, True, (100, 255, 100))
            screen.blit(text, (480, 285))
        if int(self.num2) > 0:
            for i in range(2):
                pygame.draw.rect(s, (0, 150, 150), (430 + i * 40, 220, 40, 40), width=1)
            font = pygame.font.Font(None, 50)
            text = font.render(self.num2, True, (100, 255, 100))
            screen.blit(text, (520, 225))
        if int(self.num3) > 0:
            for i in range(3):
                pygame.draw.rect(s, (0, 150, 150), (430 + i * 40, 160, 40, 40), width=1)
            font = pygame.font.Font(None, 50)
            text = font.render(self.num3, True, (100, 255, 100))
            screen.blit(text, (560, 165))
        if int(self.num4) > 0:
            for i in range(4):
                pygame.draw.rect(s, (0, 150, 150), (430 + i * 40, 100, 40, 40), width=1)
            font = pygame.font.Font(None, 50)
            text = font.render(self.num4, True, (100, 255, 100))
            screen.blit(text, (600, 105))
        if int(self.num1) + int(self.num2) + int(self.num3) + int(self.num4) != 0:
            pygame.draw.rect(s, (0, 150, 0), (460, 350, 150, 40))
        else:
            pygame.draw.rect(s, (0, 255, 0), (460, 350, 150, 40))

    def render2(self, screen):  # рисует два поля
        for j in range(10):
            for i in range(10):
                pygame.draw.rect(screen, ('white'), (10 + i * 40, 10 + j * 40, 40, 40), width=1)
        for j in range(10):
            for i in range(10):
                pygame.draw.rect(screen, ('white'), (430 + i * 40, 10 + j * 40, 40, 40), width=1)

    def proof(self, sc, i, j):  # проверяет на возможность постановки единички
        i2, i1, j2, j1 = i, i, j, j
        if i > 0:
            i2 = i - 1
        if i < 9:
            i1 = i + 1
        if j > 0:
            j2 = j - 1
        if j < 9:
            j1 = j + 1
        if sc.get_at((i * 40 + 15, j * 40 + 15))[:3] == (0, 0, 0):
            if sc.get_at((i * 40 + 15, j1 * 40 + 15))[:3] != (0, 100, 100):
                if sc.get_at((i1 * 40 + 15, j1 * 40 + 15))[:3] != (0, 100, 100):
                    if sc.get_at((i1 * 40 + 15, j2 * 40 + 15))[:3] != (0, 100, 100):
                        if sc.get_at((i1 * 40 + 15, j * 40 + 15))[:3] != (0, 100, 100):
                            if sc.get_at((i2 * 40 + 15, j1 * 40 + 15))[:3] != (0, 100, 100):
                                if sc.get_at((i2 * 40 + 15, j2 * 40 + 15))[:3] != (0, 100, 100):
                                    if sc.get_at((i2 * 40 + 15, j * 40 + 15))[:3] != (0, 100, 100):
                                        if sc.get_at((i * 40 + 15, j2 * 40 + 15))[:3] != (0, 100, 100):
                                            return True

    def ships(self, screen):  # вырисовывает корабли и красные зоны на каждом flip
        for i in range(10):
            for j in range(10):
                if self.board[i][j] != 0 and self.board[i][j] != 5:
                    self.red_zones(i, j)
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, (0, 100, 100), (i * 40 + 10, j * 40 + 10, 40, 40))
                if self.board[i][j] == 2 and i != 9:
                    pygame.draw.rect(screen, (0, 100, 100), (i * 40 + 10, j * 40 + 10, 80, 40))
        for i in range(10):
            for j in range(10):
                if self.board[i][j] == 5:
                    pygame.draw.rect(screen, (255, 0, 0), (i * 40 + 10, j * 40 + 10, 40, 40))

    def red_zones(self, i, j):  # ищет, где нужны красные зоны
        if not self.stage2:
            if i > 0 and j > 0:
                if self.board[i - 1][j - 1] == 0:
                    self.board[i - 1][j - 1] = 5
            if j < 9 and i < 9:
                if self.board[i + 1][j + 1] == 0:
                    self.board[i + 1][j + 1] = 5
            if i > 0:
                if self.board[i - 1][j] == 0:
                    self.board[i - 1][j] = 5
            if i < 9:
                if self.board[i + 1][j] == 0:
                    self.board[i + 1][j] = 5
            if j < 9:
                if self.board[i][j + 1] == 0:
                    self.board[i][j + 1] = 5
            if j > 0:
                if self.board[i][j - 1] == 0:
                    self.board[i][j - 1] = 5
            if i < 9 and j > 0:
                if self.board[i + 1][j - 1] == 0:
                    self.board[i + 1][j - 1] = 5
            if i > 0 and j < 9:
                if self.board[i - 1][j + 1] == 0:
                    self.board[i - 1][j + 1] = 5

    def set_single(self):  # ставит единичку
        for i in range(10):
            if event.pos[0] > i * 40 + 10 and event.pos[0] < (i + 1) * 40 + 10:
                for j in range(10):
                    if event.pos[1] > j * 40 + 10 and event.pos[1] < (j + 1) * 40 + 10:
                        if board.proof(screen, i, j):
                            pygame.draw.rect(screen, (0, 200, 200), (i * 40, j * 40, 40, 40))
                            self.board[i][j] = 1
                            self.mouse_ship = False
                            self.num1 = str(int(self.num1) - 1)

    def del_single(self, i, j):  # удаляет единичку
        self.num1 = str(int(self.num1) + 1)
        self.board[i][j] = 0
        if i > 0 and j > 0:
            self.board[i - 1][j - 1] = 0
        if j < 9 and i < 9:
            self.board[i + 1][j + 1] = 0
        if i > 0:
            self.board[i - 1][j] = 0
        if i < 9:
            self.board[i + 1][j] = 0
        if j < 9:
            self.board[i][j + 1] = 0
        if j > 0:
            self.board[i][j - 1] = 0
        if i < 9 and j > 0:
            self.board[i + 1][j - 1] = 0
        if i > 0 and j < 9:
            self.board[i - 1][j + 1] = 0

    def del_double(self, i, j, nap):
        self.num2 = str(int(self.num2) + 1)
        self.board[i][j] = 0
        if nap == 2:  # если двойка стоит на значениях (i, j)(i + 1, j)
            self.board[i + 1][j] = 0
        if i > 0:
            self.board[i - 1][j] = 0
        if j > 0 and i > 0:
            self.board[i - 1][j - 1] = 0
        if j > 0:
            self.board[i][j - 1] = 0
            self.board[i + 1][j - 1] = 0
        if i < 8:
            self.board[i + 2][j] = 0
        if i < 8 and j > 0:
            self.board[i + 2][j - 1] = 0
        if i < 8 and j < 9:
            self.board[i + 2][j + 1] = 0
        if i > 0 and j < 9:
            self.board[i - 1][j + 1] = 0
        if j < 9:
            self.board[i][j + 1] = 0
        self.board[i + 1][j + 1] = 0
        if nap == 4:  # если двойка стоит на значениях (i, j)(i - 1, j)
            self.board[i + 1][j] = 0
        if i > 1:
            self.board[i - 2][j] = 0
        if j > 1 and i > 0:
            self.board[i - 2][j - 1] = 0
        if j > 0:
            self.board[i][j - 1] = 0
            self.board[i - 1][j - 1] = 0
        if i < 9:
            self.board[i + 1][j] = 0
        if i < 9 and j > 0:
            self.board[i + 1][j - 1] = 0
        if i < 9 and j < 9:
            self.board[i + 1][j + 1] = 0
        if i > 1 and j < 9:
            self.board[i - 2][j + 1] = 0
        if j < 9:
            self.board[i][j + 1] = 0
            self.board[i - 1][j + 1] = 0

    def del_other(self, i, j, nap):
        if self.board[i][j] == 2:
            self.del_double(i, j, nap)

    def find_other(self, s, i, j):
        # направление: 1 - корабль наверх (а также может и вниз); 3 - вниз
        # направление: 2 - корабль вправо; 4 - влево
        if self.board[i][j] == 1:
            self.del_single(i, j)
        elif i > 0 and j > 0 and i < 9 and j < 9:
            if s.get_at((event.pos[0] + 40, event.pos[1]))[:3] == (0, 100, 100):
                self.del_other(i, j, 2)  # направление: 2 - вправо
            elif s.get_at((event.pos[0] - 40, event.pos[1]))[:3] == (0, 100, 100):
                self.del_other(i, j, 4)
            elif s.get_at((event.pos[0], event.pos[1] + 40))[:3] == (0, 100, 100):
                self.del_other(i, j, 3)
            elif s.get_at((event.pos[0], event.pos[1] - 40))[:3] == (0, 100, 100):
                self.del_other(i, j, 1)
        elif j == 9 and i == 9:
            if s.get_at((event.pos[0] - 40, event.pos[1]))[:3] == (0, 100, 100):
                self.del_other(i, j, 4)
            elif s.get_at((event.pos[0], event.pos[1] - 40))[:3] == (0, 100, 100):
                self.del_other(i, j, 1)
        elif i == 9 and j == 0:
            if s.get_at((event.pos[0] - 40, event.pos[1]))[:3] == (0, 100, 100):
                self.del_other(i, j, 4)
            elif s.get_at((event.pos[0], event.pos[1] + 40))[:3] == (0, 100, 100):
                self.del_other(i, j, 3)
        elif i == 0 and j == 9:
            if s.get_at((event.pos[0] + 40, event.pos[1]))[:3] == (0, 100, 100):
                self.del_other(i, j, 2)
            elif s.get_at((event.pos[0], event.pos[1] - 40))[:3] == (0, 100, 100):
                self.del_other(i, j, 1)
        elif i == 0 and j == 0:
            if s.get_at((event.pos[0] + 40, event.pos[1]))[:3] == (0, 100, 100):
                self.del_other(i, j, 2)
            elif s.get_at((event.pos[0], event.pos[1] + 40))[:3] == (0, 100, 100):
                self.del_other(i, j, 3)
        elif i == 0:
            if s.get_at((event.pos[0] + 40, event.pos[1]))[:3] == (0, 100, 100):
                self.del_other(i, j, 2)
            elif s.get_at((event.pos[0], event.pos[1] + 40))[:3] == (0, 100, 100):
                self.del_other(i, j, 3)
            elif s.get_at((event.pos[0], event.pos[1] - 40))[:3] == (0, 100, 100):
                self.del_other(i, j, 1)
        elif j == 0:
            if s.get_at((event.pos[0] + 40, event.pos[1]))[:3] == (0, 100, 100):
                self.del_other(i, j, 2)
            elif s.get_at((event.pos[0] - 40, event.pos[1]))[:3] == (0, 100, 100):
                self.del_other(i, j, 4)
            elif s.get_at((event.pos[0], event.pos[1] + 40))[:3] == (0, 100, 100):
                self.del_other(i, j, 3)

    def set_double(self):  # ставит двойной корабль
        for i in range(10):
            if event.pos[0] > i * 40 + 10 and event.pos[0] < (i + 1) * 40 + 10:
                for j in range(10):
                    if event.pos[1] > j * 40 + 10 and event.pos[1] < (j + 1) * 40 + 10:
                        if i <= 8:
                            if board.proof(screen, i, j) and board.proof(screen, i + 1, j):
                                pygame.draw.rect(screen, (0, 200, 200), (i * 40, j * 40, 80, 40))
                                self.board[i][j] = 2
                                self.board[i + 1][j] = 2
                                self.mouse_ship = False
                                self.num2 = str(int(self.num2) - 1)

    def set_triple(self):
        pass

    def set_four(self):
        pass

    def set_ship(self):  # определяет размер кораблика
        if self.mouse_ship:  # определяет, был ли нажат кораблик
            if self.numberofcells == 1:
                self.set_single()
            if self.numberofcells == 2:
                self.set_double()
            if self.numberofcells == 3:
                self.set_triple()
            if self.numberofcells == 4:
                self.set_four()

    def get_cell(self, sc):  # вырисовывает нажатый курсорчик
        if self.mouse_ship:
            if self.numberofcells == 1:
                pygame.draw.rect(sc, (0, 100, 100), (event.pos[0], event.pos[1], 40, 40))
            elif self.numberofcells == 2:
                pygame.draw.rect(sc, (0, 100, 100), (event.pos[0], event.pos[1], 80, 40))
            elif self.numberofcells == 3:
                pygame.draw.rect(sc, (0, 100, 100), (event.pos[0], event.pos[1], 120, 40))
            else:
                pygame.draw.rect(sc, (0, 100, 100), (event.pos[0], event.pos[1], 160, 40))

    def starting(self):  # запуск вторичного поля
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 5:
                    self.board[i][j] = 0
        self.running = False
        self.stage2 = True

    def where_pressed(self, s):
        if event.pos[0] <= 470 and event.pos[0] >= 430:
            if event.pos[1] <= 320 and event.pos[1] >= 280:
                if self.num1 != '0':
                    self.numberofcells = 1
                    self.mouse_ship = True
        if event.pos[0] <= 510 and event.pos[0] >= 430:
            if event.pos[1] <= 265 and event.pos[1] >= 225:
                if self.num2 != '0':
                    self.numberofcells = 2
                    self.mouse_ship = True
        # проверка на удаление кораблика:
        if s.get_at((event.pos[0], event.pos[1]))[:3] == (0, 100, 100):  # при нажатии на кораблик удаляет
            for i in range(10):
                if event.pos[0] > i * 40 + 10 and event.pos[0] < (i + 1) * 40 + 10:
                    for j in range(10):
                        if event.pos[1] > j * 40 + 10 and event.pos[1] < (j + 1) * 40 + 10:
                            self.find_other(s, i, j)
        self.set_ship()
        if s.get_at((event.pos[0], event.pos[1]))[:3] == (0, 255, 0):
            self.starting()


if __name__ == '__main__':
    size = width, height = 650, 420  # создание первичного поля (поле игрока)
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Морской бой')

    board = Board()

    fps = 50
    clock = pygame.time.Clock()

    board.running = True
    while board.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выход из окна
                exit()
            elif event.type == pygame.MOUSEMOTION:
                board.get_cell(screen)  # ведение курсорчика
                pygame.display.flip()
                screen.fill((0, 0, 0))
                board.render1(screen)  # создание поля
                board.ships(screen)  # заполнение кораблями
            elif event.type == pygame.MOUSEBUTTONUP:
                board.where_pressed(screen)  # проверяет, куда тыкнули
                screen.fill((0, 0, 0))
                board.render1(screen)  # создание поля
                board.ships(screen)  # заполнение кораблями
                pygame.display.flip()
            else:
                pass
        clock.tick(fps)

    screen = pygame.display.set_mode((840, 420))  # создание вторичного поля (там, где уже идёт игра)
    board.render2(screen)
    board.ships(screen)  # заполнение кораблями
    pygame.display.flip()

    # второй этап, сама игра
    board.running = True
    while board.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEMOTION:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
            else:
                pass
        clock.tick(fps)
    pygame.quit()
