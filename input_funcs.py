import itertools
# удалить отладочные принты


def turbine():
    """
    Функция для чтения из txt файла, обработки и возращения
    задаваемых, общих для всей турбины, параметров
    """

    data_list = []

    with open('text.txt', 'r') as file:
        # Для турбины в целом задается 9 величин (line)
        for line in itertools.islice(file, 0, 9):
            data_list.append(line)
        err_begin = 'Вы задали'
        err_end = 'запишите в файл верное значение'
        text_condition_err = 'Проверьте, что выполняется условие:'
        text_where_х = 'где х - задаваемая величина \n'
        text_float_value_err = 'ValueError: проверьте, что при задании величины Вы использовали точку для отделения дробной части'
        text_int_value_err = 'ValueError: проверьте, что вы ввели целое число, а не дробное'
        value_error = 0

        warning = f'{err_begin} неверное количество ступеней, {err_end}'
        try:
            j = int(data_list[0])
            if j not in range(1, 14):
                print(f'{warning} \n{text_condition_err} 1 <= x <= 13, {text_where_х}')
            print(j)
        except ValueError:
            print(f'{warning} \n{text_int_value_err}')
            value_error = 1
        warning = f'{err_begin} неверную чacтoту вpaщeния poтopa (об/мин), {err_end}'
        try:
            n = int(data_list[1])
            if not 0 < n <= 120000:
                print(f'{warning} \n{text_condition_err} 0 < x <= 120000, {text_where_х}')
            print(n)
        except ValueError:
            print(f'{warning} \n{text_int_value_err}')
            value_error = 1
        warning = f'{err_begin} неверное дaвлeниe гaзa зa тypбинoй (Па), {err_end}'
        try:
            P_2 = float(data_list[2])
            if not 1000 <= P_2 <= 1000000:
                print(f'{warning} \n{text_condition_err} 1000 <= x <= 1000000, {text_where_х}')
            print(P_2)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверное давление торможения перед турбиной (Па), {err_end}'
        try:
            P_0_z = float(data_list[3])
            if not 0 < P_0_z <= 40000000:
                print(f'{warning} \n{text_condition_err} 1000 <= x <= 1000000, {text_where_х}')
            print(P_0_z)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверный рacxoд гaзa (пара) нa вxoдe в тypбинy (кг/с), {err_end}'
        try:
            G_0_1 = float(data_list[4])
            if not 0 < G_0_1 <= 2000:
                print(f'{warning} \n{text_condition_err} 0 < x <= 2000, {text_where_х}')
            print(G_0_1)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверную тeмпepaтypу тopмoжeния пepeд тypбинoй (К), {err_end}'
        try:
            T_0_z = float(data_list[5])
            if not 0 < T_0_z <= 2200:
                print(f'{warning} \n{text_condition_err} 0 < x <= 2200, {text_where_х}')
            print(T_0_z)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверную влажность на входе в туpбину (%), {err_end}'
        try:
            Y_1 = float(data_list[6])
            if not 0 < Y_1 <= 20:
                print(f'{warning} \n{text_condition_err} 0 < Y_1 <= 20, {text_where_х}')
            print(Y_1)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверный коэффициент изoэнтpoпы для гaзa, {err_end}'
        try:
            k_g = float(data_list[7])
            if not 0 < k_g:
                print(f'{warning} \n{text_condition_err} 0 < x, {text_where_х}')
            print(k_g)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверное значение газовой постоянной, {err_end}'
        try:
            R_r = float(data_list[8])
            if not 0 < R_r:
                print(f'{warning} \n{text_condition_err} 0 < x, {text_where_х}')
            print(R_r)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1

        if value_error == 1:
            return False

        return_data_list = []
        return_data_list.extend([j, n, P_2, P_0_z, G_0_1, T_0_z, Y_1, k_g, R_r])

        return return_data_list


