#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : EmebddingModel.py
# @Author: Richard Chiming Xu
# @Date  : 2024/6/17
# @Desc  : 向量化模型

import requests
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
import numpy as np
from loguru import logger

from dwspark.config import Config


class EmebddingModel(object):
    def __init__(self, config: Config, model_url: str = 'https://emb-cn-huabei-1.xf-yun.com/'):
        '''
        图片理解（https://www.xfyun.cn/doc/spark/ImageUnderstanding.html）
        :param config: 项目配置文件
        :param model_url: 模型地址
        '''
        # 讯飞的api配置
        self.appid = config.XF_APPID
        self.apikey = config.XF_APIKEY
        self.apisecret = config.XF_APISECRET
        # url地址
        self.model_url = model_url
        self.host, self.path, self.schema = self.__parse_url(model_url)

    def get_embedding(self, text: str, style: str = 'query') -> np.array:
        # 准备请求体
        req_body = {
            "header": {"app_id": self.appid, "status": 3},
            "parameter": {"emb": {"domain": style, "feature": {"encoding": "utf8"}}},
            "payload": {"messages": {"text": base64.b64encode(json.dumps({"messages": [{"content": text, "role": "user"}]}).encode('utf-8')).decode()}}
        }
        # 生成url
        url = self.__create_url("POST")
        # 调用接口
        resp_data = requests.post(url, json=req_body, headers={'content-type': "application/json"}).json()
        # 提取输出
        code = resp_data['header']['code']
        if code != 0:
            raise Exception(f'请求错误: {code}, {resp_data}')
        else:
            sid = resp_data['header']['sid']
            text_base = resp_data["payload"]["feature"]["text"]
            # 使用base64.b64decode()函数将text_base解码为字节串text_data
            text_data = base64.b64decode(text_base)
            # 创建一个np.float32类型的数据类型对象dt，表示32位浮点数。
            dt = np.dtype(np.float32)
            # 使用newbyteorder()方法将dt的字节序设置为小端（"<"）
            dt = dt.newbyteorder("<")
            # 使用np.frombuffer()函数将text_data转换为浮点数数组text，数据类型为dt。
            text = np.frombuffer(text_data, dtype=dt)
            # # 打印向量维度
            return text

    def __create_url(self, method="GET"):
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        # date = "Thu, 12 Dec 2019 01:57:27 GMT"
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(self.host, date, method, self.path)
        signature_sha = hmac.new(self.apisecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.apikey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        values = {
            "host": self.host,
            "date": date,
            "authorization": authorization
        }

        return self.model_url + "?" + urlencode(values)

    def __parse_url(self, requset_url):
        stidx = requset_url.index("://")
        host = requset_url[stidx + 3:]
        schema = requset_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise Exception("错误的请求地址:" + requset_url)
        path = host[edidx:]
        host = host[:edidx]
        return host, path, schema


if __name__ == '__main__':
    config = Config()
    em = EmebddingModel(config)
    vector = em.get_embedding("我们是datawhale")
    logger.info(vector)
