# 実際にazureに接続しデータの読み書きができるかテストを行うツール。
import logging
from BrownieAtelierStorage import settings
from BrownieAtelierStorage.models.controller_file_model import ControllerFileModel
logging.basicConfig(level=logging.INFO)

model = ControllerFileModel()
# model.manual_mode_on()
model.manual_mode_off()
print(f'=== {model.mode_check()}')
