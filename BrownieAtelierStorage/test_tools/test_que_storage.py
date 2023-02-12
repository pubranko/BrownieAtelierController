# 実際にazureに接続しデータの読み書きができるかテストを行うツール。
import logging
from BrownieAtelierStorage import settings
from BrownieAtelierStorage.models.controller_que_model import ControllerQueModel
logging.basicConfig(level=logging.INFO)

model = ControllerQueModel()
# model.send_message('てすてす３')
model.peek_message(10)
# model.delete_message('てすてす2')
# model.peek_message(10)

# a = model.receive_message()
# a.pop_receipt
# print(f'内容確認: {a.id} / {a.content}')
# model.delete_message(a)
# model.peek_message(10)

b = model.receive_messages()
for c in b:
    print(f'内容確認: {c.id} / {c.content}')
