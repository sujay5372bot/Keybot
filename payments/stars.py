#djjdhd
def stars_invoice(app, chat_id):
    return app.send_invoice(
        chat_id,
        "Premium",
        "1 Month Premium",
        "premium",
        "",
        "XTR",
        [{"label":"Premium","amount":99}]
    )
