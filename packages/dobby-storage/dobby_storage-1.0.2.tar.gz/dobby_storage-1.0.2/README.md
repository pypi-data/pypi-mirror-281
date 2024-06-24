# dobby-storage

https://github.com/Ting-Yu/dobby-storage.git

## S3 Information

- CUSTOM_AWS_ACCESS_KEY_ID
- CUSTOM_AWS_SECRET_ACCESS_KEY
- CUSTOM_AWS_DEFAULT_REGION
- CUSTOM_AWS_BUCKET
-

## FTP Information

- CUSTOM_FTP_SERVER
- CUSTOM_FTP_USER
- CUSTOM_FTP_PASSWORD
-

## Google Drive Information

- CUSTOM_GOOGLE_DRIVE_AUTH_PATH


## Install Module

```bash
pip install dobby-storage
```

## Unit Test
    
```bash
pytest
```

## Usage

```python
from dobby_storage.storage import FileStorage

# if you want to use storage.json, please refer to dobby_storage/storage.json
# but I still recommend you to set it up in os system environment, the setting is as above, S3 Information, FTP Information, Google Drive Information
file_storage = FileStorage('storage.json')

# 1. Local storage
result = file_storage.save('upload_test.txt', 'destination.txt')
print(f"Local storage File {result}.")

# 2. Using S3 storage with upload_file
file_storage.use_disk('s3')
result = file_storage.save('upload_test.txt', 'destination.txt', bucket_name='fribooker')
print(f"S3 storage with upload_file File {result}.")

# 3. Using S3 storage with upload_fileobj
result = file_storage.save('upload_test.txt', 'destination.txt', bucket_name='fribooker', use_fileobj=True)
print(f"S3 storage with upload_fileobj File {result}.")

# 4. Using FTP storage
file_storage.use_disk('ftp')
result = file_storage.save('upload_test.txt', 'destination.txt')
print(f"FTP storage File {result}.")

# 5. Using Google Drive storage
file_storage.use_disk('google_drive')
result = file_storage.save('upload_test.txt')
print(f"Google Drive storage File {result}.")
```