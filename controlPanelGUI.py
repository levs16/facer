import sys
import json
import cv2
import face_recognition
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QListWidget, QListWidgetItem

class ControlPanelGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.json_file = "dataset/faces.json"
        self.face_data = {"emp_details": []}

        # Load existing face data
        try:
            with open(self.json_file, "r") as f:
                self.face_data = json.load(f)
        except FileNotFoundError:
            pass

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Face Recognition Control Panel')

        self.name_label = QLabel('Name:')
        self.name_entry = QLineEdit(self)
        self.image_button = QPushButton('Select Image', self)
        self.add_button = QPushButton('Add Face', self)
        self.delete_button = QPushButton('Delete Face', self)
        self.clear_button = QPushButton('Clear List', self)
        self.result_label = QLabel(self)
        self.face_list = QListWidget(self)

        self.image_button.clicked.connect(self.selectImage)
        self.add_button.clicked.connect(self.addFace)
        self.delete_button.clicked.connect(self.deleteFace)
        self.clear_button.clicked.connect(self.clearList)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_entry)
        layout.addWidget(self.image_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.face_list)

        self.setLayout(layout)

        # Update the face list on-load
        self.updateFaceList()

    def selectImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        image_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Image Files (*.jpg *.jpeg *.png);;All Files (*)", options=options)

        if image_path:
            self.image_path = image_path

    def addFace(self):
        name = self.name_entry.text()

        if name and hasattr(self, 'image_path'):
            img = cv2.imread(self.image_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_encoding = face_recognition.face_encodings(rgb_img)[0]

            self.face_data["emp_details"].append({"name": name, "face_encoding": list(face_encoding)})

            with open(self.json_file, "w") as f:
                json.dump(self.face_data, f)

            self.result_label.setText(f"Successfully added {name} to the JSON file.")
            self.updateFaceList()
        else:
            self.result_label.setText("Please provide a name and select an image.")

    def deleteFace(self):
        selected_item = self.face_list.currentItem()
        if selected_item:
            name = selected_item.text()
            for i, person in enumerate(self.face_data["emp_details"]):
                if person["name"] == name:
                    del self.face_data["emp_details"][i]
                    with open(self.json_file, "w") as f:
                        json.dump(self.face_data, f)
                    self.result_label.setText(f"Successfully deleted {name} from the JSON file.")
                    self.updateFaceList()
                    return
            self.result_label.setText(f"No such name {name} found in the JSON file.")

    def clearList(self):
        self.face_list.clear()

    def updateFaceList(self):
        self.face_list.clear()
        for person in self.face_data["emp_details"]:
            self.face_list.addItem(QListWidgetItem(person["name"]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    control_panel = ControlPanelGUI()
    control_panel.show()
    sys.exit(app.exec_())
