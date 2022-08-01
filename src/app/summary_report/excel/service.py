import pandas as pd
from xlsxwriter.worksheet import Worksheet
from src.app.summary_report.schemas import SummaryReportOut
from src.app.ticket.excel.styles import TicketStyle

COLNAMES = [
    "Объект", "Вид отхода",
    "Агрегатное состояние", "Кол-во в тоннах",
    "Кол-во в м3", "Кол-во в штуках",
    "Захоронено", "Утилизировано",
    "Переработано", "Передано подрядческой организации",
    "Повторно использовано", "Комментарий", "Дата"
]

COL_OFFSET = 2
ROW_OFFSET = 3


def write_title(date, fullname, worksheet, workbook):
    title = f"Сводный отчет от {fullname} ({date})"
    worksheet.write(1, COL_OFFSET + 4, title, workbook.add_format(TicketStyle.title))


def write_col_names(worksheet, workbook):
    for col in range(len(COLNAMES)):
        col_offset = col + COL_OFFSET
        worksheet.write(ROW_OFFSET, col_offset, COLNAMES[col], workbook.add_format(TicketStyle.header))
        if len(COLNAMES[col].split(" ")) > 1:
            col_size = (2 + len(COLNAMES[col])) / 1.5
        else:
            if COLNAMES[col] == "Дата":
                col_size = 10
            else:
                col_size = 2 + len(COLNAMES[col])
        worksheet.set_column(col_offset, col_offset, col_size)


async def write_values(sum_rep_arr: list[list[str]], total_arr, worksheet, workbook):
    row_i = ROW_OFFSET + 1

    for row in sum_rep_arr:
        col_i = COL_OFFSET
        for value in row:
            if type(value) is not float and len(value) >= len(COLNAMES[col_i - COL_OFFSET]):
                col_size = 1 + len(value)
                worksheet.set_column(col_i, col_i, col_size)
            worksheet.write(
                row_i, col_i, value,
                workbook.add_format(TicketStyle.body)
            )
            col_i += 1
        row_i += 1
    total_row_i = ROW_OFFSET + 1 + len(sum_rep_arr)
    worksheet.write(
        total_row_i, COL_OFFSET, "Сумма",
        workbook.add_format(TicketStyle.total)
    )
    total_cols_i = [5, 6, 7, 8, 9, 10, 11, 12]
    col_i = COL_OFFSET + 1
    total_i = 0
    for i in range(12):
        value = ""
        if col_i in total_cols_i:
            value = total_arr[total_i]
            worksheet.write(
                total_row_i, col_i, value,
                workbook.add_format(TicketStyle.total)
            )
            total_i += 1
        worksheet.write(
            total_row_i, col_i, value,
            workbook.add_format(TicketStyle.total)
        )
        col_i += 1


def sum_rep_to_array(sum_report_tickets: list[dict]) -> list[list]:
    sum_report_arr = []
    for ticket in sum_report_tickets:
        sum_report_arr_ticket = []
        for key, value in ticket.items():
            if type(value) is dict:
                for k, v in value.items():
                    sum_report_arr_ticket.append(v)
            else:
                if key == "aggregateState":
                    sum_report_arr_ticket.append(value.value)
                elif key == "date":
                    sum_report_arr_ticket.append(str(value))
                else:
                    sum_report_arr_ticket.append(value)
        sum_report_arr.append(sum_report_arr_ticket)
    return sum_report_arr


async def write_excel_sum_report(sum_report: SummaryReportOut):
    print(sum_report.dict()["total"])
    sum_report = sum_report.dict()
    username = sum_report["user"]["fullname"]
    date = str(sum_report["date"])

    del sum_report["id"]
    del sum_report["date"]
    del sum_report["user"]
    del sum_report["excel"]
    for ticket in sum_report["tickets"]:
        del ticket["id"]

    total_arr = [value for key, value in sum_report["total"].items()]
    sum_report_arr = sum_rep_to_array(sum_report["tickets"])
    df = pd.DataFrame()
    writer = pd.ExcelWriter("sum_report.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="sum_report", index=False)
    worksheet: Worksheet = writer.sheets["sum_report"]
    workbook = writer.book
    write_title(date, username, worksheet, workbook)
    write_col_names(worksheet, workbook)
    await write_values(sum_report_arr, total_arr, worksheet, workbook)
    writer.save()
