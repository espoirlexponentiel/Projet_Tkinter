from tkinter import Tk, Label, Button, Entry, messagebox, StringVar, Listbox, Scrollbar, END, Frame
import sqlite3
import tkinter.font as font
from database import connect

class LoanManagerApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Gestion des emprunts de livres")
        self.root.geometry("800x600")
        #self.root.resizable(False, False)

        # Cadre principal pour centrer les widgets
        self.main_frame = Frame(self.root)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Variables
        self.book_id_var = StringVar()
        self.borrower_name_var = StringVar()
        self.borrow_date_var = StringVar()
        self.return_date_var = StringVar()
        self.search_var = StringVar()

        # Polices
        self.label_font = font.Font(family="Arial", size=14)
        self.entry_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=12, weight="bold")

        self.create_loan_ui()

    def create_loan_ui(self):
        # Formulaire pour les emprunts
        Label(self.root, text="ID du livre :", font=self.label_font).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_book_id = Entry(self.root, font=self.entry_font, textvariable=self.book_id_var)
        self.entry_book_id.grid(row=0, column=1, padx=10, pady=10)

        Label(self.root, text="Nom de l'emprunteur :", font=self.label_font).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_borrower_name = Entry(self.root, font=self.entry_font, textvariable=self.borrower_name_var)
        self.entry_borrower_name.grid(row=1, column=1, padx=10, pady=10)

        Label(self.root, text="Date d'emprunt (AAAA-MM-JJ) :", font=self.label_font).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_borrow_date = Entry(self.root, font=self.entry_font, textvariable=self.borrow_date_var)
        self.entry_borrow_date.grid(row=2, column=1, padx=10, pady=10)

        Label(self.root, text="Date de retour (AAAA-MM-JJ) :", font=self.label_font).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_return_date = Entry(self.root, font=self.entry_font, textvariable=self.return_date_var)
        self.entry_return_date.grid(row=3, column=1, padx=10, pady=10)

        # Boutons alignés horizontalement
        self.button_frame = Frame(self.root)
        self.button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        Button(self.button_frame, text="Ajouter un emprunt", font=self.button_font, command=self.add_loan_handler).pack(
            side="left", padx=10
        )
        Button(self.button_frame, text="Retourner un livre", font=self.button_font, command=self.return_book_handler).pack(
            side="left", padx=10
        )

        # Liste des emprunts
        Label(self.root, text="Liste des emprunts :", font=self.label_font).grid(row=5, column=0, columnspan=2, pady=10)
        self.scrollbar = Scrollbar(self.main_frame)
        self.scrollbar.grid(row=6, column=3, sticky="ns", padx=(0, 10))
        self.listbox = Listbox(
            self.main_frame, height=10, width=70, font=self.entry_font, yscrollcommand=self.scrollbar.set
        )
        self.listbox.grid(row=8, column=0, columnspan=3, pady=10)
        self.scrollbar.configure(command=self.listbox.yview)

        # Charger les emprunts au démarrage
        self.load_loans()
    def add_loan_handler(self):
        book_id = self.entry_book_id.get().strip()
        borrower_name = self.entry_borrower_name.get().strip()
        borrow_date = self.entry_borrow_date.get().strip()
        return_date = self.entry_return_date.get().strip()
        
        if book_id and borrower_name and borrow_date:
            add_loan(book_id, borrower_name, borrow_date, return_date)
            messagebox.showinfo("Succès", "Emprunt ajouté avec succès!")
            self.clear_fields()
            self.load_loans()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir les champs obligatoires.")


    def return_book_handler(self):
        try:
            index = self.listbox.curselection()[0]
            loan_data = self.listbox.get(index).split(" | ")
            loan_id = int(loan_data[0])
            return_book(loan_id)
            messagebox.showinfo("Succès", "Livre retourné avec succès!")
            self.load_loans()
        except IndexError:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un emprunt à retourner.")

    def clear_fields(self):
        self.entry_book_id.set("")
        self.entry_borrower_name.set("")
        self.entry_borrow_date.set("")
        self.entry_return_date.set("")

    def load_loans(self):
        self.listbox.delete(0, END)
        loans = get_loans()
        for loan in loans:
            self.listbox.insert(END, f"{loan[0]} | {loan[1]} | {loan[2]} | {loan[3]} | {loan[4]}")

    def run(self):
        self.root.mainloop()

def add_loan(book_id, borrower_name, borrow_date, return_date):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO loans (book_id, borrower_name, borrow_date, return_date) VALUES (?, ?, ?, ?)",
        (book_id, borrower_name, borrow_date, return_date)
    )
    conn.commit()
    conn.close()


def return_book(loan_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE loans SET return_date = date('now') WHERE id = ?", (loan_id,))
    conn.commit()
    conn.close()


def get_loans():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, book_id, borrower_name, borrow_date, return_date FROM loans")
    loans = cursor.fetchall()
    conn.close()
    return loans



