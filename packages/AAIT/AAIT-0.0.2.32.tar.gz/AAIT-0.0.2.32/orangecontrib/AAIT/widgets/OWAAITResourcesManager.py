import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from Orange.widgets import widget
from PyQt5.QtCore import QTimer

from AnyQt.QtWidgets import QDialog, QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, \
    QTextEdit, \
    QGroupBox, QSpacerItem

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils.MetManagement import get_aait_store_requirements_json, GetFromRemote
    from Orange.widgets.orangecontrib.AAIT.utils import shared_variables, MetManagement, shared_functions, \
        SimpleDialogQt
else:
    from orangecontrib.AAIT.utils.MetManagement import get_aait_store_requirements_json, GetFromRemote
    from orangecontrib.AAIT.utils import shared_variables, MetManagement, shared_functions, SimpleDialogQt


class OWAAITResourcesManager(widget.OWWidget):
    name = "AAIT Resources Manager"
    description = "Manage AAIT resources, such as model, example workflows, datasets...."
    icon = "icons/documents.png"
    priority = 10
    # Path
    dossier_du_script = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()
        self.requirements = get_aait_store_requirements_json()
        self.controlAreaVisible = False

    # trigger if standard windows is opened
    def showEvent(self, event):
        super().showEvent(event)
        self.show_dialog()
        # We cannot close the standard ui widget it is displayed
        # so it makes a little tinkles :(
        QTimer.singleShot(0, self.close)

    def show_dialog(self):

        # third-party code execution vs standard code execution
        if False == os.path.isfile(MetManagement.get_local_store_path() + "AddOn/prefix_show_dialog.py"):
            dialog = QDialog()
            layout_a = QVBoxLayout()
            dialog.setLayout(layout_a)
            model = None
        else:
            sys.path.append(MetManagement.get_local_store_path() + "AddOn")
            import prefix_show_dialog
            stable_dependency = True
            if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
                stable_dependency = False
            dialog, model = prefix_show_dialog.prefix_dialog_function(self,stable_dependency)

        # download section
        # Creation of vertical layout
        main_layout = QVBoxLayout()
        group_box = QGroupBox("Download new minimum working example")
        group_layout = QVBoxLayout()

        # Elements are presented horizontally
        h_layout = QHBoxLayout()
        v_layout_button_combo_box = QVBoxLayout()
        self.comboBox = QComboBox()
        self.comboBox.setMinimumSize(200, 20)
        self.ressource_path_button = QPushButton('select repo')
        self.saveButton = QPushButton('download')
        v_layout_button_combo_box.addWidget(self.ressource_path_button)
        verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        v_layout_button_combo_box.addItem(verticalSpacer)
        v_layout_button_combo_box.addWidget(self.comboBox)
        v_layout_button_combo_box.addWidget(self.saveButton)
        h_layout.addLayout(v_layout_button_combo_box)

        v_layout_label_text = QVBoxLayout()
        label = QLabel('Description:')
        self.descriptionTextEdit = QTextEdit()
        v_layout_label_text.addWidget(label)
        v_layout_label_text.addWidget(self.descriptionTextEdit)
        h_layout.addLayout(v_layout_label_text)

        group_layout.addLayout(h_layout)
        group_box.setLayout(group_layout)
        main_layout.addWidget(group_box)
        dialog.layout().insertLayout(0, main_layout)

        self.comboBox.currentIndexChanged.connect(self.handleComboBoxChange)
        self.saveButton.clicked.connect(self.saveFile)
        self.populate_combo_box()
        self.ressource_path_button.clicked.connect(self.update_ressource_path)

        if False == os.path.isfile(MetManagement.get_local_store_path() + "AddOn/postfix_show_dialog.py"):
            dialog.exec()
        else:
            sys.path.append(MetManagement.get_local_store_path() + "AddOn")
            import postfix_show_dialog
            stable_dependency = True
            if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
                stable_dependency = False
            postfix_show_dialog.postfix_dialog_function(dialog, model)

    def populate_combo_box(self):
        workflows = []
        descriptions = dict()
        for element in self.requirements:
            workflows.append(element["name"])
            descriptions[element["name"]] = element["description"][0]
        self.descriptions = descriptions
        self.comboBox.addItems(workflows)

    def handleComboBoxChange(self, index):
        # Gérer le changement de sélection dans la ComboBox
        selected_file = self.comboBox.itemText(index)
        # Afficher la description dans le QTextEdit
        self.descriptionTextEdit.setPlainText(self.descriptions[selected_file])

    def read_description(self, file_name):
        # Chemin du fichier texte contenant la description
        description_file_path = os.path.join(self.dossier_du_script, 'ows_example',
                                             f'{os.path.splitext(file_name)[0]}.txt')
        # Lire le contenu du fichier s'il existe, sinon retourner une chaîne vide
        if os.path.exists(description_file_path):
            with open(description_file_path, 'r') as file:
                description = file.read()
        else:
            description = ""
        return description

    def saveFile(self):
        # Méthode pour sauvegarder le fichier sélectionné dans un nouvel emplacement
        selected_file = self.comboBox.currentText()
        GetFromRemote(selected_file)

    def update_ressource_path(self):
        folder = MetManagement.get_aait_store_remote_ressources_path()
        folder = SimpleDialogQt.BoxSelectFolder(folder)
        if folder == "":
            return
        MetManagement.set_aait_store_remote_ressources_path(folder)
        self.requirements = get_aait_store_requirements_json()
        self.populate_combo_box()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = OWAAITResourcesManager()
    window.show()
    app.exec_()
