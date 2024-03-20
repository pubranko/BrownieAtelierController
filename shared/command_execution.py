import logging

from azure.core import exceptions
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models._models_py3 import ContainerGroup


def command_execution(
    resource_group_name: str,
    aci_client: ContainerInstanceManagementClient,
    container_group_name: str,
    container_group: ContainerGroup,
    state: str,
    container_controll_command: str,
) -> str:
    """
    リクエストパラメータの container_controll_command に応じた処理を実行する。
    """
    message: str = ""
    ####################################
    # コマンドに応じた処理の分岐
    ####################################
    if container_controll_command == "create":
        if state:  # ステータスあり（既存コンテナーあり）の場合
            return f"既存のコンテナーが存在します。createを中止しました。"
        else:
            try:
                poller = aci_client.container_groups.begin_create_or_update(
                    resource_group_name=resource_group_name,
                    container_group_name=container_group_name,
                    container_group=container_group,  # 生成したコンテナーグループ
                )
                # logging.info(f'コンテナーグループ生成 : {poller.result().name}')
                logging.info(f"コンテナーグループ生成 : {poller.result()}")
            except exceptions.HttpResponseError as e:
                logging.exception(
                    f"コンテナーグループ生成できませんでした : {e.status_code}"
                )
                raise
            message = f"createで起動しました"
    elif container_controll_command == "restart":
        poller = aci_client.container_groups.begin_restart(
            resource_group_name=resource_group_name,
            container_group_name=container_group_name,
        )
        logging.info(f"コンテナーグループ開始 : {poller.result()}")
        message = f"restartで起動しました"
    elif container_controll_command == "start":
        poller = aci_client.container_groups.begin_start(
            resource_group_name=resource_group_name,
            container_group_name=container_group_name,
        )
        logging.info(f"コンテナーグループ開始 : {poller.result()}")
        message = f"startで起動しました"
    elif container_controll_command == "stop":
        poller = aci_client.container_groups.stop(
            resource_group_name=resource_group_name,
            container_group_name=container_group_name,
        )
        logging.info(f"コンテナーグループ停止 : {poller}")
        message = f"stopで起動しました"
    elif container_controll_command == "delete":
        if state:  # ステータスあり（既存コンテナーあり）の場合
            poller = aci_client.container_groups.begin_delete(
                resource_group_name=resource_group_name,
                container_group_name=container_group_name,
            )
            # logging.info(f'コンテナーグループ削除 : {poller.result().name}')
            logging.info(f"コンテナーグループ削除 : {poller.result()}")

            message = f"deleteで起動しました"
        else:
            message = f"既存のコンテナーがありません。deleteを中止しました。"

    return message
