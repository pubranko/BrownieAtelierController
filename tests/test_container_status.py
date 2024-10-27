import inspect
from pprint import pprint
from decouple import AutoConfig, config
from shared import settings
from shared.container_status_check import container_status_check
from shared.resource_client_get import resource_client_get
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerinstance import ContainerInstanceManagementClient

if __name__ == "__main__":
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

    """ statusの種類
    Creating: コンテナーが作成中です。
    Running: コンテナーが実行中です。
    Stopped: コンテナーが停止されています。
    Failed: コンテナーの作成や実行に失敗しました。
    Unknown: コンテナーの状態が不明です。
    空文字: コンテナーが存在しない。
    """

    # APPコンテナーのステータスを取得。
    container_app__state = container_status_check(
        str(resource_group.name),
        aci_client,
        settings.CONTAINER_APP__CONTAINER_GROUP_NAME,
    )
        
    print(f"App:「{type(container_app__state)}」:「{container_app__state}」")

    # Mongoコンテナーのステータスを取得。
    container_mongo__state = container_status_check(
        str(resource_group.name),
        aci_client,
        settings.CONTAINER_MONGO__CONTAINER_GROUP_NAME,
    )

    print(f"Mongo:「{type(container_app__state)}」:「{container_app__state}」")
