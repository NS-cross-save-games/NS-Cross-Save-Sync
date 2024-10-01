from converter.converter import Converter

class the_witcher_3(Converter):

    @staticmethod
    def convert_to_switch(switch_fpath, pc_folder_path):
        print(f"The Witcher 3: PC to Switch ({pc_folder_path} -> {switch_fpath})")

    @staticmethod
    def convert_to_pc(switch_fpath, pc_folder_path):
        print(f"The Witcher 3: Switch to PC ({switch_fpath} -> {pc_folder_path})")


Converter.register(the_witcher_3)