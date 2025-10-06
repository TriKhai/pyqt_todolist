from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMessageBox
import sys, json, os
from PyQt6.QtCore import Qt

DATA_FILE = "./data/task.json"

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./ui/todolist.ui", self)

        self.addButton.clicked.connect(self.add_task)
        self.deleteButton.clicked.connect(self.delete_task)
        self.clearButton.clicked.connect(self.clear_all)
        self.taskList.itemChanged.connect(self.save_tasks)

        self.load_tasks()

    def add_task(self):
        text = self.taskInput.text().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "Task is empty!")
            return
        
        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Unchecked)
        self.taskList.addItem(item)
        self.taskInput.clear()
        self.save_tasks()

    def delete_task(self):
        for item in self.taskList.selectedItems():
            self.taskList.takeItem(self.taskList.row(item))
        self.save_tasks()

    def clear_all(self):
        self.taskList.clear()
        self.save_tasks()

    def save_tasks(self):
        data = []
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            data.append({"text": item.text(), "done": item.checkState() == 2})
        os.makedirs('data', exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_tasks(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
        for task in data:
            item = QListWidgetItem(task["text"])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if task["done"] else Qt.CheckState.Unchecked)
            self.taskList.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec())