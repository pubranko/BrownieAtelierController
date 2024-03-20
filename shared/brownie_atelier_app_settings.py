# import models you need
# https://docs.microsoft.com/en-us/python/api/azure-mgmt-containerinstance/azure.mgmt.containerinstance.models?view = azure-python
from azure.mgmt.containerinstance.models import (AzureFileVolume, Container,
                                                 ContainerGroup,
                                                 ContainerGroupRestartPolicy,
                                                 EnvironmentVariable,
                                                 ImageRegistryCredential,
                                                 OperatingSystemTypes,
                                                 ResourceRequests,
                                                 ResourceRequirements, Volume,
                                                 VolumeMount)

from BrownieAtelierStorage import settings as storage_settings
from shared import settings

##########################################
# brownie-atelier-app コンテナーの定義
##########################################
container_app__resource_requests = ResourceRequests(
    memory_in_gb=settings.CONTAINER_APP__RESOURCE_MEMORY_IN_GB,
    cpu=settings.CONTAINER_APP__RESOURCE_CPU,
)
container_app__resource_requirements = ResourceRequirements(
    requests=container_app__resource_requests
)
container_app__env_vars = [
    # コンテナ作成時に必要な環境変数（コンテナ内部で使用するもの）
    ## mongoDB
    EnvironmentVariable(
        name="BROWNIE_ATELIER_MONGO__MONGO_SERVER",
        secure_value=settings.CONTAINER_APP__MONGO_SERVER,
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_MONGO__MONGO_PORT",
        secure_value=str(settings.CONTAINER_APP__MONGO_PORT),
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_MONGO__MONGO_USE_DB",
        value=settings.CONTAINER_APP__MONGO_USE_DB,
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_MONGO__MONGO_USER",
        secure_value=settings.CONTAINER_APP__MONGO_USER,
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_MONGO__MONGO_PASS",
        secure_value=settings.CONTAINER_APP__MONGO_PASS,
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_MONGO__MONGO_TLS", value=settings.CONTAINER_APP__MONGO_TLS
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_MONGO__MONGO_TLS_CA_FILE",
        secure_value=settings.CONTAINER_APP__MONGO_TLS_CA_FILE,
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_MONGO__MONGO_TLS_CERTTIFICATE_KEY_FILE",
        secure_value=settings.CONTAINER_APP__MONGO_TLS_CERTTIFICATE_KEY_FILE,
    ),
    ## Brownie atelier noticeの設定 (email)
    EnvironmentVariable(
        name="BROWNIE_ATELIER_NOTICE__SMTP_HOST",
        secure_value=settings.CONTAINER_APP__NOTICE__SMTP_HOST,
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_NOTICE__SMTP_PORT",
        secure_value=settings.CONTAINER_APP__NOTICE__SMTP_PORT,
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_NOTICE__FROM_EMAIL",
        secure_value=settings.CONTAINER_APP__NOTICE__FROM_EMAIL,
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_NOTICE__TO_EMAIL",
        secure_value=settings.CONTAINER_APP__NOTICE__TO_EMAIL,
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_NOTICE__PASSWORD",
        secure_value=settings.CONTAINER_APP__NOTICE__PASSWORD,
    ),
    EnvironmentVariable(
        name="BROWNIE_ATELIER_NOTICE__TIMEOUT_LIMIT",
        secure_value=settings.CONTAINER_APP__NOTICE__TIMEOUT_LIMIT,
    ),
    ## scrapy
    # EnvironmentVariable(name='SCRAPY_SETTINGS_MODULE',
    #                     value=settings.CONTAINER_APP__SCRAPY_SETTINGS_MODULE),
    EnvironmentVariable(
        name="SCRAPY__LOG_LEVEL", value=settings.CONTAINER_APP__SCRAPY__LOG_LEVEL
    ),
    ## prefect2
    EnvironmentVariable(
        name="PREFECT__API_URL", secure_value=settings.CONTAINER_APP__PREFECT__API_URL
    ),
    EnvironmentVariable(
        name="PREFECT__API_KEY", secure_value=settings.CONTAINER_APP__PREFECT__API_KEY
    ),
    EnvironmentVariable(
        name="PREFECT__WORK_SPACE",
        secure_value=settings.CONTAINER_APP__PREFECT__WORK_SPACE,
    ),
    EnvironmentVariable(
        name="PREFECT__WORK_POOL",
        secure_value=settings.CONTAINER_APP__PREFECT__WORK_POOL,
    ),
    # EnvironmentVariable(name='PREFECT_LOGGING_LEVEL',
    #                     secure_value=settings.CONTAINER_APP__PREFECT_LOGGING_LEVEL),
    # EnvironmentVariable(name='PREFECT_LOGGING_SERVER_LEVEL',
    #                     secure_value=settings.CONTAINER_APP__PREFECT_LOGGING_SERVER_LEVEL),
    # EnvironmentVariable(name='PREFECT_LOGGING_INTERNAL_LEVEL',
    #                     secure_value=settings.CONTAINER_APP__PREFECT_LOGGING_INTERNAL_LEVEL),
    EnvironmentVariable(
        name="PREFECT__DATA", secure_value=settings.CONTAINER_APP__PREFECT__DATA
    ),
    # ## その他
    # EnvironmentVariable(name='CONTAINER_HOME',
    #                     secure_value=f'/home/{settings.CONTAINER_APP__CONTAINER_USER}'),
    ## Azure Storage
    EnvironmentVariable(
        name="AZURE_STORAGE__BLOB_CONTAINER_NAME",
        value=storage_settings.AZURE_STORAGE__BLOB_CONTAINER_NAME,
    ),
    EnvironmentVariable(
        name="AZURE_STORAGE__BLOB_FILE_NAME",
        value=storage_settings.AZURE_STORAGE__BLOB_FILE_NAME,
    ),
]

