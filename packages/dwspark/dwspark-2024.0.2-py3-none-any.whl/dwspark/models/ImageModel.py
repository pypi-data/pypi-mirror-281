#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ImageModel.py
# @Author: Richard Chiming Xu
# @Date  : 2024/6/17
# @Desc  : 图像模型

import ssl
import websocket
import _thread as thread
import requests
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse
from dwspark.config import Config
from dwspark.utils import img_utils
from loguru import logger


class Text2Img(object):
    def __init__(self, config: Config, model_url: str = 'http://spark-api.cn-huabei-1.xf-yun.com/v2.1/tti'):
        '''
        图片生成（https://www.xfyun.cn/doc/spark/ImageGeneration.html）
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

    def gen_image(self, text: str, save_path: str) -> str:
        '''
        根据需求生成图片
        :param text: 图片描述
        :param save_path: 图片保存地址
        :return: 图片的base64数据
        '''
        # 组装请求体
        req_body = {
            "header": {"app_id": self.appid, "uid": "123456789"},
            "parameter": {"chat": {"domain": "general", "temperature": 0.5, "max_tokens": 4096}},
            "payload": {"message": {"text": [{"role": "user", "content": text}]}}
        }
        # 获取鉴权
        url = self.__create_url()
        # 发起请求
        resp_str = requests.post(url, json=req_body, headers={'content-type': "application/json"}).text
        # 保存图片
        return self.__parser_Message(resp_str, save_path)

    # 保存图片
    def __parser_Message(self, message: str, save_path: str):
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            raise Exception(f'请求错误: {code}, {data}')
        else:
            text = data["payload"]["choices"]["text"]
            imageContent = text[0]
            # if('image' == imageContent["content_type"]):
            imageBase = imageContent["content"]
            # 解码base64数据
            img_data = base64.b64decode(imageBase)
            # 将解码后的数据转换为图片
            img = Image.open(BytesIO(img_data))
            # 保存图片到本地
            img.save(save_path)
            return imageBase

    # 生成url
    def __create_url(self, method="POST"):
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
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

    # 格式化url
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


class ImageUnderstanding(object):

    def __init__(self, config: Config, model_url: str = 'wss://spark-api.cn-huabei-1.xf-yun.com/v2.1/image'):
        '''
        图片理解（https://www.xfyun.cn/doc/spark/ImageUnderstanding.html）
        :param config: 项目配置文件
        :param model_url: 模型地址
        '''
        # 讯飞的api配置
        self.appid = config.XF_APPID
        self.apikey = config.XF_APIKEY
        self.apisecret = config.XF_APISECRET
        self.model_url = model_url
        self.host = urlparse(model_url).netloc
        self.path = urlparse(model_url).path
        # 模型答案
        self.answer = ''

    def understanding(self, text: str, img_path: str) -> str:
        # 清空答案
        self.answer = ''
        # 组装请求体
        req_body = {
            "header": {"app_id": self.appid},
            "parameter": {"chat": {"domain": "image", "temperature": 0.5, "top_k": 4, "max_tokens": 2028, "auditing": "default"}},
            "payload": {"message": {"text":[{'role': 'user', 'content': img_utils.img2base64(img_path), 'content_type': 'image'}, {'role': 'user', 'content': text}]}}
        }
        websocket.enableTrace(False)
        wsUrl = self.__create_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=self.__on_message, on_error=self.__on_error, on_close=self.__on_close, on_open=self.__on_open)
        ws.appid = self.appid
        ws.req_body = req_body
        ws.question = text
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return self.answer

    def __create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.apisecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.apikey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.model_url + '?' + urlencode(v)
        # print(url)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url

    # 收到websocket错误的处理
    def __on_error(self, ws, error):
        print("### error:", error)

    # 收到websocket关闭的处理
    def __on_close(self, ws, one, two):
        print(" ")

    # 收到websocket连接建立的处理
    def __on_open(self, ws):
        thread.start_new_thread(self.__run, (ws,))

    def __run(self, ws, *args):
        ws.send(json.dumps(ws.req_body))

    # 收到websocket消息的处理
    def __on_message(self, ws, message):
        # print(message)
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            print(f'请求错误: {code}, {data}')
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            self.answer += content
            if status == 2:
                ws.close()




if __name__ == '__main__':
    config = Config()
    '''
        生成图片
    '''
    prompt = '一只鲸鱼在快乐游泳的卡通头像'
    t2i = Text2Img(config)
    t2i.gen_image(prompt, './demo.jpg')
    '''
        图片解释
    '''
    prompt = '请理解一下图片'
    iu = ImageUnderstanding(config)
    logger.info(iu.understanding(prompt, './demo.jpg'))
