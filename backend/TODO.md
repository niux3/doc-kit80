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
