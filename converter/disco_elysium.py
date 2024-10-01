import json
import shutil
import zipfile
from converter.converter import Converter
import os
import hashlib
import random
from datetime import datetime, timezone

'''
Disco Elysium
pc: SaveGames
switch SaveSlots
'''
class disco_elysium(Converter):

    @staticmethod
    def convert_to_switch(switch_fpath, pc_folder_path):
        current_time = datetime.now(timezone.utc)
        print(f"Disco Elysium: PC to Switch ({pc_folder_path} -> {switch_fpath})")
        pc_folder_path = os.path.join(pc_folder_path, 'SaveGames')

        savecache_json = []

        # SaveSlots
        # 在saves/pc/Disco Elysium下创建一个临时文件夹，包含多个子文件夹，等下会用来zip压缩。
        tmp_path = 'saves/pc/Disco Elysium/SaveSlots/'
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        for fname in os.listdir(pc_folder_path):
            if fname.endswith('.jpg'):
                basename = os.path.splitext(fname)[0]
                # 为一个fanme.ntwtf.zip 和 fname.jpg 创建一个临时文件夹
                random_string = hashlib.md5(str(random.random()).encode()).hexdigest()[:31]
                os.makedirs(tmp_path + random_string)
                # copy
                shutil.copy(os.path.join(pc_folder_path, basename) + ".jpg",
                            os.path.join(tmp_path + random_string, random_string+".jpg"))
                shutil.copy(os.path.join(pc_folder_path, basename) + ".ntwtf.zip",
                            os.path.join(tmp_path + random_string, random_string+".zip"))
                # json
                json_data = {
                    "version": 1,
                    "dateCreatedUTC": current_time.strftime("%Y-%m-%d %H:%M:%SZ"),
                    "uniqueName": "1aa3383628ec98183457aefd5ab00f6",
                    "fileName": basename,
                    "title": "Transferred from PC",
                    "subTitle": ""
                }
                savecache_json.append(json_data)
                with open(os.path.join(tmp_path + random_string, random_string+'.json'), 'w', encoding='utf-8', newline='\n') as json_file:
                    json.dump(json_data, json_file, indent=4, ensure_ascii=False)

        # SaveSlotCache
        tmp_path = 'saves/pc/Disco Elysium/SaveSlotCache/'
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
        with open(os.path.join(tmp_path, 'cache.json'), 'w', encoding='utf-8', newline='\n') as json_file:
            json.dump(savecache_json, json_file, indent=4, ensure_ascii=False)

        # zip
        tmp_path = 'saves/pc/Disco Elysium/'
        with zipfile.ZipFile(switch_fpath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(tmp_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, tmp_path)
                    zipf.write(file_path, arcname)
        
        return True

    
    @staticmethod
    def convert_to_pc(switch_fpath, pc_folder_path):
        print(f"Disco Elysium: Switch to PC ({switch_fpath} -> {pc_folder_path})")

        pc_folder_path = os.path.join(pc_folder_path, 'SaveGames')

        if not os.path.exists('saves/switch/Disco Elysium'):
            os.makedirs('saves/switch/Disco Elysium')

        switch_fname = os.path.splitext(os.path.basename(switch_fpath))[0]
        
        switch_extraction_path = os.path.join('saves', 'switch', 'Disco Elysium', switch_fname)
        if not os.path.exists(switch_extraction_path):
            os.makedirs(switch_extraction_path)
        # print('switch_extraction_path', switch_extraction_path)

        # Unzip switch_fpath
        with zipfile.ZipFile(switch_fpath, 'r') as zip_ref:
            zip_ref.extractall(switch_extraction_path)

        # read json and copy
        switch_saves_path = os.path.join(switch_extraction_path, 'SaveSlots')
        for folder_name in os.listdir(switch_saves_path):
            folder_path = os.path.join(switch_saves_path, folder_name)
            if os.path.isdir(folder_path):
                with open(os.path.join(switch_saves_path,folder_name,folder_name+'.json'), 'r', encoding='utf-8') as json_file:
                    data_dict = json.load(json_file)
                pc_savename = data_dict['fileName']
                pc_savepath = os.path.join(pc_folder_path, pc_savename)
                
                # copy
                shutil.copy(os.path.join(switch_saves_path,folder_name,folder_name+".jpg"), pc_savepath + ".jpg")
                shutil.copy(os.path.join(switch_saves_path,folder_name,folder_name+".zip"), pc_savepath + ".ntwtf.zip")

        return True


Converter.register(disco_elysium)