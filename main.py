import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QComboBox, QMessageBox
import getpass
import os
import pkgutil
import importlib

from converter.converter import Converter


package = 'converter'
for _, module_name, _ in pkgutil.iter_modules([package]):
    module = importlib.import_module(f"{package}.{module_name}")


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.load_json()
        self.initUI()

    # Load the JSON file and replace the placeholder with the actual username.
    def load_json(self):
        user_name = getpass.getuser()
        print('user_name', user_name)
        
        with open('default_path.json', 'r') as file:
            data = json.load(file)
            self.default_pc_path_list = data
        for item in self.default_pc_path_list:
            item['default_pc_path'] = item['default_pc_path'].replace('$USER_NAME', user_name)

    # Initialize the user interface for the application.
    def initUI(self):
        layout = QVBoxLayout()

        self.label_combo = QLabel('Game Select:', self)
        layout.addWidget(self.label_combo)
        self.combo_box = QComboBox(self)

    # game list combobox
        self.combo_box.addItems([item['name'] for item in self.default_pc_path_list])
        self.combo_box.currentIndexChanged.connect(self.fill_default_path)
        layout.addWidget(self.combo_box)

    # Switch gamesave zip layout
        self.label1 = QLabel('Select Switch zipped gamesaves:', self)
        layout.addWidget(self.label1)
        
        zip_layout = QHBoxLayout()
        self.zip_input = QLineEdit(self)
        zip_layout.addWidget(self.zip_input)
        
        self.zip_button = QPushButton('select', self)
        self.zip_button.clicked.connect(self.select_zip_file)
        zip_layout.addWidget(self.zip_button)
        layout.addLayout(zip_layout)

    # PC gamesave folder layout
        self.label2 = QLabel('Select Windows gamesave folder:', self)
        layout.addWidget(self.label2)
        
        folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit(self)
        folder_layout.addWidget(self.folder_input)

        self.folder_button = QPushButton('select', self)
        self.folder_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_button)

        layout.addLayout(folder_layout)

    # button layout
        button_layout = QHBoxLayout()
        
        self.button_a = QPushButton('Sync to Switch', self)
        self.button_a.clicked.connect(self.on_click_2switch)
        button_layout.addWidget(self.button_a)

        self.button_b = QPushButton('Sync to PC', self)
        self.button_b.clicked.connect(self.on_click_2pc)
        button_layout.addWidget(self.button_b)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        
        self.fill_default_path();
        self.setWindowTitle('NS-CROSS-SAVE-SYNC')
        self.resize(500, 180)
        self.show()

    # Fill the default path based on the selected game.
    def fill_default_path(self):
        select_name = self.combo_box.currentText()
        print(select_name)
        # find
        for item in self.default_pc_path_list:
            if item["name"] == select_name:
                default_pc_path = item["default_pc_path"]
                # print('default_pc_path', default_pc_path)
                self.folder_input.setText(default_pc_path)
                break

    # Open file dialog to select a ZIP file.
    def select_zip_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "select Switch gamesave zips", "", "ZIP Files (*.zip);;All Files (*)", options=options)
        if file_name:
            self.zip_input.setText(file_name)

    # Open folder dialog to select a gamesave folder.
    def select_folder(self):
        options = QFileDialog.Options()
        folder_name = QFileDialog.getExistingDirectory(self, "select Windows gamesave folder", options=options)
        if folder_name:
            self.folder_input.setText(folder_name)

    # Handle sync from PC to Switch.
    def on_click_2switch(self):
        zip_file = self.zip_input.text()
        folder = self.folder_input.text()
        
        print('pc to switch')
        print(f'switch: {zip_file}')
        print(f'pc: {folder}')

        # find
        select_name = self.combo_box.currentText()
        print(select_name)
        class_name = ''
        for item in self.default_pc_path_list:
            if item["name"] == select_name:
                class_name = item["class_name"]
        ret = Converter.get_converter(class_name).convert_to_switch(zip_file, folder)
        if ret:
            QMessageBox.information(self, "success", "success: PC to Switch")
        else:
            QMessageBox.information(self, "fail", "fail: PC to Switch")
        
    # Handle sync from Switch to PC.
    def on_click_2pc(self):
        zip_file = self.zip_input.text()
        folder = self.folder_input.text()
        print('switch to pc')
        print(f'switch: {zip_file}')
        print(f'pc: {folder}')
        
        # find
        select_name = self.combo_box.currentText()
        print(select_name)
        class_name = ''
        for item in self.default_pc_path_list:
            if item["name"] == select_name:
                class_name = item["class_name"]
        ret = Converter.get_converter(class_name).convert_to_pc(zip_file, folder)
        if ret:
            QMessageBox.information(self, "success", "success: Switch to PC")
        else:
            QMessageBox.information(self, "fail", "fail: Switch to PC")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())