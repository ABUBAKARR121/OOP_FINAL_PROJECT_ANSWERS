import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QPushButton, QGridLayout, QLabel, QLineEdit, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
import sqlite3

class LibraryManagementSystem(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.create_table()
        self.create_form()

        self.layout.addWidget(self.table)
        self.layout.addLayout(self.form_layout)

        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("DROP TABLE IF EXISTS books")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                isbn TEXT,
                genre TEXT,
                publication_year INTEGER
            )
        """)

        self.conn.commit()

        self.cursor.execute("INSERT INTO books (id, title, author, isbn, genre, publication_year) VALUES (1, 'Python Crash Course', 'Eric Matthes', '9781593279288', 'Programming', 2016)")
        self.cursor.execute("INSERT INTO books (id, title, author, isbn, genre, publication_year) VALUES (2, 'The C++ Programming Language', 'Bjarne Stroustrup', '9780321563842', 'Programming', 2013)")
        self.cursor.execute("INSERT INTO books (id, title, author, isbn, genre, publication_year) VALUES (3, 'Head First Java', 'Kathy Sierra and Bert Bates', '9780596009205', 'Programming', 2005)")
        self.cursor.execute("INSERT INTO books (id, title, author, isbn, genre, publication_year) VALUES (4, 'Eloquent JavaScript', 'Marijn Haverbeke', '9781593279509', 'Programming', 2018)")
        self.cursor.execute("INSERT INTO books (id, title, author, isbn, genre, publication_year) VALUES (5, 'Computer Networking: A Top-Down Approach', 'James F. Kurose and Keith W. Ross', '9780133594140', 'Networking', 2016)")
        self.cursor.execute("INSERT INTO books (id, title, author, isbn, genre, publication_year) VALUES (6, 'Discrete Mathematics and Its Applications', 'Kenneth H. Rosen', '9780073383095', 'Mathematics', 2018)")

        self.conn.commit()

        self.load_data()

    def create_table(self):
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "ISBN", "Genre", "Publication Year"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def create_form(self):
        self.form_layout = QGridLayout()

        self.title_label = QLabel("Title:")
        self.title_input = QLineEdit()

        self.author_label = QLabel("Author:")
        self.author_input = QLineEdit()

        self.isbn_label = QLabel("ISBN:")
        self.isbn_input = QLineEdit()

        self.genre_label = QLabel("Genre:")
        self.genre_input = QComboBox()
        self.genre_input.addItem("Programming")
        self.genre_input.addItem("Networking")
        self.genre_input.addItem("Mathematics")
        self.genre_input.addItem("Science")
        self.genre_input.addItem("History")

        self.publication_year_label = QLabel("Publication Year:")
        self.publication_year_input = QLineEdit()

        self.add_button = QPushButton("Add Book")
        self.add_button.clicked.connect(self.add_book)

        self.update_button = QPushButton("Update Book")
        self.update_button.clicked.connect(self.update_book)

        self.delete_button = QPushButton("Delete Book")
        self.delete_button.clicked.connect(self.delete_book)

        self.search_button = QPushButton("Search Book")
        self.search_button.clicked.connect(self.search_book)

        self.search_input = QLineEdit()

        self.form_layout.addWidget(self.title_label, 0, 0)
        self.form_layout.addWidget(self.title_input, 0, 1)
        self.form_layout.addWidget(self.author_label, 1, 0)
        self.form_layout.addWidget(self.author_input, 1, 1)
        self.form_layout.addWidget(self.isbn_label, 2, 0)
        self.form_layout.addWidget(self.isbn_input, 2, 1)
        self.form_layout.addWidget(self.genre_label, 3, 0)
        self.form_layout.addWidget(self.genre_input, 3, 1)
        self.form_layout.addWidget(self.publication_year_label, 4, 0)
        self.form_layout.addWidget(self.publication_year_input, 4, 1)
        self.form_layout.addWidget(self.add_button, 5, 0)
        self.form_layout.addWidget(self.update_button, 5, 1)
        self.form_layout.addWidget(self.delete_button, 5, 2)
        self.form_layout.addWidget(self.search_input, 6, 0)
        self.form_layout.addWidget(self.search_button, 6, 1)

    def load_data(self):
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()
        genre = self.genre_input.currentText()
        publication_year = self.publication_year_input.text()

        self.cursor.execute("INSERT INTO books (title, author, isbn, genre, publication_year) VALUES (?, ?, ?, ?, ?)", (title, author, isbn, genre, publication_year))
        self.conn.commit()

        self.load_data()

        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.publication_year_input.clear()

    def update_book(self):
        row = self.table.currentRow()
        if row != -1:
            id = self.table.item(row, 0).text()
            title = self.title_input.text()
            author = self.author_input.text()
            isbn = self.isbn_input.text()
            genre = self.genre_input.currentText()
            publication_year = self.publication_year_input.text()

            self.cursor.execute("UPDATE books SET title = ?, author = ?, isbn = ?, genre = ?, publication_year = ? WHERE id = ?", (title, author, isbn, genre, publication_year, id))
            self.conn.commit()

            self.load_data()

            self.title_input.clear()
            self.author_input.clear()
            self.isbn_input.clear()
            self.publication_year_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Please select a book to update")

    def delete_book(self):
        row = self.table.currentRow()
        if row != -1:
            id = self.table.item(row, 0).text()

            self.cursor.execute("DELETE FROM books WHERE id = ?", (id,))
            self.conn.commit()

            self.load_data()
        else:
            QMessageBox.warning(self, "Error", "Please select a book to delete")

    def search_book(self):
        search_term = self.search_input.text()

        self.cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?", (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        rows = self.cursor.fetchall()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryManagementSystem()
    window.show()
    sys.exit(app.exec_())