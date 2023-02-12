
import os
from decouple import config, AutoConfig
# .envファイルが存在するパスを指定
# config = AutoConfig(search_path="./shared")

# タイムゾーン
TIME_ZONE: str = str(config('TIME_ZONE', default='Asia/Tokyo'))

# azure共通設定
AZURE_SUBSCRIPTION_ID: str = str(config('AZURE_SUBSCRIPTION_ID'))
AZURE_RESOURCE_GROUP_NAME: str = str(
    config('AZURE_RESOURCE_GROUP_NAME', default='RankoKoushin'))
AZURE_LOCATION: str = str(config('AZURE_LOCATION', default='japaneast'))
# Azure Storage設定
AZURE_STORAGE__ACCOUNT_NAME: str = str(
    config('AZURE_STORAGE__ACCOUNT_NAME', default='brownieatelierdata'))
AZURE_STORAGE__ACCOUNT_KEY: str = str(config('AZURE_STORAGE__ACCOUNT_KEY'))
AZURE_STORAGE__CONNECTION_STRING: str = str(
    config('AZURE_STORAGE__CONNECTION_STRING'))
AZURE_STORAGE__FILE_SHARE: str = str(config('AZURE_STORAGE__FILE_SHARE'))
AZURE_QUE__NAME: str = str(config('AZURE_QUE__NAME'))
# AZURE_QUE__URL:str = str(config('AZURE_QUE__URL'))
AZURE_STORAGE_BLOB__CONTAINER_NAME: str = str(
    config('AZURE_STORAGE_BLOB__CONTAINER_NAME', default='brownie-atelier'))
AZURE_STORAGE_BLOB__FILE_NAME: str = str(
    config('AZURE_STORAGE_BLOB__FILE_NAME', default='container-stop-coomand-execute'))

# Azure Functions設定
AZURE_FUNCTION_URL: str = str(config('AZURE_FUNCTION_URL', default=''))
AZURE_FUNCTION_KEY: str = str(config('AZURE_FUNCTION_KEY', default=''))
AZURE_FUNCTION_SCOPE: str = str(config('AZURE_FUNCTION_SCOPE', default=''))
# Azure AD設定
#   'client_id' Azure portal に登録されているアプリケーションの 'アプリケーション (クライアント) ID'。 この値は、Azure portal のアプリの [概要] ページで確認できます。
AZURE_AD_CLIENT_ID: str = str(config('AZURE_AD_CLIENT_ID'))
# 'authority'	ユーザーが認証するための STS エンドポイント。 通常、パブリック クラウド上では
#   https://login.microsoftonline.com/{tenant} です。
#   {tenant} はご自分のテナントの名前またはテナント ID です。
AZURE_AD_AUTHORITY: str = str(config('AZURE_AD_AUTHORITY'))
# 'secret'	Azure Portal 上でアプリケーションに対して作成されるクライアント シークレット。
AZURE_AD_CLIENT_CREDENTIAL: str = str(config('AZURE_AD_CLIENT_CREDENTIAL'))

# コンテナーグループ設定
ACI_DOCKER_IMAGE_REGISTRY_SERVER: str = str(
    config('ACI_DOCKER_IMAGE_REGISTRY_SERVER', default='docker.io'))
ACI_DOCKER_IMAGE_REGISTRY_USERNAME: str = str(
    config('ACI_DOCKER_IMAGE_REGISTRY_USERNAME'))
ACI_DOCKER_IMAGE_REGISTRY_PASSWORD: str = str(
    config('ACI_DOCKER_IMAGE_REGISTRY_PASSWORD'))
ACI_GROUP_CONTAINER_GROUP_NAME: str = str(
    config('ACI_GROUP_CONTAINER_GROUP_NAME', default='BrownieAtelierGrp'))
ACI_GROUP_DNS_NAME_LABEL: str = str(
    config('ACI_GROUP_DNS_NAME_LABEL', default='news-clip-mongo-v5'))
