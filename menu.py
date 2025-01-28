from tkinter import Tk, Button, messagebox
from ui import LibraryApp  # Importer l'interface d'enregistrement des livres
from loan import LoanManagerApp  # Importer l'interface de gestion des emprunts

class MainMenu:
    def __init__(self):
        self.root = Tk()
        self.root.title("Menu Principal")
        self.root.geometry("400x300")

        # Ajouter les boutons pour les fonctionnalités
        self.button_books = Button(self.root, text="Enregistrer des livres", command=self.launch_books_interface)
        self.button_books.pack(pady=10)

        self.button_loans = Button(self.root, text="Gérer les emprunts", command=self.launch_loans_interface)
        self.button_loans.pack(pady=10)

    def launch_books_interface(self):
        """
        Lance directement l'interface pour enregistrer des livres.
        """
        try:
            app = LibraryApp()  # Instancie l'interface des livres
            app.run()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer l'interface des livres : {e}")

    def launch_loans_interface(self):
        """
        Lance directement l'interface pour gérer les emprunts.
        """
        try:
            app = LoanManagerApp()  # Instancie l'interface des emprunts
            app.run()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer l'interface des emprunts : {e}")

    def run(self):
        self.root.mainloop()





