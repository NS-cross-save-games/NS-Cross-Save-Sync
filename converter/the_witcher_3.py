import shutil
from converter.converter import Converter
import os
import zipfile

from utils import zip_path

'''
The Witcher 3
PC: gamesaves/*png and *.sav
switch: unzip *.png *.sav *.req
'''
class the_witcher_3(Converter):

    @staticmethod
    def convert_to_switch(switch_fpath, pc_folder_path):
        print(f"The Witcher 3: PC to Switch ({pc_folder_path} -> {switch_fpath})")
        # copy gamesave
        tmp_path = 'saves/pc/The Witcher 3/'
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        # collect
        save_files = []
        for fname in os.listdir(os.path.join(pc_folder_path, 'gamesaves')):
            if fname.endswith('.png'):
                full_path = os.path.join(pc_folder_path, 'gamesaves', fname)
                save_files.append((fname, os.path.getmtime(full_path)))
        # sort by mtime
        save_files.sort(key=lambda x: x[1], reverse=True)

        # only copy the first 10
        for fname, _ in save_files[:10]:
            basename = os.path.splitext(fname)[0]
            shutil.copy2(os.path.join(pc_folder_path, 'gamesaves', basename+'.png'), tmp_path)
            shutil.copy2(os.path.join(pc_folder_path, 'gamesaves', basename+'.sav'), tmp_path)
            # with open(os.path.join(tmp_path, basename + '.req'), 'w', encoding='utf-8') as req_file:
            #     req_file.write("content0;content1;content2;content3;content4;")
        
        # copy settings
        tmp_path = 'saves/pc/The Witcher 3/user.settings/'
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
        
        shutil.copy(os.path.join(pc_folder_path,'user.settings'), os.path.join(tmp_path+'settings.txt'))

        zip_path(switch_fpath, 'saves/pc/The Witcher 3')

        return True


    @staticmethod
    def convert_to_pc(switch_fpath, pc_folder_path):
        print(f"The Witcher 3: Switch to PC ({switch_fpath} -> {pc_folder_path})")

        # Unzip switch_fpath
        switch_fname = os.path.splitext(os.path.basename(switch_fpath))[0]
        switch_extraction_path = os.path.join('saves', 'switch', 'The Witcher 3', switch_fname)
        if not os.path.exists(switch_extraction_path):
            os.makedirs(switch_extraction_path)
        with zipfile.ZipFile(switch_fpath, 'r') as zip_ref:
            zip_ref.extractall(switch_extraction_path)

        ###########
        
        # copy settings
        if not os.path.exists(os.path.join(pc_folder_path,'user.settings')):
            os.makedirs(os.path.join(pc_folder_path,'user.settings'))
        shutil.copy(os.path.join(switch_extraction_path,'user.settings','settings.txt'), 
                    os.path.join(pc_folder_path,'user.settings'))
            
        # copy gamesaves
        tmp_path = os.path.join(pc_folder_path, 'gamesaves')
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
        if not os.path.exists("offzip"):
            os.makedirs("offzip")

        for fname in os.listdir(switch_extraction_path):
            if fname.endswith('.png'):
                basename = os.path.splitext(fname)[0]
                shutil.copy2(os.path.join(switch_extraction_path, basename+'.png'), tmp_path)
                # use offzip to extract the .sav file
                # Note: If the versions don't match, you can change the value at offset C16 to 0 in hex edit.
                os.system(f".\\offzip.exe -a {os.path.join(switch_extraction_path, basename + '.sav')} offzip 0")
                shutil.move(os.path.join('offzip', "0000000c.snf"), os.path.join(tmp_path, basename + '.sav'))
                
        return True

Converter.register(the_witcher_3)