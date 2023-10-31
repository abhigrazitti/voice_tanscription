from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Specify the location of the client secrets file
client_secrets_file = "client_secret.json"

# Create a GoogleAuth instance and set the client secrets file
gauth = GoogleAuth()
gauth.settings['client_config_file'] = client_secrets_file

# Authenticate using LocalWebserverAuth
gauth.LocalWebserverAuth()

# Create a GoogleDrive instance
drive = GoogleDrive(gauth)

# Replace the file ID with your file's ID
file_id = "1QgX4HKXFB9iUO_nCEt_kUC9in5Y7gub6"

# Get the JPG file and specify the mimetype for JPG
file = drive.CreateFile({'id': file_id})
file.GetContentFile("downloaded_image.jpg", mimetype="image/jpeg")
