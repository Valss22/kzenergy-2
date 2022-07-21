from datetime import date

import pandas as pd
from xlsxwriter.worksheet import Worksheet

from src.app.ticket.excel.styles import TicketStyle
from src.app.ticket.model import Ticket

COLNAMES = [
    "Дата вывоза", "Вид отхода",
    "Агрегатное состояние", "Метод обращения",
    "Единица измерения",
    "Количество",
    "Объект откуда вывозятся отходы",
    "Ф.И.О, ответственного по управлению отходами на объекте",
    "Комментарий"
]
COL_OFFSET = 4
ROW_OFFSET = 3

async def get_ticket_data(ticket: Ticket):
    facility = await ticket.facility
    facility_name = facility.name
    user = await ticket.user
    username = user.fullname
    print(f"get_ticket_data { ticket.__dict__ }")
    return {
        "Дата вывоза": str(ticket.date),
        "Наименование отходов": ticket.wasteName,
        "Агрегатное состояние отходов": ticket.aggregateState.value,
        "Метод обращения отходов": ticket.wasteDestinationType.value,
        "Единица измерения отходов": ticket.measureSystem.value,
        "Количество отходов": ticket.quantity,
        "Объект откуда вывозятся отходы": facility_name,
        "Ф.И.О, ответственного по управлению отходами на объекте": username,
        "Комментарий": ticket.message,
    }


async def get_max_len_each_col(ticket: Ticket) -> tuple[list[tuple[int, bool]], list[int]]:
    ticket_data = await get_ticket_data(ticket)
    max_len_each_col = []
    len_each_val = []
    i = 0
    for value in ticket_data.values():
        if len(str(value)) > len(COLNAMES[i]):
            max_len_col = len(str(value))
            value_is_longer = True
        else:
            max_len_col = len(COLNAMES[i])
            value_is_longer = False
        max_len_each_col.append((max_len_col, value_is_longer))
        len_each_val.append(len(str(value)))
        i += 1
    return max_len_each_col, len_each_val


def write_title(worksheet, workbook):
    title = "Контрольный Талон для передачи отходов на переработку/размещение"
    worksheet.write(1, 6, title, workbook.add_format(TicketStyle.title))


async def write_col_names(ticket: Ticket, worksheet, workbook):
    tuple_len_cols = await get_max_len_each_col(ticket)
    max_len_each_col = tuple_len_cols[0]
    len_each_val = tuple_len_cols[1]

    for col in range(len(COLNAMES)):
        col_offset = col + COL_OFFSET
        worksheet.write(ROW_OFFSET, col_offset, COLNAMES[col], workbook.add_format(TicketStyle.header))
        if col == 0:
            col_size = 1 + max_len_each_col[col][0]
        elif len(COLNAMES[col].split(" ")) > 1:
            if max_len_each_col[0][1]:
                divide_coef = 1
            else:
                divide_coef = 1.5
            col_size = (2 + max_len_each_col[col][0]) / divide_coef
            if int(col_size) <= len_each_val[col]:
                col_size = (2 + max_len_each_col[col][0])
        else:
            col_size = 2 + max_len_each_col[col][0]
        worksheet.set_column(col_offset, col_offset, col_size)


async def write_values(ticket: Ticket, worksheet, workbook):
    ticket_data = await get_ticket_data(ticket)
    col = COL_OFFSET
    for key, value in ticket_data.items():
        worksheet.write(ROW_OFFSET + 1, col, value, workbook.add_format(TicketStyle.body))
        col += 1


async def write_ticket_to_excel(ticket: Ticket):
    # FIXME: название табл и файла
    df = pd.DataFrame()
    writer = pd.ExcelWriter("ticket.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="ticket_report", index=False)
    worksheet: Worksheet = writer.sheets['ticket_report']
    workbook = writer.book

    write_title(worksheet, workbook)
    await write_col_names(ticket, worksheet, workbook)
    await write_values(ticket, worksheet, workbook)
    writer.save()
