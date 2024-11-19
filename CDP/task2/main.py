from random import randint, choice

class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        # Инициализация корабля с заданной длиной, типом ориентации и координатами
        self._x = x  # координата x начальной позиции корабля
        self._y = y  # координата y начальной позиции корабля
        self._length = length  # длина корабля (число палуб)
        self._tp = tp  # тип ориентации (1 - горизонтальная, 2 - вертикальная)
        self._is_move = True  # флаг возможности перемещения корабля
        self._cells = [1] * length  # список, сигнализирующий о состоянии палуб (1 - целая, 2 - повреждена)

    def set_start_coords(self, x, y):
        # Установка начальных координат корабля
        self._x = x
        self._y = y

    def get_start_coords(self):
        # Получение начальных координат корабля
        return self._x, self._y

    def move(self, go):
        # Перемещение корабля в заданном направлении
        if self._is_move:  # проверяем, возможно ли перемещение
            if self._tp == 1:  # горизонтальное перемещение
                self._x += go  # изменяем координату x
            else:  # вертикальное перемещение
                self._y += go  # изменяем координату y

    def is_collide(self, ship):
        # Проверка на столкновение с другим кораблем
        for i in range(self._length):
            # вычисляем координаты текущей палубы текущего корабля
            x1 = self._x + i if self._tp == 1 else self._x
            y1 = self._y if self._tp == 1 else self._y + i
            for j in range(ship._length):
                # вычисляем координаты текущей палубы другого корабля
                x2 = ship._x + j if ship._tp == 1 else ship._x
                y2 = ship._y if ship._tp == 1 else ship._y + j
                # проверяем, находятся ли палубы слишком близко (соприкасаются)
                if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    return True  # есть столкновение
        return False  # столкновения нет

    def is_out_pole(self, size):
        # Проверка на выход за пределы игрового поля
        if self._tp == 1:  # если корабль расположен горизонтально
            return not (0 <= self._x < size and 0 <= self._x + self._length - 1 < size)  # проверяем координаты x
        else:  # если корабль расположен вертикально
            return not (0 <= self._y < size and 0 <= self._y + self._length - 1 < size)  # проверяем координаты y

    def __getitem__(self, indx):
        # Получение состояния палубы по индексу
        return self._cells[indx]

    def __setitem__(self, indx, value):
        # Установка состояния палубы по индексу
        self._cells[indx] = value
        if value == 2:
            self._is_move = False  # если есть попадание, перемещение прекращается


class GamePole:
    def __init__(self, size):
        # Инициализация игрового поля заданного размера
        self._size = size  # размер игрового поля
        self._ships = []  # список кораблей на поле
        self._pole = [[0] * size for _ in range(size)]  # двумерный массив, представляющий игровое поле

    def init(self):
        # Инициализация поля с размещением кораблей
        ships_config = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # конфигурация кораблей (их длины)
        for length in ships_config:
            while True:
                tp = randint(1, 2)  # случайная ориентация корабля
                x = randint(0, self._size - 1)  # случайная координата x
                y = randint(0, self._size - 1)  # случайная координата y
                ship = Ship(length, tp, x, y)
                # проверяем, не выходит ли корабль за границы поля и не сталкивается ли с другими кораблями
                if not ship.is_out_pole(self._size) and not any(ship.is_collide(s) for s in self._ships):
                    self._ships.append(ship)  # добавляем корабль на поле
                    self._place_ship_on_pole(ship)  # размещаем корабль на игровом поле
                    break

    def _place_ship_on_pole(self, ship):
        # Размещение корабля на игровом поле
        x, y = ship.get_start_coords()  # получаем начальные координаты корабля
        for i in range(ship._length):
            if ship._tp == 1:  # горизонтальное размещение
                self._pole[y][x + i] = ship[i]  # устанавливаем состояние палубы на поле
            else:  # вертикальное размещение
                self._pole[y + i][x] = ship[i]  # устанавливаем состояние палубы на поле

    def get_ships(self):
        # Получение списка кораблей на поле
        return self._ships

    def move_ships(self):
        # Перемещение всех кораблей на одну клетку в случайном направлении
        for ship in self._ships:
            go = choice([-1, 1])  # случайное направление перемещения
            original_x, original_y = ship.get_start_coords()  # сохраняем текущие координаты
            ship.move(go)  # выполняем перемещение
            # проверяем, не вышел ли корабль за пределы поля или не столкнулся ли с другим кораблем
            if ship.is_out_pole(self._size) or any(ship.is_collide(s) for s in self._ships if s != ship):
                ship.set_start_coords(original_x, original_y)  # отменяем перемещение, если оно невозможно

    def show(self, show_ships=True):
        # Отображение игрового поля
        for row in self._pole:
            if show_ships:
                print(' '.join(map(str, row)))
            else:
                # скрываем корабли противника, показывая их как воду
                print(' '.join('0' if cell == 1 else str(cell) for cell in row))

    def get_pole(self):
        # Получение текущего состояния игрового поля в виде двумерного кортежа
        return tuple(tuple(row) for row in self._pole)


