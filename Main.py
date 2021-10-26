# -*- coding: utf-8 -*-
from time import time, sleep
from random import randint
lag_txt = '''Слишком большая задержка.
Выберите меньший размер поле или меньшую частоту кадров в следующий раз.'''
shades = ('  ', '░░', '▒▒', '▓▓', '██')
bg_shade = 1
fg_shade = 4
def random_mode():
    global n, m, entry
    n = int(input_with_path("Высота:"))
    m = int(input_with_path('Ширина:'))
    path.append("{}x{}".format(n, m))
    entry = [[randint(0, 1) * (0 < i < n - 1 and 0 < j < m - 1)
                         for j in range(m)] for i in range(n)]
def from_file_mode():
    global n, m, entry
    file_path = input_with_path('Путь к файлу:')
    entry = [list(map(int, list(line[:-1])))
             for line in open(file_path, 'r')]
    path.append(file_path)
    n = len(entry)
    m = len(entry[0])
def default_rules():
    global surv_rule, birth_rule
    surv_rule, birth_rule = [2, 3], [3]
def custom_rules():
    global surv_rule, birth_rule
    surv_rule = list(map(int, input_with_path('Правила выживания:').split(',')))
    birth_rule = list(map(int, input_with_path('Правила рождения:').split(',')))
    path.append("{}x{}".format(','.join(map(str, surv_rule)),
                              ','.join(map(str, birth_rule))))
def input_with_path(text):
    return input("/".join(('/'.join(path), text)))
path = []
modes = {'с': random_mode,
         'ф': from_file_mode}
rules = {'с': default_rules,
         'п': custom_rules}
mode, rule = '', ''
while mode not in modes.keys():
    mode = input_with_path('Выберите режим (с - случайный, ф - из файла):')
path.append('режим '+('случ.' if mode == 'с' else 'из файла'))
modes[mode]()
while rule not in rules.keys():
    rule = input_with_path(
        'Выберите правила (с - стандартные, п - пользовательские):')
path.append('правила '+('станд.' if rule == 'с' else 'свои'))
rules[rule]()
fps = int(input_with_path("Количество кадров в секунду:"))
memory = [[0 for j in range(m)] for i in range(n)]
while True:
    start = time()
    [print(''.join(map(str, entry[i][1:-1])).replace(
        '0', shades[bg_shade]).replace(
            '1', shades[fg_shade])) for i in range(1, n - 1)]
    print('\n')
    for x in range(1, n - 1):
        for y in range(1, m - 1):
            memory[x][y] = sum([sum([entry[x + i][y + j]
                                     for j in range(-1, 2)])
                                for i in range(-1, 2)]) - entry[x][y]
    for i in range(n):
        for j in range(m):
            entry[i][j] = int(entry[i][j] == 1 and memory[i][j] in surv_rule
                              or
                              entry[i][j] == 0 and memory[i][j] in birth_rule)
    sleep(1 / fps)
    end = time()
    if 1 / fps / (end - start) < 0.75:
        print(lag_txt +
              str(round(1 / fps / (end - start) * 100)) + '% эффективности')
