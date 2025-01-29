from tkinter import Tk, Label, Button, Entry, messagebox, StringVar, Listbox, Scrollbar, Spinbox, Toplevel, font, END, Frame
import sqlite3
import tkinter.font as font
from database import connect
from datetime import datetime


class LoanManagerApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Gestion des emprunts de livres")
        self.root.geometry("1100x800")

        # Cadre principal pour centrer les widgets
        self.main_frame = Frame(self.root)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Variables
        self.book_id_var = StringVar()
        self.borrower_name_var = StringVar()
        self.borrow_date_var = StringVar()
        self.return_date_var = StringVar()
        self.quantity_var = StringVar()
        self.return_quantity_var = StringVar()

        # Polices
        self.label_font = font.Font(family="Arial", size=14)
        self.entry_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=12, weight="bold")

        self.create_loan_ui()

    def create_loan_ui(self):
        # Formulaire pour les emprunts
        Label(self.main_frame, text="ID du livre :", font=self.label_font).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_book_id = Entry(self.main_frame, font=self.entry_font, width=30)
        self.entry_book_id.grid(row=0, column=1, padx=10, pady=10)

        Label(self.main_frame, text="Nom de l'emprunteur :", font=self.label_font).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_borrower_name = Entry(self.main_frame, font=self.entry_font, width=30)
        self.entry_borrower_name.grid(row=1, column=1, padx=10, pady=10)

        Label(self.main_frame, text="Date d'emprunt (AAAA-MM-JJ) :", font=self.label_font).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_borrow_date = Entry(self.main_frame, font=self.entry_font, width=30)
        self.entry_borrow_date.grid(row=2, column=1, padx=10, pady=10)

        Label(self.main_frame, text="Date de retour (AAAA-MM-JJ) :", font=self.label_font).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_return_date = Entry(self.main_frame, font=self.entry_font, width=30)
        self.entry_return_date.grid(row=3, column=1, padx=10, pady=10)

        Label(self.main_frame, text="Quantité empruntée :", font=self.label_font).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_quantity = Entry(self.main_frame, font=self.entry_font, width=30)
        self.entry_quantity.grid(row=4, column=1, padx=10, pady=10)

        
        # Boutons alignés horizontalement
        self.button_frame = Frame(self.main_frame)
        self.button_frame.grid(row=5, column=0, columnspan=3, pady=20)

        Button(self.button_frame, text="Ajouter un emprunt", font=self.button_font, command=self.add_loan_handler).pack(
            side="left", padx=10
        )
        Button(self.button_frame, text="Retourner un livre", font=self.button_font, command=self.return_book_handler).pack(
            side="left", padx=10
        )

        # Liste des emprunts
        Label(self.main_frame, text="Liste des emprunts :", font=self.label_font).grid(row=6, column=0, columnspan=2, pady=10)
        self.scrollbar = Scrollbar(self.main_frame)
        self.scrollbar.grid(row=7, column=3, sticky="ns", padx=(0, 10))
        self.listbox = Listbox(
            self.main_frame, height=10, width=70, font=self.entry_font, yscrollcommand=self.scrollbar.set
        )
        self.listbox.grid(row=7, column=0, columnspan=3, pady=10)
        self.scrollbar.configure(command=self.listbox.yview)

        # Charger les emprunts au démarrage
        self.load_loans()

    def add_loan_handler(self):
        book_id = self.entry_book_id.get().strip()
        borrower_name = self.entry_borrower_name.get().strip()
        borrow_date = self.entry_borrow_date.get().strip()
        return_date = self.entry_return_date.get().strip()
        quantity_str = self.entry_quantity.get().strip()
        
        if book_id and borrower_name and borrow_date and quantity_str:
            try:
                quantity = int(quantity_str)
                available_quantity = get_book_quantity(book_id)
                if quantity > 0 and quantity <= available_quantity:
                    add_loan(book_id, borrower_name, borrow_date, return_date, quantity)
                    update_book_quantity(book_id, available_quantity - quantity)
                    messagebox.showinfo("Succès", "Emprunt ajouté avec succès!")
                    self.clear_fields()
                    self.load_loans()
                elif quantity > available_quantity:
                    messagebox.showwarning("Erreur", f"Quantité demandée ({quantity}) supérieure à la quantité disponible ({available_quantity}).")
                else:
                    messagebox.showwarning("Erreur", "La quantité doit être supérieure à 0.")
            except ValueError:
                messagebox.showwarning("Erreur", "Veuillez entrer une quantité valide.")
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir les champs obligatoires.")


    def return_book_handler(self):
        try:
            index = self.listbox.curselection()[0]
            loan_data = self.listbox.get(index).split(" | ")
            loan_id = int(loan_data[0])
            current_quantity = int(loan_data[5])

            def confirm_return():
                return_quantity = int(return_quantity_spinbox.get())
                if return_quantity > 0 and return_quantity <= current_quantity:
                    return_book(loan_id, return_quantity, current_quantity)
                    available_quantity = get_book_quantity(loan_data[1])
                    update_book_quantity(loan_data[1], available_quantity + return_quantity)
                    messagebox.showinfo("Succès", "Livre retourné avec succès!")
                    self.load_loans()
                    return_window.destroy()
                else:
                    messagebox.showwarning("Erreur", "Quantité à retourner invalide.")

            # Créer une nouvelle fenêtre pour sélectionner la quantité à retourner
            return_window = Toplevel(self.root)
            return_window.title("Retourner un livre")
            return_window.geometry("300x200")

            Label(return_window, text="Quantité à retourner :", font=self.label_font).pack(pady=10)
            return_quantity_spinbox = Spinbox(return_window, from_=1, to=current_quantity, font=self.entry_font)
            return_quantity_spinbox.pack(pady=10)

            Button(return_window, text="Confirmer", font=self.button_font, command=confirm_return).pack(pady=10)

        except IndexError:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un emprunt à retourner.")



    def clear_fields(self):
        self.entry_book_id.delete(0, END)
        self.entry_borrower_name.delete(0, END)
        self.entry_borrow_date.delete(0, END)
        self.entry_return_date.delete(0, END)
        self.entry_quantity.delete(0, END)
        #self.entry_return_quantity.delete(0, END)
        self.selected_id = None

    def load_loans(self):
        self.listbox.delete(0, END)
        loans = get_loans()
        for loan in loans:
            status = self.get_loan_status(loan[4], loan[5])
            self.listbox.insert(END, f"{loan[0]} | {loan[1]} | {loan[2]} | {loan[3]} | {loan[4]} | {loan[5]} | {status}")

    def get_loan_status(self, return_date, quantity):
        if quantity == 0:
            return "À jour"
        elif datetime.strptime(return_date, '%Y-%m-%d') < datetime.now():
            return "Retard"
        else:
            return "En cours"

    def run(self):
        self.root.mainloop()

