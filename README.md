# alipay_customs
Simply demo for alipay customs

# How to Use
Python 3.6+
pip3 --cache-dir=.pip install -i https://pypi.douban.com/simple/ -r requirements.txt
# Setup Alipay Customs Module
1. 报关接入流程 https://opendocs.alipay.com/support/01rgj9    
2. Configuration:
```shell
    _APP_PRIVATE_KEY = 'MIICXAIBAAKBg**'
    _CHARSET = "utf-8"
    _PARTNER = "2088**"
    _MERCHANT_CUSTOMS_CODE = "3110**"
    _MERCHANT_CUSTOMS_NAME = "**"
    _CUSTOMS_PLACE = "zongshu"
    _SERVER_URL = "https://mapi.alipay.com/gateway.do"
```
# Declare Payment Order to Customs
1. update payment order fields
```shell
    param_fields = {
        ...
        "out_request_no": "customs20220520001",
        "trade_no": "20220**",
        "amount": "0.02",
    }
```
2. change to project directory and run `python customs.py`