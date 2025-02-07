import os
import re
import shutil
import json
from datetime import datetime
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QListView, QMessageBox, QFileDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap

from settings import Settings
from gui_ui import Ui_Main
from LoggingHandler import Logger
from GraphControler import GraphControler

try:
    import matplotlib.pyplot as plt
except Exception as e:
    print(f"An error occured when starting up! {e}. Some functionality of the program might not work properly! Usage of the program is a risk!")

class GraphList:
    _instance = None

    def __new__(cls, gui: Ui_Main, settings: Settings):
        if cls._instance is None:
            cls._instance = super(GraphList, cls).__new__(cls)
            cls._instance.__init__(gui, settings)
        return cls._instance

    def __init__(self, gui: Ui_Main, settings: Settings):
        if not hasattr(self, 'initialized'):
            self.settings = settings
            self.logger = Logger()
            self.graph_controler = GraphControler(gui, settings)
            self.path = self.settings.get("graphSavePath")
            self.model = QStandardItemModel()
            self.default_icon = QIcon()
            self.default_icon.addFile(u":/Menu/menu/Graph.png", QSize())
            self.default_icon_path = (u"icons/menu/Graph.png")
            self.view = QListView()
            self.listView = gui.list_graph
            self.listView.setModel(self.model)
            self.current_index = 0
            self.graphs_number = 0

            self.deleteMode = False
            self.delete_selection = "[Error: Something went wrong with getting the name of the graph.]"

            self.load_list()
            self.initialized = True

    def load_list(self):
        self.graphs_number = self.model.rowCount()
        if self.graphs_number == 0:
            self.reset_index_marker = True
        self.model.setRowCount(0)
        folders = [folder for folder in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, folder))]
        for folder in reversed(folders):
            folder_path = os.path.join(self.path, folder)
            if os.path.isdir(folder_path) and any(file.endswith('.json') for file in os.listdir(folder_path)):
                match = re.match(r'measurement_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})', folder)
                if match:
                    date_str = match.group(1)
                    time_str = match.group(2)
                    date_time_str = f"{date_str.replace('-', '.')} {time_str.replace('-', ':')}"
                    display_name = f"Pomiar [{date_time_str}]"
                else:
                    display_name = folder

                icon_path = self.find_icon(folder_path)
                item = QStandardItem(display_name)
                item.setData(folder, Qt.UserRole)
                if icon_path:
                    item.setIcon(QIcon(icon_path))
                else:
                    item.setIcon(self.default_icon)
                self.model.appendRow(item)
        self.listView.setModel(self.model)
        self.listView.selectionModel().selectionChanged.connect(self.selection_changed)
        
        if self.reset_index_marker or self.graphs_number != self.model.rowCount():
            self.current_index = 0
            self.reset_index_marker = False
        if not self.deleteMode:
            self.listView.setCurrentIndex(self.model.index(self.current_index, 0))

    def find_icon(self, folder_path):
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
        files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                return os.path.join(folder_path, file).replace('\\', '/')
        return None
    
    def selection_changed(self, selected):
        if selected.indexes():
            selected_index = selected.indexes()[0]
            if self.deleteMode == False:
                self.current_index = selected_index.row()
                self.graph_controler.load_graph(self.current_index)
            elif self.deleteMode == True and self.listView.selectionModel().hasSelection():
                self.delete_index = selected_index.row()
                self.delete_selection = self.listView.model().data(selected_index)
                self.graph_controler.load_graph(self.delete_index)
            
                self.popup_delete = QMessageBox()
                self.popup_delete.setWindowTitle("Usuwanie Wykresu")

                folder_name = os.listdir(self.path)[::-1][self.delete_index]
                folder_path = os.path.join(self.path, folder_name)
                icon = self.find_icon(folder_path)
                if not icon:
                    icon = self.default_icon_path
                pixmap = QPixmap(icon)
                scaled_pixmap = pixmap.scaledToHeight(100)
                self.popup_delete.setIconPixmap(scaled_pixmap)
                self.popup_delete.setText(f"<center>Czy jesteś pewien że chcesz usunąć wykres:<br><strong>{self.delete_selection}</strong>?")
                self.popup_delete.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                self.popup_delete.button(QMessageBox.Yes).setText("Zatwierdź")
                self.popup_delete.button(QMessageBox.No).setText("Anuluj")
                self.popup_delete.setDefaultButton(QMessageBox.No)
                delete_icon_active = QIcon()
                delete_icon_active.addFile(u":/Graph/graph/delete_active.png", QSize())
                self.popup_delete.setWindowIcon(delete_icon_active)
                self.popup_delete_response = self.popup_delete.exec_()
                if self.popup_delete_response == 16384:
                    try:
                        shutil.rmtree(folder_path)
                        self.delete_index = -1
                        self.listView.clearSelection()
                        self.load_list()
                        self.graph_controler.load_graph(0)
                    except Exception as e:
                        self.logger.log_error(f"An error occured during graph deletion: {str(e)}")
                self.listView.clearSelection()
                return
            else:
                self.logger.log_error(f"An error occured during a selection call: Invalid Delete Mode State: {self.deleteMode}")

    def refresh_graph(self):
        self.graph_controler.load_graph(self.current_index)


    def deleteMode_on(self):
        self.deleteMode = True
        self.listView.clearSelection()

    def deleteMode_off(self):
        self.deleteMode = False
        self.listView.setCurrentIndex(self.listView.model().index(self.current_index, 0))



    def save_graph_to_file(self):
        export_location = QFileDialog.getExistingDirectory(None, "Wybierz lokalizację eksportu")
        
        if export_location:
            filename = self.listView.model().data(self.model.index(self.current_index, 0))
            sanitized_filename = re.sub(r'[<>:"/\\|?*]', '_', filename).replace(':', '_').replace('[', '').replace(']', '')
            export_folder = os.path.join(export_location, sanitized_filename)
            os.makedirs(export_folder, exist_ok=True)

            self.original_folder = os.path.join(self.path, self.listView.model().data(self.model.index(self.current_index, 0), Qt.UserRole))

            for filename in os.listdir(self.original_folder):
                file_path = os.path.join(self.original_folder, filename)
                if os.path.isfile(file_path):
                    if filename.endswith('.json'):
                            json_file_path = file_path
                    shutil.copy2(file_path, export_folder)

            if json_file_path:
                with open(json_file_path, 'r') as f:
                    data = json.load(f)
                    seconds = data['seconds']
                    force = [float(re.search(r'-?\d{1,3}\.\d+', val).group()) for val in data['force']]
                    image_size = (2400, 1200)
                    dpi = 300
                    plt.figure(figsize=(image_size[0] / dpi, image_size[1] / dpi), dpi=dpi)
                    
                    plt.plot(seconds, force)
                    plt.xlabel('Czas [s]')
                    plt.ylabel('Siła [N]')
                    plt.title('Wykres siły w funkcji czasu')
                    plt.grid(True)
                    plt.savefig(os.path.join(export_folder, 'graph.png'), dpi=300)
                    plt.close()

                    self.popup_export_success = QMessageBox()
                    self.popup_export_success.setText("Eksport powiódł się.")
                    self.popup_export_success.setWindowTitle("Eksport")
                    self.popup_export_success.setWindowIcon(self.default_icon)
                    self.popup_export_success.exec()
            
            self.logger.log_info(f"Pliki wyeksportowane do: {export_folder}")



    def load_graph_from_file(self, import_path):
        required_keys = ['seconds', 'force']
        try:
            with open(import_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.logger.log_error(f"Nie można odnaleźć pliku na ścieżce {import_path}!")
        except json.JSONDecodeError:
            self.logger.log_error(f"Plik nie może zostać wczytany. Wybrany plik ze ścieżki {import_path} jest niemożliwy do przetworzenia.")
            return

        conditions = [
            all(key in data for key in required_keys),
            all(isinstance(data[key], list) for key in required_keys),
            all(isinstance(value, (int, float)) for value in data['seconds']),
            all(
                len(parts := value.replace(" ", "").split('N')) == 2 
                and parts[1] == '' 
                and parts[0].replace('.', '', 1).replace('-', '', 1).isdigit()
                for value in data['force']
            )
        ]

        if not all(conditions):
            self.logger.log_error(f"Plik nie może zostać wczytany. Wybrany plik ze ścieżki {import_path} jest w nieprawidłowym formacie.")
            return

        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"measurement_{current_datetime}"
        folder_path = os.path.join(self.path, folder_name)
        try:
            os.mkdir(folder_path)
        except FileExistsError:
            self.logger.log_error(f"Wystąpił błąd podczas tworzenia katalogu dla wczytywanego wykresu: Taki folder już istnieje. Proszę spróbować jeszcze raz.")
        except OSError as e:
            self.logger.log_error(f"Wystąpił błąd podczas tworzenia katalogu dla wczytywanego wykresu '{folder_name}': {e}")
        
        file_name = f"{folder_name}.json"
        file_path = os.path.join(folder_path, file_name)
        try:
            shutil.copy2(import_path, file_path)
        except OSError as e:
            self.logger.log_error(f"Wystąpił błąd podczas kopiowania pliku do katalogu '{folder_name}': {e}")

        self.refresh()

    

    def refresh(self):
        self.graph_controler.load_graph(self.current_index)
        try:
            for folder_name in os.listdir(self.path):
                folder_path = os.path.join(self.path, folder_name)
                if os.path.isdir(folder_path):
                    # Delete existing icon files
                    for file_name in os.listdir(folder_path):
                        if file_name.startswith("icon_") and file_name.endswith(".jpeg"):
                            icon_path = os.path.join(folder_path, file_name)
                            try:
                                os.remove(icon_path)
                            except Exception as e:
                                print(f"Failed to delete icon file: {e}")
                                self.logger.log_error(f"Failed to delete icon file: {e}")

                    # Create new icon files
                    for file_name in os.listdir(folder_path):
                        if file_name.endswith(".json"):
                            file_path = os.path.join(folder_path, file_name)
                            with open(file_path, 'r') as file:
                                data = json.load(file)
                            image_size = (160, 100)
                            dpi = 100
                            plt.figure(figsize=(image_size[0] / dpi, image_size[1] / dpi), dpi=dpi)
                            plt.xticks([])
                            plt.yticks([])
                            plt.axis('off')

                            forces = []
                            for f in data["force"]:
                                f = f.replace("N", "").strip()
                                if "-" in f:
                                    forces.append(-float(f.replace("-", "").strip()))
                                else:
                                    forces.append(float(f))

                            plt.plot(data["seconds"], forces)
                            icon_file_name = f"icon_{file_name.replace('.json', '')}.jpeg"
                            icon_path = os.path.join(folder_path, icon_file_name)
                            plt.savefig(icon_path, bbox_inches="tight")
                            plt.close()
        except Exception as e:
            print(f"Refresh failed: {e}")
            self.logger.log_error(f"Icon refresh failed! {e}")
            return
        self.load_list()