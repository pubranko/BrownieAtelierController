from datetime import datetime, timezone
import logging

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from dateutil import tz

from BrownieAtelierStorage.models.controller_file_model import \
    ControllerFileModel
from shared import (brownie_atelier_app_settings,
                    brownie_atelier_mongo_settings, settings)
from shared.command_execution import command_execution
from shared.container_status_check import container_status_check
from shared.resource_client_get import resource_client_get


def main(myblob: func.InputStream):
    JST = tz.gettz(settings.TIME_ZONE)
    jst_timestamp = datetime.now(timezone.utc).replace(tzinfo=JST).isoformat()
    logging.info(f"BrownieAtelier_BlobTrigger 開始時間: {jst_timestamp}")
    logging.info(f"BLOB名: {myblob.name}")
    logging.info(f"BLOBサイズ: {myblob.length} bytes")

    # azureのリソースグループ情報を取得。
    resource_client = resource_client_get()
    resource_group = resource_client.resource_groups.get(
        settings.AZURE_RESOURCE_GROUP_NAME,
    )

    ##############################################
    # コンテナーの存在・ステータスチェックを行う。
    ##############################################
    # azuruと接続するための認証を行う。 https://learn.microsoft.com/ja-jp/azure/developer/java/sdk/identity-azure-hosted-auth
    credential = DefaultAzureCredential()
    # ACI情報を取り扱うためのクラスのようだ。
    aci_client = ContainerInstanceManagementClient(
        credential, settings.AZURE_SUBSCRIPTION_ID
    )

    container_app__state: str = ""  # app側のコンテナーのステータス
    container_mongo__state: str = ""  # mongo側のコンテナーのステータス
    result_message: str = ""  # HttpTriggerのresponseメッセージ

    # 各コンテナーのステータスチェック
    # appコンテナ
    container_app__state = container_status_check(
        str(resource_group.name),
        aci_client,
        settings.CONTAINER_APP__CONTAINER_GROUP_NAME,
    )
    # mongoコンテナ
    container_mongo__state = container_status_check(
        str(resource_group.name),
        aci_client,
        settings.CONTAINER_MONGO__CONTAINER_GROUP_NAME,
    )

    # コントローラーファイルのmodel初期化
    controller_file_model = ControllerFileModel()
    mongo_mode_flag = controller_file_model.mode_check()
    logging.info(f"マニュアルモードチェック: {mongo_mode_flag}")

    ########################################
    # Brownie atelier mongo DBコンテナー
    ########################################
    # mongoコンテナーに対する操作（自動側）
    # マニュアルモードがONでストップコマンドの場合
    if mongo_mode_flag == controller_file_model.ON:
        logging.info(
            f"マニュアルモードがONのため、Brownie atelier mongo DBコンテナーへのコマンドをキャンセルしました。"
        )
    else:
        # コンテナーが実行中している場合、コンテナーを削除する。
        if container_app__state == "Running":
            logging.info(f"Brownie atelier mongo DBコンテナー 自動削除")
            result_message = command_execution(
                str(resource_group.name),
                aci_client,
                settings.CONTAINER_MONGO__CONTAINER_GROUP_NAME,
                brownie_atelier_mongo_settings.CONTAINER_GROUP,
                container_mongo__state,
                settings.CONTAINER_CONTROLL__DELETE,
            )

            logging.info(
                f"Brownie atelier mongo DBコンテナー 自動削除結果 : {result_message}"
            )
        else:
            logging.warning(
                f"Brownie atelier mongo DBコンテナーが実行中(Running)以外のステータスであったため削除処理をキャンセルしました。"
            )

    #################################
    # Brownie atelier APP コンテナー
    #################################
    # appコンテナーに対する操作（自動側）
    # コンテナーが実行中している場合、コンテナーを削除する。
    if container_app__state == "Running":
        logging.info(f"Brownie atelier APP コンテナー 自動削除")
        result_message = command_execution(
            str(resource_group.name),
            aci_client,
            settings.CONTAINER_APP__CONTAINER_GROUP_NAME,
            brownie_atelier_app_settings.CONTAINER_GROUP__AUTO,
            container_app__state,
            settings.CONTAINER_CONTROLL__DELETE,
        )
        logging.info(f"Brownie atelier APPコンテナー 自動削除結果 : {result_message}")
    else:
        logging.warning(
            f"Brownie atelier APPコンテナーが実行中(Running)以外のステータスであったため削除処理をキャンセルしました。"
        )
