from openpyxl import Workbook, load_workbook
import pandas as pd

from collecting import hoarder
from openpyxl.utils.dataframe import dataframe_to_rows
from table_compared import compared


def save_in_excel(data_list, path):
    try:
        workbook = load_workbook(path)
        sheet = workbook.active
    except FileNotFoundError:
        workbook = Workbook()
        sheet = workbook.active

    headers = list(data_list[0].keys())

    if sheet.max_row == 1:
        for col_idx, header in enumerate(headers, start=1):
            cell = sheet.cell(row=1, column=col_idx, value=header)

    next_row = sheet.max_row + 1

    for item in data_list:
        for col_idx, header in enumerate(headers, start=1):
            cell = sheet.cell(row=next_row, column=col_idx, value=item[header])
        next_row += 1

    workbook.save(path)


def second_save(data_list, original_path, compared_path):
    save_in_excel(data_list, compared_path)
    compared(original_path, compared_path)


original_table = 'original.xlsx'
compared_table = 'compared.xlsx'

counter = 1
while True:
    if hoarder(counter):
        save_in_excel(hoarder(counter), original_table)
        counter += 1
    else:
        break


