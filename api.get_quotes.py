async def websocket(token, exch="NFO"):
    global feedjson, orderJson

    try:
        feed_opened = False

        # feedjson = {}
        # orderJson = {}

        def event_handler_feed_update(tick_data):
            if ("lp" in tick_data) & ("tk" in tick_data):
                print("tis is the webstocket function")
                feedjson[tick_data["tk"]] = float(tick_data["lp"])
                print(feedjson)

        def event_handler_order_update(order):
            print(f"order feed {order}")
            if ("norenordno" in order) & ("status" in order):
                orderJson[order["norenordno"]] = order["status"]

        def open_callback():
            nonlocal feed_opened
            feed_opened = True

        api.start_websocket(
            order_update_callback=event_handler_order_update,
            subscribe_callback=event_handler_feed_update,
            socket_open_callback=open_callback,
        )

        while feed_opened == False:
            pass

        # token = api.get_quotes(exchange=exch, token=token)
        # token = token["token"]

        api.subscribe(f"{exch}|{token}")

    except Exception as err:
        error(f"this is error in the webstocket {err}")