ACI_GROUP_MONGO_PORT: int = int(config('ACI_GROUP_MONGO_PORT', default=27017))

# BrownieAtelierAppコンテナー設定
CONTAINER_APP__USER: str = 'mikuras'
CONTAINER_APP__CONTAINER_GROUP_NAME: str = str(
    config('CONTAINER_APP__CONTAINER_GROUP_NAME', default='BrownieAtelierApp'))  # appの自動操作版
CONTAINER_APP__CONTAINER_GROUP_NAME__MANUAL: str = str(
    config('CONTAINER_APP__CONTAINER_GROUP_NAME__MANUAL', default='BrownieAtelierAppManual'))  # appのマニュアル操作版
CONTAINER_APP__RESOURCE_MEMORY_IN_GB: float = float(
    config('CONTAINER_APP__RESOURCE_MEMORY_IN_GB', default=2.0))
CONTAINER_APP__RESOURCE_CPU: float = float(
    config('CONTAINER_APP__RESOURCE_CPU', default=1))
CONTAINER_APP__DOCKER_IMAGE: str = str(
    config('CONTAINER_APP__DOCKER_IMAGE', default='docker.io/mikuras/brownie_atelier_app:0.11'))
CONTAINER_APP__VOLUME_MOUNT_PATH__BROWNIE_ATELIER_APP_DATA: str = str(
    config('CONTAINER_APP__VOLUME_MOUNT_PATH__BROWNfrom pathlib import PathIE_ATELIER_APP_DATA', default=f'/home/{CONTAINER_APP__USER}/BrownieAtelier'))
CONTAINER_APP__VOLUME_MOUNT_PATH__MONGO_KEY: str = str(
    config('CONTAINER_APP__VOLUME_MOUNT_PATH__MONGO_KEY', default=f'/home/{CONTAINER_APP__USER}/mongo-key'))
# コンテナー内部で使用する環境変数
CONTAINER_APP__MONGO_SERVER: str = str(config(
    'CONTAINER_APP__MONGO_SERVER', default=f'{ACI_GROUP_DNS_NAME_LABEL}.{AZURE_LOCATION}.azurecontainer.io'))
CONTAINER_APP__MONGO_PORT: int = int(config(
    'CONTAINER_APP__MONGO_PORT', default=f'{ACI_GROUP_MONGO_PORT}'))   # ex) 27017
CONTAINER_APP__MONGO_USER: str = str(config('CONTAINER_APP__MONGO_USER'))
CONTAINER_APP__MONGO_PASS: str = str(config('CONTAINER_APP__MONGO_PASS'))
CONTAINER_APP__MONGO_TLS: str = str(
    config('CONTAINER_APP__MONGO_TLS', default='true'))
CONTAINER_APP__MONGO_TLS_CA_FILE: str = os.path.join(CONTAINER_APP__VOLUME_MOUNT_PATH__MONGO_KEY, str(
    config('CONTAINER_APP__MONGO_TLS_CA_FILE', default='ca.crt')))
CONTAINER_APP__MONGO_TLS_CERTTIFICATE_KEY_FILE: str = os.path.join(CONTAINER_APP__VOLUME_MOUNT_PATH__MONGO_KEY, str(
    config('CONTAINER_APP__MONGO_TLS_CERTTIFICATE_KEY_FILE', default='mongo5_client.pem')))
CONTAINER_APP__MONGO_USE_DB: str = str(
    config('CONTAINER_APP__MONGO_USE_DB', default='test_crawler_db'))
CONTAINER_APP__MONGO_CRAWLER_RESPONSE: str = str(
    config('CONTAINER_APP__MONGO_CRAWLER_RESPONSE', default='crawler_response'))
CONTAINER_APP__MONGO_CONTROLLER: str = str(
    config('CONTAINER_APP__MONGO_CONTROLLER', default='controller'))
CONTAINER_APP__MONGO_CRAWLER_LOGS: str = str(
    config('CONTAINER_APP__MONGO_CRAWLER_LOGS', default='crawler_logs'))
