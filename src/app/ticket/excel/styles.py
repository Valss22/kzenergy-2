# style = {
#     "body": {
#         'text_wrap': True,
#         'valign': 'top',
#         'border': 1,
#         'bg_color': '#FFE7E7',
#     },
#     "header": 0
# }


class Style:
    body = {
        'text_wrap': True,
        'valign': 'top',
        'border': 1,
        'bg_color': '#FFE7E7',
    }
    header = {**body, "bold": True}
