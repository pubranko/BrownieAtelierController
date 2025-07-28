import logging

from azure.core import exceptions
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

from shared import settings


def resource_client_get() -> ResourceManagementClient:
    """ """
    # azuruと接続するための認証を行う。 https://learn.microsoft.com/ja-jp/azure/developer/java/sdk/identity-azure-hosted-auth
    #   順序  認証方式
    #     1 	環境変数
    #     2 	マネージド ID
    #     3 	IntelliJ アカウント
    #     4 	Visual Studio Code
    #     5 	Azure CLI
    credential = DefaultAzureCredential()

    # リソース情報を取り扱うためのクラスのようだ。
    resource_client = ResourceManagementClient(
        credential=credential,
        # subscription_id=settings.AZURE_SUBSCRIPTION_ID,  # azureアカウントのサブスクリプションID
        subscription_id="f1a4dbd6-2833-4f2b-addb-1c07e6f0f220",  # azureアカウントのサブスクリプションID
    )
    print(resource_client)

    #######################################################
    # 上記のリソースクライアントが正常かチェックしている。
    #######################################################
    logging.info("リソースグループのチェック")
    try:
        # リソースグループにアクセスできるか確認
        resource_group = resource_client.resource_groups.get(
            "BrownieAtelierGroupWest",
        )
    except exceptions.HttpResponseError as e:
        if e.status_code == 404:
            logging.exception(
                f"リソースグループがありませんでした: {settings.AZURE_RESOURCE_GROUP_NAME}"
            )
        else:
            logging.exception(
                f"リソースグループにアクセスできませんでした。 : {e.status_code}"
            )
        raise

    return resource_client


if __name__ == "__main__":
    
    resource_client = resource_client_get()
    print(resource_client.__dict__)