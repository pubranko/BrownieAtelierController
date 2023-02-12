import logging
from typing import Final
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.fileshare import ShareFileClient
from BrownieAtelierStorage import settings

class ControllerFileModel():
    __file_client: ShareFileClient
    __file_name:str = 'mongo_mode'
    __download_flag:str = ''
    ON:Final[str] = 'on'
    OFF:Final[str] = 'off'

    def __init__(self):
        self.__file_client = ShareFileClient.from_connection_string(
            settings.AZURE_STORAGE__CONNECTION_STRING,
            settings.AZURE_STORAGE__FILE_SHARE,
            self.__file_name)

    def __upload(self,flag):
        '''ファイルをアップロードする'''
        try:
            self.__file_client.share_name
            self.__file_client.file_name
            logging.info(f'ファイルアップロード: {self.__file_client.share_name} / {self.__file_client.file_name}')
            self.__file_client.upload_file(flag)

        except ResourceExistsError as ex:
            logging.error(f'ResourceExistsError: {ex.message}')

        except ResourceNotFoundError as ex:
            logging.error(f'ResourceNotFoundError: {ex.message}')

    def __download(self):
        '''ファイルをダウンロードする'''
        try:
            stream = self.__file_client.download_file()
            logging.info(f'ファイルダウンロード: {self.__file_client.share_name} / {self.__file_client.file_name}')
            self.__download_flag = str(stream.content_as_text())

        except ResourceNotFoundError as ex:
            logging.error(f'ResourceNotFoundError: {ex.message}')

    def manual_mode_on(self):
        self.__upload(self.ON)

    def manual_mode_off(self):
        self.__upload(self.OFF)

    def mode_check(self) -> str:
        self.__download()
        return self.__download_flag
