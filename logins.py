import sqlite3
import bcrypt
from tkinter import Tk, Label, Button, Entry, messagebox, StringVar, Frame
import tkinter.font as font


# Fonction pour authentifier l'utilisateur
def authenticate_user(username, password):
    
    try:
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password, role FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()  # Récupère l'utilisateur correspondant au nom d'utilisateur
            print(f"Utilisateur trouvé dans la base : {user}")
            if user:
                user_id, hashed_password, role = user
                # Vérifie le mot de passe
                if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
                    return user_id, role
                else:
                    print("Mot de passe incorrect.")  # Debug
            else:
                print(f"Utilisateur '{username}' non trouvé.")  # Debug
    except sqlite3.Error as e:
        print(f"Erreur de base de données : {e}")
    return None


# Fonction pour créer un utilisateur (avec hachage de mot de passe)
def create_user(username, password, role="user"):
    
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    try:
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed_password.decode("utf-8"), role),
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de l'utilisateur : {e}")

    
# Fonction pour créer un administrateur par défaut si aucun utilisateur n'existe
def setup_default_admin():
   
    try:
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                create_user("admin", "admin123", "admin")
    except sqlite3.Error as e:
        print(f"Erreur lors de la configuration de l'administrateur : {e}")


# Classe pour l'écran de login
class LoginApp:
    def __init__(self, callback):
        self.root = Tk()
        self.root.title("Connexion")
        self.root.geometry("400x300")  # Taille de la fenêtre
        self.root.resizable(False, False)  # Empêche le redimensionnement

        # Variables
        self.username_var = StringVar()
        self.password_var = StringVar()

        # Polices
        self.label_font = font.Font(family="Arial", size=14)
        self.entry_font = font.Font(family="Arial", size=12)

        self.callback = callback  # Fonction à exécuter après login

        self.create_login_ui()

    def create_login_ui(self):
        """
        Crée l'interface utilisateur pour le login.
        """
        Label(self.root, text="Nom d'utilisateur", font=self.label_font).pack(pady=10)
        self.entry_username = Entry(self.root, font=self.entry_font, textvariable=self.username_var)
        self.entry_username.pack(pady=10)

        Label(self.root, text="Mot de passe", font=self.label_font).pack(pady=10)
        self.entry_password = Entry(self.root, font=self.entry_font, show="*", textvariable=self.password_var)
        self.entry_password.pack(pady=10)

        Button(self.root, text="Se connecter", font=self.label_font, command=self.login).pack(pady=20)

    def login(self):
        """
        Gère le processus de connexion.
        """
        username = self.username_var.get()
        password = self.password_var.get()

        # Appelle authenticate_user pour vérifier les informations de connexion
        user = authenticate_user(username, password)

        if user:
            user_id, role = user
            messagebox.showinfo("Connexion réussie", f"Bienvenue, {username}!")
            self.callback(role)  # Passe le rôle au callback
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

    def run(self):
        self.root.mainloop()

