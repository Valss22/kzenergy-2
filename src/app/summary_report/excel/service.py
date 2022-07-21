import pandas as pd
from xlsxwriter.worksheet import Worksheet

from src.app.facility.model import Facility
from src.app.summary_report.excel.types import Excel
from src.app.ticket.excel.styles import TicketStyle

COLNAMES = [
    "Объект", "Вид отхода",
    "Агрегатное состояние", "Кол-во в тоннах",
    "Кол-во в м3", "Кол-во в штуках",
    "Захоронено", "Утилизировано",
    "Переработано", "Передано подрядческой организации",
    "Повторно использовано", "Комментарий", "Дата"
]

COL_OFFSET = 4
ROW_OFFSET = 3

def write_title(date, fullname, worksheet, workbook):
    title = f"Сводный отчет от {fullname} {date}"
    worksheet.write(1, COL_OFFSET + 4, title, workbook.add_format(TicketStyle.title))


def write_col_names(worksheet, workbook):
    for col in range(len(COLNAMES)):
        col_offset = col + COL_OFFSET
        worksheet.write(ROW_OFFSET, col_offset, COLNAMES[col], workbook.add_format(TicketStyle.header))
        if len(COLNAMES[col].split(" ")) > 1:
            col_size = (2 + len(COLNAMES[col])) / 1.5
        else:
            col_size = 2 + len(COLNAMES[col])
        worksheet.set_column(col_offset, col_offset, col_size)


async def write_values(excel_data: list[Excel], worksheet, workbook):
    row_i = ROW_OFFSET + 1
    for excel_row in excel_data:
        wastes = excel_row["facility"]["wastes"]
        waste_num = len(wastes)
        row_v = row_i - 1
        for waste in wastes:
            row_v += 1
            i = 0
            col_i = COL_OFFSET + 1
            for key, value in waste.items():
                if col_i > (COL_OFFSET + 1 + len(COLNAMES)):
                    break
                if len(str(value)) >= len(COLNAMES[i]):
                    col_size = 1 + len(str(value))
                    worksheet.set_column(col_i, col_i, col_size)
                worksheet.write(
                    row_v, col_i, value,
                    workbook.add_format(TicketStyle.body)
                )
                i += 1
                col_i += 1
        fac_name = excel_row["facility"]["name"]
        if len(fac_name) >= len("Объект"):
            col_size = 1 + len(fac_name)
            worksheet.set_column(COL_OFFSET, COL_OFFSET, col_size)
        worksheet.write(
            row_i, COL_OFFSET, excel_row["facility"]["name"],
            workbook.add_format(TicketStyle.body)
        )
        worksheet.write(
            row_i + waste_num - 1, COL_OFFSET, "",
            workbook.add_format(TicketStyle.body)
        )
        row_i += 1


async def write_excel_sum_report(excel_data: list[Excel], date, fullname):
    df = pd.DataFrame()
    writer = pd.ExcelWriter("sum_report.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="sum_report", index=False)
    worksheet: Worksheet = writer.sheets["sum_report"]
    workbook = writer.book

    write_title(date, fullname, worksheet, workbook)
    write_col_names(worksheet, workbook)
    await write_values(excel_data, worksheet, workbook)
    writer.save()
