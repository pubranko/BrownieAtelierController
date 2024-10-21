import os

from decouple import AutoConfig, config

# .envファイルが存在するパスを指定
# config = AutoConfig(search_path="./shared")

# タイムゾーン
TIME_ZONE: str = str(config("TIME_ZONE", default="Asia/Tokyo"))

# azure共通設定
AZURE_SUBSCRIPTION_ID: str = str(config("AZURE_SUBSCRIPTION_ID"))
AZURE_RESOURCE_GROUP_NAME: str = str(config("AZURE_RESOURCE_GROUP_NAME"))
AZURE_LOCATION: str = str(config("AZURE_LOCATION"))

# dockerレジストリサーバー接続情報
ACI_DOCKER_IMAGE__REGISTRY_SERVER: str = str(
    config("ACI_DOCKER_IMAGE__REGISTRY_SERVER", default="docker.io")
)
ACI_DOCKER_IMAGE__REGISTRY_USERNAME: str = str(
    config("ACI_DOCKER_IMAGE__REGISTRY_USERNAME")
)
ACI_DOCKER_IMAGE__REGISTRY_PASSWORD: str = str(
    config("ACI_DOCKER_IMAGE__REGISTRY_PASSWORD")
)

# コンテナーグループ設定
ACI_GROUP_CONTAINER_GROUP_NAME: str = str(
    config("ACI_GROUP_CONTAINER_GROUP_NAME", default="BrownieAtelierGrp")
)

###########################
# MongoDBコンテナー設定
###########################
CONTAINER_MONGO__CONTAINER_GROUP_NAME: str = str(
    config("CONTAINER_MONGO__CONTAINER_GROUP_NAME", default="BrownieAtelierMongo")
)
CONTAINER_MONGO__RESOURCE_CPU: float = float(
    config("CONTAINER_MONGO__RESOURCE_CPU", default=1)
)
CONTAINER_MONGO__RESOURCE_MEMORY_IN_GB: float = float(
    config("CONTAINER_MONGO__RESOURCE_MEMORY_IN_GB", default=1.0)
)
CONTAINER_MONGO__MONGO_TAG: str = str(
    config("CONTAINER_MONGO__MONGO_TAG", default="latest")
)
CONTAINER_MONGO__MONGO_CONF: str = str(config("CONTAINER_MONGO__MONGO_CONF"))
CONTAINER_MONGO__DNS_NAME_LABEL: str = str(
    config("CONTAINER_MONGO__DNS_NAME_LABEL", default="news-clip-mongo")
)
CONTAINER_MONGO__PORT: int = int(config("CONTAINER_MONGO__PORT", default="27017"))
CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_DB: str = str(
    config("CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_DB", default="/data/db")
)
CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_CONF: str = str(
    config("CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_CONF", default="/etc/mongo-conf")
)
CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_KEY: str = str(
    config("CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_KEY", default="/etc/mongo-key")
)
CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_LOG: str = str(
    config("CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_LOG", default="/var/log/mongodb")
)
CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_INIT: str = "/docker-entrypoint-initdb.d"
# コンテナー内で使用する環境変数
CONTAINER_MONGO__MONGO_INITDB_ROOT_USERNAME: str = str(
    config("CONTAINER_MONGO__MONGO_INITDB_ROOT_USERNAME")
)
CONTAINER_MONGO__MONGO_INITDB_ROOT_PASSWORD: str = str(
    config("CONTAINER_MONGO__MONGO_INITDB_ROOT_PASSWORD")
)

