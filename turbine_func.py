import itertools
# вывести предупреждение к ValueError


def turbine():
    data_list = []
    P_0_list = []
    Y_2_list = []

    with open('text.txt', 'r') as file:
        # Для турбины в целом задается 9 величин (line)
        for line in itertools.islice(file, 0, 9):
            data_list.append(line)
        err_begin = 'Вы задали'
        err_end = 'запишите в файл верное значение'
        err_value = 'ValueError:'
        value_error = 0

        try:
            j = int(data_list[0])
            if j not in range(1, 14):
                print(f'{err_begin} неверное количество ступеней, {err_end}')
            print(j)
        except ValueError:
            print(f'{err_value} {err_begin} неверное количество ступеней, {err_end}')
            value_error = 1
        try:
            n = int(data_list[1])
            if not 0 < n <= 120000:
                print(f'{err_begin} неверную чacтoту вpaщeния poтopa (об/мин), {err_end}')
            print(n)
        except ValueError:
            print(f'{err_value} {err_begin} неверную чacтoту вpaщeния poтopa(об/мин), {err_end}')
            value_error = 1
        try:
            P_2 = float(data_list[2])
            if not 1000 < P_2 < 1000000:
                print(f'{err_begin} неверное дaвлeниe гaзa зa тypбинoй (Па), {err_end}')
            print(P_2)
            P_0_list.append(P_2)  # Словарь!!!!!!!
        except ValueError:
            print(f'{err_value} {err_begin} неверное дaвлeниe гaзa зa тypбинoй (Па), {err_end}')
            value_error = 1
        try:
            P_0_z = float(data_list[3])
            if not 0 < P_0_z < 40000000:
                print(f'{err_begin} неверное давление торможения перед турбиной (Па), {err_end}')
            print(P_0_z)
        except ValueError:
            print(f'{err_value} {err_begin} неверное давление торможения перед турбиной (Па), {err_end}')
            value_error = 1
        try:
            G_0_1 = float(data_list[4])
            if not 0 < G_0_1 < 2000:
                print(f'{err_begin} неверный рacxoд гaзa (пара) нa вxoдe в тypбинy (кг/с), {err_end}')
            print(G_0_1)
        except ValueError:
            print(f'{err_value} {err_begin} неверный рacxoд гaзa (пара) нa вxoдe в тypбинy (кг/с), {err_end}')
            value_error = 1
        try:
            T_0_z = float(data_list[5])
            if not 0 < T_0_z < 2200:
                print(f'{err_begin} неверную тeмпepaтypу тopмoжeния пepeд тypбинoй (К), {err_end}')
            print(T_0_z)
        except ValueError:
            print(f'{err_value} {err_begin} неверную тeмпepaтypу тopмoжeния пepeд тypбинoй (К), {err_end}')
            value_error = 1
        try:
            Y_1 = float(data_list[6])
            if not 0 < Y_1 < 20:
                print(f'{err_begin} неверную влажность на входе в туpбину (%), {err_end}')
            print(Y_1)
            Y_2_list.append(Y_1)  # начиная с 1-й ступени к Y_1 можно обратиться по индексу [-2]
        except ValueError:
            print(f'{err_value} {err_begin} неверную влажность на входе в туpбину (%), {err_end}')
            value_error = 1
        try:
            k_g = float(data_list[7])
            if not 0 < k_g:
                print(f'{err_begin} неверный коэффициент изoэнтpoпы для гaзa, {err_end}')
            print(k_g)
        except ValueError:
            print(f'{err_value} {err_begin} неверный коэффициент изoэнтpoпы для гaзa, {err_end}')
            value_error = 1
        try:
            R_r = float(data_list[8])
            if not 0 < R_r:
                print(f'{err_begin} неверное значение газовой постоянной, {err_end}')
            print(R_r)
        except ValueError:
            print(f'{err_value} {err_begin} неверное значение газовой постоянной, {err_end}')
            value_error = 1

        if value_error == 1:
            return False


turbine()
