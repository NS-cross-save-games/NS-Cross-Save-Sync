import shutil
from converter.converter import Converter
import os
import zipfile

from utils import zip_path

'''
balatro
PC: *
switch: .lovegame/*
'''
class balatro(Converter):

    @staticmethod
    def convert_to_switch(switch_fpath, pc_folder_path):
        print(f"balatro: PC to Switch ({pc_folder_path} -> {switch_fpath})")
        # copy gamesave
        tmp_path = 'saves/pc/balatro/.lovegame'
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
        
        for item in os.listdir(pc_folder_path):
            src_item = os.path.join(pc_folder_path, item)
            dst_item = os.path.join(tmp_path, item)
            if os.path.isdir(src_item):
                shutil.copytree(src_item, dst_item)
            else:
                shutil.copy2(src_item, dst_item)

        zip_path(switch_fpath, 'saves/pc/balatro')

        return True


    @staticmethod
    def convert_to_pc(switch_fpath, pc_folder_path):
        print(f"balatro: Switch to PC ({switch_fpath} -> {pc_folder_path})")

        # Unzip switch_fpath
        switch_fname = os.path.splitext(os.path.basename(switch_fpath))[0]
        switch_extraction_path = os.path.join('saves', 'switch', 'balatro', switch_fname)
        if not os.path.exists(switch_extraction_path):
            os.makedirs(switch_extraction_path)
        with zipfile.ZipFile(switch_fpath, 'r') as zip_ref:
            zip_ref.extractall(switch_extraction_path)

        ###########
        
        switch_extraction_path = os.path.join(switch_extraction_path, '.lovegame')
        for root, dirs, files in os.walk(switch_extraction_path):
            for dir in dirs:
                src_dir = os.path.join(root, dir)
                dst_dir = os.path.join(pc_folder_path, os.path.relpath(src_dir, switch_extraction_path))
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(pc_folder_path, os.path.relpath(src_file, switch_extraction_path))
                shutil.copy2(src_file, dst_file)
                
        return True

Converter.register(balatro)