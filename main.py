import math as m

from input_funcs import input_stage, input_turbine, stage, turbine



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


P_0_list = []
Y_2_list = []


def main():

    # Исходные данные
    file = input('Считать исходные данные из подготовленного файла text.txt? \n'
                 '(Введите "yes", если да, или "no", если нет)')

    # Для турбины в целом
    while file not in ['yes', 'no']:
        if file == 'yes':
            print('Начинается чтение из файла text.txt')
            turbine_data_list = turbine()
            j, n, P_2, P_0_z, G_0_1, T_0_z, Y_1, k_g, R_r = turbine_data_list
        elif file == 'no':
            print('Начинается ручной ввод данных для турбины в целом')
            turbine_data_list = input_turbine()
            j, n, P_2, P_0_z, G_0_1, T_0_z, Y_1, k_g, R_r = turbine_data_list
        else:
            while file not in ['yes', 'no']:
                file = input('Вы ввели неверное значение. \n'
                             'Введите "yes", если хотите считать данные из подготовленного файла text.txt \n'
                             'Введите "no", если хотите вводить данные вручную')

    P_0_list.append(P_2)
    Y_2_list.append(Y_1)  # начиная с 1-й ступени к Y_1 можно обратиться по индексу [-2]

    # Объявление списков перед циклом
    N_list = []
    N_t_list = []
    alfa_list = []

    # Для отдельной ступени
    for current_stage in range(1, j + 1):

        if file == 'yes':
            stage_data_list = stage(current_stage)
            (l_1, l_2, d_1, d_2, z_1, z_2, Y_2,
             h_0, rho_t, G_0_otn, bandage) = stage_data_list
        elif file == 'no':
            print('Начинается ручной ввод данных для каждой ступени \n'
                  f'Для {current_stage} ступени:')
            stage_data_list = input_stage(current_stage)
            (l_1, l_2, d_1, d_2, z_1, z_2, Y_2,
             h_0, rho_t, G_0_otn, bandage) = stage_data_list

        Y_2_list.append(Y_2)

        # Расчетные формулы

        # Сечение I-I

        # 1) Теоретическая скорость смеси газа и охлаждающего воздуха С_1_t
        C_0 = m.sqrt(2 * h_0)  # условная скорость
        C_1_t = C_0 * m.sqrt(1-rho_t)

        # 2) Скорость смеси
        fi = 0.97  # Коэффициент скорости в СА
        C_v_1 = 1  # для газового расчета уточнить
        C_v_1_otn = 1  # для более точного расчета уточнить
        # C_v_1_otn = C_v_1 / C_1  # задается, относительная скорость воздуха, охл-его НЛ
        G_v_1_otn = 0  # задается пользователем на каждой ступени. G_v_otn = G_v / G_0 - относительный расход на входе в ступень. Отношение расхода в текущей ступени к расходу в первую ступень. Числитель меняется от ступени к ступени.
        G_v_2_otn = 0  # для газовой уточнить
        C_1 = fi * C_1_t * ((1 + G_v_1_otn * C_v_1) / (1 + G_v_1_otn))

        # 3) Теплоёмкости основного потока и потока охлаждающего воздуха
        R_v = 287100  # Дж /(кг * К)
        k_v = 1.39  # точно
        C_pr = k_g / (k_v - 1) * R_r
        C_pv = k_g / (k_v - 1) * R_v

        # 4) Температура смеси в конце изоэнтропного расширения ВОПРОС (здесь и далее T_0_z - для турбины в целом или для ступени?)
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
        d_y_t_sh = 0.3  # (300 мм). диаметр лабиринта
        k_y_t = 0.6
        d_1_sh = d_y_t_sh / k_y_t  # ВОПРОС (Это правильно?). корневой диаметр НЛ
        delta_y_t_sh_otn = 0.0008  # (0.8 мм)
        delta_y_t_sh = delta_y_t_sh_otn * d_y_t_sh  # диматер лабиринта
        mi_y_t = 0.95  # (0.95) . коэф. расхода = [3, 5, 10], в зависимости от типа уплотнения

        #############
        kpd_rho = 0.8  # точно
        z_ypl = 2  # точно
        rho_t_sh = 1 - (1 - rho_t) * (d_1 / d_1_sh) ** (2 * kpd_rho)  # термодинамическая степень реактивности в корневом сечении ступени
        h_1_sh_z = h_0 * (1 - rho_t_sh)  # изоэнтропийный перепад энтальпий в корневом сечении НЛ
        C_1_t_sh = m.sqrt(2 * h_1_sh_z)  # скорость потока в изоэнтропийном расширении от P_O_z до P_1_sh
        T_1_t_sh = T_0_z - C_1_t_sh ** 2 / (2 * C_pr)  # Температура в конце изоэнтропинйного расширения от давления P_0_z до P_1_sh
        P_1_sh = P_0_z * (T_1_t_sh / T_0_z) ** (k_g / (k_g - 1))  # давление в потоке у корня НЛ
        #############
        P_0 = P_0_list[-1]
        G_y_t_sh = m.pi * mi_y_t * k_y_t * d_1_sh * delta_y_t_sh * m.sqrt((P_0**2 - P_1_sh**2) / (R_r * T_0_z * z_ypl))  # ВОПРОС

        # 11) Расход рабочего тела в сечении I-I
        #  ВОПРОС (Откуда брать G_0, G_v_1)
        G_0 = G_0_otn * G_0_1
        G_v_1 = 0  # для газовой турбины уточнить
        G_v_1_otn = G_v_1 / G_0  # задается предварительно
        G_1 = G_0_1 * G_0_otn * (1 + G_v_1_otn) - G_y_t_sh

        # 12) Угол потока в сечении I-I в абсолютном движении
        alfa_1 = m.asin(G_1 / (m.pi * d_1 * l_1 * rho_1 * C_1))

        # 13) Коэффициент профильных потерь, обусловленных геометрией НЛ
        if not alfa_list:
            alfa_0 = 90  # ВОПРОС (уточнить, 90 ли в первой ступени)
        else:
            alfa_0 = alfa_list[-1]
        # alfa_0 - угол входа потока в НЛ, отсчитывается от отрицательного направления переносной скорости u
        L_1 = ((alfa_0 + alfa_1) ** (0.04)) * m.sin(alfa_0 / m.sin(alfa_1))
        t_1 = m.pi * d_1 / z_1  # шаг НЛ
        a_1 = t_1 * m.sin(alfa_1)
        S_1_otn = S_1 / a_1  # ВОПРОС (S_otn или S_1 чему равно? (или это не S, а dzeta?)) задается, относительная толщина входных кромок НЛ
        dzeta_1_pr_r = 1.2 / (L_1 ** 2) + (8 * 10 ** (-6)) * (L_1 ** 2) + 0.38 * (S_1_otn ** 2) + 0.034 * S_1_otn + 0.035

        # 14)  Число Маха по скорости C_1
        M_c_1 = C_1 / m.sqrt(k_g * R_r * T_1)

        # 15) Увеличение профильных потерь под влиянием числа M_c_1
        M_c_1_pred = 0.9  # ВОПРОС (уточнить, так ли это) принимаем, что решетка околозвуковая (для дозвуковой 0.7)
        if M_c_1 <= M_c_1_pred:
            delta_dzeta_1_pr_M = 0
        else:
            delta_dzeta_1_pr_M = 0.21 * ((M_c_1 - M_c_1_pred) ** 2)

        # 16) Оптимальный относительный шаг НЛ (если есть охлаждение, необходимо добавить условие)
        Q_1 = 0.45  # коэффициент для НЛ
        C_otn = 0.12
        # alfa_0 и alfa_1 в градусах
        t_1_otn = Q_1 * ((180 / (180 - (alfa_0 + alfa_1)) * m.sin(alfa_0) / m.sin(alfa_1)) ** (0.333)) * (1 - C_otn)

        # 17) Шаг НЛ
        t_1 = m.pi * d_1 / z_1

        # 18) Хорда Нл
        b_1 = t_1 / t_1_otn

        # 19) Коэффициент динамической вязкости потока в сечении I-I
        alfa_v = 1  # для газовой турбины необходимо запрашивать это значение перед началом расчетов
        mi_1 = (0.229 * ((T_1 / 1000) ** 3) - 1.333 * ((T_1 / 1000) ** 2) + 4.849 * (T_1 / 1000) + 0.505 - 0.275 / alfa_v) * (10 ** (-5))
        # где alfa_v - коэффициент избытка воздуха в осноной камере сгорания ГТД

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
        Y_1 = Y_2_list[-2]  # влажность на входе
        delta_Y = Y_2 - Y_1
        Y_rk = delta_Y * rho_t  # влажность в рабочем колесе
        Y_rk_sr = (Y_2 + Y_rk) / 2  # средняя влажность в рабочем колесе
        Y_sa = delta_Y * (1 - rho_t)  # влажность в сопловом аппарате
        Y_sa_sr = (Y_1 + Y_sa) / 2  # средняя влажность в сопловом аппарате

        dzeta_1 = dzeta_1_pr + dzeta_1_v_t + G_v_1_otn * ((1 - C_v_1_otn) ** 2) + Y_sa_sr

        # 25) Коэффициент скорости для НЛ (ВОПРОС:  эту формулу не использую?)
        # fi = m.sqrt(1 - dzeta_1)
        # Значение fi сравнивается с принятым ранее и, при
        # необходимости, уточняется, а расчет возвращается в пункт 2

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
        Psi = 0.95  # коэффициент скорсоти для РЛ ВОПРОС (надо ли его уточнять?)
        C_v_2_otn = 1  # для газовой уточнить
        W_2 = Psi * W_2_t * (1 + G_v_2_otn * C_v_2_otn) / (1 + G_v_2_otn)  # ВОПРОС (C_v_2_otn)

        # 36) Температура потока в конце изоэнтропийного расширения
        T_2_t = T_w_2_z - (W_2_t ** 2) / (2 * C_pr)

        # 37) Температура смеси
        T_2 = T_w_2_cm_z - (W_2 ** 2) / (2 * C_pr)

        # 38) Давление смеси ВОПРОС (это то же P_2, что и в Дано или нет?)
        P_2 = P_w_2_t_z * ((T_2_t / T_w_2_z) ** (k_g / (k_g - 1)))

        # 39) Плотность смеси
        rho_2 = P_2 / (R_r * T_2)

        # 40) Расход рабочего тела в сечении 2-2
        G_2 = G_0 * G_0 / G_1 * (1 + G_v_1_otn + G_v_2_otn)

        # 41) Угол потока в сечении 2-2 в относительном движении
        beta_2 = m.asin(G_2 / (m.pi * d_2 * l_2 * rho_2 * W_2))

        # 43) Число Маха по скорости W_2
        M_w_2 = W_2 / m.sqrt(k_g * R_r * T_2)

        # 44) Увеличение профильных потерь под влиянием числа M_w_2
        M_w_2_pred = 0.9  # ВОПРОС (уточнить 0.9)
        if M_w_2 <= M_w_2_pred:
            delta_dzeta_2_n_rho_m = 0
        else:
            delta_dzeta_2_n_rho_m = 0.21 * ((M_w_2 - M_w_2_pred) ** 2)

        # 45) Оптимальный относительный шаг РЛ ВОПРОС (эти данные потом нигде не нужны, их стереть?)
        Q_2 = 0.6
        t_2_otn = Q_2 * (((180 / 180 - (beta_1 + beta_2)) * m.sin(beta_1) / m.sin(beta_2)) ** (0.333)) * (1 - C_otn)

        # 46) Шаг РЛ (перенес выше)
        t_2 = m.pi * d_2 / z_2

        # 42) Коэффициент профильных потерь, обусловленный геометрией РЛ
        L_2 = ((beta_1 + beta_2) ** 0.4) * m.sin(beta_1) / m.sin(beta_2)
        a_2 = t_2 * m.sin(beta_2)  # горло РЛ

        # 47) Хорда РЛ
        b_2 = t_2 / t_2_otn

        # 48) Коэффициент динамической вязкости потока в сечении 2-2
        mi_2 = (0.229 * ((T_2 / 1000) ** 3) - 1.333 * ((T_2 / 1000) ** 2) + 4.849 * (T_2 / 1000) + 0.505 - 0.275 / alfa_v) * 10 ** (-5)

        # 49) Число Рейнольдса для потока в РЛ
        Re_w_2 = W_2 * b_2 * rho_2 / mi_2

        # 50) Увеличение профильных потерь под влиянием числа Re
        if Re_w_2 >= 10 ** (6):
            delta_dzeta_2_n_rho_Re = 0
        else:
            delta_dzeta_2_n_rho_Re = 2100 / Re_w_2 - 0.0021

        # 51) Коэффициент профильных потерь ВОПРОС (где используется?)
        # перенесенные формулы
        dzeta_2_otn = dzeta_2 / a_2  # задается, относительная величина входных кромок РЛ
        dzeta_2_n_rho_r = 1.2 / (L_2 ** 2) + 8 * (10 ** (-6)) * (L_2 ** 2) + 0.38 * (dzeta_2_otn ** 2) + 0.034 * dzeta_2_otn + 0.049
        ##########
        delta_dzeta_2_n_rho = dzeta_2_n_rho_r + delta_dzeta_2_n_rho_m + delta_dzeta_2_n_rho_Re

        # 52) Коэффициент вторичных потерь ВОПРОС
        dzeta_2_v_t = 2 * dzeta_2_n_rho * a_2 / l_2

        # 53) Коэффициент потреь для потка через РЛ
        C_2_v_otn = 0  # для газовых уточнить
        # C_2_v_otn = W_2_v / W_2  # средняя приведенная относителная скорость потока вдува
        dzeta_2 = dzeta_2_n_rho * dzeta_2_v_t + G_v_2_otn * ((1 - C_2_v_otn) ** 2) + Y_rk_sr

        # 54) Коэффициент скорости для РЛ ВОПРОС(эту формулу не использовать?)
        # Psi = m.sqrt(1 - dzeta)
        # значение Psi сравнивается с принятым ранее и, при необходимости,
        # уточняяется, а расчет возвращается в пункт 35 ВОПРОС (уточнение значения)

        # Параметры ступени

        # 55) Термодинамическая степень реактивности у переферии ступени ВОПРОС(kpd_rho)
        d_1_2sh = d_1 + l_1
        rho_t_2sh = 1 - (1 - rho_t) * ((d_1 / d_1_2sh) ** (2 * kpd_rho))

        # 56) Радиальный зазор у переферии РЛ
        d_2_2sh = d_2 + l_2
        delta_2_2sh = delta_2_2sh_otn * d_2_2sh
        # ВОПРОС (delta_2_2sh_otn задается)????

        # 57) Открытый осевой зазор у переферии обандаженного рабочего колеса (РК)
        k_z = 1  # k_z = delta_1 / delta_2_2sh = 1
        delta_1 = k_z * delta_z_2sh  # ВОПРОС (может тут не z или до этого было не 2?)

        # 58) Эквивалентный радиальный зазор у переферии обандаженного РК ПРОВЕРИТЬ ШТРИХИ!!!!!!
        mi_ocn = 0.5  # ВОПРОС (уточнить 0.5 ... 0.6)
        mi_oc = mi_ocn - (1 - kpd_rho) / 5
        delta_eq = ((d_2_2sh / ((mi_oc * d_1_2sh * delta_1) ** 2) + Z_y / ((mi_r_2sh * k_y_2sh * delta_z_2sh) ** 2))) ** (-0.5)
        # mi_oc, mi_r, k_y_2sh коэффициенты расхода через открытый осевой зазор и лабиринтовые уплотнения бандажа (ВОПРОС откуда их взять?)
        # Z_y - число лабиринтов (ВОПРОС Z_y = z_ypl?)
        #  mi_r_2sh, k_y_2sh, Z_y_2sh задаются (ВОПРОС)

        # 59) Утечка рабочего тела через бандажное уплотнение РК
        A = C_p_s / C_1_2sh  # ВОПРОС ("обычно А задается")
        if bandage is False:
            G_y_t_2sh = 0
        else:
            G_y_t_2sh = m.pi * d_2_2sh * delta_eq * rho_2 * m.sqrt(rho_t_2sh + ((A * fi) ** 2) * (1 - rho_t_2sh)) * m.sqrt(2 * h_0)
        # C_p_s -скорость на входе в радиальный зазор
        # C_1_2sh - скорость у переферии на выходе из НА

        # 60) Окружная и осевая составляющие относительной скорости
        W_2_u = W_2 * m.cos(beta_2)
        W_2_z = W_2 * m.sin(beta_2)

        # 61) Угол выхода потока из РК в абсолютном движении
        alfa_2 = m.atan(W_2_z / (W_2_u - U_2))
        alfa_list.append(alfa_2)

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
            kpd_v = kpd_u * (1 - (Teta_1 * G_y_t_sh + Teta_2 * G_y_t_2sh) / G_0)
        elif bandage == 0:
            # Если РК не имеет бандажа, то
            kpd_v = kpd_u * (1 - Teta_1 * G_y_t_sh / G_0) - (2 - 0.85 * (1 - kpd_rho)) * delta_2_2sh / l_2
            # ВОПРОС (уточнить условие)

        # 67) Температура за ступенью в конце изоэнтропийного расширения
        T_2_t_t = T_0_z - h_0 / C_pr

        # 68) Давление торможения за ступенью
        P_2_z = P_2 * ((T_2_z / T_2) ** (k_g / (k_g-1)))

        # 69) Давление торможения за ступенью в конце изоэнтропийного расширения
        T_2_t_t_z = T_2_t_t * ((P_2_z / P_2) ** ((k_g - 1) / k_g))

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
        P_2_y_z = sigma_delta_z * P_2_z * (((T_2_z - ((1 - ae) * (C_2 ** 2)) / (2 * C_pr)) / T_2_z) ** (k_g / (k_g - 1)))
        # sigma_delta_z - ВОПРОС (значение?). задается, коэффициент потерь полного давления в патрубке за ступенью


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

        print(f'Результаты расчета ступени {current_stage} \n'
              f'G_1 = {G_1} кг/с \n'
              f'U_1 = {U_1} м/с \n'
              f'C_1 = {C_1} м/с \n'
              f'alfa_1 = {alfa_1} град. \n'
              f'T_1 = {T_1} К \n'
              f'T_1_z = {T_1_z} К \n'
              f'T_1_w_z = {T_1_w_z} К \n'  # ВОПРОС Температура на выходе потока из соплового аппарата в относительном движении T_1 + (W_1 ** 2) / 2 / C_p
              f'P_1 = {P_1} Па \n'
              f'W_1 = {W_1} м/с \n'
              f'beta_1 = {beta_1} град. \n'
              f'M_c_1 = {M_c_1} \n'
              f'Re_c_1 = {Re_c_1} \n'
              f'b_1 = {b_1} м \n'
              f't_1 / b_1 = {t_1_otn} \n'  # относительный шаг профиля
              f'dzeta_1_n = {dzeta_1} \n'  # ВОПРОС (уточнить, правильно ли это (форумла 24)). отношение потерь в сопловом аппарате к располагаемому перепаду на СА 
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
              f'dzeta_2_n = {dzeta_2} \n'  # ВОПРОС (уточнить, правильно ли это (форумла 53)). суммарная всех вторых дзет
              f'P_2_y_z = {P_2_y_z} Па \n'
              ###########################
              f'h_u = {h_u} Дж/кг \n'  # 63
              f'N_3 = {N} Вт \n'  # 72
              f'kpd_v = {kpd_v} \n'  # 66
              f'kpd_y_z = {kpd_y_z} \n')  # 76
        current_stage += 1

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
