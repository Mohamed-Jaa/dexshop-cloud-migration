# DexShop - Système de Gestion E-Commerce & Données

## Description du Projet
DexShop est une application web dynamique Full-Stack développée en utilisant Python et le micro-framework Flask. Initialement conçu comme un projet web statique, il a été étendu en une plateforme e-commerce entièrement fonctionnelle pour démontrer la maîtrise de l'intégration Backend, la gestion des sessions et le rendu dynamique des données.

L'application simule une boutique de matériel informatique haute performance, permettant aux utilisateurs de parcourir les produits, de consulter des spécifications détaillées et de simuler des commandes via une interface réactive. Elle inclut une zone d'administration restreinte pour la gestion des données.

## Architecture Technique

### Backend
- **Langage :** Python 3
- **Framework :** Flask
- **Sécurité :** Werkzeug (pour le hachage des mots de passe), Flask-Session (pour la gestion d'état)
- **Stockage des Données :** Couche de persistance basée sur des fichiers JSON (simulant une structure de base de données NoSQL)

### Frontend
- **Moteur de Template :** Jinja2 (Rendu côté serveur)
- **Style :** CSS3 Personnalisé (Thème Sombre Moderne, Mise en page Grid Responsive)
- **Interactivité :** JavaScript Vanilla (Manipulation DOM pour le Checkout Latéral, Navbar Fixe, Effets de Défilement)

## Fonctionnalités Clés

### Interface Utilisateur Publique
1.  **Catalogue Dynamique :** Affichage des produits depuis la base de données JSON avec une logique de pagination côté serveur.
2.  **Détails du Produit :** Page dédiée pour chaque article affichant les spécifications techniques et des produits similaires.
3.  **Achat Interactif :** Système de caisse latéral (Sidebar Checkout) alimenté par JavaScript qui valide l'état de connexion de l'utilisateur avant la soumission de la commande.
4.  **Design Responsive :** Mise en page optimisée pour les ordinateurs de bureau et les appareils mobiles.

### Administration & Sécurité
1.  **Système d'Authentification :** Système sécurisé d'Inscription/Connexion/Déconnexion utilisant des mots de passe hachés.
2.  **Protection des Routes :** Implémentation de décorateurs Python personnalisés (`@login_required`) pour restreindre l'accès aux routes administratives.
3.  **Tableau de Bord Admin :** Interface protégée pour la gestion des opérations du magasin.

## Installation et Configuration

Pour exécuter ce projet localement, suivez ces étapes :

1.  **Cloner le dépôt :**
    ```bash
    git clone <url_du_dépôt>
    cd <dossier_du_projet>
    ```

2.  **Créer un environnement virtuel (Recommandé) :**
    ```bash
    python -m venv venv
    # Windows :
    venv\Scripts\activate
    # macOS/Linux :
    source venv/bin/activate
    ```

3.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Lancer l'application :**
    ```bash
    python app.py
    ```

5.  **Accéder à l'application :**
    Ouvrez un navigateur web et naviguez vers : http://127.0.0.1:5000/

## Déploiement

L'application est configurée pour le déploiement sur des plateformes PaaS comme Render. Elle inclut :
- `Procfile` pour la configuration de Gunicorn.
- Support des variables d'environnement pour les données sensibles (SECRET_KEY).

**Note sur la Persistance :** En raison du système de fichiers éphémère des offres d'hébergement gratuites (comme Render), les modifications apportées aux fichiers de données JSON (par exemple, les nouvelles inscriptions) peuvent être réinitialisées après le redémarrage du serveur. Pour un environnement de production, une migration vers une base de données persistante (MongoDB/PostgreSQL) est recommandée.

## Identifiants d'Accès (Pour le Test)

Pour accéder au **Tableau de Bord (Dashboard)** et tester les restrictions d'achat, utilisez le compte Administrateur suivant :

- **Email :** mohamed.cyber@hotmail
- **Mot de passe :** default_password

---

**Auteur :** Mohamed Jaa
**Institution :** Faculté des Sciences Semlalia (FSSM) - Marrakech
**Département :** Informatique