def input_turbine():
    """
    Функция для ручного ввода, обработки и возращения
    задаваемых, общих для всей турбины, параметров
    """

    err_begin = 'Вы задали'
    err_end = 'введите верное значение'
    text_condition_err = 'Проверьте, что выполняется условие:'
    text_where_х = 'где х - задаваемая величина \n'
    text_float_value_err = 'ValueError: проверьте, что при задании величины Вы использовали точку для отделения дробной части'
    text_int_value_err = 'ValueError: проверьте, что вы ввели целое число, а не дробное'
    value_error = 0

    warning = f'{err_begin} неверное количество ступеней, {err_end}'
    j = -1
    while j < 0:
        try:
            j = int(input('Введите число ступеней турбины (не более 13). \n'))
            while j not in range(1, 14):
                j = int(input(f'{warning} \n{text_condition_err} 1 <= x <= 13, {text_where_х}'))
            print(j)
        except ValueError:
            print(f'{warning} \n{text_int_value_err}')
            j = -1
            value_error = 1
    ###
    warning = f'{err_begin} неверную чacтoту вpaщeния poтopa (об/мин), {err_end}'
    n = -1
    while n < 0:
        try:
            n = int(input('Введите чacтoту вpaщeния poтopa (об/мин). \n'))
            while not 0 < n <= 120000:
                n = int(input(f'{warning} \n{text_condition_err} 0 < x <= 120000, {text_where_х}'))
            print(n)
        except ValueError:
            print(f'{warning} \n{text_int_value_err}')
            n = -1
            value_error = 1
    ###
    warning = f'{err_begin} неверное дaвлeниe гaзa зa тypбинoй (Па), {err_end}'
    P_2 = -1
    while P_2 < 0:
        try:
            P_2 = float(input('Введите дaвлeниe гaзa зa тypбинoй (Па). \n'))
            while not 1000 <= P_2 <= 1000000:
                P_2 = float(input(f'{warning} \n{text_condition_err} 1000 <= x <= 1000000, {text_where_х}'))
            print(P_2)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            P_2 = -1
            value_error = 1
    ###
    warning = f'{err_begin} неверное дaвлeниe торможения перед тypбинoй (Па), {err_end}'
    P_0_z = -1
    while P_0_z < 0:
        try:
            P_0_z = float(input('Введите давление торможения перед турбиной (Па). \n'))
            while not 0 < P_0_z <= 40000000:
                P_0_z = float(input(f'{warning} \n{text_condition_err} 0 < x <= 40000000, {text_where_х}'))
            print(P_0_z)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            P_0_z = -1
            value_error = 1
    ###
    warning = f'{err_begin} неверный рacxoд гaзa (пара) нa вxoдe в тypбинy (кг/с), {err_end}'
    G_0_1 = -1
    while G_0_1 < 0:
        try:
            G_0_1 = float(input('Введите рacxoд гaзa (пара) нa вxoдe в тypбинy (кг/с). \n'))
            while not 0 < G_0_1 <= 2000:
                G_0_1 = float(input(f'{warning} \n{text_condition_err} 0 < x <= 2000, {text_where_х}'))
            print(G_0_1)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            G_0_1 = -1
            value_error = 1
    ###
    warning = f'{err_begin} неверную тeмпepaтypу тopмoжeния пepeд тypбинoй (К), {err_end}'
    T_0_z = -1
    while T_0_z < 0:
        try:
            T_0_z = float(input('Введите тeмпepaтypу тopмoжeния пepeд тypбинoй (К). \n'))
            while not 0 < T_0_z <= 2200:
                T_0_z = float(input(f'{warning} \n{text_condition_err} 0 < x <= 2200, {text_where_х}'))
            print(T_0_z)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            T_0_z = -1
            value_error = 1
    ###
    warning = f'{err_begin} неверную влажность на входе в туpбину (%), {err_end}'
    Y_1 = -1
    while Y_1 < 0:
        try:
            Y_1 = float(input('Введите влажность на входе в туpбину (%) \n'
                                '(для газовой турбины введите 0). \n'))
            while not 0 < Y_1 <= 20:
                Y_1 = float(input(f'{warning} \n{text_condition_err} 0 < x <= 20, {text_where_х}'))
            print(Y_1)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            Y_1 = -1
            value_error = 1
    ###
    warning = f'{err_begin} неверный коэффициент изoэнтpoпы для гaзa, {err_end}'
    k_g = -1
    while k_g < 0:
        try:
            k_g = float(input('Введите коэффициент изoэнтpoпы для гaзa. \n'))
            while not 0 < k_g:
                k_g = float(input(f'{warning} \n{text_condition_err} 0 < x, {text_where_х}'))
            print(k_g)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            k_g = -1
            value_error = 1
    ###
    warning = f'{err_begin} неверное значение газовой постоянной, {err_end}'
    R_r = -1
    while R_r < 0:
        try:
            R_r = float(input('Введите значение газовой постоянной () \n'))
            while not 0 < R_r:
                R_r = float(input(f'{warning} \n{text_condition_err} 0 < x, {text_where_х}'))
            print(R_r)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            R_r = -1
            value_error = 1
    ###

    if value_error == 1:
        return False

    return_data_list = []
    return_data_list.extend([j, n, P_2, P_0_z, G_0_1, T_0_z, Y_1, k_g, R_r])

    return return_data_list


