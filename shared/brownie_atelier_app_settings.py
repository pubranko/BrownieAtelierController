from shared import settings

# import models you need
# https://docs.microsoft.com/en-us/python/api/azure-mgmt-containerinstance/azure.mgmt.containerinstance.models?view = azure-python
from azure.mgmt.containerinstance.models import (
    ContainerGroup, Container,
    ResourceRequirements, ResourceRequests, OperatingSystemTypes,
    EnvironmentVariable,
    VolumeMount, Volume, AzureFileVolume,
    ContainerGroupRestartPolicy,
    ImageRegistryCredential,
)
##########################################
# brownie-atelier-app コンテナーの定義
##########################################
container_app__resource_requests = ResourceRequests(
    memory_in_gb = settings.CONTAINER_APP__RESOURCE_MEMORY_IN_GB,
    cpu = settings.CONTAINER_APP__RESOURCE_CPU
)
container_app__resource_requirements = ResourceRequirements(
    requests = container_app__resource_requests
)
container_app__env_vars = [
    # コンテナ作成時に必要な環境変数（コンテナ内部で使用するもの）
    EnvironmentVariable(name = 'MONGO_SERVER',
                        secure_value = settings.CONTAINER_APP__MONGO_SERVER),
    EnvironmentVariable(name = 'MONGO_PORT',
                        secure_value = str(settings.CONTAINER_APP__MONGO_PORT)),
    EnvironmentVariable(name = 'MONGO_USER',
                        secure_value = settings.CONTAINER_APP__MONGO_USER),
    EnvironmentVariable(name = 'MONGO_PASS',
                        secure_value = settings.CONTAINER_APP__MONGO_PASS),
    EnvironmentVariable(name = 'MONGO_TLS',
                        value = settings.CONTAINER_APP__MONGO_TLS),
    EnvironmentVariable(name = 'MONGO_TLS_CA_FILE',
                        secure_value = settings.CONTAINER_APP__MONGO_TLS_CA_FILE),
    EnvironmentVariable(name = 'MONGO_TLS_CERTTIFICATE_KEY_FILE',
                        secure_value = settings.CONTAINER_APP__MONGO_TLS_CERTTIFICATE_KEY_FILE),
    EnvironmentVariable(name = 'MONGO_USE_DB',
                        value = settings.CONTAINER_APP__MONGO_USE_DB),
    EnvironmentVariable(name = 'MONGO_CRAWLER_RESPONSE',
                        value = settings.CONTAINER_APP__MONGO_CRAWLER_RESPONSE),
    EnvironmentVariable(name = 'MONGO_CONTROLLER',
                        value = settings.CONTAINER_APP__MONGO_CONTROLLER),
    EnvironmentVariable(name = 'MONGO_CRAWLER_LOGS',
                        value = settings.CONTAINER_APP__MONGO_CRAWLER_LOGS),
    EnvironmentVariable(name = 'MONGO_SCRAPED_FROM_RESPONSE',
                        value = settings.CONTAINER_APP__MONGO_SCRAPED_FROM_RESPONSE),
    EnvironmentVariable(name = 'MONGO_NEWS_CLIP_MASTER',
                        value = settings.CONTAINER_APP__MONGO_NEWS_CLIP_MASTER),
    EnvironmentVariable(name = 'MONGO_SCRAPER_BY_DOMAIN',
                        value = settings.CONTAINER_APP__MONGO_SCRAPER_BY_DOMAIN),
    EnvironmentVariable(name = 'MONGO_ASYNCHRONOUS_REPORT',
                        value = settings.CONTAINER_APP__MONGO_ASYNCHRONOUS_REPORT),
    EnvironmentVariable(name = 'MONGO_STATS_INFO_COLLECT',
                        value = settings.CONTAINER_APP__MONGO_STATS_INFO_COLLECT),
    EnvironmentVariable(name = 'EMAIL_FROM',
                        secure_value = settings.CONTAINER_APP__EMAIL_FROM),
    EnvironmentVariable(name = 'EMAIL_TO',
                        secure_value = settings.CONTAINER_APP__EMAIL_TO),
    EnvironmentVariable(name = 'EMAIL_PASS',
                        secure_value = settings.CONTAINER_APP__EMAIL_PASS),
    EnvironmentVariable(name = 'SCRAPY_SETTINGS_MODULE',
                        value = settings.CONTAINER_APP__SCRAPY_SETTINGS_MODULE),
    EnvironmentVariable(name = 'SCRAPY__LOG_LEVEL',
                        value = settings.CONTAINER_APP__SCRAPY__LOG_LEVEL),
    EnvironmentVariable(name = 'PRECECT_AUTH',
                        secure_value = settings.CONTAINER_APP__PRECECT_AUTH),
    EnvironmentVariable(name = 'PREFECT_DATA_DIR_PATH',
                        value = settings.CONTAINER_APP__PREFECT_DATA_DIR_PATH),
    EnvironmentVariable(name = 'PREFECT__LOGGING__LEVEL',
                        value = settings.CONTAINER_APP__PREFECT__LOGGING__LEVEL),
    EnvironmentVariable(name = 'PREFECT__LOGGING__FORMAT',
                        value = settings.CONTAINER_APP__PREFECT__LOGGING__FORMAT),
    EnvironmentVariable(name = 'PREFECT__LOGGING__DATEFMT',
                        value = settings.CONTAINER_APP__PREFECT__LOGGING__DATEFMT),
    EnvironmentVariable(name = 'PYTHONPATH',
                        value = settings.CONTAINER_APP__PYTHONPATH),
    EnvironmentVariable(name = 'GIT_REMOTE_REPOSITORY',
                        value = settings.CONTAINER_APP__GIT_REMOTE_REPOSITORY),
    EnvironmentVariable(name = 'AZURE_STORAGE_BLOB__CONTAINER_NAME',
                        value = settings.AZURE_STORAGE_BLOB__CONTAINER_NAME),
    EnvironmentVariable(name = 'AZURE_STORAGE_BLOB__FILE_NAME',
                        value = settings.AZURE_STORAGE_BLOB__FILE_NAME),
]

