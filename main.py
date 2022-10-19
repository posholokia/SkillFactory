play_area = [
    ['\\', '1', '2', '3'],
    ['1', ' ', ' ', ' '],
    ['2', ' ', ' ', ' '],
    ['3', ' ', ' ', ' ']
]


def start_area():  # создаем копию стартового поля, которое будем менять
    area = []
    for i in play_area:
        area.append(i.copy())
    return area


def show(area):  # выводим поле на экран
    for i in area:
        print('| ' + " | ".join(i) + ' |')
        print('-----------------')


def rules():
    print("--------------------------")
    print("     Приветствуем вас     ")
    print("          в игре          ")
    print("     крестики-нолики      ")
    print("--------------------------")
    print(" Каждый игрок по очереди  ")
    print("   вводит 2 координаты    ")
    print("        от 1 до 3.        ")
    print(" Координаты можно вводить ")
    print("  слитно или через любой  ")
    print("    разделяющий символ    ")
    print("--------------------------")


def score(player, score_x, score_0):  # считаем количество побед
    if player == 'Х':  # если победили крестики
        score_x += 1
    if player == '0':  # если победили нолики
        score_0 += 1
    print('Счет игры:')
    print(f'Игрок Х: {score_x}  |  Игрок 0: {score_0}')  # выводим счет на экран
    return score_x, score_0  # возвращаем счет


def welcome(func):  # приветствуем игроков и запрашиваем согласие на начало игры или продолжение
    plays = 0  # 0 - первая игра, приветствуем. 1 - не первая игра, запрашиваем продолжение
    score_x = score_0 = 0  # записываем набранные очки, начальный счет 0-0

    def wrapper():
        nonlocal plays, score_x, score_0
        if plays == 0:
            plays += 1  # увеличиваем счетчик игр
            start = input('Готовы начать игру?(y/n): ')
            if start == 'y' or start == 'Y':
                player = func()  # запускаем функцию начала игры и получаем победителя
                score_x, score_0 = score(player, score_x, score_0)  # запускаем счет побед и перезаписываем
                wrapper()  # предлагаем сыграть еще
            else:
                print('Сыграем в другой раз :(')
                return
        else:
            start = input('Сыграем еще разок?(y/n): ')
            if start == 'y' or start == 'Y':
                player = func()
                score_x, score_0 = score(player, score_x, score_0)
                wrapper()
            else:
                print('Сыграем в другой раз :(')
                return

    return wrapper


@welcome
def start_play():  # начало игры
    area = start_area()  # получаем стартовое поле
    show(play_area)
    count = 1  # счетчик ходов
    player = ''  # символ игрока - 0 или Х
    who_next = 'Х'  # кто ходит следующий, первый Х

    def main():  # основная игра, запускает функции запроса координат, проверки победителя и счетчик ходов
        nonlocal area, count, player, who_next
        if winner(area):  # проверяем наличие победителя
            print(f'Игрок {player} победил!')  # player - тот кто ходил последним
            return player  # возвращаем победителя
        if count == 10:  # по достижении 10 хода выводим ничью
            print('Ничья')
            return ''  # победителя нет, возвращаем пустое значение
        print(f'Ходит игрок {who_next}')  # выводим на экран кто ходит
        i, j = coordinates()  # получаем координаты игрока
        if area[i][j] != ' ':  # не даем заменить уже проставленные Х и 0
            print('Эта клетка занята, укажите другую')
            return main()
        else:  # если клетка свободна
            count, player, who_next = turn(count)  # запускаем счетчик ходов
            area[i][j] = player  # подставляем символ игрока в поле и выводим его на экран
            show(area)
            return main()

    return main()


def turn(count):  # счетчик ходов
    if count % 2 == 0:  # каждый четный ход за игроком 0
        count += 1
        player = '0'  # символ игрока
        who_next = 'Х'  # кто ходит следующий
        return count, player, who_next
    else:  # каждый нечетный ход за игроком Х
        count += 1
        player = 'Х'
        who_next = '0'
        return count, player, who_next


def coordinates():  # координаты игрока
    coord = input('Введите координаты клетки: ')
    i, j = coord.zfill(2)[0], coord.zfill(2)[-1]  # дополняем недостающие координаты нулями
    if i.isdigit() and j.isdigit():  # проверяем получили ли мы цифры
        if (0 < int(i) < 4) and (0 < int(j) < 4):  # проверяем, что координаты в нужных рамках
            return int(i), int(j)
        else:  # если координаты выходят за пределы поля
            print('Нужно ввести два числа от 1 до 3, введите повторно')
            return coordinates()
    else:
        print('Нужно вводить числа')
        return coordinates()


def winner(area):  # проверяем есть ли победитель
    for i in range(1, 4):
        for j in range(1, 4):
            if area[i][1] != ' ' and area[i][1] == area[i][2] == area[i][3]:  # в строке
                return True
            elif area[1][j] != ' ' and area[1][j] == area[2][j] == area[3][j]:  # в столбце
                return True
            elif area[1][1] != ' ' and area[1][1] == area[2][2] == area[3][3]:  # по диагонали \
                return True
            elif area[1][3] != ' ' and area[1][3] == area[2][2] == area[3][1]:  # по диагонали /
                return True
    return False


rules()
start_play()  # запускаем игру
