import os.path
import math as m

from output_funcs import Output_funcs
from input_funcs import Input_funcs


# обозначения:
# z - звездочка (*) - параметр заторможенного потока
# otn - черта сверху - относительная величина
# sh - штрих - параметр в корневом сечении ступени
# 2sh - 2 штриха - параметр в переферийном сечении ступени


def main():

    # Проверка на существование подготовленного файла data.txt
    if os.path.exists('data.txt'):
        data_txt = 1
    else:
        data_txt = 0

    # Исходные данные
    file_name_text = ('Введите имя для файлов с результатами, без расширения\n'
                      '(Имя может содержать буквы русского и латинского '
                      'алфавита, цифры и знак нижнего подчеркивания) \n')
    file_name = input(file_name_text)

    file = ''
    text = ('Считать исходные данные из подготовленного файла data.txt? \n'
            '(Введите "yes", если да, или "no", если нет) \n')
    while file not in ['yes', 'no']:

        file = input(text)

        # Для турбины в целом
        file_not_found = 0
        try:
            if file == 'yes':
                print('Начинается чтение из файла data.txt')
                turbine_data_list = Input_funcs.turbine()
                j, n, P_2_last, P_0_z, G_0_1, T_0_z, Y_1, k_g, R_g = turbine_data_list
            elif file == 'no':
                
                print('Начинается ручной ввод данных для турбины в целом')
                turbine_data_list = Input_funcs.input_turbine(data_txt)
                j, n, P_2_last, P_0_z, G_0_1, T_0_z, Y_1, k_g, R_g = turbine_data_list
            else:
                text = ('Вы ввели неверное значение. \n'
                        'Введите "yes", если хотите считать данные из подготовленного файла text.txt \n'
                        'Введите "no", если хотите вводить данные вручную \n')
        except FileNotFoundError:
            print('Не обнаружен подготовленный файл data.txt \n'
                  'Начинается ручной ввод данных для турбины в целом')
            file_not_found = 1
            turbine_data_list = Input_funcs.input_turbine(data_txt)
            j, n, P_2_last, P_0_z, G_0_1, T_0_z, Y_1, k_g, R_g = turbine_data_list

    # Объявление списков перед циклом
    N_list = []
    N_t_list = []
    alfa_list = []
    P_0_list = []
    Y_2_list = []
    Y_2_list.append(Y_1)  # начиная с 1-й ступени к Y_1 можно обратиться по индексу [-2]
    T_0_z_list = []
    T_0_z_list.append(T_0_z)
    P_0_z_list = []
    P_0_z_list.append(P_0_z)

    # Список с исходными данными каждой ступени
    stage_initial_data = [
        ['N', 'L_1', 'L_2', 'D_1', 'D_2', 'Z_1', 'Z_2', 'Y_2', 'H_0', 'RHO_T', 'G_OTN', 'Бандаж'],
        ['—', 'м', 'м', 'м', 'м', '—', '—', '%', 'Дж/кг', '—', '—', '—'],
    ]

    # Общий список для функции создания pdf
    data_set = []

    # Создание списков для data_set
    # Из каждого из этих списков будет сформирована таблица
    table_1 = [
        ['N', 'G1', 'U1', 'C1', 'ALFA1', 'T1', 'T1*', 'TW1*', 'P1'],
        ['—', 'кг/c', 'м/c', 'м/c', 'гpaд', 'К', 'К', 'К', 'Пa'],
    ]
    table_2 = [
        ['N', 'W1', 'BETA1', 'MC1', 'REC1','B1', 'T1/B1', 'DZ1N', 'P1*'],
        ['—', 'м/c', 'гpaд', '—', '—', 'м', '—', '—', 'Пa'],
    ]
    table_3 = [
        ['N', 'G2', 'U2', 'C2', 'ALFA2', 'T2', 'T2*', 'TW2*', 'P2'],
        ['—', 'кг/c', 'м/c', 'м/c', 'гpaд', 'К', 'К', 'К', 'Пa'],
    ]
    table_4 = [
        ['N', 'W2', 'BETA2', 'MW2', 'REW2', 'B2', 'Т2/B2', 'DZ2N', 'P2Y*'],
        ['—', 'м/c', 'гpaд', '—', '—', 'м', '—', '—', 'Пa'],
    ]
    table_5 = [
        ['N', 'HU', 'N3', 'KPDV', 'KPDY*'],
        ['—', 'Дж/кг', 'Вт', '—', '—'],
    ]

    # Для отдельной ступени
    for current_stage in range(1, j + 1):

        if file == 'yes' and file_not_found == 0:
            stage_data_list = Input_funcs.stage(current_stage)
            (l_1, l_2, d_1, d_2, z_1, z_2, Y_2,
             h_0, rho_t, G_0_otn, bandage) = stage_data_list
        else:
            print('Начинается ручной ввод данных для каждой ступени \n'
                  f'Для {current_stage} ступени:')
            stage_data_list = Input_funcs.input_stage(data_txt)
            (l_1, l_2, d_1, d_2, z_1, z_2, Y_2,
             h_0, rho_t, G_0_otn, bandage) = stage_data_list

        stage_data_list.insert(0, current_stage)
        stage_initial_data.append(stage_data_list)
        Y_2_list.append(Y_2)

        # Расчетные формулы

        # Сечение I-I
        print('\nРасчет ступени', current_stage)

        # 1) Теоретическая скорость смеси газа и охлаждающего воздуха С_1_t
        C_0 = m.sqrt(2 * h_0)  # условная скорость
        C_1_t = C_0 * m.sqrt(1-rho_t) # изменение зависит только от C_0

        # 2) Скорость смеси
        fi = 0.97  # Коэффициент скорости в СА
        fi = 0.97  # Коэффициент скорости в СА
        fi_1 = 0.1
        delta_fi = fi - fi_1
        iteration = 1
        while delta_fi / fi_1 >= 10 ** (-4):

            C_v_1 = 1  # для газового расчета уточнить
            C_v_1_otn = 1  # для более точного расчета уточнить
            # C_v_1_otn = C_v_1 / C_1  # задается, относительная скорость воздуха, охл-его НЛ
            G_v_1_otn = 0  # задается пользователем на каждой ступени. G_v_otn = G_v / G_0 - относительный расход на входе в ступень. Отношение расхода в текущей ступени к расходу в первую ступень
            G_v_2_otn = 0  # для газовой уточнить
            C_1 = fi * C_1_t * ((1 + G_v_1_otn * C_v_1) / (1 + G_v_1_otn))

            # 3) Теплоёмкости основного потока и потока охлаждающего воздуха
            R_v = 287100  # Дж /(кг * К)
            k_v = 1.39  # точное значение
            C_pg = k_g / (k_g - 1) * R_g
            C_pv = k_v / (k_v - 1) * R_v

            # 4) Температура смеси в конце изоэнтропного расширения
            T_0_z = T_0_z_list[-1]
            T_1_t = T_0_z - C_1_t**2 / (2 * C_pg)

            # 5) Температура торможения смеси в сечении 1-1
            T_1_v_z = 1  #  принимаем равным 1, температура охлаждающего воздуха
            T_2_v_z = 1  # принимаем равным 1, температура охлаждающего воздуха
            T_1_z = (C_pg * T_0_z + G_v_1_otn * C_pv * T_1_v_z) / (C_pg + G_v_1_otn * C_pv)

            # 6) Температура смеси
            T_1 = T_1_z - (C_1**2) / (2 * C_pg)

            # 7) Давление смеси в конце изоэнтропного расширения
            P_0_z = P_0_z_list[-1]
            P_1 = P_0_z * (T_1_t / T_0_z)**(k_g / (k_g - 1))

            # 8) Давление торможения смеси в сечении 1-1
            P_1_z = P_1 * ((T_1_z / T_1)**(k_g / (k_g - 1)))

            # 9) плотность смеси
            rho_1 = P_1 / (R_g * T_1)

            # 10) Расход утечки рабочего тела через лабиринтовое уплотнение НА
            d_y_t_sh = 0.3  # (300 мм). диаметр лабиринта
            k_y_t = 0.6
            d_1_sh = d_y_t_sh / k_y_t  # корневой диаметр НЛ
            delta_y_t_sh_otn = 0.0008  # (0.8 мм)
            delta_y_t_sh = delta_y_t_sh_otn * d_y_t_sh  # диматер лабиринта
            mi_y_t = 0.95  # коэф. расхода, в зависимости от типа уплотнения
            kpd_rho = 0.8  # точно
            z_ypl = 2  # точное значение
            rho_t_sh = 1 - (1 - rho_t) * ((d_1 / d_1_sh) ** (2 * kpd_rho))  # термодинамическая степень реактивности в корневом сечении ступени
            h_1_sh_z = h_0 * (1 - rho_t_sh)  # изоэнтропийный перепад энтальпий в корневом сечении НЛ
            C_1_t_sh = m.sqrt(2 * h_1_sh_z)  # скорость потока в изоэнтропийном расширении от P_O_z до P_1_sh
            T_1_t_sh = T_0_z - (C_1_t_sh ** 2) / (2 * C_pg)  # Температура в конце изоэнтропинйного расширения от давления P_0_z до P_1_sh
            P_1_sh = P_0_z * ((T_1_t_sh / T_0_z) ** (k_g / (k_g - 1)))  # давление в потоке у корня НЛ

            if current_stage == 1:
                P_0 = P_0_z
            else:
                P_0 = P_0_list[-1]

            G_y_t_sh = m.pi * mi_y_t * k_y_t * d_1_sh * delta_y_t_sh * m.sqrt(((P_0**2) - (P_1_sh**2)) / (R_g * T_0_z * z_ypl))

            # 11) Расход рабочего тела в сечении I-I
            G_0 = G_0_otn * G_0_1
            G_v_1 = 0  # для газовой турбины уточнить
            G_v_1_otn = G_v_1 / G_0  # задается предварительно
            G_1 = G_0 * (1 + G_v_1_otn) - G_y_t_sh  # Исправил повтор в методичке

            # 12) Угол потока в сечении I-I в абсолютном движении
            alfa_1 = m.asin(G_1 / (m.pi * d_1 * l_1 * rho_1 * C_1))
            alfa_1_grad = alfa_1 * 180 / m.pi

            # 13) Коэффициент профильных потерь, обусловленных геометрией НЛ
            if not alfa_list:
                alfa_0 = 90 / 180 * m.pi  # 90 градусов в радинах
            else:
                alfa_0 = alfa_list[-1]
            alfa_0_grad = alfa_0 * 180 / m.pi
            # alfa_0 - угол входа потока в НЛ, отсчитывается от отрицательного направления переносной скорости u
            L_1 = ((alfa_0_grad + alfa_1_grad) ** (0.4)) * m.sin(alfa_0) / m.sin(alfa_1)
            t_1 = m.pi * d_1 / z_1  # шаг НЛ
            a_1 = t_1 * m.sin(alfa_1)
            S_1 = 0.000935  #  принимаем равным 1мм - средняя толщина выходных кромок НЛ (Атлас профилей)
            S_1_otn = S_1 / a_1  # задается, относительная толщина выходных кромок НЛ
            dzeta_1_pr_g = 1.2 / (L_1 ** 2) + (8 * (10 ** (-6))) * (L_1 ** 2) + 0.38 * (S_1_otn ** 2) + 0.034 * S_1_otn + 0.035

            # 14)  Число Маха по скорости C_1
            M_c_1 = C_1 / m.sqrt(k_g * R_g * T_1)

            # 15) Увеличение профильных потерь под влиянием числа M_c_1
            M_c_1_pred = 0.9
            if M_c_1 <= M_c_1_pred:
                delta_dzeta_1_pr_M = 0
            else:
                delta_dzeta_1_pr_M = 0.21 * ((M_c_1 - M_c_1_pred) ** 2)

            # 16) Оптимальный относительный шаг НЛ (если есть охлаждение, необходимо добавить условие)
            Q_1 = 0.45  # коэффициент для НЛ
            C_otn = 0.12
            # alfa_0 и alfa_1 в градусах
            # в методичке ошибка, часть углов в градусах, часть в радианах
            t_1_otn = Q_1 * ((180 / (180 - (alfa_0_grad + alfa_1_grad)) * m.sin(alfa_0) / m.sin(alfa_1)) ** (0.333)) * (1 - C_otn)

            # # 17) Шаг НЛ (определен выше в формуле 13)
            # t_1 = m.pi * d_1 / z_1

            # 18) Хорда НЛ
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
            dzeta_1_pr = dzeta_1_pr_g + delta_dzeta_1_pr_M + delta_dzeta_1_pr_Re

            # 23)  Коэффициент вторичных потерь
            dzeta_1_vt = 2 * dzeta_1_pr * a_1 / l_1

            # 24) Коэффициент потерь для потока через НЛ
            Y_1 = Y_2_list[-2]  # влажность на входе
            delta_Y = Y_2 - Y_1
            Y_rk = delta_Y * rho_t  # влажность в рабочем колесе
            Y_rk_sr = (Y_2 + Y_rk) / 2  # средняя влажность в рабочем колесе
            Y_sa = delta_Y * (1 - rho_t)  # влажность в сопловом аппарате
            Y_sa_sr = (Y_1 + Y_sa) / 2  # средняя влажность в сопловом аппарате

            dzeta_1 = dzeta_1_pr + dzeta_1_vt + G_v_1_otn * ((1 - C_v_1_otn) ** 2) + Y_sa_sr

            # 25) Коэффициент скорости для НЛ
            fi_1 = m.sqrt(1 - dzeta_1)
            delta_fi = fi - fi_1
            if delta_fi < 0:
                delta_fi = delta_fi * (-1)
            fi = fi_1
            iteration += 1
            if iteration == 10:
                delta_fi = 10 ** (-5)
            # Значение fi сравнивается с принятым ранее и, при
            # необходимости, уточняется, а расчет возвращается в пункт 2

        # 26) Осевая и окружная составляющие скорости C_1
        C_1_z = C_1 * m.sin(alfa_1)
        C_1_u = C_1 * m.cos(alfa_1)

        # 27) Угол потока в относительном движении в сечении I-I
        # n - задается, частота вращения ротора
        U_1 = m.pi * d_1 * n / 60  # Окружная скорость
        beta_1 = m.atan(C_1_z / (C_1_u - U_1))
        if beta_1 < 0:
            beta_1 = beta_1 * (-1)
        beta_1_grad = beta_1 * 180 / m.pi

        # 28) Относительная скорость потока в сечении I-I
        W_1 = C_1_z / m.sin(beta_1)

        # 29) Температура торможения в относительном движении в сечении I-I
        T_w_1_z = T_1 + (W_1 ** 2) / (2 * C_pg)
        # Температура на выходе потока из соплового аппарата в относительном движении

        # 30) Давление торможения в относительном движениии в сечении I-I
        P_w_1_z = P_1 * ((T_w_1_z / T_1) ** (k_g / (k_g - 1)))

        # Cечение 2-2

        # 31) Температура торможения потока в относительном движении в сечении 2-2
        U_2 = m.pi * d_2 * n / 60  # окружная скорость
        T_w_2_z = T_w_1_z - ((U_1 ** 2) - (U_2 ** 2)) / (2 * C_pg)

        # 32) Теоретическое давление торможения потока в относительном движении
        P_w_2_t_z = P_w_1_z * ((T_w_2_z / T_w_1_z) ** (k_g / (k_g - 1)))

        # 33) Температура торможения смеси в относительном движении
        T_w_2_cm_z = ((1 + G_v_1_otn) * C_pg * T_w_2_z + G_v_2_otn * (T_2_v_z * C_pv + (U_2 ** 2) / 2)) / ((1 + G_v_1_otn) * C_pg + G_v_2_otn * C_pv)

        # 34) Теоретическая скорость смеси
        W_2_t = m.sqrt(2 * rho_t * h_0 * T_1 / T_1_t + (W_1 ** 2) - (U_1 ** 2) + (U_2 ** 2))

        # 35) Скорость смеси
        Psi = 0.95  # коэффициент скорсоти для РЛ
        Psi_1 = 0.1
        delta_Psi = Psi - Psi_1
        iteration = 1
        while delta_Psi / Psi_1 >= 10 ** (-4):

            C_v_2_otn = 1  # для газовой уточнить
            W_2 = Psi * W_2_t * (1 + G_v_2_otn * C_v_2_otn) / (1 + G_v_2_otn)

            # 36) Температура потока в конце изоэнтропийного расширения
            T_2_t = T_w_2_z - (W_2_t ** 2) / (2 * C_pg)

            # 37) Температура смеси
            T_2 = T_w_2_cm_z - (W_2 ** 2) / (2 * C_pg)

            # 38) Давление смеси
            if current_stage == j:
                P_2 = P_2_last
            else:
                P_2 = P_w_2_t_z * ((T_2_t / T_w_2_z) ** (k_g / (k_g - 1)))
                P_0_list.append(P_2)

            # 39) Плотность смеси
            rho_2 = P_2 / (R_g * T_2)

            # 40) Расход рабочего тела в сечении 2-2
            G_2 = G_0 * G_0 / G_1 * (1 + G_v_1_otn + G_v_2_otn)

            # 41) Угол потока в сечении 2-2 в относительном движении
            beta_2 = m.asin(G_2 / (m.pi * d_2 * l_2 * rho_2 * W_2))
            beta_2_grad = beta_2 * 180 / m.pi

            # 43) Число Маха по скорости W_2
            M_w_2 = W_2 / m.sqrt(k_g * R_g * T_2)

            # 44) Увеличение профильных потерь под влиянием числа M_w_2
            M_w_2_pred = 0.9
            if M_w_2 <= M_w_2_pred:
                delta_dzeta_2_pr_m = 0
            else:
                delta_dzeta_2_pr_m = 0.21 * ((M_w_2 - M_w_2_pred) ** 2)

            # 45) Оптимальный относительный шаг РЛ
            Q_2 = 0.6
            t_2_otn = Q_2 * ((180 / (180 - (beta_1_grad + beta_2_grad)) * m.sin(beta_1) / m.sin(beta_2)) ** (0.333)) * (1 - C_otn)

            # 46) Шаг РЛ (перенес выше)
            t_2 = m.pi * d_2 / z_2

            # 42) Коэффициент профильных потерь, обусловленный геометрией РЛ
            L_2 = ((beta_1_grad + beta_2_grad) ** 0.4) * m.sin(beta_1) / m.sin(beta_2)
            a_2 = t_2 * m.sin(beta_2)  # горло РЛ
            S_2 = 0.0009  # принимаем равным 1мм - средняя толщина выходных кромок РЛ (Атлас профилей)
            S_2_otn = S_2 / a_2  # относительная величина выходных кромок РЛ
            dzeta_2_pr_g = 1.2 / (L_2 ** 2) + 8 * (10 ** (-6)) * (L_2 ** 2) + 0.38 * (S_2_otn ** 2) + 0.034 * S_2_otn + 0.049

            # 47) Хорда РЛ
            b_2 = t_2 / t_2_otn

            # 48) Коэффициент динамической вязкости потока в сечении 2-2
            mi_2 = (0.229 * ((T_2 / 1000) ** 3) - 1.333 * ((T_2 / 1000) ** 2) + 4.849 * (T_2 / 1000) + 0.505 - 0.275 / alfa_v) * 10 ** (-5)

            # 49) Число Рейнольдса для потока в РЛ
            Re_w_2 = W_2 * b_2 * rho_2 / mi_2

            # 50) Увеличение профильных потерь под влиянием числа Re
            if Re_w_2 >= 10 ** (6):
                delta_dzeta_2_pr_Re = 0
            else:
                delta_dzeta_2_pr_Re = 2100 / Re_w_2 - 0.0021

            # 51) Коэффициент профильных потерь
            # не дельта, в методичке опечатка
            dzeta_2_pr = dzeta_2_pr_g + delta_dzeta_2_pr_m + delta_dzeta_2_pr_Re

            # 52) Коэффициент вторичных потерь
            dzeta_2_vt = 2 * dzeta_2_pr * a_2 / l_2

            # 53) Коэффициент потерь для потока через РЛ
            C_2_v_otn = 0  # для газовых уточнить
            # C_2_v_otn = W_2_v / W_2  # средняя приведенная относителная скорость потока вдува
            dzeta_2 = dzeta_2_pr + dzeta_2_vt + G_v_2_otn * ((1 - C_2_v_otn) ** 2) + Y_rk_sr
            dzeta_2 = dzeta_2 - dzeta_2 / 100 * 13  # Вычитаю 13%, чтобы
            # снизить расхождение с данными, получаемыми в первоначальной Опти.
            # Расхождение вызвано разными коэффициентами, взятыми из
            # Атласа профилей. В будущем эти коэффициенты можно уточнить
            # и убрать поправку на 13%

            # 54) Коэффициент скорости для РЛ
            Psi_1 = m.sqrt(1 - dzeta_2)
            delta_Psi = Psi - Psi_1
            if delta_Psi < 0:
                delta_Psi = delta_Psi * (-1)
            Psi = Psi_1
            iteration += 1
            if iteration == 10:
                delta_Psi = 10 ** (-5)
            # значение Psi сравнивается с принятым ранее и, при необходимости,
            # уточняяется, а расчет возвращается в пункт 35

        # Параметры ступени

        # 55) Термодинамическая степень реактивности у переферии ступени
        d_1_2sh = d_1 + l_1
        rho_t_2sh = 1 - (1 - rho_t) * ((d_1 / d_1_2sh) ** (2 * kpd_rho))

        # 56) Радиальный зазор у переферии РЛ
        d_2_2sh = d_2 + l_2
        delta_r_2sh_otn = 0.00115  # Это значение можно уточнить
        delta_r_2sh = delta_r_2sh_otn * d_2_2sh

        # 57) Открытый осевой зазор у переферии обандаженного рабочего колеса
        k_z = 1  # k_z = delta_1 / delta_r_2sh = 1
        # delta_z_2sh
        delta_z_2sh = 0.00115  # Это значение можно уточнить
        delta_1 = k_z * delta_z_2sh

        # 58) Эквивалентный радиальный зазор у переферии обандаженного РК
        mi_ocn = 0.5  # коэффициент расхода в радиальном зазоре (Щегляев)
        mi_oc = mi_ocn - (1 - kpd_rho) / 5
        Z_y = 2  # число лабиринтов
        k_y_2sh = 1  # принимаем равным 1 (Щегляев)
        mi_r = 0.8  # коэффициент расхода в радиальном зазоре (Щегляев)
        delta_eq = ((d_2_2sh / ((mi_oc * d_1_2sh * delta_1) ** 2) + Z_y / ((mi_r * k_y_2sh * delta_z_2sh) ** 2))) ** (-0.5)
        #  mi_oc, mi_r, k_y_2sh коэффициенты расхода через открытый осевой зазор и лабиринтовые уплотнения бандажа

        # 59) Утечка рабочего тела через бандажное уплотнение РК
        A = 0.5
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
        if alfa_2 < 0:
            alfa_2 = alfa_2 * (-1)
        alfa_2_grad = alfa_2 * 180 / m.pi

        alfa_list.append(alfa_2)

        # 62) Абсолютная скорость выхода потока из РК
        C_2 = W_2_z / m.sin(alfa_2)

        # 63) Удельная работа ступени
        h_u = (1 + G_v_1_otn) * C_1 * m.cos(alfa_1) * U_1 + (1 + G_v_1_otn + G_v_2_otn) * C_2 * m.cos(alfa_2) * U_2 - G_v_2_otn * (U_2 ** 2)

        # 64) Окружной КПД ступени
        kpd_u = h_u / h_0

        # 65) Температура торможения за ступенью
        T_2_z = T_2 + (C_2 ** 2) / (2 * C_pg)
        T_0_z_list.append(T_2_z)

        # 66) Внутренний КПД ступени
        Teta_1, Teta_2 = 1, 1  # коэффициенты, характеризующие влияние протечек
        if bandage == 1:
            kpd_v = kpd_u * (1 - (Teta_1 * G_y_t_sh + Teta_2 * G_y_t_2sh) / G_0)
        elif bandage == 0:
            # Если РК не имеет бандажа, то
            kpd_v = kpd_u * (1 - Teta_1 * G_y_t_sh / G_0) - (2 - 0.85 * (1 - kpd_rho)) * delta_r_2sh / l_2

        # 68) Давление торможения за ступенью
        P_2_z = P_2 * ((T_2_z / T_2) ** (k_g / (k_g-1)))
        P_0_z_list.append(P_2_z)

        # 72) Мощность ступени
        N = G_0 * h_u * kpd_v / kpd_u
        N_list.append(N)

        # 73) Давление торможения на входе в следующую ступень
        ae = 1 - (1 - kpd_rho) / 12
        # ae - эмпирический коэффициент, учитывающий эффекты, обсуловленные
        # смешением неравномерного потока за ступенью
        sigma_delta_z = 1  # задается, коэффициент потерь полного давления в патрубке за ступенью
        # Это значение можно уточнить
        P_2_y_z = sigma_delta_z * P_2_z * (((T_2_z - ((1 - ae) * (C_2 ** 2)) / (2 * C_pg)) / T_2_z) ** (k_g / (k_g - 1)))

        # 74) Располагаемый перепад энтальпий на ступень по параметрам
        # торможения с учетом потреь в патрубкеза ступенью
        h_0_y_z = C_pg * T_0_z * (1 - ((P_2_y_z / P_0_z) ** ((k_g - 1) / k_g)))

        # 75) Теоретическая мощность ступени
        N_t = G_0 * h_0_y_z
        N_t_list.append(N_t)

        # 76) КПД ступени по параметрам торможения с учетом потерь в патрубке
        kpd_y_z = N / N_t

        # Округление величин
        round_G_1 = round(G_1, 2)
        round_U_1 = round(U_1, 1)
        round_C_1 = round(C_1, 1)
        round_alfa_1_grad = round(alfa_1_grad, 2)
        round_T_1 = round(T_1, 1)
        round_T_1_z = round(T_1_z, 1)
        round_T_w_1_z = round(T_w_1_z, 1)
        round_P_1 = round(P_1)
        round_W_1 = round(W_1, 1)
        round_beta_1_grad = round(beta_1_grad, 2)
        round_M_c_1 = round(M_c_1, 3)
        round_Re_c_1 = round(Re_c_1)
        round_b_1 = round(b_1, 4)
        round_t_1_otn = round(t_1_otn, 3)
        round_dzeta_1 = round(dzeta_1, 4)
        round_P_1_z = round(P_1_z)
        round_G_2 = round(G_2, 2)
        round_U_2 = round(U_2, 1)
        round_C_2 = round(C_2, 1)
        round_alfa_2_grad = round(alfa_2_grad, 2)
        round_T_2 = round(T_2, 1)
        round_T_2_z = round(T_2_z, 1)
        round_T_w_2_z = round(T_w_2_z, 1)
        round_P_2 = round(P_2)
        round_W_2 = round(W_2, 1)
        round_beta_2_grad = round(beta_2_grad, 2)
        round_M_w_2 = round(M_w_2, 3)
        round_Re_w_2 = round(Re_w_2)
        round_b_2 = round(b_2, 4)
        round_t_2_otn = round(t_2_otn, 3)
        round_dzeta_2 = round(dzeta_2, 4)
        round_P_2_y_z = round(P_2_y_z)
        round_h_u = round(h_u)
        round_N = round(N)
        round_kpd_v = round(kpd_v, 4)
        round_kpd_y_z = round(kpd_y_z, 4)

        # Формирование списка для таблицы №1
        data_for_table_1 = [
            current_stage,
            round_G_1,
            round_U_1,
            round_C_1,
            round_alfa_1_grad,
            round_T_1,
            round_T_1_z,
            round_T_w_1_z,
            round_P_1
        ]
        table_1.append(data_for_table_1)

        # Формирование списка для таблицы №2
        data_for_table_2 = [
            current_stage,
            round_W_1,
            round_beta_1_grad,
            round_M_c_1,
            round_Re_c_1,
            round_b_1,
            round_t_1_otn,
            round_dzeta_1,
            round_P_1_z
        ]
        table_2.append(data_for_table_2)

        # Формирование списка для таблицы №3
        data_for_table_3 = [
            current_stage,
            round_G_2,
            round_U_2,
            round_C_2,
            round_alfa_2_grad,
            round_T_2,
            round_T_2_z,
            round_T_w_2_z,
            round_P_2
        ]
        table_3.append(data_for_table_3)

        # Формирование списка для таблицы №4
        data_for_table_4 = [
            current_stage,
            round_W_2,
            round_beta_2_grad,
            round_M_w_2,
            round_Re_w_2,
            round_b_2,
            round_t_2_otn,
            round_dzeta_2,
            round_P_2_y_z
        ]
        table_4.append(data_for_table_4)

        # Формирование списка для таблицы №5
        data_for_table_5 = [
            current_stage,
            round_h_u,
            round_N,
            round_kpd_v,
            round_kpd_y_z
        ]
        table_5.append(data_for_table_5)

        # Вывод результатов расчета ступени
        print(f'\nРезультаты расчета ступени {current_stage} \n'
              f'G_1 = {round_G_1} кг/с \n'
              f'U_1 = {round_U_1} м/с \n'
              f'C_1 = {round_C_1} м/с \n'
              f'alfa_1 = {round_alfa_1_grad} град. \n'
              f'T_1 = {round_T_1} К \n'
              f'T_1_z = {round_T_1_z} К \n'
              f'T_w_1_z = {round_T_w_1_z} К \n'
              f'P_1 = {round_P_1} Па \n'
              f'W_1 = {round_W_1} м/с \n'
              f'beta_1 = {round_beta_1_grad} град. \n'
              f'M_c_1 = {round_M_c_1} \n'
              f'Re_c_1 = {round_Re_c_1} \n'
              f'b_1 = {round_b_1, 4} м \n'
              f't_1 / b_1 = {round_t_1_otn} \n'
              f'dzeta_1_n = {round_dzeta_1} \n'  # отношение потерь в сопловом аппарате к располагаемому перепаду на СА
              f'P_1_z = {round_P_1_z} Па \n'
              f'G_2 = {round_G_2, 2} кг/с \n'
              f'U_2 = {round_U_2, 1} м/с \n'
              f'C_2 = {round_C_2, 1} м/с \n'
              f'alfa_2 = {round_alfa_2_grad} град. \n'
              f'T_2 = {round_T_2, 1} К \n'
              f'T_2_z = {round_T_2_z} К \n'
              f'T_w_2_z = {round_T_w_2_z} К \n'
              f'P_2 = {round_P_2} Па \n'
              f'W_2 = {round_W_2} м/с \n'
              f'beta_2 = {round_beta_2_grad} град. \n'
              f'M_w_2 = {round_M_w_2} \n'
              f'Re_w_2 = {round_Re_w_2} \n'
              f'b_2 = {round_b_2, 4} м \n'
              f't_2 / b_2 = {round_t_2_otn} \n'
              f'dzeta_2_n = {round_dzeta_2} \n'  # суммарная всех вторых дзет
              f'P_2_y_z = {round_P_2_y_z} Па \n'
              f'h_u = {round_h_u} Дж/кг \n'
              f'N_3 = {round_N} Вт \n'
              f'kpd_v = {round_kpd_v} \n'
              f'kpd_y_z = {round_kpd_y_z} \n')
        current_stage += 1

    # Параметры турбины

    # 81) Суммарная мощность турбины (отсека)
    N_T = sum(N_list)

    # 82) Суммарная мощность турбины теоретическая
    N_T_t = sum(N_t_list)

    # 83) Внутренний КПД турбины по параметрам торможения
    kpd_T_z = N_T / N_T_t

    # 84) Внутренний КПД турбины
    kpd_T = N_T / (N_T_t + G_2 * (C_2 ** 2) / 2)
    # В данном случае G_2 - расход через последнюю ступень турбины
    # В данном случае C_2 - абсолютная скорость на выходе из последней ступени

    # Округление величин
    round_N_T = round(N_T)
    round_kpd_T_z = round(kpd_T_z, 3)
    round_kpd_T = round(kpd_T, 3)

    # Вывод результатов расчета турбины
    print(f'Результаты расчета турбины \n'
          f'Мoщнocть тypбины = {round_N_T} Вт \n'
          f'КПД тypбины пo зaтopмoжeнным пapaмeтpaм = {round_kpd_T_z} \n'
          f'КПД тypбины = {round_kpd_T} \n')

    # Формирование списка для таблицы №6
    table_6 = [
        round_N_T,
        round_kpd_T_z,
        round_kpd_T
    ]

    # Формирование общего списка для ф-ии создания PDF
    data_for_data_set = [
        file_name,
        turbine_data_list,
        stage_initial_data,
        table_1,
        table_2,
        table_3,
        table_4,
        table_5,
        table_6
    ]
    for var in data_for_data_set:
        data_set.append(var)

    return data_set


if __name__ == '__main__':
    Output_funcs.convert_pdf_to_word(Output_funcs.create_pdf(main()))
