from uuid import uuid4
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from log import logging

def blob_connect():
    connect_string = 'DefaultEndpointsProtocol=https;AccountName=respacimages;AccountKey=ges4SuaECA10B++lZjlNfhTTorcRkqZXH9+PmyaBG6kFCWH2esd3dE5KHlp63hkHNCPw2cT7bv/bfu2TyRFJEg==;EndpointSuffix=core.windows.net'
    return BlobServiceClient.from_connection_string(connect_string)


def upload_image(service: BlobServiceClient, data, container_name='post'):
    blob_name = uuid4()
    logging.debug(len(data))
    container_client = service.get_container_client(container_name)
    container_client.upload_blob(name=str(blob_name), data=data)


if __name__ == '__main__':
    test_service = blob_connect()
    with open('bccard.gif', 'rb') as f:
        upload_image(test_service, f.read())

