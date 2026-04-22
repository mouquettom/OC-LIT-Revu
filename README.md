# LIT-Revu

Application web Django permettant de publier des demandes de critiques (billets), d’écrire des critiques en réponse, de suivre d’autres utilisateurs et de consulter un flux personnalisé.

## Fonctionnalités

- Inscription, connexion, déconnexion
- Création, modification et suppression de billets
- Création, modification et suppression de critiques
- Création d’un billet + critique en une seule étape
- Système d’abonnement entre utilisateurs
- Flux personnalisé
- Recherche/autocomplete d’utilisateurs

## Choix techniques

- Python
- Django
- SQLite
- HTML / CSS / JavaScript
- Git / GitHub

## Architecture du projet

```text
src/
    accounts/   # utilisateurs, authentification, abonnements
    tickets/    # billets [demandes de critiques]
    reviews/    # critiques + flux personnalisé
    templates/  # HTML
    static/     # CSS / JS
    LIT_Revu/   # settings — projet
    manage.py   # point d'entrée
    db.sqlite3  # base de données
    README.md   
```

## Installation locale

### 1. Cloner le projet
```bash
git clone https://github.com/mouquettom/OC-LIT-Revu.git
cd OC-LIT-Revu/src
```

### 2. Créer et activer un environnement virtuel
#### macOS / Linux
```bash
python3 -m venv .env
source .env/bin/activate
```

#### Windows PowerShell
```powershell
py -m venv .env
.env\Scripts\Activate.ps1
```

### 3. Installer les dépendances
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Créer les migrations et lancer le serveur
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Annexes

Le projet utilise un dossier `media/` pour stocker les images uploadées pour les billets.
Si le dossier n'existe pas déjà, il sera alors créé lorsque vous allez uploader votre 
première image lors de la création d'un billet. Si vous supprimez un billet contenant 
une image uploadée, l'image sera également supprimée de la base de données.

### Commande utile

Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

@tommouquet