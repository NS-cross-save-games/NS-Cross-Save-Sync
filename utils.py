import os
import zipfile


# Zip all files in target_fpath directory into zip_fpath
def zip_path(zip_fpath, target_fpath):
    with zipfile.ZipFile(zip_fpath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_fpath):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, target_fpath)
                zipf.write(file_path, arcname)