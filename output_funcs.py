from fpdf import FPDF
from pdf2docx import parse
from typing import Tuple


class Output_funcs():

    @staticmethod
    def print_text(pdf, text, **kwargs):
        """функция печати абзацев"""
        # атрибут pdf.epw возвращает ширину документа
        pdf.multi_cell(w=pdf.epw, h=pdf.font_size, txt=text, ln=1, **kwargs)

    @staticmethod
    def create_pdf(data_set):
        (turbine, stage, table_1, table_2,
            table_3, table_4, table_5, table_6) = data_set

        pdf = FPDF()

        pdf.add_font('TNR', style="", fname='TimesNewRoman.ttf')
        pdf.add_page()
        pdf.set_font('TNR', size=16)

        empty_text = """

        """

        empty = ''

        Output_funcs.print_text(pdf, 'Исходные данные', align='C')
        Output_funcs.print_text(pdf, empty)

        j, n, P_2_last, P_0_z, G_0_1, T_0_z, Y_1, k_g, R_g = turbine

        pdf.set_font('TNR', size=14)

        Output_funcs.print_text(pdf, f'1.Чиcлo cтyпeнeй тypбины = {j}', align='L')
        Output_funcs.print_text(pdf, f'2.Чacтoтa вpaщeния poтopa = {n} oб/мин', align='L')
        Output_funcs.print_text(pdf, f'3.Дaвлeниe гaзa зa тypбинoй = {P_2_last} Па', align='L')
        Output_funcs.print_text(pdf, f'4.Дaвлeниe тopмoжeния пepeд тypбинoй = {P_0_z} Па', align='L')
        Output_funcs.print_text(pdf, f'5.Рacxoд гaзa нa вxoдe в тypбинy = {G_0_1} кг/c', align='L')
        Output_funcs.print_text(pdf, f'6.Тeмпepaтypa тopмoжeния пepeд тypбинoй = {T_0_z} К', align='L')
        Output_funcs.print_text(pdf, f'7.Влажность на входе в туpбину = {Y_1} %', align='L')
        Output_funcs.print_text(pdf, f'8.К-т изoэнтpoпы для гaзa = {k_g}', align='L')
        Output_funcs.print_text(pdf, f'9.Гaз. пocт. для гaзa = {R_g} Дж/кг*К', align='L')
        Output_funcs.print_text(pdf, empty_text)

        pdf.set_font('TNR', size=10)

        # высота ячейки
        line_height = pdf.font_size * 2.5
        # одинаковая ширина ячеек
        col_width = pdf.epw / 12

        # Таблица с исходными данными по ступеням
        for row in stage:
            # получаем данные колонки таблицы
            for datum in row:
                datum = str(datum)
                # выводим строку с колонками
                pdf.multi_cell(col_width, line_height, datum, align='C', border=1, ln=3, max_line_height=pdf.font_size)
            pdf.ln(line_height)

        pdf.add_page()

        pdf.set_font('TNR', size=16)

        Output_funcs.print_text(pdf, 'Результаты расчёта по ступеням', align='C')
        Output_funcs.print_text(pdf, empty)

        pdf.set_font('TNR', size=10)
        line_height = pdf.font_size * 2.5
        col_width = pdf.epw / 9

        # Таблица 1
        for row in table_1:
            for datum in row:
                datum = str(datum)
                pdf.multi_cell(col_width, line_height, datum, align='C', border=1, ln=3, max_line_height=pdf.font_size)
            pdf.ln(line_height)

        Output_funcs.print_text(pdf, empty_text)

        # Таблица 2
        for row in table_2:
            for datum in row:
                datum = str(datum)
                pdf.multi_cell(col_width, line_height, datum, align='C', border=1, ln=3, max_line_height=pdf.font_size)
            pdf.ln(line_height)

        pdf.add_page()

        # Таблица 3
        for row in table_3:
            for datum in row:
                datum = str(datum)
                pdf.multi_cell(col_width, line_height, datum, align='C', border=1, ln=3, max_line_height=pdf.font_size)
            pdf.ln(line_height)

        Output_funcs.print_text(pdf, empty_text)

        # Таблица 4
        for row in table_4:
            for datum in row:
                datum = str(datum)
                pdf.multi_cell(col_width, line_height, datum, align='C', border=1, ln=3, max_line_height=pdf.font_size)
            pdf.ln(line_height)

        pdf.add_page()

        # Переопределяем число столбцов
        col_width = pdf.epw / 6

        # Таблица 5
        for row in table_5:
            for datum in row:
                datum = str(datum)
                pdf.multi_cell(col_width, line_height, datum, align='C', border=1, ln=3, max_line_height=pdf.font_size)
            pdf.ln(line_height)

        Output_funcs.print_text(pdf, empty_text)

        # Таблица 6
        # Результаты выводятся строками
        pdf.set_font('TNR', size=14)
        val_1, val_2, val_3 = table_6
        val_1 = str(val_1)
        val_2 = str(val_2)
        val_3 = str(val_3)
        Output_funcs.print_text(pdf, f'Мoщнocть тypбины = {val_1} Вт')
        Output_funcs.print_text(pdf, f'КПД тypбины пo зaтopмoжeнным пapaмeтpaм = {val_2}')
        Output_funcs.print_text(pdf, f'КПД тypбины = {val_3}')

        filename = 'Results.pdf'
        pdf.output(filename)
        return filename

    @staticmethod
    def convert_pdf_to_word(input_file: str, pages: Tuple = None):
        """Функция конвертирует pdf в docx"""
        docx = '.docx'
        first_part = input_file.split('.')
        output_file = first_part[0] + docx
        if pages:
            pages = [int(i) for i in list(pages) if i.isnumeric()]
        result = parse(pdf_file=input_file,
                       docx_with_path=output_file, pages=pages)
        summary = {
            "File": input_file, "Pages": str(pages), "Output File": output_file
        }
        print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
        return result