CONTAINER_APP__MONGO_SCRAPED_FROM_RESPONSE: str = str(config(
    'CONTAINER_APP__MONGO_SCRAPED_FROM_RESPONSE', default='scraped_from_response'))
CONTAINER_APP__MONGO_NEWS_CLIP_MASTER: str = str(
    config('CONTAINER_APP__MONGO_NEWS_CLIP_MASTER', default='news_clip_master'))
CONTAINER_APP__MONGO_SCRAPER_BY_DOMAIN: str = str(
    config('CONTAINER_APP__MONGO_SCRAPER_BY_DOMAIN', default='scraper_by_domain'))
CONTAINER_APP__MONGO_ASYNCHRONOUS_REPORT: str = str(config(
    'CONTAINER_APP__MONGO_ASYNCHRONOUS_REPORT', default='asynchronous_report'))
CONTAINER_APP__MONGO_STATS_INFO_COLLECT: str = str(
    config('CONTAINER_APP__MONGO_STATS_INFO_COLLECT', default='stats_info_collect'))
CONTAINER_APP__EMAIL_FROM: str = str(config('CONTAINER_APP__EMAIL_FROM'))
CONTAINER_APP__EMAIL_TO: str = str(config('CONTAINER_APP__EMAIL_TO'))
CONTAINER_APP__EMAIL_PASS: str = str(config('CONTAINER_APP__EMAIL_PASS'))
CONTAINER_APP__SCRAPY_SETTINGS_MODULE: str = str(
    config('CONTAINER_APP__SCRAPY_SETTINGS_MODULE', default='news_crawl.settings'))
CONTAINER_APP__SCRAPY__LOG_LEVEL: str = str(
    config('CONTAINER_APP__SCRAPY__LOG_LEVEL', default='INFO'))
CONTAINER_APP__PRECECT_AUTH: str = str(config('CONTAINER_APP__PRECECT_AUTH'))
CONTAINER_APP__PREFECT_DATA_DIR_PATH: str = str(
    config('CONTAINER_APP__PREFECT_DATA_DIR_PATH', default='../data_dir'))
CONTAINER_APP__PREFECT__LOGGING__LEVEL: str = str(
    config('CONTAINER_APP__PREFECT__LOGGING__LEVEL', default='INFO'))
CONTAINER_APP__PREFECT__LOGGING__FORMAT: str = str(config(
    'CONTAINER_APP__PREFECT__LOGGING__FORMAT', default=r"%(asctime)s %(levelname)s [%(name)s] : %(message)s"))
CONTAINER_APP__PREFECT__LOGGING__DATEFMT: str = str(config(
    'CONTAINER_APP__PREFECT__LOGGING__DATEFMT', default=r'%Y-%m-%d %H:%M:%S'))
CONTAINER_APP__PYTHONPATH: str = str(config(
    'CONTAINER_APP__PYTHONPATH', default=f'/home/{CONTAINER_APP__USER}/BrownieAtelier/.venv/bin/'))
CONTAINER_APP__GIT_REMOTE_REPOSITORY: str = str(
    config('CONTAINER_APP__GIT_REMOTE_REPOSITORY'))

# MongoDBコンテナー設定
CONTAINER_MONGO__CONTAINER_GROUP_NAME: str = str(
    config('CONTAINER_MONGO__CONTAINER_GROUP_NAME', default='BrownieAtelierMongo'))
CONTAINER_MONGO__RESOURCE_MEMORY_IN_GB: float = float(
    config('CONTAINER_MONGO__RESOURCE_MEMORY_IN_GB', default=1.0))
CONTAINER_MONGO__RESOURCE_CPU: float = float(
    config('CONTAINER_MONGO__RESOURCE_CPU', default=1))
CONTAINER_MONGO__DNS_NAME_LABEL: str = str(config(
    'CONTAINER_MONGO__DNS_NAME_LABEL', default=f'{ACI_GROUP_DNS_NAME_LABEL}'))
