from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles.colors import COLOR_INDEX


def within_range(bounds: tuple, cell: Cell) -> bool:
    """
    Функция, определяющая, входит ли клетка в состав большой слитой или нет.
    :param bounds: границы merged клеток
    :param cell: сама клетка
    :return: True, если merged клетка, иначе False
    """
    column_start, row_start, column_end, row_end = bounds  # границы merged клетки
    row = cell.row  # проверка, находится ли клетка в этом слиянии
    if row_start <= row <= row_end:  # ___________________
        column = cell.column  # |value|empty|empty|
        if (
            column_start <= column <= column_end
        ):  # |empty|empty|empty|  Пример merged клетки
            return True  # |empty|empty|empty|
    return False


def get_value_merged(sheet: Worksheet, cell: Cell) -> any:
    """
    Функция, возвращающая значение, лежащее в клетке, вне зависимости от того, является ли клетка merged, или нет.
    :param sheet: таблица с расписанием
    :param cell: клетка таблицы
    :return: значение, лежащее в клетке
    """
    for (
        merged
    ) in (
        sheet.merged_cells
    ):  # смотрим в списке слитых клеток (структура данных openpyxl.worksheet)
        if within_range(merged.bounds, cell):
            return sheet.cell(
                merged.min_row, merged.min_col
            ).value  # смотрим значение в левой верхней клетке
    return cell.value


def get_color_merged(sheet: Worksheet, cell: Cell) -> any:
    """
    Функция, возвращающая цвет клетки, вне зависимости от того, является ли клетка merged, или нет.
    :param sheet: таблица с расписанием
    :param cell: клетка таблицы
    :return: значение, лежащее в клетке
    """
    for (
        merged
    ) in (
        sheet.merged_cells
    ):  # смотрим в списке слитых клеток (структура данных openpyxl.worksheet)
        if within_range(merged.bounds, cell):
            # смотрим цвет левой верхней клетки
            color = sheet.cell(merged.min_row, merged.min_col).fill.start_color.index
            color = (
                "#" + COLOR_INDEX[color][2:] if type(color) == int else "#" + color[2:]
            )
            return color
    color = cell.fill.start_color.index
    color = "#" + COLOR_INDEX[color][2:] if type(color) == int else "#" + color[2:]
    return color
