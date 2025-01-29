from database import create_tables, show_tables
from logins import setup_default_admin # Importation de la fonction depuis logins
from logins import LoginApp  # Importation du menu principal

if __name__ == "__main__":
    # Créer les tables si elles n'existent pas
    create_tables()

    # Affiche les tables existantes (pour vérification)
    show_tables()

    # Créer un administrateur par défaut si aucun utilisateur n'existe
    setup_default_admin()  # Appel de la fonction setup_default_admin() depuis logins.py

    # Lance le menu principal, qui va ensuite gérer les actions de connexion
    app = LoginApp()  
    app.run()  # Démarre le menu principal