CONTAINER_MONGO__PORT: int = int(
    config('CONTAINER_MONGO__PORT', default=f'{ACI_GROUP_MONGO_PORT}'))
CONTAINER_MONGO__DOCKER_IMAGE: str = str(
    config('CONTAINER_MONGO__DOCKER_IMAGE', default='mongo:5.0.10-focal'))
CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_AZURE_DB: str = str(
    config('CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_AZURE_DB', default='/data/mongo-azure-db'))
CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_CONF: str = str(
    config('CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_CONF', default='/etc/mongo-conf'))
CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_KEY: str = str(
    config('CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_KEY', default='/etc/mongo-key'))
CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_LOG: str = str(
    config('CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_LOG', default='/var/log/mongo-log'))
# コンテナー内で使用する環境変数
CONTAINER_MONGO__MONGO_INITDB_ROOT_USERNAME: str = str(
    config('CONTAINER_MONGO__MONGO_INITDB_ROOT_USERNAME'))
CONTAINER_MONGO__MONGO_INITDB_ROOT_PASSWORD: str = str(
    config('CONTAINER_MONGO__MONGO_INITDB_ROOT_PASSWORD'))

# コンテナーコントロールコマンド
CONTAINER_CONTROLL__CREATE: str = 'create'
CONTAINER_CONTROLL__START: str = 'start'
CONTAINER_CONTROLL__RESTART: str = 'restart'
CONTAINER_CONTROLL__STOP: str = 'stop'
CONTAINER_CONTROLL__DELETE: str = 'delete'
CONTAINER_CONTROLL_LIST: list[str] = [
    CONTAINER_CONTROLL__CREATE, CONTAINER_CONTROLL__START, CONTAINER_CONTROLL__RESTART, CONTAINER_CONTROLL__STOP, CONTAINER_CONTROLL__DELETE]
# 対象コンテナー
TARGET_CONTAINER__AUTO: str = 'Auto'
TARGET_CONTAINER_LIST: list[str] = [
    TARGET_CONTAINER__AUTO, CONTAINER_APP__CONTAINER_GROUP_NAME, CONTAINER_APP__CONTAINER_GROUP_NAME__MANUAL, CONTAINER_MONGO__CONTAINER_GROUP_NAME]

# Azure FunctionsからMongoDBと接続するための設定。
#   ※ca fileやkey fileはFunctions内のファイルを参照。それ以外はappコンテナー内の設定を流用。
AZURE_FUNCTIONS__MONGO_SERVER = str(
    config('AZURE_FUNCTIONS__MONGO_SERVER', default=CONTAINER_APP__MONGO_SERVER))
AZURE_FUNCTIONS__MONGO_PORT = str(
    config('AZURE_FUNCTIONS__MONGO_PORT', default=CONTAINER_APP__MONGO_PORT))
AZURE_FUNCTIONS__MONGO_USE_DB = str(
    config('AZURE_FUNCTIONS__MONGO_USE_DB', default=CONTAINER_APP__MONGO_USE_DB))
AZURE_FUNCTIONS__MONGO_USER = str(
    config('AZURE_FUNCTIONS__MONGO_USER', default=CONTAINER_APP__MONGO_USER))
AZURE_FUNCTIONS__MONGO_PASS = str(
    config('AZURE_FUNCTIONS__MONGO_PASS', default=CONTAINER_APP__MONGO_PASS))
AZURE_FUNCTIONS__MONGO_TLS = str(
    config('AZURE_FUNCTIONS__MONGO_TLS', default=CONTAINER_APP__MONGO_TLS))
AZURE_FUNCTIONS__MONGO_TLS_CA_FILE: str = str(
    config('AZURE_FUNCTIONS__MONGO_TLS_CA_FILE'))
AZURE_FUNCTIONS__MONGO_TLS_CERTTIFICATE_KEY_FILE: str = str(
    config('AZURE_FUNCTIONS__MONGO_TLS_CERTTIFICATE_KEY_FILE'))