container_app__volume_mount_1 = VolumeMount(
    name="data",
    mount_path=settings.CONTAINER_APP__VOLUME_MOUNT_PATH__DATA,
)
container_app__container_mongo__volume_mount = VolumeMount(
    name="mongo-key",
    mount_path=settings.CONTAINER_APP__VOLUME_MOUNT_PATH__MONGO_KEY,
)

container_app_manual = Container(
    name="brownie-atelier-app",
    image=f"{settings.ACI_DOCKER_IMAGE__REGISTRY_SERVER}/{settings.ACI_DOCKER_IMAGE__REGISTRY_USERNAME}/brownie_atelier_app:{settings.CONTAINER_APP__APP_TAG}",
    command=["bash", "-c", "while :; do sleep 10000; done"],
    resources=container_app__resource_requirements,
    environment_variables=container_app__env_vars,
    volume_mounts=[
        container_app__volume_mount_1,
        container_app__container_mongo__volume_mount,
    ],
)
container_app_auto = Container(
    name="brownie-atelier-app",
    image=f"{settings.ACI_DOCKER_IMAGE__REGISTRY_SERVER}/{settings.ACI_DOCKER_IMAGE__REGISTRY_USERNAME}/brownie_atelier_app:{settings.CONTAINER_APP__APP_TAG}",
    # コンテナ起動時に左記のシェルを動かす。
    # command=['bash', '-c', 'while :; do sleep 10000; done'],
    command=["bash", f"{settings.CONTAINER_APP__CONTAINER_START_COMMAND}"],
    resources=container_app__resource_requirements,
    environment_variables=container_app__env_vars,
    volume_mounts=[
        container_app__volume_mount_1,
        container_app__container_mongo__volume_mount,
    ],
)

##############################
# マウントするボリューム
##############################
storage_account_name: str = storage_settings.AZURE_STORAGE__ACCOUNT_NAME
storage_account_key: str = storage_settings.AZURE_STORAGE__ACCOUNT_KEY

aci_group__volume_1 = Volume(
    name="data",
    azure_file=AzureFileVolume(
        share_name="data",
        storage_account_name=storage_account_name,
        storage_account_key=storage_account_key,
    ),
)
aci_group__volume_2 = Volume(
    name="mongo-key",
    azure_file=AzureFileVolume(
        share_name="mongo-key",
        storage_account_name=storage_account_name,
        storage_account_key=storage_account_key,
    ),
)

###########################################
# コンテナーグループ作成
###########################################
CONTAINER_GROUP__MANUAL = ContainerGroup(
    containers=[container_app_manual],
    location=settings.AZURE_LOCATION,
    restart_policy=ContainerGroupRestartPolicy.NEVER,
    image_registry_credentials=[
        ImageRegistryCredential(
            server=settings.ACI_DOCKER_IMAGE__REGISTRY_SERVER,
            username=settings.ACI_DOCKER_IMAGE__REGISTRY_USERNAME,
            password=settings.ACI_DOCKER_IMAGE__REGISTRY_PASSWORD,
        )
    ],
    os_type=OperatingSystemTypes.LINUX,
    volumes=[aci_group__volume_1, aci_group__volume_2],
)
CONTAINER_GROUP__AUTO = ContainerGroup(
    containers=[container_app_auto],
    location=settings.AZURE_LOCATION,
    restart_policy=ContainerGroupRestartPolicy.NEVER,
    image_registry_credentials=[
        ImageRegistryCredential(
            server=settings.ACI_DOCKER_IMAGE__REGISTRY_SERVER,
            username=settings.ACI_DOCKER_IMAGE__REGISTRY_USERNAME,
            password=settings.ACI_DOCKER_IMAGE__REGISTRY_PASSWORD,
        )
    ],
    os_type=OperatingSystemTypes.LINUX,
    volumes=[aci_group__volume_1, aci_group__volume_2],
)
