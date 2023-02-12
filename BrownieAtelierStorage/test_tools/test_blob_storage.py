# 実際にazureに接続しデータの読み書きができるかテストを行うツール。
import logging
from BrownieAtelierStorage import settings
from BrownieAtelierStorage.models.controller_blob_model import ControllerBlobModel
logging.basicConfig(level=logging.INFO)

###########################
# model.container_create()
# model.create_page_blob()
# model.container_info_lists()
# for _ in model.container_info_lists():
#     print(f'==={_.name}')

model = ControllerBlobModel()
model.delete_blob()
model.upload_blob()
for _ in model.blob_info_lists():
    print(f'==={_.name}')
