from shared import settings

# import models you need
# https://docs.microsoft.com/en-us/python/api/azure-mgmt-containerinstance/azure.mgmt.containerinstance.models?view = azure-python
from azure.mgmt.containerinstance.models import (
    ContainerGroup, Container,
    ResourceRequirements, ResourceRequests, OperatingSystemTypes,
    EnvironmentVariable,
    ContainerPort, IpAddress, Port, ContainerGroupIpAddressType, ContainerGroupNetworkProtocol,
    VolumeMount, Volume, AzureFileVolume,
    ContainerGroupRestartPolicy,
    ImageRegistryCredential,
)
##########################################
# mongo コンテナーの定義
##########################################
container_mongo__resource_requests = ResourceRequests(
    memory_in_gb = settings.CONTAINER_MONGO__RESOURCE_MEMORY_IN_GB,
    cpu = settings.CONTAINER_MONGO__RESOURCE_CPU,
)
container_mongo__resource_requirements = ResourceRequirements(
    requests = container_mongo__resource_requests
)

container_mongo__env_vars = [
    EnvironmentVariable(name = 'MONGO_INITDB_ROOT_USERNAME',
                        secure_value = settings.CONTAINER_MONGO__MONGO_INITDB_ROOT_USERNAME),
    EnvironmentVariable(name = 'MONGO_INITDB_ROOT_PASSWORD',
                        secure_value = settings.CONTAINER_MONGO__MONGO_INITDB_ROOT_PASSWORD),
]

# コンテナーの中のディレクトリを定義
container_mongo__volume_mount_1 = VolumeMount(
    name = 'mongo-azure-db',
    mount_path = settings.CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_AZURE_DB,
)
container_mongo__volume_mount_2 = VolumeMount(
    name = 'mongo-conf',
    mount_path = settings.CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_CONF,
)
container_mongo__volume_mount_3 = VolumeMount(
    name = 'mongo-key',
    mount_path = settings.CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_KEY,
)
container_mongo__volume_mount_4 = VolumeMount(
    name = 'mongo-log',
    mount_path = settings.CONTAINER_MONGO__VOLUME_MOUNT_PATH__MONGO_LOG,
)
# MongoDBコンテナーの定義を生成
container_mongo = Container(
    name = 'mongo',
    image = settings.CONTAINER_MONGO__DOCKER_IMAGE,
    command = ["mongod", "--config", f"/etc/mongo-conf/{settings.CONTAINER_MONGO__MONGO_CONF}"],
    resources = container_mongo__resource_requirements,
    ports = [ContainerPort(
        port = settings.CONTAINER_MONGO__PORT,
        protocol = ContainerGroupNetworkProtocol.TCP)],
    environment_variables = container_mongo__env_vars,
    volume_mounts = [container_mongo__volume_mount_1, container_mongo__volume_mount_2,
                   container_mongo__volume_mount_3, container_mongo__volume_mount_4]
)

##############################
# マウントするボリューム
##############################
storage_account_name: str = settings.AZURE_STORAGE__ACCOUNT_NAME
storage_account_key: str = settings.AZURE_STORAGE__ACCOUNT_KEY

# コンテナーの外のストレージの定義
aci_group__volume_1 = Volume(
    name = 'mongo-azure-db',
    azure_file = AzureFileVolume(
        share_name = 'mongo-azure-db',
        storage_account_name = storage_account_name,
        storage_account_key = storage_account_key,
    ),
)
aci_group__volume_2 = Volume(
    name = 'mongo-conf',
    azure_file = AzureFileVolume(
        share_name = 'mongo-conf',
        storage_account_name = storage_account_name,
        storage_account_key = storage_account_key,
    ),
)
aci_group__volume_3 = Volume(
    name = 'mongo-key',
    azure_file = AzureFileVolume(
        share_name = 'mongo-key',
        storage_account_name = storage_account_name,
        storage_account_key = storage_account_key,
    ),
)
aci_group__volume_4 = Volume(
    name = 'mongo-log',
    azure_file = AzureFileVolume(
        share_name = 'mongo-log',
        storage_account_name = storage_account_name,
        storage_account_key = storage_account_key,
    ),
)

###########################################
# コンテナーグループ作成
###########################################
CONTAINER_GROUP = ContainerGroup(
    containers = [container_mongo,],
    location = settings.AZURE_LOCATION,
    restart_policy = ContainerGroupRestartPolicy.NEVER,
    image_registry_credentials = [ImageRegistryCredential(
        server = settings.ACI_DOCKER_IMAGE__REGISTRY_SERVER,
        username = settings.ACI_DOCKER_IMAGE__REGISTRY_USERNAME,
        password = settings.ACI_DOCKER_IMAGE__REGISTRY_PASSWORD,
    )],
    os_type = OperatingSystemTypes.LINUX,
    ip_address = IpAddress(
        ports = [Port(port = settings.CONTAINER_MONGO__PORT)],
        type = ContainerGroupIpAddressType.PUBLIC,
        dns_name_label = settings.CONTAINER_MONGO__DNS_NAME_LABEL
    ),
    volumes = [aci_group__volume_1, aci_group__volume_2,
             aci_group__volume_3, aci_group__volume_4]
)
