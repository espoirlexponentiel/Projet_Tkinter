from tkinter import Tk, Label, Button, Entry, messagebox, Listbox, Scrollbar, StringVar, END, Frame
from controllers import add_book, get_books, delete_book, update_book, update_book_quantity
import tkinter.font as font
from tkinter import Tk
from tkinter import Toplevel, Spinbox

class LibraryApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Gestion de bibliothèque")
        self.root.geometry("1100x800")  # Taille de la fenêtre
        

        # Cadre principal pour centrer les widgets
        self.main_frame = Frame(self.root)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Polices
        self.label_font = font.Font(family="Arial", size=16)  # Police agrandie pour les étiquettes
        self.entry_font = font.Font(family="Arial", size=14)  # Police pour les champs d'entrée
        self.button_font = font.Font(family="Arial", size=14, weight="bold")  # Police pour les boutons

        self.selected_book_id = None
        self.search_var = StringVar()  # Variable pour le champ de recherche
        self.create_main_ui()

    def create_main_ui(self):
        # Barre de recherche
        Label(self.main_frame, text="Rechercher :", font=self.label_font).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_search = Entry(self.main_frame, font=self.entry_font, width=50, textvariable=self.search_var)
        self.entry_search.grid(row=0, column=1, padx=10, pady=10)
        Button(self.main_frame, text="Rechercher", font=self.button_font, command=self.search_books_handler).grid(
            row=0, column=2, padx=10, pady=10
        )

        # Formulaire pour les livres
        Label(self.main_frame, text="Titre :", font=self.label_font).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_title = Entry(self.main_frame, font=self.entry_font, width=30)
        self.entry_title.grid(row=1, column=1, padx=10, pady=10)

        Label(self.main_frame, text="Auteur :", font=self.label_font).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_author = Entry(self.main_frame, font=self.entry_font, width=30)
        self.entry_author.grid(row=2, column=1, padx=10, pady=10)

        Label(self.main_frame, text="Genre :", font=self.label_font).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_genre = Entry(self.main_frame, font=self.entry_font, width=30)
        self.entry_genre.grid(row=3, column=1, padx=10, pady=10)

        Label(self.main_frame, text="Année :", font=self.label_font).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_year = Entry(self.main_frame, font=self.entry_font, width=30)
        self.entry_year.grid(row=4, column=1, padx=10, pady=10)

        Label(self.main_frame, text="Quantité :", font=self.label_font).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.entry_quantite = Entry(self.main_frame, font=self.entry_font, width=30)
        self.entry_quantite.grid(row=5, column=1, padx=10, pady=10)

        # Boutons alignés horizontalement
        self.button_frame = Frame(self.main_frame)  # Cadre pour les boutons
        self.button_frame.grid(row=6, column=0, columnspan=3, pady=20)

        Button(self.button_frame, text="Ajouter un livre", font=self.button_font, command=self.add_book_handler).pack(
            side="left", padx=10
        )
        Button(self.button_frame, text="Modifier le livre", font=self.button_font, command=self.update_book_handler).pack(
            side="left", padx=10
        )
        Button(self.button_frame, text="Supprimer le livre", font=self.button_font, command=self.delete_book_handler).pack(
            side="left", padx=10
        )

        # Liste des livres
        Label(self.main_frame, text="Liste des livres :", font=self.label_font).grid(
            row=7, column=0, columnspan=3, pady=10
        )
        self.scrollbar = Scrollbar(self.main_frame)
        self.scrollbar.grid(row=8, column=3, sticky="ns", padx=(0, 10))
        self.listbox = Listbox(
            self.main_frame, height=10, width=70, font=self.entry_font, yscrollcommand=self.scrollbar.set
        )
        self.listbox.grid(row=8, column=0, columnspan=3, pady=10)
        self.scrollbar.configure(command=self.listbox.yview)

        # Liaison de la sélection
        self.listbox.bind("<<ListboxSelect>>", self.on_select_book)

        # Charger les livres au démarrage
        self.load_books()

    def add_book_handler(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        genre = self.entry_genre.get()
        year = self.entry_year.get()
        quantite = self.entry_quantite.get()
        if title and author:
            add_book(title, author, genre, year, quantite)
            messagebox.showinfo("Succès", "Livre ajouté avec succès!")
            self.clear_fields()
            self.load_books()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir les champs obligatoires.")

    def search_books_handler(self):
        search_query = self.entry_search.get().lower()
        books = get_books()
        self.listbox.delete(0, END)
        for book in books:
            if any(search_query in str(field).lower() for field in book):
                self.listbox.insert(END, f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {book[5]}")

    def update_book_handler(self):
        if self.selected_book_id:
            title = self.entry_title.get()
            author = self.entry_author.get()
            genre = self.entry_genre.get()
            year = self.entry_year.get()
            quantite = self.entry_quantite.get()
            if title and author:
                update_book(self.selected_book_id, title, author, genre, year, quantite)
                messagebox.showinfo("Succès", "Livre modifié avec succès!")
                self.clear_fields()
                self.load_books()
            else:
                messagebox.showwarning("Erreur", "Veuillez remplir les champs obligatoires.")
        else:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un livre à modifier.")


            



    def delete_book_handler(self):
        if self.selected_book_id:
            def delete_confirm():
                quantite_to_delete = int(quantite_spinbox.get())
                if quantite_to_delete <= current_quantite:
                    new_quantite = current_quantite - quantite_to_delete
                    if new_quantite > 0:
                        update_book_quantity(self.selected_book_id, new_quantite)
                    else:
                        delete_book(self.selected_book_id)
                    messagebox.showinfo("Succès", "Livre supprimé avec succès!")
                    self.clear_fields()
                    self.load_books()
                    confirm_window.destroy()
                else:
                    messagebox.showwarning("Erreur", "Quantité à supprimer supérieure à la quantité actuelle.")

            current_quantite = int(self.entry_quantite.get())
            confirm_window = Toplevel(self.root)
            confirm_window.title("Confirmer la suppression")
            Label(confirm_window, text="Quantité à supprimer :").pack(padx=10, pady=10)
            quantite_spinbox = Spinbox(confirm_window, from_=1, to=current_quantite)
            quantite_spinbox.pack(padx=10, pady=10)
            Button(confirm_window, text="Supprimer", command=delete_confirm).pack(pady=10)
        else:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un livre à supprimer.")



    def on_select_book(self, event):
        try:
            index = self.listbox.curselection()[0]
            book_data = self.listbox.get(index).split(" | ")
            self.selected_book_id = int(book_data[0])  # ID du livre
            self.entry_title.delete(0, END)
            self.entry_title.insert(END, book_data[1])
            self.entry_author.delete(0, END)
            self.entry_author.insert(END, book_data[2])
            self.entry_genre.delete(0, END)
            self.entry_genre.insert(END, book_data[3])
            self.entry_year.delete(0, END)
            self.entry_year.insert(END, book_data[4])
            self.entry_quantite.delete(0, END)
            self.entry_quantite.insert(END, book_data[5])
        except IndexError:
            pass

    def clear_fields(self):
        self.entry_title.delete(0, "end")
        self.entry_author.delete(0, "end")
        self.entry_genre.delete(0, "end")
        self.entry_year.delete(0, "end")
        self.entry_quantite.delete(0, "end")
        self.selected_book_id = None

    def load_books(self):
        self.listbox.delete(0, END)
        books = get_books()
        for book in books:
           self.listbox.insert(END, f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {book[5]}")

    def run(self):
        self.root.mainloop()
