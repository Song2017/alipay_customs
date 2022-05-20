import base64
import json
import logging
from urllib.parse import quote_plus

import requests
import rsa

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a', )
logger = logging.getLogger('')


def get_sign_content(all_params):
    sign_content = ""
    for (k, v) in sorted(all_params.items()):
        value = v
        if not isinstance(value, str):
            value = json.dumps(value, ensure_ascii=False)
        sign_content += ("&" + k + "=" + value)
    sign_content = sign_content[1:]
    return sign_content


def sign_with_rsa(sign_content):
    sign_content = sign_content.encode(_CHARSET)
    private_key_str = "-----BEGIN RSA PRIVATE KEY-----"
    private_key_str += f"\n{_APP_PRIVATE_KEY}\n-----END RSA PRIVATE KEY-----"
    signature = rsa.sign(sign_content, rsa.PrivateKey.load_pkcs1(
        private_key_str.encode(), format='PEM'), 'SHA-1')
    sign = base64.b64encode(signature)
    sign = str(sign, encoding=_CHARSET)
    return sign


def declare_customs_get(parameter_fields):
    """
    https://opendocs.alipay.com/pre-open/01x3kh
    """
    paras_sign = dict(parameter_fields)
    paras_sign["sign_type"] = "RSA"
    sign_content = get_sign_content(parameter_fields)
    paras_sign["sign"] = sign_with_rsa(sign_content)
    paras_content = ""
    # get
    response = requests.get(_SERVER_URL, paras_sign)
    logger.info(f"Result: {response.text}")
    # save get url
    for (k, v) in paras_sign.items():
        paras_content += ("&" + k + "=" + quote_plus(v))
    paras_content = paras_content[1:]
    with open("url_customs.txt", "w") as f:
        f.write(_SERVER_URL + '?' + paras_content)


def declare_customs_post(parameter_fields):
    """
    https://opendocs.alipay.com/pre-open/01x3kh
    """
    paras_sign = dict(parameter_fields)
    paras_sign["sign_type"] = "RSA"
    sign_content = get_sign_content(parameter_fields)
    paras_sign["sign"] = sign_with_rsa(sign_content)
    response = requests.request(
        "POST", url=_SERVER_URL, params=paras_sign)
    logger.info(f"Result: {response.text}")


if __name__ == '__main__':
    # 报关接入流程 https://opendocs.alipay.com/support/01rgj9

    # configuration
    _APP_PRIVATE_KEY = 'MIICXAIBAAKBg**'
    _CHARSET = "utf-8"
    _PARTNER = "2088**"
    _MERCHANT_CUSTOMS_CODE = "3110**"
    _MERCHANT_CUSTOMS_NAME = "**"
    _CUSTOMS_PLACE = "zongshu"
    _SERVER_URL = "https://mapi.alipay.com/gateway.do"

    # declare payment order to customs
    param_fields = {
        "service": "alipay.acquire.customs",
        "partner": _PARTNER,
        "_input_charset": _CHARSET,
        # "sign": "",
        "merchant_customs_code": _MERCHANT_CUSTOMS_CODE,
        "merchant_customs_name": _MERCHANT_CUSTOMS_NAME,
        "customs_place": _CUSTOMS_PLACE,
        "out_request_no": "customs20220520001",
        "trade_no": "20220**",
        "amount": "0.02",
    }
    # declare_customs_get(para_fields)
    declare_customs_post(param_fields)
