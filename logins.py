import sqlite3
from database import connect
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, font
import bcrypt
from menu import MainMenu

def create_user(username, password, role="user"):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    try:
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed_password.decode("utf-8"), role),
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de l'utilisateur : {e}")

def setup_default_admin():
    try:
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                create_user("admin", "admin123", "admin")
    except sqlite3.Error as e:
        print(f"Erreur lors de la configuration de l'administrateur : {e}")

class LoginApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Connexion à la bibliothèque")
        self.root.geometry("400x300")

        self.username_var = StringVar()
        self.password_var = StringVar()

        self.label_font = font.Font(family="Arial", size=14)
        self.entry_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=12, weight="bold")

        self.create_login_ui()

    def create_login_ui(self):
        Label(self.root, text="Nom d'utilisateur :", font=self.label_font).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_username = Entry(self.root, font=self.entry_font, textvariable=self.username_var)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        Label(self.root, text="Mot de passe :", font=self.label_font).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_password = Entry(self.root, font=self.entry_font, show="*", textvariable=self.password_var)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        Button(self.root, text="Se connecter", font=self.button_font, command=self.login_handler).grid(row=2, column=0, columnspan=2, pady=20)
    
    def login_handler(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        
        if username and password:
            try:
                with connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
                    result = cursor.fetchone()
                    
                    if result:
                        stored_hashed_password, role = result
                        if bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password.encode("utf-8")):
                            messagebox.showinfo("Succès", f"Connexion réussie! Rôle : {role}")
                            self.root.destroy()
                            MainMenu(username, role).run()
                        else:
                            messagebox.showwarning("Erreur", "Mot de passe incorrect.")
                    else:
                        messagebox.showwarning("Erreur", "Nom d'utilisateur non trouvé.")
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", f"Problème avec la base de données : {e}")
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

    def run(self):
        self.root.mainloop()