class Battle:
    def __init__(self, size=10):
        # Инициализация игры Морской бой
        self._size = size  # размер игрового поля
        self._player_pole = GamePole(size)  # поле игрока
        self._computer_pole = GamePole(size)  # поле компьютера
        self._player_pole.init()  # инициализация поля игрока
        self._computer_pole.init()  # инициализация поля компьютера

    def player_turn(self, x, y):
        # Ход игрока по координатам x, y
        if self._computer_pole._pole[y][x] == 1:  # проверяем, есть ли корабль в данной клетке
            self._computer_pole._pole[y][x] = 2  # попадание
            print("Попадание!")
        else:
            print("Мимо!")

    def computer_turn(self):
        # Ход компьютера (случайный выбор координат)
        while True:
            x = randint(0, self._size - 1)  # случайная координата x
            y = randint(0, self._size - 1)  # случайная координата y
            if self._player_pole._pole[y][x] in (0, 1):  # проверяем, была ли эта клетка уже атакована
                if self._player_pole._pole[y][x] == 1:
                    self._player_pole._pole[y][x] = 2  # попадание
                    print(f"Компьютер попал в точку ({x}, {y})!")
                else:
                    print(f"Компьютер промахнулся в точке ({x}, {y})!")
                break

    def play(self):
        # Основной игровой цикл
        while True:
            print("Поле игрока:")
            self._player_pole.show()  # отображение поля игрока
            print("Поле противника (компьютера):")
            self._computer_pole.show(show_ships=False)  # отображение поля компьютера с сокрытием кораблей
            try:
                x, y = map(int, input("Введите координаты выстрела (x y): ").split())  # ввод координат
                if not (0 <= x < self._size and 0 <= y < self._size):  # проверка на корректность координат
                    raise ValueError("Координаты вне диапазона поля. Попробуйте снова.")
            except ValueError as e:
                print(e)
                continue
            self.player_turn(x, y)  # ход игрока
            self.computer_turn()  # ход компьютера


# Тесты
ship = Ship(2)
ship = Ship(2, 1)
ship = Ship(3, 2, 0, 0)
assert ship._length == 3 and ship._tp == 2 and ship._x == 0 and ship._y == 0, "неверные значения атрибутов объекта класса Ship"
assert ship._cells == [1, 1, 1], "неверный список _cells"
assert ship._is_move, "неверное значение атрибута _is_move"
ship.set_start_coords(1, 2)
assert ship._x == 1 and ship._y == 2, "неверно отработал метод set_start_coords()"
assert ship.get_start_coords() == (1, 2), "неверно отработал метод get_start_coords()"
ship.move(1)
s1 = Ship(4, 1, 0, 0)
s2 = Ship(3, 2, 0, 0)
s3 = Ship(3, 2, 0, 2)
assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 0)"
assert s1.is_collide(s3) == False, "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)"
s2 = Ship(3, 2, 1, 1)
assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 1, 1)"
s2 = Ship(3, 1, 8, 1)
assert s2.is_out_pole(10), "неверно работает метод is_out_pole() для корабля Ship(3, 1, 8, 1)"
s2 = Ship(3, 2, 1, 5)
assert s2.is_out_pole(10) == False, "неверно работает метод is_out_pole(10) для корабля Ship(3, 2, 1, 5)"
s2[0] = 2
assert s2[0] == 2, "неверно работает обращение ship[indx]"
p = GamePole(10)
p.init()
for nn in range(5):
    for s in p._ships:
        assert s.is_out_pole(10) == False, "корабли выходят за пределы игрового поля"
        for ship in p.get_ships():
            if s != ship:
                assert s.is_collide(ship) == False, "корабли на игровом поле соприкасаются"
    p.move_ships()

gp = p.get_pole()
assert type(gp) == tuple and type(gp[0]) == tuple, "метод get_pole должен возвращать двумерный кортеж"
assert len(gp) == 10 and len(gp[0]) == 10, "неверные размеры игрового поля, которое вернул метод get_pole"
pole_size_8 = GamePole(8)
pole_size_8.init()
print("\n Passed")

Battle().play()
