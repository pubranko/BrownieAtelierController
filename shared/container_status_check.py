import logging
from typing import Any
from azure.core import exceptions
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models._models_py3 import ContainerGroup


def container_status_check(resource_group_name: str, aci_client: ContainerInstanceManagementClient, container_group_name: str) -> str:
    '''
    引数で渡されたコンテナーグループ名のステータスを確認し返す。
    コンテナーがない場合は空白を返す。
    '''
    # 戻り値初期化
    state: str = ''
    try:
        # コンテナーグループ名
        container_group: ContainerGroup = aci_client.container_groups.get(
            resource_group_name=resource_group_name,
            container_group_name=container_group_name,
        )
        # 対象のコンテナーグループを取得できたら？
        # 起動しているコンテナーグループのステータスがSucceededだったら？
        if hasattr(container_group.instance_view, "state"):
            poller: Any = container_group.instance_view
            state: str = poller.state
    except exceptions.HttpResponseError as e:
        if e.status_code == 404:
            logging.info(f'コンテナーグループがありません : {container_group_name}')
        else:
            logging.exception(f'コンテナーグループにアクセスできません : {e.status_code}')
            raise

    logging.info(f'コンテナーグループ({container_group_name}) : ステータス({state})')
    # ex) Succeeded Stopped Waiting Running Pulled Pulling
    #       実行中 -> Running   停止後 -> Stopped
    return state
