import os
from azure.storage.blob import BlobServiceClient, ContainerClient

def download_json_files(connection_string, container_name, local_folder):
    """
    Download all JSON files from an Azure Blob container to a local folder.
    
    Parameters:
    connection_string (str): Azure Storage connection string
    container_name (str): Name of the Azure Blob container
    local_folder (str): Local folder path to save the downloaded files
    """
    # Create the local folder if it doesn't exist
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)
        print(f"Created local folder: {local_folder}")
    
    try:
        # Initialize the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Get the container client
        container_client = blob_service_client.get_container_client(container_name)
        
        # List all blobs in the container
        blob_list = container_client.list_blobs()
        
        # Counter for downloaded files
        download_count = 0
        
        # Process each blob
        for blob in blob_list:
            # Only download JSON files
            if blob.name.lower().endswith('.pdf'):
                # Construct the local file path
                local_file_path = os.path.join(local_folder, os.path.basename(blob.name))
                
                # Get the blob client
                blob_client = container_client.get_blob_client(blob.name)
                
                # Download the blob
                with open(local_file_path, "wb") as file:
                    download_stream = blob_client.download_blob()
                    file.write(download_stream.readall())
                
                print(f"Downloaded: {blob.name} to {local_file_path}")
                download_count += 1
        
        print(f"Download complete. Downloaded {download_count} pdf files.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Replace these with your values
    connection_string = "DefaultEndpointsProtocol=https;AccountName=aisearchstract;AccountKey=7+GBVJQNgCs0rPvZ3yVInrmd9X9AmZ6YDFiECMCW4Y/AulohYtkf9rlOETUczKMI/CtSJSDhLI7f+ASthWzQUw==;EndpointSuffix=core.windows.net"
    container_name = "evidencefiles-master"
    local_folder = "."
    
    download_json_files(connection_string, container_name, local_folder)