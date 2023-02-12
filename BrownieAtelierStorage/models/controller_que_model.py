import logging
from typing import Final

from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage
from azure.core.paging import ItemPaged
from BrownieAtelierStorage import settings


class ControllerQueModel():
    __queue_client: QueueClient

    def __init__(self):
        '''
        Azure Storage Queへ接続を行う。
        他メソッドで使用するコンテナークライアント、BLOBクライアントを取得しクラス変数に保存する。
        （前提）
        環境変数 = AZURE_STORAGE__CONNECTION_STRINGより取得した接続文字列により接続を行う。
        '''
        self.__queue_client = QueueClient.from_connection_string(
             conn_str=settings.AZURE_STORAGE__CONNECTION_STRING,
             queue_name=settings.AZURE_STORAGE_QUE__NAME)

    def create_queue(self):
        '''キューを作成する。'''
        self.__queue_client.create_queue()

    def delete_queue(self):
        '''キューを削除する。'''
        self.__queue_client.delete_queue()

    def send_message(self, message):
        '''キューにメッセージを送信（登録）する'''
        self.saved_message = self.__queue_client.send_message(message)

    def peek_message(self, max_messages:int):
        '''キューに格納されているメッセージを指定件数分取得する。'''
        peeked_messages:list[QueueMessage] = self.__queue_client.peek_messages(max_messages=max_messages)

        for peeked_message in peeked_messages:
            logging.info(f'Message ID/Content: {peeked_message.id} / {str(peeked_message.content)}')

    def delete_message(self, message:QueueMessage):
        '''
        キューに格納されているメッセージを削除する。
        '''
        self.__queue_client.delete_message(message)

    def receive_message(self) -> QueueMessage:
        '''
        キューを先頭から１件取得する。
        '''
        return self.__queue_client.receive_message()

    def receive_messages(self,max_messages:int = 2) -> ItemPaged[QueueMessage]:
        '''
        キューを全件取得する。
        '''
        return self.__queue_client.receive_messages(max_messages=max_messages)