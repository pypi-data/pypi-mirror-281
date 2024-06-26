#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : VoiceModel.py
# @Author: Richard Chiming Xu
# @Date  : 2024/6/17
# @Desc  : 语音相关模型
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os

from dwspark.config import Config
from multiprocessing import Lock

from loguru import logger

# 接口状态
STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Text2Audio():
    def __init__(self, config: Config, model_url: str = 'wss://tts-api.xfyun.cn/v2/tts'):
        '''
        文本生成语音模型（https://www.xfyun.cn/doc/tts/online_tts/API.html）
        :param config: 项目配置文件
        :param model_url: 语音地址
        '''
        # 讯飞的api配置
        self.appid = config.XF_APPID
        self.apikey = config.XF_APIKEY
        self.apisecret = config.XF_APISECRET
        self.model_url = model_url
        # 合成语音的必要参数,具体详情可查看API文档
        self.BusinessArgs = {"aue": "lame", "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8"}

    def gen_audio(self, text: str, output_path: str = './demo.mp3'):
        '''
        生成语音
        :param text: 文本
        :param output_path: 输出路径
        :return:
        '''

        websocket.enableTrace(False)
        # 创建socket地址
        wsUrl = self.__create_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=self.__on_message, on_error=self.__on_error, on_close=self.__on_close)
        ws.data = {"status": 2, "text": str(base64.b64encode(text.encode('utf-8')), "UTF8")}
        ws.on_open = self.__on_open
        ws.output_path = output_path
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        logger.info('语音合成路径：' + ws.output_path)

    # 生成url
    def __create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.apisecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.apikey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = self.model_url + '?' + urlencode(v)
        return url

    # 收到websocket消息，进行出来（核心处理逻辑）
    def __on_message(self, ws, message):
        try:
            message = json.loads(message)
            code = message["code"]
            sid = message["sid"]
            audio = message["data"]["audio"]
            audio = base64.b64decode(audio)
            status = message["data"]["status"]
            if status == 2:
                ws.close()
            if code != 0:
                errMsg = message["message"]
                logger.info("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            else:

                with open(ws.output_path, 'ab') as f:
                    f.write(audio)

        except Exception as e:
            logger.info("receive msg,but parse exception:", e)

    # 收到websocket错误的处理
    def __on_error(self, ws, error):
        logger.info("### error:", error)

    # 收到websocket关闭的处理
    def __on_close(self, ws):
        logger.info("### closed ###")

    # 收到websocket连接建立的处理
    def __on_open(self, ws):
        def run(*args):
            d = {"common": {"app_id": self.appid},
                 "business": self.BusinessArgs,
                 "data": ws.data,
                 }
            d = json.dumps(d)
            ws.send(d)
            if os.path.exists('./demo.mp3'):
                os.remove('./demo.mp3')

        thread.start_new_thread(run, ())


class Audio2Text():
    def __init__(self, config: Config, model_url: str = 'wss://ws-api.xfyun.cn/v2/iat'):
        '''
        语音转文本模型（https://www.xfyun.cn/doc/asr/voicedictation/API.html）
        :param config: 项目配置文件
        :param model_url: 语音地址
        '''
        # 讯飞的api配置
        self.appid = config.XF_APPID
        self.apikey = config.XF_APIKEY
        self.apisecret = config.XF_APISECRET
        self.model_url = model_url

        # 语音识别的必要参数,具体详情可查看API文档
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo": 1, "vad_eos": 10000}
        # # 语音文件路径
        # self.audio_path = ''
        # # 通用返回
        # self.resp_text = ''

    def gen_text(self, audio_path: str):
        # # 初始化属性
        # self.resp_text = ''
        # self.audio_path = audio_path
        # 创建url
        websocket.enableTrace(False)
        wsUrl = self.__create_url()
        # 调用ws
        ws = websocket.WebSocketApp(wsUrl, on_message=self.__on_message, on_error=self.__on_error, on_close=self.__on_close)
        ws.resp_text = ''
        ws.audio_path = audio_path
        ws.on_open = self.__on_open
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        logger.info('语音识别结果：' + ws.resp_text)
        return ws.resp_text

    # 生成url
    def __create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.apisecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.apikey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url

    # 收到websocket消息的处理
    def __on_message(self, ws, message):
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            if code != 0:
                errMsg = json.loads(message)["message"]
                logger.info("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

            else:
                data = json.loads(message)["data"]["result"]["ws"]
                result = ""
                for i in data:
                    for w in i["cw"]:
                        result += w["w"]
                ws.resp_text += result
        except Exception as e:
            logger.info("receive msg,but parse exception:", e)

    # 收到websocket错误的处理
    def __on_error(self, ws, error):
        logger.info("### error:", error)

    # 收到websocket关闭的处理
    def __on_close(self, ws, a, b):
        logger.info("### closed ###")

    # 收到websocket连接建立的处理
    def __on_open(self, ws):
        def run(*args):
            frameSize = 8000  # 每一帧的音频大小
            intervel = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

            with open(ws.audio_path, "rb") as fp:
                while True:
                    buf = fp.read(frameSize)
                    # 文件结束
                    if not buf:
                        status = STATUS_LAST_FRAME
                    # 第一帧处理
                    # 发送第一帧音频，带business 参数
                    # appid 必须带上，只需第一帧发送
                    if status == STATUS_FIRST_FRAME:

                        d = {"common": {"app_id": self.appid},
                             "business": self.BusinessArgs,
                             "data": {"status": 0, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "lame"}}
                        d = json.dumps(d)
                        ws.send(d)
                        status = STATUS_CONTINUE_FRAME
                    # 中间帧处理
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "lame"}}
                        ws.send(json.dumps(d))
                    # 最后一帧处理
                    elif status == STATUS_LAST_FRAME:
                        d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "lame"}}
                        ws.send(json.dumps(d))
                        time.sleep(1)
                        break
                    # 模拟音频采样间隔
                    time.sleep(intervel)
            ws.close()

        thread.start_new_thread(run, ())


if __name__ == '__main__':
    lock = Lock()
    config = Config()
    text = '2023年5月，讯飞星火大模型正式发布，迅速成为千万用户获取知识、学习知识的“超级助手”，成为解放生产力、释放想象力的“超级杠杆”。2024年4月，讯飞星火V3.5春季升级长文本、长图文、长语音三大能力。一年时间内，讯飞星火从1.0到3.5，每一次迭代都是里程碑式飞跃。'
    audio_path = './demo.mp3'
    '''
        文字生成语音
    '''
    t2a = Text2Audio(config)
    # 对生成上锁，预防公有变量出现事务问题，但会降低程序并发性能。
    with lock:
        t2a.gen_audio(text, audio_path)
    '''
        语音识别文字
    '''
    a2t = Audio2Text(config)
    # 对生成上锁，预防公有变量出现事务问题，但会降低程序并发性能。
    with lock:
        audio_text = a2t.gen_text(audio_path)
