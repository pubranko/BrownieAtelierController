import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from shared import settings, brownie_atelier_app_settings, brownie_atelier_mongo_settings
from shared.container_status_check import container_status_check
from shared.command_execution import command_execution
from shared.resource_client_get import resource_client_get
from BrownieAtelierHttpTrigger.brownie_atelier_http_trigger_input import BrownieAtelierHttpTriggerInput
from BrownieAtelierStorage.models.controller_file_model import ControllerFileModel


def main(req: func.HttpRequest) -> func.HttpResponse:

    # =======================================================
    logging.info('BrownieAtelier_HttpTrigger 開始')

    # リクエストパラメータチェック(target_container, container_controll_command) & デフォルト値設定
    logging.info(f'リクエストパラメータ確認 : {req.get_json()}')
    checked_params = BrownieAtelierHttpTriggerInput(**dict(req.get_json()))

    logging.info(
        f'''以下のリクエストパラメータとして処理を実施します。
            target_container = {checked_params.target_container} ,
            container_controll_command = {checked_params.container_controll_command}''')

    # azureのリソースグループ情報を取得。
    resource_client = resource_client_get()
    resource_group = resource_client.resource_groups.get(
        settings.AZURE_RESOURCE_GROUP_NAME,
    )

    ###################################################################################################
    # コンテナーの存在・ステータスチェックを行い、リクエストパラメータで指定されたコマンドを実行する。
    ###################################################################################################
    # azuruと接続するための認証を行う。 https://learn.microsoft.com/ja-jp/azure/developer/java/sdk/identity-azure-hosted-auth
    credential = DefaultAzureCredential()
    # ACI情報を取り扱うためのクラスのようだ。
    aci_client = ContainerInstanceManagementClient(
        credential,
        settings.AZURE_SUBSCRIPTION_ID)

    container_app__state: str = ''      # app側のコンテナーのステータス
    container_mongo__state: str = ''    # mongo側のコンテナーのステータス
    result_message: str = ''                   # HttpTriggerのresponseメッセージ

    # 各コンテナーのステータスチェック
    # appコンテナ
    container_app__state = container_status_check(
        str(resource_group.name),
        aci_client,
        settings.CONTAINER_APP__CONTAINER_GROUP_NAME)
    # mongoコンテナ
    container_mongo__state = container_status_check(
        str(resource_group.name),
        aci_client,
        settings.CONTAINER_MONGO__CONTAINER_GROUP_NAME)

    # コントローラーファイルのmodel初期化
    controller_file_model = ControllerFileModel()
    mongo_mode_flag = controller_file_model.mode_check()
    logging.info(f'マニュアルモードチェック: {mongo_mode_flag}')

    ########################################
    # Brownie atelier mongo DBコンテナー
    ########################################
    # mongoコンテナーに対する操作（自動側）
    if checked_params.target_container == settings.TARGET_CONTAINER__AUTO:
        # マニュアルモードがONでストップコマンドの場合
        if mongo_mode_flag == controller_file_model.ON:
            logging.info(f'マニュアルモードがONのため、Brownie atelier mongo DBコンテナーへのコマンドをキャンセルしました。')
        else:
            logging.info(f'Brownie atelier mongo DBコンテナー 自動操作開始')
            result_message = command_execution(str(resource_group.name),
                                        aci_client,
                                        settings.CONTAINER_MONGO__CONTAINER_GROUP_NAME,
                                        brownie_atelier_mongo_settings.CONTAINER_GROUP,
                                        container_mongo__state,
                                        checked_params.container_controll_command)

    # mongoコンテナーに対する操作（手動側）
    if checked_params.target_container == settings.CONTAINER_MONGO__CONTAINER_GROUP_NAME:
        logging.info(f'Brownie atelier mongo DBコンテナー 手動操作開始')
        # スタートコマンドがリクエストされた場合、コントローラーファイルをONにする。
        # ストップコマンドがリクエストされた場合、コントローラーファイルをOFFにする。
        if checked_params.container_controll_command in [settings.CONTAINER_CONTROLL__START, settings.CONTAINER_CONTROLL__RESTART]:
            controller_file_model.manual_mode_on()
        elif checked_params.container_controll_command == settings.CONTAINER_CONTROLL__STOP:
            controller_file_model.manual_mode_off()

        result_message = command_execution(str(resource_group.name),
                                    aci_client,
                                    settings.CONTAINER_MONGO__CONTAINER_GROUP_NAME,
                                    brownie_atelier_mongo_settings.CONTAINER_GROUP,
                                    container_mongo__state,
                                    checked_params.container_controll_command)

        mongo_mode_flag = controller_file_model.mode_check()
        logging.info(f'マニュアルモード更新 : {mongo_mode_flag}')


    #################################
    # Brownie atelier APP コンテナー
    #################################
    # appコンテナーに対する操作（自動側）
    if checked_params.target_container in [settings.TARGET_CONTAINER__AUTO,
                                           settings.CONTAINER_APP__CONTAINER_GROUP_NAME,]:
        logging.info(f'Brownie atelier APP コンテナー 操作開始')
        result_message = command_execution(str(resource_group.name),
                                    aci_client,
                                    settings.CONTAINER_APP__CONTAINER_GROUP_NAME,
                                    brownie_atelier_app_settings.CONTAINER_GROUP__AUTO,
                                    container_app__state,
                                    checked_params.container_controll_command)

    # appコンテナーに対する操作（手動側）
    if checked_params.target_container in [settings.CONTAINER_APP__CONTAINER_GROUP_NAME__MANUAL,]:
        logging.info(f'Brownie atelier APP Manual コンテナー 操作開始')
        result_message = command_execution(str(resource_group.name),
                                    aci_client,
                                    settings.CONTAINER_APP__CONTAINER_GROUP_NAME__MANUAL,
                                    brownie_atelier_app_settings.CONTAINER_GROUP__MANUAL,
                                    container_app__state,
                                    checked_params.container_controll_command)


    return func.HttpResponse(result_message)
