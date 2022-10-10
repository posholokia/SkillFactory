player = None  # сюда записываем крестики и нолики
# игровое поле:
play_area = [
    [' ', ' 1', '2', '3'],
    ['1', '-', '-', '-'],
    ['2', '-', '-', '-'],
    ['3', '-', '-', '-']
]


def change_area():  # создаем копию стартового поля, которое будем менять
    area = []
    for i in play_area:
        area.append(i.copy())
    return area


area = change_area()  # присваиваем копию в переменную


def welcome(func):  # приветствуем игроков и запрашиваем согласие на начало игры или продолжение
    global plays
    plays = 0  # 0 - первая игра, приветствуем. 1 - не первая игра, запрашиваем продолжение
    if plays == 0:
        plays += 1  # увеличиваем счетчик игр
        start = input('Привет! Сыграем в крестики-нолики?(y/n): ')
        if start == 'y' or start == 'Y':
            func()  # запускаем функцию начала игры
        else:
            print('Сыграем в другой раз :(')
            return
    else:  # запрашиваем согласие на продолжение после игры
        start = input('Сыграем еще разок?(y/n): ')
        if start == 'y' or start == 'Y':
            func()
        else:
            print('Сыграем в другой раз :(')
            return


def start_play():  # функция начала игры
    global player
    global area
    print(((((str(play_area).replace('[', '')).rstrip(']')).replace(']', '\n')).replace("'", '')).replace(',', ''))
    turn = 1  # количество ходов
    while turn <= 9:
        if turn % 2 == 0:  # каждый четный ход за игроком 0
            player = '0'  # отправляем в глобал новое значение, которе будет подставлено в поле
            print('ход игрока 0')
            turn += 1  # счетчик ходов
            coordinats()  # запускаем ввод координат игроком
            if winner():  # проверяем есть ли победитель
                print('Игрок 0 победил!')
                area = change_area()  # очищаем поле для повторной игры
                return welcome(start_play)  # предлагаем сыграть еще раз
        else:  # каждый нечетный ход за игроком Х
            player = 'X'
            print('ход игрока X')
            turn += 1
            coordinats()
            if winner():
                print('Игрок Х победил!')
                area = change_area()  # очищаем поле для повторной игры
                return welcome(start_play)
    if turn == 10:
        print('Ничья!')
        area = change_area()
        return welcome(start_play)


def current_area(func):  # функция подставляет в поле крестики и нолики, декорируем функцию с координатами игрока
    global area

    def wrapper():
        try:  # зацикливаем ввод координат если введены недопустимые значения
            i, j = func()  # получаем координаты игрока
        except TypeError:
            wrapper()
        except ValueError:
            print('нужно ввести два числа от 1 до 3')
            wrapper()
        else:
            if (0 < i < 4) and (0 < j < 4):  # проверяем, что координаты в нужных рамках
                if area[i][j] == '-':  # не даем заменить уже проставленные Х и 0
                    area[i][j] = player  # подставляем символ игрока в поле и выводим его на экран
                    print(((((str(area).replace('[', '')).rstrip(']')
                             ).replace(']', '\n')).replace("'", '')).replace(',', ''))
                else:  # если клетка занята
                    print('Эта клетка занята, укажите другую')
                    wrapper()
            else:  # если координаты выходят за пределы поля
                print('координаты должны быть в пределах от 1 до 3, введите повторно')
                wrapper()
    return wrapper


@current_area
def coordinats():  # координаты игрока
    # если без вложенной функции, то на каждое исключение будет в пустую запрашиваться ввод координат
    def correct():  # проверяем, что введено не меньше 2-х символов
        coord = input('введите координаты клетки, строка и столбец: ')
        i, j = int(coord.zfill(2)[0]), int(coord.zfill(2)[-1])  # если меньше, zfill заменяет недостающие нулями
        return i, j  # возвращаем координаты игрока
    return correct()


def winner():  # проверяем есть ли победитель
    win = False  # True - есть победитель, False - нет
    if not win:  # по текущему полю проверяем условия для победы
        for i in range(1, 4):
            for j in range(1, 4):
                if area[i][1] != '-' and area[i][1] == area[i][2] == area[i][3]:  # в строке
                    win = True
                elif area[1][j] != '-' and area[1][j] == area[2][j] == area[3][j]:  # в столбце
                    win = True
                elif area[1][1] != '-' and area[1][1] == area[2][2] == area[3][3]:  # по диагонали \
                    win = True
                elif area[1][3] != '-' and area[1][3] == area[2][2] == area[3][1]:  # по диагонали /
                    win = True
    return win


welcome(start_play)  # запускаем игру