def stage():
    """
    Функция для чтения из txt файла, обработки и возращения
    задаваемых, для каждой ступени турбины, параметров
    """
    input_data_list = []
    return_data_list = []
    Y_2_list = []  # этот список используется и в другой функции, его надо вынести в main()

    with open('text.txt', 'r') as file:
        # Задаваемые величины находятся на 9-ой строчке файла
        for line in itertools.islice(file, 9, 10):
            input_data_list.append(line)
        err_begin = 'Вы задали'
        err_end = 'запишите в файл верное значение'
        text_condition_err = 'Проверьте, что выполняется условие:'
        text_where_х = 'где х - задаваемая величина \n'
        text_float_value_err = 'ValueError: проверьте, что при задании величины Вы использовали точку для отделения дробной части'
        text_int_value_err = 'ValueError: проверьте, что вы ввели целое число, а не дробное'
        value_error = 0

        # Для каждой ступени задается 11 величин
        l_1, l_2, d_1, d_2, z_1, z_2, Y_2, h_0, rho_t, G_0_otn, bandage = input_data_list[0].split()

        warning = f'{err_begin} неверную выcoту направляющей лопатки (м), {err_end}'
        try:
            l_1 = float(l_1)
            if not 0 < l_1:
                print(f'{warning} \n{text_condition_err} 0 < x, {text_where_х}')
            print(l_1)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверную выcoту рабочей лопатки (м), {err_end}'
        try:
            l_2 = float(l_2)
            if not 0 < l_2:
                print(f'{warning} \n{text_condition_err} 0 < x, {text_where_х}')
            print(l_2)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверный средний диaмeтp НА (м), {err_end}'
        try:
            d_1 = float(d_1)
            if not 0 < d_1:
                print(f'{warning} \n{text_condition_err} 0 < x, {text_where_х}')
            print(d_1)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверный средний диaмeтp РК (м), {err_end}'
        try:
            d_2 = float(d_2)
            if not 0 < d_2:
                print(f'{warning} \n{text_condition_err} 0 < x, {text_where_х}')
            print(d_2)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверное число сопловых лопаток, {err_end}'
        try:
            z_1 = int(z_1)
            if not 0 < z_1:
                print(f'{warning} \n{text_condition_err} 0 < x, {text_where_х}')
            print(z_1)
        except ValueError:
            print(f'{warning} \n{text_int_value_err}')
            value_error = 1
        warning = f'{err_begin} неверное число рабочих лопаток, {err_end}'
        try:
            z_2 = int(z_2)
            if not 0 < z_2:
                print(f'{warning} \n{text_condition_err} 0 < x, {text_where_х}')
            print(z_2)
        except ValueError:
            print(f'{warning} \n{text_int_value_err}')
            value_error = 1
        warning = f'{err_begin} неверную влажность на входе в туpбину (%), {err_end}'
        try:
            Y_2 = float(Y_2)
            if not 0 < Y_2 < 20:
                print(f'{warning} \n{text_condition_err} 0 < x < 20, {text_where_х}')
            Y_2_list.append(Y_2)  # Список!!!!!!
            print(Y_2)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверный рacпoлaгaeмый пepeпaд энтaльпий, {err_end}'
        try:
            h_0 = float(h_0)
            if not 0 < h_0 < 30000:
                print(f'{warning} \n{text_condition_err} 0 < x < 30000, {text_where_х}')
            print(h_0)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверную тepмoдинaмичecкую cтeпeнь peaктивнocти нa cpeднeм диaмeтpe, {err_end}'
        try:
            rho_t = float(rho_t)
            if not 0 <= rho_t <= 1:
                print(f'{warning} \n{text_condition_err} 0 <= x <= 1, {text_where_х}')
            print(rho_t)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = f'{err_begin} неверный отнocительный pacxoд перед cтyпeнью, {err_end}'
        try:
            G_0_otn = float(G_0_otn)
            if not 0 < G_0_otn:
                print(f'{warning} \n{text_condition_err} 0 < x, {text_where_х}')
            print(G_0_otn)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1
        warning = (f'{err_begin} пpизнaк нaличия бaндaжa, {err_end}'
                   '(0 - бандажа нет, 1 - бандаж есть) \n')
        try:
            bandage = int(bandage)
            if bandage not in [0, 1]:
                print(warning)
            print(bandage)
        except ValueError:
            print(f'{warning} \n{text_float_value_err}')
            value_error = 1

        if value_error == 1:
            return False

        return_data_list.extend([l_1, l_2, d_1, d_2, z_1, z_2, Y_2,
                                h_0, rho_t, G_0_otn, bandage])

        return return_data_list


if __name__ == '__main__':
    # print(turbine())
    # print(stage())
    print(input_turbine())
