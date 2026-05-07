from azure.storage.blob import BlobServiceClient
import os

connection_string = "YOUR_CONNECTION_STRING"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = "myfiles"

media_folder = "media"

for filename in os.listdir(media_folder):

    file_path = os.path.join(media_folder, filename)

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=filename
    )

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"Uploaded {filename}")