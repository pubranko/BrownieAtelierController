import logging
from datetime import datetime
from typing import Final
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContainerProperties, BlobProperties, StorageStreamDownloader,ContentSettings
from azure.core.paging import ItemPaged
from BrownieAtelierStorage import settings


class ControllerBlobModel():
    '''
    Azure Storage Blobを操作するクラス。
    '''
    __blob_service_client: BlobServiceClient
    __container_client: ContainerClient
    __blob_client: BlobClient
    timestamp:Final[str] = datetime.now().isoformat()
    __blob_container_name = settings.AZURE_STORAGE_BLOB__CONTAINER_NAME
    __blob_file_name = settings.AZURE_STORAGE_BLOB__FILE_NAME


    def __init__(self):
        '''
        Azure Storage Blobへ接続を行う。
        他メソッドで使用するコンテナークライアント、BLOBクライアントを取得しクラス変数に保存する。
        （前提）
        環境変数 = AZURE_STORAGE__CONNECTION_STRINGより取得した接続文字列により接続を行う。
        BLOBにはブロックBLOB、追加BLOB、ページBLOBの３種類存在するが、ここではブロックBLOBを使用する。
        '''
        self.__blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=settings.AZURE_STORAGE__CONNECTION_STRING)

        if self.__blob_container_name not in [_.name for _ in self.container_info_lists()]:
            self.create_container()
        self.__container_client = self.__blob_service_client.get_container_client(
            container=self.__blob_container_name)

        self.__blob_client = self.__blob_service_client.get_blob_client(
            container=self.__blob_container_name, blob=self.__blob_file_name)

    def container_info_lists(self) -> ItemPaged[ContainerProperties]:
        '''
        BLOBコンテナー情報の一覧を作成する。
        ※補足）BLOBファイルごとにコンテナー化されている。
            コンテナー → フォルダのような使い方となる。
        '''
        return self.__blob_service_client.list_containers()

    def create_container(self):
        ''' BLOBコンテナーを作成する。 '''
        self.__blob_service_client.create_container(self.__blob_container_name)

    def delete_container(self):
        ''' BLOBコンテナーを削除する。（使う予定はないがとりあえずメソッドは残す） '''
        self.__container_client.delete_container()

    def blob_info_lists(self) -> ItemPaged[BlobProperties]:
        ''' BLOBファイル情報のリストを取得する。 '''
        return self.__container_client.list_blobs()

    def upload_blob(self):
        '''
        BLOBファイルをアップロードする。
        （前提）アップロード先に同名のBLOBファイルがないこと。存在した場合はエラーとなる。
        '''
        if self.__blob_file_name in [_.name for _ in self.blob_info_lists()]:
            logging.warning(f'作成対象のBLOBが既に存在するため作成処理(upload_blob)を中止しました。 BLOB = {self.__blob_file_name}')
        else:
            self.__blob_client.upload_blob(datetime.now().isoformat())  # 特に使用予定は無いが、BLOBファイル内にタイムスタンプを保存

    def download_blob(self) -> StorageStreamDownloader:
        ''' BLOBファイルをダウンロードする。'''
        return self.__blob_client.download_blob()

    def delete_blob(self):
        ''' BLOBファイルを削除する。 '''
        if self.__blob_file_name in [_.name for _ in self.blob_info_lists()]:
            self.__blob_client.delete_blob()
        else:
            logging.warning(f'削除対象のBLOBがないため削除処理を中止しました。 BLOB = {self.__blob_file_name}')
