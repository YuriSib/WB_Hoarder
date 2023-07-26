from collecting import hoarder
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd


def save_in_excel(data_list, start_row=1):
    workbook = Workbook()
    sheet = workbook.active

    headers = list(data_list[0].keys())
    for col_idx, header in enumerate(headers, start=1):
        cell = sheet.cell(row=start_row, column=col_idx, value=header)

    for row_idx, item in enumerate(data_list, start=start_row + 1):
        for col_idx, header in enumerate(headers, start=1):
            cell = sheet.cell(row=row_idx, column=col_idx, value=item[header])

    workbook.save('output.xlsx')


save_in_excel(hoarder(2), 101)