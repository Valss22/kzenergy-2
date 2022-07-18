from datetime import date

import pandas as pd
from xlsxwriter.worksheet import Worksheet

from src.app.ticket.excel.styles import Style
from src.app.ticket.model import Ticket

COLNAMES = [
    "Дата вывоза", "Наименование отходов",
    "Агрегатное состояние отходов", "Метод обращения отходов",
    "Единица измерения отходов",
    "Количество отходов",
    "Объект откуда вывозятся отходы",
    "Ф.И.О, ответственного по управлению отходами на объекте",
    "Комментарий"
]
COL_OFFSET = 4
ROW_OFFSET = 3
# FIXME: название табл и файла
df = pd.DataFrame()
writer = pd.ExcelWriter("ticket.xlsx", engine='xlsxwriter')
df.to_excel(writer, sheet_name="ticket_report", index=False)
worksheet: Worksheet = writer.sheets['ticket_report']
workbook = writer.book


def write_title():
    title = "Контрольный Талон для передачи отходов на переработку/размещение"
    worksheet.write(1, 6, title, workbook.add_format(Style.title))


def write_col_names():
    for col in range(len(COLNAMES)):
        col_offset = col + COL_OFFSET
        worksheet.write(ROW_OFFSET, col_offset, COLNAMES[col], workbook.add_format(Style.header))
        if len(COLNAMES[col].split(" ")) > 1:
            col_size = (2 + len(COLNAMES[col])) / 1.5
        else:
            col_size = 2 + len(COLNAMES[col])
        worksheet.set_column(col_offset, col_offset, col_size)


async def write_values(ticket: Ticket):
    facility = await ticket.facility
    facility_name = facility.name
    user = await ticket.user
    username = user.fullname
    ticket_values = {
        "Дата вывоза": str(date.today()),
        "Наименование отходов": ticket.wasteName,
        "Агрегатное состояние отходов": ticket.aggregateState.value,
        "Метод обращения отходов": ticket.wasteDestinationType.value,
        "Единица измерения отходов": ticket.measureSystem.value,
        "Количество отходов": ticket.quantity,
        "Объект откуда вывозятся отходы": facility_name,
        "Ф.И.О, ответственного по управлению отходами на объекте": username,
        "Комментарий": ticket.message,
    }
    col = COL_OFFSET
    for key, value in ticket_values.items():
        worksheet.write(ROW_OFFSET + 1, col, value, workbook.add_format(Style.body))
        col += 1


async def write_ticket_to_excel(ticket: Ticket):
    write_title()
    write_col_names()
    await write_values(ticket)
    writer.save()
