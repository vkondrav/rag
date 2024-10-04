import urllib.request
import zipfile
import os

url = "https://github.com/android/nowinandroid/archive/refs/heads/main.zip"
zip_path = "main.zip"
 
urllib.request.urlretrieve(url, zip_path)

save_dir = 'data'
os.makedirs(save_dir, exist_ok = True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(save_dir)

os.remove(zip_path)
