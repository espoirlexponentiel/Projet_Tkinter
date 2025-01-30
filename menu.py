from tkinter import Tk, Button, messagebox
from ui import LibraryApp
from loan import LoanManagerApp
from register import RegisterUser
from database import connect

def get_user_role(username):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
    return result[0] if result else "user"

class MainMenu:
    def __init__(self, username, role):
        self.root = Tk()
        self.root.title("Menu Principal")
        self.root.geometry("400x300")

        self.username = username
        self.role = role

        Button(self.root, text="Enregistrer des livres", command=self.launch_books_interface).pack(pady=10)
        Button(self.root, text="Gérer les emprunts", command=self.launch_loans_interface).pack(pady=10)
        
        if self.role == "admin":
            Button(self.root, text="Enregistrer un utilisateur", command=self.launch_register_interface).pack(pady=10)

    def launch_books_interface(self):
        try:
            app = LibraryApp()
            app.run()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer l'interface des livres : {e}")

    def launch_loans_interface(self):
        try:
            app = LoanManagerApp()
            app.run()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer l'interface des emprunts : {e}")

    def launch_register_interface(self):
        try:
            RegisterUser()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer l'interface d'enregistrement : {e}")

    def run(self):
        self.root.mainloop()




