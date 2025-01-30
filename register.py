import sqlite3
import bcrypt
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from database import connect

class RegisterUser:
    def __init__(self):
        self.root = Tk()
        self.root.title("Enregistrement Utilisateur")
        self.root.geometry("400x250")
        
        self.username_var = StringVar()
        self.password_var = StringVar()
        
        Label(self.root, text="Nom d'utilisateur:").pack(pady=5)
        self.entry_username = Entry(self.root, textvariable=self.username_var)
        self.entry_username.pack(pady=5)
        
        Label(self.root, text="Mot de passe:").pack(pady=5)
        self.entry_password = Entry(self.root, textvariable=self.password_var, show="*")
        self.entry_password.pack(pady=5)
        
        Button(self.root, text="S'enregistrer", command=self.register_user).pack(pady=20)
    
    def register_user(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Erreur", "Tous les champs sont obligatoires")
            return
        
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Utilisateur enregistré avec succès")
            self.clear_fields()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Ce nom d'utilisateur est déjà utilisé")
    
    def clear_fields(self):
        if self.entry_username.winfo_exists():
            self.entry_username.delete(0, "end")
        if self.entry_password.winfo_exists():
            self.entry_password.delete(0, "end")

    
    def run(self):
        self.root.mainloop()