def add_loan(book_id, borrower_name, borrow_date, return_date, quantity):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO loans (book_id, borrower_name, borrow_date, return_date, quantite) VALUES (?, ?, ?, ?, ?)",
        (book_id, borrower_name, borrow_date, return_date, quantity)
    )
    cursor.execute("UPDATE books SET quantite = quantite - ? WHERE id = ?", (quantity, book_id))
    conn.commit()
    conn.close()

def update_book_quantity(book_id, new_quantity):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET quantite = ? WHERE id = ?", (new_quantity, book_id))
    conn.commit()
    conn.close()

def get_book_quantity(book_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT quantite FROM books WHERE id = ?", (book_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0



def return_book(loan_id, return_quantity, current_quantity):
    conn = connect()
    cursor = conn.cursor()
    new_quantity = current_quantity - return_quantity
    if new_quantity > 0:
        cursor.execute("UPDATE loans SET quantite = ? WHERE id = ?", (new_quantity, loan_id))
    else:
        cursor.execute("UPDATE loans SET quantite = ?, return_date = date('now') WHERE id = ?", (0, loan_id))
    conn.commit()
    conn.close()

def get_loans():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, book_id, borrower_name, borrow_date, return_date, quantite FROM loans")
    loans = cursor.fetchall()
    conn.close()
    return loans





