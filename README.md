```                                                                                                                                                              
 ____                                      ____                                                
/\  _`\                                   /\  _`\                                              
\ \ \L\_\   _ __    __      __     ___    \ \ \L\_\    ____    ___      __     _____      __   
 \ \ \L_L  /\`'__\/'__`\  /'__`\ /' _ `\   \ \  _\L   /',__\  /'___\  /'__`\  /\ '__`\  /'__`\ 
  \ \ \/, \\ \ \//\  __/ /\  __/ /\ \/\ \   \ \ \L\ \/\__, `\/\ \__/ /\ \L\.\_\ \ \L\ \/\  __/ 
   \ \____/ \ \_\\ \____\\ \____\\ \_\ \_\   \ \____/\/\____/\ \____\\ \__/.\_\\ \ ,__/\ \____\
    \/___/   \/_/ \/____/ \/____/ \/_/\/_/    \/___/  \/___/  \/____/ \/__/\/_/ \ \ \/  \/____/
                                                                                 \ \_\         
                                                                                  \/_/         
```                                                                                                                                                        
**Green Escape** est une application web gamifiée et éco-responsable dans laquelle l'utilisateur doit résoudre un labyrinthe le plus rapidement possible.  
S’il réussit à battre les différents algorithmes de recherche de chemins, l'utilisateur aura une medaille et son score affiché dans le leaderboard général.  

---

## 🎯 Objectif

Créer un jeu web où l’utilisateur affronte un algorithme de type **A\***, **Dijkstra** ou encore **BFS** dans un labyrinthe généré par seed.

## 🧑‍💻 Stack technique

### 🔹 Front-end
- HTML / CSS / JavaScript

### 🔹 Back-end
- Django (Python)
- MongoDB (NoSQL)

---

## **🚀 Lancer le projet 🚀**

### <ins>💻 En ligne :</ins>  https://green-escape.onrender.com/api/login-page/

### <ins>💾 En local :</ins>

 💡Prérequis :
 - Connexion internet
 - Python 3.8 ou supérieur
 - Pip 



** 🤖 Cloner le projet : **
    - git clone https://github.com/votre-utilisateur/green-escape.git
    - cd green-escape/backend/GreenEscape-backend
    
    - python -m venv env
    - Set-ExecutionPolicy Unrestricted -Scope Process
    - env\Scripts\Activate

    - pip install django==3.2
    - pip install djongo==1.3.6
    - pip install pymongo==3.12.0
    - pip install sqlparse==0.2.4
    - pip install django-cors-headers==3.13.0
    - pip install djangorestframework
    - pip install pymongo[srv]
    - pip install setuptools
    - pip install legacy-cgi
    
    - python manage.py runserver
    - Cliquez sur l'addresse http://-.-.-.-:----/

---

## 🤝Contribuer au projet 🤝

- Messages de commit clairs : Description du changement(type)
types possibles : doc, feature, fix, test

git checkout -b votre_branche
git add .
git commit -m "Description du changement(type)"
git push origin votre_branche
Nous nous occupons des pull request

---

## 📝Description des fonctionnalités
1. Utilisateurs
- Inscription, connexion et déconnexion.
- Modification du profil utilisateur.
- Affichage des statistiques personnelles (médailles, parties jouées).
2. Jeu
- Génération dynamique de labyrinthes basés sur une seed aléatoire.
- Résolution des labyrinthes avec différents algorithmes (A*, Dijkstra, BFS).
3. Classements et scores
- Classement global des joueurs basé sur les médailles.
- Enregistrement des meilleurs temps par seed.

---

## 📚Historique des contributions
Nom	            Contributions
Hugo        	Déploiement du projet et de la BDD et gestion de cette dernière
Victor  	    Partie algorithmique du labyrinthe et session de jeu
Mathieu     	Analyse de l'empreinte carbone et de l'impact écologique du site
Roland      	Interfaces utilisateurs et implémentations de la communication Joueur-BDD