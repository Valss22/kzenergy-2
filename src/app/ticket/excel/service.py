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

df = pd.DataFrame()
writer = pd.ExcelWriter("test_file.xlsx", engine='xlsxwriter')
df.to_excel(writer, sheet_name="my_analysis", index=False)
worksheet: Worksheet = writer.sheets['my_analysis']
workbook = writer.book


def write_col_names():
    for col in range(len(COLNAMES)):
        worksheet.write(0, col, COLNAMES[col], workbook.add_format(Style.header))
        col_size = len(COLNAMES[col]) / 1.5
        worksheet.set_column(col, col, col_size)


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
    col = 0
    for key, value in ticket_values.items():
        worksheet.write(1, col, value, workbook.add_format(Style.body))
        col += 1


async def write_ticket_to_excel(ticket: Ticket):
    write_col_names()
    await write_values(ticket)
    writer.save()
