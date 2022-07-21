class TicketStyle:
    body = {
        "text_wrap": True,
        "valign": 'top',
        "border": 1,
        "bg_color": '#F5FFFA',
    }
    header = {
        **body,
        "bold": True,
        "bg_color": "F0FFF0"
    }
    title = {
        "bold": True,
        "font_size": 17,
    }
    extra_body = {**body, "border": 0}
