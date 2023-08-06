import openpyxl
import time
from search_sale import ya_search


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время выполнения функции {func.__name__}: {execution_time:.6f} секунд")
        return result
    return wrapper


@timing_decorator
def link_collecting(table):
    workbook = openpyxl.load_workbook(table)
    sheet = workbook.active
    list_link_ = []
    for row in range(2, sheet.max_row-1):
        cell_value = sheet.cell(row=row, column=2).value
        list_link = ya_search(cell_value, 20)
        count = 5
        for link in list_link:
            if 'https://market.yandex.ru' not in link and 'https://www.vseinstrumenti.ru' not in link \
                    and 'https://www.WildBerries.ru' not in link:
                sheet.cell(row=row, column=count, value=link)
                list_link_.append(link)
                count += 1
    workbook.save(table)

    return list_link_


test_table = 'Test.xlsx'
list_link = link_collecting(test_table)
print(list_link)
