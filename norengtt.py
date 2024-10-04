import requests
import json
import urllib

class NorenGTT:
    __service_config = {
      'host': 'https://api.shoonya.com/NorenWClientTP/',
      'routes': {
          "placegtt": "/PlaceGTTOrder",
          "gtt": "/GetPendingGTTOrder",
          "enabledgtt": "/GetEnabledGTTs",
          "cancelgtt": "/CancelGTTOrder",
          "ocogtt": "/PlaceOCOOrder",
          "modifyoco": "/ModifyOCOOrder", 
      },
      'websocket_endpoint': 'wss://api.shoonya.com/NorenWSTP/',
      #'eoddata_endpoint' : 'http://eodhost/',
      'eodhost':'https://api.shoonya.com/chartApi/getdata/'
    }
    def __init__(self, host, websocket,uid,token):
        self.__service_config['host'] = host
        self.__service_config['websocket_endpoint'] = websocket
        self.__accountid  = uid
        self.__susertoken = token

    def get_enabled_gtt_orders(self):
        config = NorenGTT.__service_config
        url = f"{config['host']}{config['routes']['enabledgtt']}"
        values = {"ordersource": "API"}
        values["uid"] = self.__accountid
        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"
        res = requests.post(url, data=payload)
        resDict = json.loads(res.text)
        if type(resDict) != list:
            return None
        else:
            return resDict
    def place_gtt_order(
        self,
        tradingsymbol: str,
        exchange: str,
        alert_type: str,  # 'LTP_A_O' or 'LTP_B_O' 
        alert_price: float,
        buy_or_sell: str,  # 'B' or 'S'
        product_type: str,  # 'I' Intraday, 'C' Delivery, 'M' Normal Margin for options
        quantity: int,
        price_type: str = "MKT", #"MKT", "LMT"
        price: float = 0.0,
        remarks: str = None,
        retention: str = "DAY",
        validity: str = "GTT",
        discloseqty: int = 0,
    ):
        config = NorenGTT.__service_config
        url = f"{config['host']}{config['routes']['placegtt']}"
        values = {"ordersource": "API"}
        values["uid"] = self.__accountid
        values["actid"] = self.__accountid
        values["tsym"] = urllib.parse.quote_plus(tradingsymbol)
        values["exch"] = exchange
        values["ai_t"] = alert_type
        values["validity"] = validity
        values["d"] = str(alert_price)
        values["remarks"] = remarks
        values["trantype"] = buy_or_sell
        values["prctyp"] = price_type
        values["prd"] = product_type
        values["ret"] = retention
        values["qty"] = str(quantity)
        values["prc"] = str(price)
        values["dscqty"] = str(discloseqty)

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"
        res = requests.post(url, data=payload)
        resDict = json.loads(res.text)
        if type(resDict) != list:
            return None
        else:
            return resDict
    def get_pending_gtt_orders(self):
        config = NorenGTT.__service_config
        url = f"{config['host']}{config['routes']['gtt']}"
        values = {"ordersource": "API"}
        values["uid"] = self.__accountid
        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"
        res = requests.post(url, data=payload)
        resDict = json.loads(res.text)
        if type(resDict) != list:
            return None
        else:
            return resDict
    def cancelgtt(self, alert_id):
        config = NorenGTT.__service_config
        url = f"{config['host']}{config['routes']['cancelgtt']}"
        values = {"ordersource": "API"}
        values["uid"] = self.__accountid
        values["al_id"] = str(alert_id)
        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"
        res = requests.post(url, data=payload)
        resDict = json.loads(res.text)
        if resDict["stat"] != "OI deleted":
            return None
        return resDict["al_id"]