container_app__volume_mount_1 = VolumeMount(
    name = 'brownie-atelier-app-data',
    mount_path = settings.CONTAINER_APP__VOLUME_MOUNT_PATH__BROWNIE_ATELIER_APP_DATA,
)
container_app__container_mongo__volume_mount = VolumeMount(
    name = 'mongo-key',
    mount_path = settings.CONTAINER_APP__VOLUME_MOUNT_PATH__MONGO_KEY,
)

container_app_manual = Container(
    name = 'brownie-atelier-app',
    image = settings.CONTAINER_APP__DOCKER_IMAGE,
    command = ['bash', '-c', 'while :; do sleep 10000; done'],
    resources = container_app__resource_requirements,
    environment_variables = container_app__env_vars,
    volume_mounts = [container_app__volume_mount_1,
                   container_app__container_mongo__volume_mount]
)
container_app_auto = Container(
    name = 'brownie-atelier-app',
    image = settings.CONTAINER_APP__DOCKER_IMAGE,
    command = ['bash', '/home/mikuras/BrownieAtelier/sh/prefect_agent_start.sh'],   # コンテナ起動時に左記のシェルを動かす。
    resources = container_app__resource_requirements,
    environment_variables = container_app__env_vars,
    volume_mounts = [container_app__volume_mount_1,
                   container_app__container_mongo__volume_mount]
)

##############################
# マウントするボリューム
##############################
storage_account_name: str = settings.AZURE_STORAGE__ACCOUNT_NAME
storage_account_key: str = settings.AZURE_STORAGE__ACCOUNT_KEY

aci_group__volume_1 = Volume(
    name = 'brownie-atelier-app-data',
    azure_file = AzureFileVolume(
        share_name = 'brownie-atelier-app-data',
        storage_account_name = storage_account_name,
        storage_account_key = storage_account_key,
    ),
)
aci_group__volume_2 = Volume(
    name = 'mongo-key',
    azure_file = AzureFileVolume(
        share_name = 'mongo-key',
        storage_account_name = storage_account_name,
        storage_account_key = storage_account_key,
    ),
)

###########################################
# コンテナーグループ作成
###########################################
CONTAINER_GROUP__MANUAL = ContainerGroup(
    containers = [container_app_manual],
    location = settings.AZURE_LOCATION,
    restart_policy = ContainerGroupRestartPolicy.NEVER,
    image_registry_credentials = [ImageRegistryCredential(
        server = settings.ACI_DOCKER_IMAGE_REGISTRY_SERVER,
        username = settings.ACI_DOCKER_IMAGE_REGISTRY_USERNAME,
        password = settings.ACI_DOCKER_IMAGE_REGISTRY_PASSWORD,
    )],
    os_type = OperatingSystemTypes.LINUX,
    volumes = [aci_group__volume_1, aci_group__volume_2]
)
CONTAINER_GROUP__AUTO = ContainerGroup(
    containers = [container_app_auto],
    location = settings.AZURE_LOCATION,
    restart_policy = ContainerGroupRestartPolicy.NEVER,
    image_registry_credentials = [ImageRegistryCredential(
        server = settings.ACI_DOCKER_IMAGE_REGISTRY_SERVER,
        username = settings.ACI_DOCKER_IMAGE_REGISTRY_USERNAME,
        password = settings.ACI_DOCKER_IMAGE_REGISTRY_PASSWORD,
    )],
    os_type = OperatingSystemTypes.LINUX,
    volumes = [aci_group__volume_1, aci_group__volume_2]
)
