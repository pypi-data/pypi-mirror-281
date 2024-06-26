# SDK调用方式
## 1. 安装SDK
```bash
pip install dwspark-2024.0.2-py3-none-any.whl -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=600
```

## 2. 加载配置
```python
from dwspark.config import Config
# 加载系统环境变量：SPARKAI_UID、SPARKAI_APP_ID、SPARKAI_API_KEY、SPARKAI_API_SECRET
config = Config()
# 自定义key写入
config = Config('14****93', 'eb28b****b82', 'MWM1MzBkOD****Mzk0')
```

## 3.调用模型
```python
# SDK引入模型
from dwspark.models import ChatModel, Text2Img, ImageUnderstanding, Text2Audio, Audio2Text
# 讯飞消息对象
from sparkai.core.messages import ChatMessage
# 日志
from loguru import logger
'''
对话
'''
# 模拟问题
question = '你好呀'
logger.info('----------批式调用对话----------')
model = ChatModel(config, stream=False)
logger.info(model.generate([ChatMessage(role="user", content=question)]))
logger.info('----------流式调用对话----------')
model = ChatModel(config, stream=True)
for r in model.generate_stream(question):
logger.info(r)
logger.info('done.')
'''
文字生成语音
'''
text = '2023年5月，讯飞星火大模型正式发布，迅速成为千万用户获取知识、学习知识的“超级助手”，成为解放生产力、释放想象力的“超级杠杆”。2024年4月，讯飞星火V3.5春季升级长文本、长图文、长语音三大能力。一年时间内，讯飞星火从1.0到3.5，每一次迭代都是里程碑式飞跃。'
audio_path = './demo.mp3'
t2a = Text2Audio(config)
# 对生成上锁，预防公有变量出现事务问题，但会降低程序并发性能。
t2a.gen_audio(text, audio_path)
'''
语音识别文字
'''
a2t = Audio2Text(config)
# 对生成上锁，预防公有变量出现事务问题，但会降低程序并发性能。
audio_text = a2t.gen_text(audio_path)
logger.info(audio_text)
'''
生成图片
'''
logger.info('----------生成图片----------')
prompt = '一只鲸鱼在快乐游泳的卡通头像'
t2i = Text2Img(config)
t2i.gen_image(prompt, './demo.jpg')
'''
图片解释
'''
logger.info('----------图片解释----------')
prompt = '请理解一下图片'
iu = ImageUnderstanding(config)
logger.info(iu.understanding(prompt, './demo.jpg'))
'''
获取文本向量
'''
logger.info('----------获取文本向量----------')
em = EmebddingModel(config)
vector = em.get_embedding("我们是datawhale")
logger.info(vector)
```

# 模型列表
|模型名称| 浇在调用方式                                                                                                                                        |
|--|-----------------------------------------------------------------------------------------------------------------------------------------------|
|批式调用对话| model = ChatModel(config, stream=False)</br>model.generate([ChatMessage(role="user", content='对话内容')])                                        |
|流式调用对话| model = ChatModel(config, stream=True)</br>model = ChatModel(config, stream=True)</br>[logger.info(r) for r in model.generate_stream('对话内容')] |
|文字生成语音| t2a = Text2Audio(config)</br>model = ChatModel(config, stream=True)</br>t2a.gen_audio('你好啊', '生成音频地址')                                        |
|生成图片| t2i = Text2Img(config)</br>t2i.gen_image('生成图片需求', '图片地址')                                                                                    |
|图片解释| iu = ImageUnderstanding(config)</br>iu.understanding('图片理解方向描述', '图片地址')                                                                      |
|获取文本向量| em = EmebddingModel(config)</br>vector = em.get_embedding("需要向量化的文本")                                                                         |
