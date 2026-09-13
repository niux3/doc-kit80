1. Prise en main (Getting Started)

    Introduction & Philosophie

        Raison d'être du projet et objectifs

        Choix techniques (Sémantique HTML5, CSS natif, zéro Virtual DOM)

    Installation & Prérequis

        Environnement requis (Node.js/runtime, gestionnaire de paquets)

        Démarrage rapide (Quickstart)

        Structure globale du projet

    Configuration

        Fichiers de configuration (.env, config applicative)

        Variables d'environnement et options par défaut

2. Architecture & Concepts Clés

    Arborescence & Organisation

        Rôle des répertoires (/src, /components, /routes, etc.)

        Conventions de nommage et organisation des fichiers

    Routage & Cycle de vie

        Fonctionnement du routeur (client/serveur)

        Hooks de cycle de vie (beforeLoad, beforeRender, afterRender)

    Gestion de l'état (State Management)

        Propagation du contexte

        Communication entre vues et composants

3. UI & Web Components

    Composants d'interface

        ui-selector (Menu déroulant accessible)

        ui-toggle (Basculeur de thème / état)

    Thématisation & CSS

        Variables CSS (:root, [data-theme="light"], [data-theme="dark"])

        Layouts réutilisables (Grid, Flexbox, Sticky elements)

        Accessibilité (ARIA, WCAG, sr-only)

4. Guide d'API & Intégration

    Services & Requêtes

        Gestion des appels API / Endpoints REST

        Traitement et validation des données (entrées/sorties)

    Gestion des erreurs

        Interception des erreurs réseau et de rendu

        Fallbacks et pages d'erreur (404, 500)

5. Déploiement & Tooling

    Build & Optimisation

        Minification et bundling

        Bonnes pratiques de performance (Core Web Vitals)

    Déploiement

        Hébergement et intégration continue (CI/CD)

        Modèles de configuration serveur (Nginx, Caddy, etc.)

1. Le contrat HTTP (Tests d'intégration des endpoints)

À l'aide du TestClient de FastAPI (basé sur httpx), on valide le comportement global de l'API de bout en bout :

    Codes HTTP de retour : Vérifier qu'un POST renvoie bien 201 Created, une suppression réussie 204 No Content, ou une ressource inexistante 404 Not Found.

    Validation Pydantic : S'assurer qu'un payload invalide envoyé sur un POST ou PUT renvoie immédiatement une erreur 422 Unprocessable Entity.

    Structure des réponses : Vérifier que le JSON renvoyé par un GET ou POST correspond exactement au schéma de lecture (ReadSchema).

2. La logique du service BDD (SQLModelCRUD)

On teste directement l'instance de SQLModelCRUD sans passer par la couche HTTP pour vérifier les opérations en base :

    Opérations CRUD de base : Insertion, lecture par ID, mise à jour partielle (exclude_unset=True), et suppression effective.

    Effets de bord BDD : Vérifier la persistence effective des données en base après un commit.

    Gestion des erreurs : S'assurer que le service renvoie None (ou lève l'exception attendue) lorsqu'on cherche ou modifie un identifiant inexistant.

3. Les requêtes et méthodes sur-mesure

Pour les entités complexes comme Post ou Category qui étendent le CRUD de base :

    Chargement des relations : S'assurer que les méthodes personnalisées (ex: get_with_categories ou get_with_posts) chargent correctement les sous-ressources associées via les stratégies de chargement de SQLModel (selectinload).

    Filtres ou requêtes spécifiques : Valider la logique de requête propre aux modèles de domaine.

4. L'isolation de l'environnement de test

Avant d'écrire le moindre test, la priorité absolue est la mise en place de la stratégie d'isolation via les fixtures pytest :

    Base de données de test éphémère : Utiliser une base dédiée (ou SQLite :memory: / Postgres de test) recréée à zéro avant la suite de tests pour isoler le dev de la BDD de test.

    Transaction Rollback / Teardown : S'assurer que chaque test s'exécute dans un état propre et remet la base à zéro pour ne pas impacter les tests suivants.

    Surcharge de dépendance (dependency_overrides) : Remplacer le generator db.get_session de FastAPI par une session pointant vers la base de test.
