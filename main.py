from cmath import atan
import math as m


def is_digit(string):
    """Проверяет, является ли строка числом"""
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def is_positive_digit(string):
    """Проверяет, является ли строка положительным числом"""
    if string.isdigit():
        if int(string) > 0:
            return True
        else:
            return False
    else:
        try:
            if float(string) > 0:
                return True
            else:
                return False
        except ValueError:
            return False


def is_positive_int_digit(string):
    """Проверяет, является ли строка целым положительным числом"""
    if string.isdigit():
        if int(string) > 0:
            return True
    else:
        return False

# Вопросы:
#   1) delta_y_t_sh
#   2) P_0 ?
#   3) Должны ли быть еще какие нибудь исходные данные?

# обозначения:
# z - звездочка (*) - параметр заторможенного потока
# otn - черта сверху - относительная величина
# sh - штрих - параметр в корневом сечении ступени
# 2sh - 2 штриха - параметр в переферийном сечении ступени

# заданные величины:




def main():

    # Исходные данные

    # Для турбины в целом
    engine = input('Введите название двигателя \n')
    j = input('Введите число ступеней турбины (не более 13). \n')
    while j not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']:
        j = input('Вы задали неверное количество ступеней, введите верное значение \n')
    j = int(j)
    n = input('Введите чacтoту вpaщeния poтopa (об/мин). \n')
    while not is_positive_int_digit(n) and 0 < int(n) < 120000:
        n = input('Вы задали неверную чacтoту вpaщeния poтopa, введите верное значение \n')
    n = int(n)
    input('Введите дaвлeниe гaзa зa тypбинoй (Па). \n')  # ВОПРОС P_T уточнить от 1000 до 1000000
    alfa_v = input('Введите коэффициент избыткa вoздyxa в кaмepe cгopaния \n'  # ВОПРОС (19-ая формула)
                   '(для паровой турбины необходимо ввести 1). \n')
    while not 0 < float(alfa_v) < 5:
        alfa_v = input('Вы задали неверный коэффициент избыткa вoздyxa в кaмepe cгopaния. \n'  
                       'Введите верное значение (для паровой турбины необходимо ввести 1). \n')
    alfa_v = float(alfa_v)
    P_0_z = input('Введите давление торможения перед турбиной (Па). \n')
    while not 0 < float(P_0_z) < 40000000:
        P_0_z = input('Вы задали неверное давление торможения перед турбиной \n'
                      'Введите верное значение. \n')
    P_0_z = float(P_0_z)
    G_0_1 = input('Введите рacxoд гaзa (пара) нa вxoдe в тypбинy (кг/с). \n')
    while not 0 < float(G_0_1) < 2000:
       G_0_1 = input('Вы задали неверный рacxoд гaзa (пара) нa вxoдe в тypбинy \n'
                     'Введите верное значение. \n')
    G_0_1 = float(G_0_1)
    T_0_z = input('Введите тeмпepaтypу тopмoжeния пepeд тypбинoй (К). \n')
    while not 0 < float(T_0_z) < 2200:
        T_0_z = input('Вы задали неверную тeмпepaтypу тopмoжeния пepeд тypбинoй (К). \n'
                      'Введите верное значение. \n')
    T_0_z = float(T_0_z)
    input('Введите влажность на входе в туpбину (%) \n'      # Y_1 в dzeta_1_n искать
          '(для газовой турбины введите 0). \n')
    k_g = input(f'Введите коэффициент изoэнтpoпы для гaзa. \n')  # > 0
    while not is_positive_digit(k_g):
        k_g = input('Вы задали неверный коэффициент изoэнтpoпы для гaзa. \n'
                    'Введите верное значение. \n')
    k_g = float(k_g)
    # k_g = 1.035 + 0.1 * (1 - y) - для влажного пара, где y - степень влажности
    R_r = input('Введите значение газовой постоянной () \n')
    while not is_positive_digit(R_r):
        R_r = input('Вы задали неверное значение газовой постоянной. \n'
                    'Введите верное значение. \n')
    R_r = float(R_r)

    # Объявление списков перед циклом
    N_list = []
    N_t_list = []

    # Для отдельной ступени
    for stage in range(1, j + 1):
        print(f'Для {stage} ступени:')
        l_1 = input('Введите выcoту направляющей лопатки (м). \n')
        while not is_positive_digit(l_1):
            l_1 = input('Вы задали неверную выcoту направляющей лопатки. \n'
                        'Введите верное значение. \n')
        l_1 = float(l_1)
        l_2 = input('Введите выcoту рабочей лопатки (м). \n')
        while not is_positive_digit(l_2):
            l_2 = input('Вы задали неверную выcoту рабочей лопатки. \n'
                        'Введите верное значение. \n')
        l_2 = float(l_2)
        d_1 = int(input('Введите средний диaмeтp НА (м). \n'))
        while not is_positive_digit(d_1):
            d_1 = input('Вы задали неверный средний диaмeтp НА. \n'
                        'Введите верное значение. \n')
        d_1 = float(d_1)
        d_2 = int(input('Введите средний диaмeтp РК (м). \n'))
        while not is_positive_digit(d_2):
            d_2 = input('Вы задали неверный средний диaмeтp РК. \n'
                        'Введите верное значение. \n')
        d_2 = float(d_2)
        z_1 = input('Введите число сопловых лопаток. \n')
        while not is_positive_int_digit(z_1):
            z_1 = input('Вы задали неверное число сопловых лопаток. \n'
                        'Введите верное значение. \n')
        z_1 = int(z_1)
        z_2 = input('Введите число рабочих лопаток. \n')
        while not is_positive_int_digit(z_2):
            z_2 = input('Вы задали неверное число рабочих лопаток. \n'
                        'Введите верное значение. \n')
        z_2 = int(z_2)
        input('Введите влажность на выходе из ступени (%). \n')  # ВОПРОС (где это надо?) Y_2
            # от 0 включительно, до 20 %
        h_0 = input('Введите рacпoлaгaeмый пepeпaд энтaльпий (Дж/кг). \n')
        while not 0 < float(h_0) < 30000:
            h_0 = input('Вы задали неверный рacпoлaгaeмый пepeпaд энтaльпий. \n'
                        'Введите верное значение. \n')
        h_0 = float(h_0)
        rho_t = input(f'Введите тepмoдинaмичecкую cтeпeнь peaктивнocти нa cpeднeм диaмeтpe. \n')
        while not 0 <= float(rho_t) <= 1:
            rho_t = input('Вы задали неверную тepмoдинaмичecкую cтeпeнь peaктивнocти нa cpeднeм диaмeтpe. \n'
                          'Введите верное значение. \n')
        rho_t = float(rho_t)
        G_v_0_otn = input(f'Введите отнocительный pacxoд перед cтyпeнью. \n')  # ВОПРОС (это G_v_1_otn или G_v_2_otn). отношение расхода пара в текущей ступени к расходу в 1 ступень
        while not is_positive_digit(G_v_0_otn):
            G_v_0_otn = input('Вы задали неверный отнocительный pacxoд перед cтyпeнью. \n'
                          'Введите верное значение. \n')
        G_v_0_otn = float(G_v_0_otn)
        bandage = input(f'Введите пpизнaк нaличия бaндaжa \n'
            f'(0 - бандажа нет, 1 - бандаж есть) \n')
        while bandage not in ['0', '1']:
            bandage = input(f'Введите 0, если бандажа нет, или 1, если бандаж есть. \n')
        bandage = int(bandage)  # ВОПРОС (на что влияет в расчетах)

        # Расчетные формулы

        # Сечение I-I

        # 1) Теоретическая скорость смеси газа и охлаждающего воздуха С_1_t
        C_0 = m.sqrt(2 * h_0)  # условная скорость
        C_1_t = C_0 * m.sqrt(1-rho_t)

        # 2) Скорость смеси
        fi = 0.97  # Потом надо будет уточнить по результатам расчета потерь. Коэффициент скорости в СА
        C_v_1 = 1  # задается, ВОПРОС
        G_v_1_otn = 0  # ВОПРОС. задается пользователем на каждой ступени. G_v_otn = G_v / G_0 - относительный расход на входе в ступень. Отношение расхода в текущей ступени к расходу в первую ступень. Числитель меняется от ступени к ступени.
        G_v_2_otn = 0  # ВОПРОС. уточнить!
        C_1 = fi * C_1_t * ((1 + G_v_1_otn * C_v_1) / (1 + G_v_1_otn))
        C_v_1_otn = C_v_1 / C_1  # задается, относительная скорость воздуха, охл-его НЛ

        # 3) Теплоёмкости основного потока и потока охлаждающего воздуха
        R_v = 287100  # Дж /(кг * К)
        k_v = 1.39  # точно
        C_pr = k_g / (k_v - 1) * R_r
        C_pv = k_g / (k_v - 1) * R_v

        # 4) Температура смеси в конце изоэнтропного расширения ВОПРОС (здесь и далее T_0_z - для турбины в целом или для стуаени?)
        T_1_t = T_0_z - C_1_t**2 / (2 * C_pr)

        # 5) Температура торможения смеси в сечении 1-1
        T_1_v_z = 1  # ВОПРОС (у меня нигде больше нет охлаждения, какой коэффициент брать?). задается, температура охлаждающего воздуха
        T_2_v_z = 1  # задается,температура охлаждающего воздуха
        T_1_z = (C_pr * T_0_z + G_v_1_otn * C_pv * T_1_v_z) / (C_pr + G_v_1_otn * C_pv)

        # 6) Температура смеси
        T_1 = T_1_z - C_1**2 / (2 * C_pr)

        # 7) Давление смеси в конце изоэнтропного расширения
        P_1 = P_0_z * (T_1_t / T_0_z)**(k_g / (k_g - 1))

        # 8) Давление торможения смеси в сечении 1-1
        P_1_z = P_1 * (T_1_z / T_1)**(k_g / (k_g - 1))

        # 9) плотность смеси
        rho_1 = P_1 / (R_r - T_1)

        # 10) Расход утечки рабочего тела через лабиринтовое уплотнение НА
        d_y_t_sh = 1  # ВОПРОС (откуда брать). диаметр лабиринта
        delta_y_t_sh_otn  # задается. ВОПРОС (Откуда брать)
        delta_y_t_sh = delta_y_t_sh_otn * d_y_t_sh  # диматер лабиринта
        mi_y_t = 3  # ВОПРОС (как и где выбиарется). коэф. расхода = [3, 5, 10], в зависимости от типа уплотнения
        d_1_sh = 1  # ВОПРОС (Откуда брать). корневой диаметр НЛ
        k_y_t = d_y_t_sh / d_1_sh  # ВОПРОС (это надо использовать?)
        k_y_t = 0.6
        #############
        kpd_rho = 0.8  # точно
        z_ypl = 2  # точно
        rho_t_sh = 1 - (1 - rho_t) * (d_1 / d_1_sh) ** (2 * kpd_rho)  # термодинамическая степень реактивности в корневом сечении ступени
        h_1_sh_z = h_0 * (1 - rho_t_sh)  # изоэнтропийный перепад энтальпий в корневом сечении НЛ
        C_1_t_sh = m.sqrt(2 * h_1_sh_z)  # скорость потока в изоэнтропийном расширении от P_O_z до P_1_sh
        T_1_t_sh = T_0_z - C_1_t_sh ** 2 / (2 * C_pr)  # Температура в конце изоэнтропинйного расширения от давления P_0_z до P_1_sh
        P_1_sh = P_0_z * (T_1_t_sh / T_0_z) ** (k_g / (k_g - 1))  # давление в потоке у корня НЛ
        #############
        G_y_t_sh = m.pi * mi_y_t * k_y_t * d_1_sh * delta_y_t_sh * m.sqrt((P_0**2 - P_1_sh**2) / (R_r * T_0_z * z_ypl)) # ВОПРОС

        # 11) Расход рабочего тела в сечении I-I
        #  ВОПРОС (Откуда брать G_0, G_v_1)
        G_0_otn = G_0 / G_0_1  # задается предварительно
        G_v_1_otn = G_v_1 / G_0  # задается предварительно
        G_1 = G_0_1 * G_0_otn * (1 + G_v_1_otn) - G_y_t_sh

        # 12) Угол потока в сечении I-I в абсолютном движении
        alfa_1 = m.asin(G_1 / (m.pi * d_1 * l_1 * rho_1 * C_1))

        # 13) Коэффициент профильных потерь, обусловленных геометрией НЛ
        L_1 = ((alfa_0 + alfa_1) ** (0.04)) * m.sin(alfa_0 / m.sin(alfa_1))  # ВОПРОС
        alfa_n_i = alfa_2 * (i + 1)  # ВОПРОС (совсем непонятно) угол входа потока в НЛ, отсчитывается от отрицательного направления переносной скорости u
        t_1 = m.pi * d_1 / z_1  # шаг НЛ
        a_1 = t_1 * m.sin(alfa_1)
        dzeta_1_otn = dzeta_1 / a_1  # задается, относительная толщина входных кромок НЛ
        dzeta_1_pr_r = 1.2 / (L_1 ** 2) + (8 * 10 ** (-6)) * (L_1 ** 2) + 0.38 * (dzeta_1_otn ** 2) + 0.034 * dzeta_1_otn + 0.035

        # 14)  Число Маха по скорости C_1
        M_c_1 = C_1 / m.sqrt(k_g * R_r * T_1)

        # 15) Увеличение профильных потерь под влиянием числа M_c_1
        M_c_1_pred = 0.9  # принимаем, что решетка околозвуковая (для дозвуковой 0.7)
        if M_c_1 <= M_c_1_pred:
            delta_dzeta_1_pr_M = 0
        else:
            delta_dzeta_1_pr_M = 0.21 * ((M_c_1 - M_c_1_pred) ** 2)

        # 17) Шаг НЛ
        t_1 = m.pi * d_1 / z_1

        # 18) Хорда Нл
        b_1 = t_1 / t_1_otn

        # 16) Оптимальный относительный шаг НЛ
        Q_1 = 0, 45  # коэффициент для НЛ
        if freezing:  # ВОПРОС (убираю улосвие?)
            C_otn = 0, 2
        else:
            C_otn = 0, 12
        # alfa_0 и alfa_1 в градусах
        t_1_otn = t_1 / b_1  # = Q_1 * (180 / (180 - (alfa_0 + alfa_1)) * m.sin(alfa_0) / m.sin(alfa_1)) ** (0,333) * (1 - C_otn)

        # 19) Коэффициент динамической вязкости потока в сечении I-I
        mi_1 = (0.229 * ((T_1 / 1000) ** 3) - 1.333 * ((T_1 / 1000) ** 2) + 4.849 * (T_1 / 1000) + 0.505 - 0.275 / alfa_v) * (10 ** (-5))
        # где alfa_v - (численное значение??) коэффициент избытка воздуха в осноной камере сгорания ГТД 

        # 20) Число Рейнольдса для потока в НЛ
        Re_c_1 = C_1 * b_1 * rho_1 / mi_1

        # 21) Увеличение профильных потерь под влиянием числа Re
        if Re_c_1 >= 10 ** 6:
            delta_dzeta_1_pr_Re = 0
        else:
            delta_dzeta_1_pr_Re = 2100 / Re_c_1 - 0.0021

        # 22)  Коэффициент профильных потерь
        dzeta_1_pr = dzeta_1_pr_r + delta_dzeta_1_pr_M + delta_dzeta_1_pr_Re

        # 23)  Коэффициент вторичных потерь
        dzeta_1_v_t = 2 * dzeta_1_pr * a_1 / l_1  # ПРОВЕРИТЬ ФОРМУЛУ!!!!

        # 24) Коэффициент потерь для потока через НЛ
        dzeta_1 = dzeta_1_pr + dzeta_1_v_t + G_v_1_otn * ((1 - C_v_1_otn) ** 2)

        # 25) Коэффициент скорости для НЛ
        fi = m.sqrt(i - dzeta_1)  # ПРОВЕРИТЬ ФОРМУЛУ !!!!
        # Значение fi сравнивается с принятым ранее и, при
        # необходимости, уточняется, а расчет возвращается в пункт 2
        # ЭТОТ МОМЕНТ НЕОБХОДИМО УТОЧНИТЬ !!!!

        # 26) Осевая и окружная составляющие скорости C_1
        C_1_z = C_1 * m.sin(alfa_1)
        C_1_u = C_1 * m.cos(alfa_1)

        # 27) Угол потока в относительном движении в сечении I-I
        # n - задается, частота вращения ротора
        U_1 = m.pi * d_1 * n / 60  # Окружная скорость
        beta_1 = m.atan(C_1_z / (C_1_u - U_1))

        # 28) Относительная скорость потока в сечении I-I
        W_1 = C_1_z / m.sin(beta_1)

        # 29) Температура торможения в относительном движении в сечении I-I
        T_w_1_z = T_1 + (W_1 ** 2) / (2 * C_pr)

        # 30) Давление торможения в относительном движениии в сечении I-I
        P_w_1_z = P_1 + (((T_w_1_z ** 2) / T_1) ** (k_g / (k_g - 1)))

        # Cечение 2-2

        # 31) Температура торможения потока в относительном движении в сечении 2-2
        U_2 = m.pi * d_2 * n / 60  # окружная скорость
        T_w_2_z = T_w_1_z - ((U_1 ** 2) - (U_2 ** 2) / (2 * C_pr))

        # 32) Теоретическое давление торможения потока в относительном движении
        P_w_2_t_z = P_w_1_z + ((T_w_2_z / T_w_1_z) ** (k_g / (k_g - 1)))

        # 33) Температура торможения смеси в относительном движении ВОПРОС (надо ли рассчитывать это)
        T_w_2_cm_z = ((1 + G_v_1_otn) * C_pr * T_w_2_z + G_v_2_otn * (T_2_v_z * C_pv + (U_2 ** 2) / 2)) / ((1 + G_v_1_otn) * C_pr + G_v_2_otn * C_pv)

        # 34) Теоретическая скорость смеси
        W_2_t = m.sqrt(2 * rho_t * h_0 * T_1 / T_1_t + (W_1 ** 2) - (U_1 ** 2) + (U_1 ** 2))

        # 35) Скорость смеси
        # Psi = W_2 / W_2_t
        Psi = 0.95 # коэффициент скорсоти для РЛ ВОПРОС (надо ли его уточнять?)
        W_2 = Psi * W_2_t * (1 + G_v_2_otn * C_v_2_otn) / (1 + G_v_2_otn)  # ВОПРОС (C_v_2_otn)

        # 36) Температура потока в конце изоэнтропийного расширения
        T_2_t = T_w_2_z - (W_2_t ** 2) / (2 * C_pr)

        # 37) Температура смеси
        T_2 = T_w_2_cm_z - (W_2 ** 2) / (2 * C_pr)

        # 38) Давление смеси
        P_2 = P_w_2_t_z * ((T_2_t / T_w_2_z) ** (k_g / (k_g - 1)))

        # 39) Плотность смеси
        rho_2 = P_2 / (R * T_2)  # ВОПРОС (R - это газовая постояннаяя R_r из ДАНО?)

        # 40) Расход рабочего тела в сечении 2-2
        G_2 = G_0 * G_0 / G_1 * (1 + G_v_1_otn + G_v_2_otn)

        # 41) Угол потока в сечении 2-2 в относительном движении
        beta_2 = m.asin(G_2 / (m.pi * d_2 * l_2 * rho_2 * W_2))

        # 46) Шаг РЛ (перенес выше)
        t_2 = m.pi * d_2 / z_2

        # 42) Коэффициент профильных потерь, обусловленный геометрией РЛ
        L_2 = ((beta_1 + beta_2) ** 0.4) * m.sin(beta_1) / m.sin(beta_2)
        a_2 = t_2 * m.sin(beta_2)  # горло РЛ
        # Форумлы перенес в пункт

        # 43) Число Маха по скорости W_2
        M_w_2 = W_2 / m.sqrt(k_g * R_r * T_2)

        # 44) Увеличение профильных потерь под влиянием числа M_w_2 ВОПРОС (M_w_2_pred)
        if M_w_2 <= M_w_2_pred:
            delta_dzeta_2_n_rho_m = 0
        else:
            delta_dzeta_2_n_rho_m = 0.21 * ((M_w_2 - M_w_2_pred) ** 2)


        # 47) Хорда РЛ
        b_2 = t_2 / (t_2 / b_2)

        # 45) Оптимальный относительный шаг РЛ ВОПРОС (эти данные потом нигде не нужны, их стереть?)
        Q_2 = 0.6
        C_otn = 0.2  # для охлаждаемых и C_otn = 0.12 для неохлаждаемых решеток
        t_2_otn = t_2 / b_2  # = Q_2 * ((((180 / 180 - (beta_1 + beta_2)) * m.sin(beta_1) / m.sin(beta_2)) ** 0.333) * (1 - C_otn)

        # 48) Коэффициент динамической вязкости потока в сечении 2-2
        mi_2 = (0.229 * ((T_2 / 1000) ** 3) - 1.333 * ((T_2 / 1000) ** 2) + 4.849 * (T_2 / 1000) + 0.505 - 0.275 / alfa_v) * 10 ** (-5)

        # 49) Число Рейнольдса для потока в РЛ
        Re_w_2 = W_2 * b_2 * rho_2 / mi_2

        # 50) Увеличение профильных потерь под влиянием числа Re
        if Re_w_2 >= 10 ** (6):
            delta_dzeta_2_n_rho_Re = 0
        else:
            delta_dzeta_2_n_rho_Re = 2100 / Re_w_2 - 0.0021

        # 51) Коэффициент профильных потерь ВОПРОС
        delta_dzeta_2_n_rho = dzeta_2_n_rho_r + delta_dzeta_2_n_rho_m + delta_dzeta_2_n_rho_Re

        # 52) Коэффициент вторичных потерь ВОПРОС
        dzeta_2_v_t = 2 * dzeta_2_n_rho * a_2 / l_2

        # 53) Коэффициент потреь для потка через РЛ
        C_2_v_otn = W_2_v / W_2  # ВОПРОС. задается, средняя приведенная относителная скорость потока вдува
        dzeta_2 = dzeta_2_n_rho * dzeta_2_v_t + G_v_2_otn * ((1 - C_2_v_otn) ** 2)
        # перенесенные формулы
        dzeta_2_otn = dzeta_2 / a_2  # задается, относительная величина входных кромок РЛ
        dzeta_2_n_rho_r = 1.2 / (L_2 ** 2) + 8 * (10 ** (-6)) * (L_2 ** 2) + 0.38 * (dzeta_2_otn ** 2) + 0.034 * dzeta_2_otn + 0.049

        # 54) Коэффициент скорости для РЛ ВОПРОС(dzeta)
        Psi = m.sqrt(1 - dzeta)
        # значение Psi сравнивается с принятым ранее и, при необходимости,
        # уточняяется, а расчет возвращается в пункт 35 ВОПРОС (уточнение значения)

        # Параметры ступени

        # 55) Термодинамическая степень реактивности у переферии ступени ВОПРОС(kpd_rho)
        d_1_2sh = d_1 + l_1
        rho_t_2sh = 1 - (1 - rho_t) * ((d_1 / d_1_2sh) ** (2 * kpd_rho))

        # 56) Радиальный зазор у переферии РЛ
        d_2_2sh = d_2 + l_2
        delta_2_2sh = delta_2_2sh_otn * d_2_2sh
        # delta_2_2sh_otn задается ????

        # 57) Открытый осевой зазор у переферии обандаженного рабочего колеса (РК)
        k_z = 1  # k_z = delta_1 / delta_2_2sh = 1
        delta_1 = 1 * delta_z_2sh  # ВОПРОС (может тут не z или до этого было не 2?)

        # 58) Эквивалентный радиальный зазор у переферии обандаженного РК ПРОВЕРИТЬ ШТРИХИ!!!!!!
        mi_ocn = 0.5  # ВОПРОС (уточнить 0.5 ... 0.6)
        mi_oc = mi_ocn - (1 - kpd_rho) / 5
        delta_eq = ((d_2_2sh / ((mi_oc * d_1_2sh * delta_1) ** 2) + Z_y / ((mi_r_2sh * k_y_2sh * delta_z_2sh) ** 2))) ** (-0.5)
        # mi_oc, mi_r, k_y_2sh коэффициенты расхода через открытый осевой зазор и лабиринтовые уплотнения бандажа (ВОПРОС откуда их взять?)
        # Z_y - число лабиринтов (ВОПРОС Z_y = z_ypl?)
        #  mi_r_2sh, k_y_2sh, Z_y_2sh задаются (ВОПРОС)

        # 59) Утечка рабочего тела через бандажное уплотнение РК
        A = C_p_s / C_1_2sh  # ВОПРОС
        G_y_t_2sh = m.pi * d_2_2sh * delta_eq * rho_2 * m.sqrt(rho_t_2sh + ((A * fi) ** 2) * (1 - rho_t_2sh)) * m.sqrt(2 * h_0)
        # C_p_s -скорость на входе в радиальный зазор
        # C_1_2sh - скорость у переферии на выходе из НА
        # ВОПРОС УСЛОВИЕ УТОЧНИТЬ!!!!!!!!!!

        # 60) Окружная и осевая составляющие относительной скорости
        W_2_u = W_2 * m.cos(beta_2)
        W_2_z = W_2 * m.sin(beta_2)

        # 61) Угол выхода потока из РК в абсолютном движении
        alfa_2 = m.atan(W_2_z / (W_2_u - U_2))

        # 62) Абсолютная скорость выхода потока из РК
        C_2 = W_2_z / m.sin(alfa_2)

        # 63) Удельная работа ступени
        h_u = (1 + G_v_1_otn) * C_1 * m.cos(alfa_1) * U_1 + (1 + G_v_1_otn + G_v_2_otn) * C_2 * m.cos(alfa_2) * U_2 - G_v_2_otn * (U_2 ** 2)

        # 64) Окружной КПД ступени
        kpd_u = h_u / h_0

        # 65) Температура торможения за ступенью
        T_2_z = T_2 + (C_2 ** 2) / (2 * C_pr)

        # 66) Внутренний КПД ступени
        Teta_1, Teta_2 = 1, 1  # ВОПРОС (это точно?). коэффициенты, характеризующие влияние протечек
        if bandage == 1:
            kpd_v = kpd_u (1 - (Teta_1 * G_y_t_sh + Teta_2 * G_y_t_2sh) / G_0)
        elif bandage == 0:
            # Если РК не имеет бандажа, то
            kpd_v = kpd_u (1 - Teta_1 * G_y_t_sh / G_0) - (2 - 0.85 * (1 - kpd_rho)) * delta_2_2sh / l_2
            # ВОПРОС (уточнить условие)

        # 67) Температура за ступенью в конце изоэнтропийного расширения
        T_2_t_t = T_0_z - h_0 / C_pr

        # 68) Давление торможения за ступенью
        P_2_z = P_2 * ((T_2_z / T_2) ** (k_g / (k_g-1)))

        # 69) Давление торможения за ступенью в конце изоэнтропийного расширения
        T_2_t_t_z = T_2_t_t * ((P_2_z / P_2)** ((k_g - 1) / k_g))

        # 70) Располагаемый перепад энтальпий на ступень по параметрам торможения
        h_0_z = C_pr * (T_0_z - T_2_t_t_z)

        # 71) Внутренний КПД ступени по параметрам торможения
        kpd_v_z = kpd_u * kpd_v / (h_0_z * kpd_u)  # ВОПРОС (куда идёт?)

        # 72) Мощность ступени
        N = G_0 * h_u * kpd_v / kpd_u
        N_list.append(N)

        # 73) Давление торможения на входе в следующую ступень
        ae = 1 - (1 - kpd_rho) / 12
        # ae - эмпирический коэффициент, учитывающий эффекты, обсуловленные
        # смешением неравномерного потока за ступенью
        P_2_y_z = sigma_x_z * P_2_z * (((T_2_z - ((1 - ae) * (C_2 ** 2)) / (2 * C_pr)) / T_2_z) ** (k_g / (k_g - 1)))
        # P_2_y_z = P_0_z(i+1) ВОПРОС (важно ли это)
        # sigma_x_z - ВОПРОС (значение?). задается, коэффициент потерь полного давления в патрубке за ступенью


        # 74) Располагаемый перепад энтальпий на ступень по параметрам
        # торможения с учетом потреь в патрубкеза ступенью
        h_0_y_z = C_pr * T_0_z * (1 - ((P_2_y_z / P_0_z) ** ((k_g - 1) / k_g)))

        # 75) Теоретическая мощность ступени
        N_t = G_0 * h_0_y_z
        N_t_list.append(N_t)

        # 76) КПД ступени по параметрам торможения с учетом потерь в патрубке
        kpd_y_z = N / N_t

        # Вывод результатов расчета ступени
        # ВСЕ ПРИНТЫ НУЖНО ОКРУГЛИТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!
        # ВОПРОС (до скольки знаков после запятой округлять?)

        print(f'Результаты расчета ступени {stage} \n'
              f'G_1 = {G_1} кг/с \n'
              f'U_1 = {U_1} м/с \n'
              f'C_1 = {C_1} м/с \n'
              f'alfa_1 = {alfa_1} град. \n'
              f'T_1 = {T_1} К \n'
              f'T_1_z = {T_1_z} К \n'
              f'T_1_w_z = {T_1_w_z} К \n'  # ВОПРОС Температура на выходе потока из соплового аппарата в относительном движении T_1 + (W_1 ** 2)/ 2 / C_p
              f'P_1 = {P_1} Па \n'
              f'W_1 = {W_1} м/с \n'
              f'beta_1 = {beta_1} град. \n'
              f'M_c_1 = {M_c_1} \n'
              f'Re_c_1 = {Re_c_1} \n'
              f'b_1 = {b_1} м \n'
              f't_1 / b_1 = {t_1_otn} \n'  # относительный шаг профиля
              f'dzeta_1_n = {dzeta_1_n} \n'  # ВОПРОС (откуда брать?). отношение потерь в сопловом аппарате к располагаемому перепаду на СА 
              f'P_1_z = {P_1_z} Па \n'
              #########################
              f'G_2 = {G_2} кг/с \n'
              f'U_2 = {U_2} м/с \n'
              f'C_2 = {C_2} м/с \n'
              f'alfa_2 = {alfa_2} град. \n'
              f'T_2 = {T_2} К \n'
              f'T_2_z = {T_2_z} К \n'
              f'T_2_w_z = {T_2_w_z} К \n'  # ВОПРОС
              f'P_2 = {P_2} Па \n'
              f'W_2 = {W_2} м/с \n'
              f'beta_2 = {beta_2} град. \n'
              f'M_w_2 = {M_w_2} \n'
              f'Re_w_2 = {Re_w_2} \n'
              f'b_2 = {b_2} м \n'
              f't_2 / b_2 = {t_1_otn} \n'
              f'dzeta_2_n = {dzeta_2_n} \n'  # ВОПРОС (уточнить, какие вторые dzeta). суммарная всех вторых дзет
              f'P_2_y_z = {P_2_y_z} Па \n'
              ###########################
              f'h_u = {h_u} Дж/кг \n'  # 63
              f'N_3 = {N} Вт \n'  # 72
              f'kpd_v = {kpd_v} \n'  #  66
              f'kpd_y_z = {kpd_y_z} \n')  #  76
        stage += 1

    # Параметры турбины

    # 81) Суммарная мощность турбины (отсека)
    N_T = sum(N_list)

    # 82) Суммарная мощность турбины теоретическая
    N_T_t = sum(N_t_list)

    # 83) Внутренний КПД турбины по параметрам торможения
    kpd_T_z = N_t / N_T_t

    # 84) Внутренний КПД турбины
    # ВОПРОС (откуда брать G_2_j и C_2_j ?)
    kpd_T = N_T / (N_T_t + G_2_j * (C_2_j ** 2) / 2)
    # G_2_j - расход через последнюю ступень турбины
    # C_2_j - абсолютная скорость на выходе из последней ступени

    # Вывод результатов расчета турбины
    # ВСЕ ПРИНТЫ НУЖНО ОКРУГЛИТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!
    # (ВСЕ ОКРУГЛЕНИЯ НУЖНО СОГЛАСОВАТЬ)

    print(f'Результаты расчета турбины \n'  # ВОПРОС (это все значения, которые нужно вывести?)
          f'Мoщнocть тypбины = {N_T} Вт \n'
          f'КПД тypбины пo зaтopмoжeнным пapaмeтpaм = {kpd_T_z} \n'
          f'КПД тypбины = {kpd_T} \n')
          