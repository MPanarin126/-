#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,QMessageBox, QRadioButton, QGroupBox,QHBoxLayout,QListWidget,QTextEdit, QFormLayout
import json


app = QApplication([])
notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(300, 200)



list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')

button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('удалить заметку')
button_note_save = QPushButton('сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')

button_teg_add = QPushButton('добавить к заметке')
button_teg_del = QPushButton('открепить от заметке')
button_teg_search = QPushButton('искать заметку по тегу')
list_tegs = QListWidget()
list_tegs_label = QLabel('список тегов')

field_text = QTextEdit()

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)
col_2.addWidget(list_tegs_label)
col_2.addWidget(list_tegs)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_teg_add)
row_3.addWidget(button_teg_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_teg_search)
col_2.addLayout(row_3)
col_2.addLayout(row_4)
layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)

notes_win.setLayout(layout_notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes=notes[key]['текст'])
    list_tegs.clear()
    list_tegs.addItems(notes=notes[key]['теги'])
    

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавить заметку', 'название заметки: ')
    if ok and note_name != '':
        notes = notes[note_name] = {'текст' : '', 'теги' : []}
        list_notes.addItem(note_name)
        list_tegs.addItems(notes[note_name]['теги'])


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tegs.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes,file, sort_keys=True, ensure_ascii=False)
            print(notes)
    else:
        print('Заметка не выбрана')



def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текс'] = field_text.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes,file, sort_keys=True, ensure_ascii=False)
            print(notes)
    else:
        print('заметка')


def add_teg():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        teg = field_tag.text()
        if not teg in notes[key]['теги']:
            notes[key]['теги'].append(teg)
            list_tegs.addItem(teg)
            field_tag.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes,file, sort_keys=True,ensure_ascii=False)
    else:
        print('Заметка для добавленя тега не выбрана')

def del_teg():
    if list_tegs.selectedItems():
        key = list_notes.selectedItems()[0].text()
        teg = list_notes.selectedItems()[0].text()
        notes[key]['теги'].remove(teg)
        list_tegs.clear()
        list_tegs.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes,file, sort_keys=True,ensure_ascii=False)
    else:
        print('тег для удаления')

def search_teg():
    print(button_teg_search.text())
    teg = field_tag.text()
    if button_teg_search.text() == 'Искать заметки по тегу' and teg:
        print(teg)
        notes.filtered = {}
        for note in notes:
            if teg in notes[note]['теги']:
                notes_filtered[note] = notes[note]
                button_teg_search.setText('сбросить поиск')
                list_notes.clear()
                list_tegs.clear()
                list_notes.addItems(notes_filtered)
                print(button_teg_search.text())
            elif button_teg_search.text() == 'сбросить поиск':
                field_tag.clear()
                list_notes.clear()
                list_tegs.clear()
                list_notes.addItems(notes)
                button_teg_search.setText('искать заметки по тегу')
                print(button_teg_search.text())
            else:
                pass

'''Запуск приложения'''
button_note_create.clicked.connect(add_note)
list_notes.clicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_teg_add.clicked.connect(add_teg)
button_teg_del.clicked.connect(del_teg)
button_teg_search.clicked.connect(search_teg)

notes_win.show()



app.exec_()