##################################
# BrownieAtelierAppコンテナー設定
##################################
## その他
CONTAINER_APP__CONTAINER_USER: str = str(
    config("CONTAINER_APP__CONTAINER_USER", default="common_user")
)
# CONTAINER_APP__USER: str = 'common_user'
CONTAINER_APP__CONTAINER_GROUP_NAME: str = str(
    config("CONTAINER_APP__CONTAINER_GROUP_NAME", default="BrownieAtelierApp")
)  # appの自動操作版
CONTAINER_APP__CONTAINER_GROUP_NAME__MANUAL: str = str(
    config(
        "CONTAINER_APP__CONTAINER_GROUP_NAME__MANUAL", default="BrownieAtelierAppManual"
    )
)  # appのマニュアル操作版
CONTAINER_APP__RESOURCE_CPU: float = float(
    config("CONTAINER_APP__RESOURCE_CPU", default=1)
)
CONTAINER_APP__RESOURCE_MEMORY_IN_GB: float = float(
    config("CONTAINER_APP__RESOURCE_MEMORY_IN_GB", default=2.0)
)
CONTAINER_APP__APP_TAG: str = str(config("CONTAINER_APP__APP_TAG", default="latest"))
CONTAINER_APP__VOLUME_MOUNT_PATH__DATA: str = str(
    config(
        "CONTAINER_APP__VOLUME_MOUNT_PATH__DATA",
        default=f"/home/{CONTAINER_APP__CONTAINER_USER}/BrownieAtelier/data",
    )
)
CONTAINER_APP__VOLUME_MOUNT_PATH__MONGO_KEY: str = str(
    config(
        "CONTAINER_APP__VOLUME_MOUNT_PATH__MONGO_KEY",
        default=f"/home/{CONTAINER_APP__CONTAINER_USER}/mongo-key",
    )
)
CONTAINER_APP__CONTAINER_START_COMMAND: str = str(
    config(
        "CONTAINER_APP__CONTAINER_START_COMMAND",
        default=f"/home/{CONTAINER_APP__CONTAINER_USER}/BrownieAtelier/sh/prefect_worker_start__cloud.sh",
    )
)
# コンテナー内部で使用する環境変数
## mongoDBとの接続設定
CONTAINER_APP__MONGO_SERVER: str = str(
    config(
        "CONTAINER_APP__MONGO_SERVER",
        default=f"{CONTAINER_MONGO__DNS_NAME_LABEL}.{AZURE_LOCATION}.azurecontainer.io",
    )
)
CONTAINER_APP__MONGO_PORT: int = int(
    config("CONTAINER_APP__MONGO_PORT", default=27017)
)  # ex) 27017
CONTAINER__MONGO_USE_DB: str = str(
    config("CONTAINER__MONGO_USE_DB", default="crawler_db")
)
CONTAINER__MONGO_USER: str = str(config("CONTAINER__MONGO_USER"))
CONTAINER__MONGO_PASS: str = str(config("CONTAINER__MONGO_PASS"))
CONTAINER_APP__MONGO_TLS: str = str(config("CONTAINER_APP__MONGO_TLS", default="false"))
CONTAINER_APP__MONGO_TLS_CA_FILE: str = os.path.join(
    CONTAINER_APP__VOLUME_MOUNT_PATH__MONGO_KEY,
    str(config("CONTAINER_APP__MONGO_TLS_CA_FILE")),
)
CONTAINER_APP__MONGO_TLS_CERTTIFICATE_KEY_FILE: str = os.path.join(
    CONTAINER_APP__VOLUME_MOUNT_PATH__MONGO_KEY,
    str(config("CONTAINER_APP__MONGO_TLS_CERTTIFICATE_KEY_FILE")),
)
## Brownie atelier noticeの設定 (Slack)
CONTAINER_APP__NOTICE__SLACK_TOKEN: str = str(config("CONTAINER_APP__NOTICE__SLACK_TOKEN"))
CONTAINER_APP__NOTICE__SLACK_CHANNEL_ID__ERROR: str = str(config("CONTAINER_APP__NOTICE__SLACK_CHANNEL_ID__ERROR"))
CONTAINER_APP__NOTICE__SLACK_CHANNEL_ID__NOMAL: str = str(config("CONTAINER_APP__NOTICE__SLACK_CHANNEL_ID__NOMAL"))
## scrapy
# CONTAINER_APP__SCRAPY_SETTINGS_MODULE: str = str(
#     config('CONTAINER_APP__SCRAPY_SETTINGS_MODULE', default='news_crawl.settings'))
CONTAINER_APP__SCRAPY__LOG_LEVEL: str = str(
    config("CONTAINER_APP__SCRAPY__LOG_LEVEL", default="INFO")
)
## prefect2
CONTAINER_APP__PREFECT__API_URL: str = str(config("CONTAINER_APP__PREFECT__API_URL"))
CONTAINER_APP__PREFECT__API_KEY: str = str(config("CONTAINER_APP__PREFECT__API_KEY"))
CONTAINER_APP__PREFECT__WORK_SPACE: str = str(
    config("CONTAINER_APP__PREFECT__WORK_SPACE")
)
CONTAINER_APP__PREFECT__WORK_POOL: str = str(
    config("CONTAINER_APP__PREFECT__WORK_POOL", default="default-agent-pool")
)
# CONTAINER_APP__PREFECT_LOGGING_LEVEL: str = str(
#     config('CONTAINER_APP__PREFECT_LOGGING_LEVEL', default='INFO'))
# CONTAINER_APP__PREFECT_LOGGING_SERVER_LEVEL: str = str(
#     config('CONTAINER_APP__PREFECT_LOGGING_SERVER_LEVEL', default='INFO'))
# CONTAINER_APP__PREFECT_LOGGING_INTERNAL_LEVEL: str = str(
#     config('CONTAINER_APP__PREFECT_LOGGING_INTERNAL_LEVEL', default='INFO'))
CONTAINER_APP__PREFECT__DATA: str = str(
    config(
        "CONTAINER_APP__PREFECT__DATA",
        default=f"/home/{CONTAINER_APP__CONTAINER_USER}/BrownieAtelier/data",
    )
)

# 定数：コンテナーコントロールコマンド
CONTAINER_CONTROLL__CREATE: str = "create"
CONTAINER_CONTROLL__START: str = "start"
CONTAINER_CONTROLL__RESTART: str = "restart"
CONTAINER_CONTROLL__STOP: str = "stop"
CONTAINER_CONTROLL__DELETE: str = "delete"
CONTAINER_CONTROLL_LIST: list[str] = [
    CONTAINER_CONTROLL__CREATE,
    CONTAINER_CONTROLL__START,
    CONTAINER_CONTROLL__RESTART,
    CONTAINER_CONTROLL__STOP,
    CONTAINER_CONTROLL__DELETE,
]
# 定数：対象コンテナー
TARGET_CONTAINER__AUTO: str = "Auto"
TARGET_CONTAINER_LIST: list[str] = [
    TARGET_CONTAINER__AUTO,
    CONTAINER_APP__CONTAINER_GROUP_NAME,
    CONTAINER_APP__CONTAINER_GROUP_NAME__MANUAL,
    CONTAINER_MONGO__CONTAINER_GROUP_NAME,
]
