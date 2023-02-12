
from decouple import config, AutoConfig
# .envファイルが存在するパスを指定。実行時のカレントディレクトリに.envを配置している場合、以下の設定不要。
# config = AutoConfig(search_path="./shared")

# Azure Storage設定
AZURE_STORAGE__CONNECTION_STRING: str = str(config('AZURE_STORAGE__CONNECTION_STRING'))
AZURE_STORAGE__FILE_SHARE:str = str(config('AZURE_STORAGE__FILE_SHARE', default='controller'))
AZURE_STORAGE_QUE__NAME:str = str(config('AZURE_QUE__NAME'))
AZURE_STORAGE_BLOB__CONTAINER_NAME:str = str(config('AZURE_STORAGE_BLOB__CONTAINER_NAME', default='brownie-atelier'))
AZURE_STORAGE_BLOB__FILE_NAME:str = str(config('AZURE_STORAGE_BLOB__FILE_NAME', default='container-stop-coomand-execute'))
