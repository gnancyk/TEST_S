# Explication Technique Détaillée du Code Frontend

Ce document décrit comment le code de ton projet Vue.js s'exécute, fichier par fichier et concept par concept, pour te permettre de bien comprendre son architecture globale et le fonctionnement de son outil principal.

---

## 1. L'Initialisation de l'Application Vue

Tout commence quand le navigateur ouvre ton site. C'est le point de départ classique d'une application Vue 3.

### [src/main.js](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/main.js)
C'est le chef d'orchestre au démarrage.
*   **Lignes 1 à 5** : Il importe le CSS principal (les styles Tailwind) et les outils de Vue (`createApp`), ainsi que le `router` (qui s'occupe de la navigation).
*   **Lignes 7 à 13** : Il demande beaucoup d'icônes à *FontAwesome* (pour tes boutons et menus) et les installe globalement dans le projet.
*   **Lignes 15 à 19** : Il construit l'application et "branche" le tout dans la balise HTML identifiée par `id="app"` (qui se trouve dans le fichier caché [index.html](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/index.html) à la racine de ton projet).

### [src/App.vue](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/App.vue)
C'est le composant racine, le tout premier bloc visuel qui s'affiche à l'écran. 
*   **Lignes 26-29** : Dans la balise `<style>`, il importe les styles d'interface de **Flowbite**, une bibliothèque qui donne un joli style aux éléments HTML de Tailwind.
*   **Ligne 8** : Ton fichier est volontairement épuré. Il ne contient rien d'autre que l'appel à `<Layout/>`. Cela veut dire que toute ton application se passera en réalité à l'intérieur du composant Layout.

---

## 2. L'Interface Générale et la Navigation

Pour que l'utilisateur puisse naviguer sans jamais recharger la page, on utilise un routeur et une enveloppe (le Layout).

### [src/components/layouts/Layout.vue](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/components/layouts/Layout.vue)
C'est la charpente de ton site.
*   **Lignes 15 à 56 (`<aside>`)** : C'est le menu latéral gauche (Sidebar) au fond orange (`bg-orange-400`). Il contient les liens (balises `<RouterLink>`) pour aller vers la page "Accueil" ou "Outils".
*   **Lignes 58 à 60 (`div.sm:ml-64`)** : Juste à droite du menu latéral se trouve l'espace principal de l'écran. La balise spéciale `<RouterView />` est comme un écran blanc dynamique : c'est là que le routeur viendra injecter les vraies pages (Accueil, Checklist, etc.) en fonction des clics de l'utilisateur.

### [src/router/index.js](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/router/index.js)
C'est le fichier du "facteur". Il décide quelle page charger dans le fameux `<RouterView/>`.
*   Si l'URL est `/`, il demande d'afficher le fichier [HomeView.vue](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/HomeView.vue).
*   Si l'URL est `/tools`, il demande le fichier [ToolsView.vue](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/ToolsView.vue).
*   Si l'URL est `/tools/checklist`, il donne [ChecklistView.vue](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/tools/ChecklistView.vue).

---

## 3. Les Vues Métier et le Tableau de Bord

### [src/views/ToolsView.vue](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/ToolsView.vue)
C'est simplement un catalogue visuel.
Tu as organisé cette page avec des grilles et des "cartes" descriptives. La majorité des cartes étant commentées (voir l'analyse précédente), la seule carte visible est celle expliquant à quoi sert l'outil "Checklist", avec un bouton ("Accéder à l'outil") qui dirige l'utilisateur vers son propre `/tools/checklist`.

### [src/views/tools/ChecklistView.vue](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/tools/ChecklistView.vue) (L'Intelligence Artificielle de la page)
C'est le cerveau visuel de ton application d'audit, et de très loin le composant le plus lourd (près de 1900 lignes). Voici comment il se lit.

#### A. La Logique Javascript (`<script>`)
*   **[data()](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/tools/ChecklistView.vue#5-51) (Lignes 5 à 49)** : C'est la mémoire de la page.
    *   Le composant liste ici toutes les variables dont il aura besoin pour mettre à jour l'écran : un tableau pour les `organisations`, des compteurs pour savoir où en est le chargement (`check_param`, [check_crm](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/backend/run.py#434-454)), et surtout l'objet `serveurs: { frontend: {...}, bd: {...} }` qui stockera si les serveurs sont cassés ou non.
*   **[mounted()](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/tools/ChecklistView.vue#51-54) (Lignes 51-53)** : Événement spécial déclenché dès que la page s'allume. Il appelle immédiatement la fonction [getOrganisations()](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/tools/ChecklistView.vue#63-74) pour aller demander discrètement au Backend la liste des organisations et remplir la liste déroulante `<select>` (afin que l'utilisateur ait directement les choix sous les yeux).
*   **[onOrganisationChange()](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/tools/ChecklistView.vue#76-132) (Lignes 76 à 131)** : C'est cette fonction qui se déclenche quand tu cliques sur une organisation dans la liste déroulante.
    *   Elle commence par passer **la totalité** des variables de [data()](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/tools/ChecklistView.vue#5-51) à "vide" ou "false". Pourquoi ? Pour s'assurer de nettoyer les anciens résultats de l'écran si tu fais deux audits différents de suite.
    *   Ensuite, elle passe le relais à l'imposante fonction [fetchOrganisationDetails(id)](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/tools/ChecklistView.vue#133-365).

#### B. La Grande Vague d'Audit ([fetchOrganisationDetails](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/tools/ChecklistView.vue#133-365) - Lignes 133 à 364)
Le principe est simple : on met la ligne sur pause (`await`) à chaque étape pour envoyer une requête au backend (API Python), puis on enregistre son résultat pour modifier ce qui sera affiché.
*   **Étape 1 (`/organisation/{id}`, l. 137)** : Il récupère depuis le Python les logins et les mots de passe de l'architecture.
*   **Étape 2 (`/verification/serveur`, l. 154)** : Il demande l'état des serveurs, récupère le JSON du backend, et trouve le statut de chaque rôle (ex: l. 165 `this.serveurs.backend.etat = ...etat`) en regardant dans le JSON renvoyé.
*   **Étape 3 et +, l. 201 à l. 353 : L'Avalanche de vérifications**
    *   Il demande au backend l'état de l'instance de SQL Serveur (`/disponibilite/serveur-sql`).
    *   Il teste l'URL web du CRM Dynamics (`/disponibilite/frontend-crm`).
    *   Il liste les "catalogues" de bases de données et isole uniquement ceux contenant "*_mscrm*".
    *   Il envoie ces catalogues pour vérifier les procédures stockées ou la justesse des numéros "OrganisationID" via des requêtes [fetch](file:///c:/Users/USER/OneDrive/Documents/test_api/TEST_S-main/SaphirV3.ToolsSupport/frontend/src/views/tools/ChecklistView.vue#133-365).

#### C. L'Affichage Visuel (`<template>` - Lignes 369 et suivantes)
Le rôle du template est de venir "écouter" (lire) les variables HTML qu'on a mises à jour dans le bloc JS ci-dessus.
*   **Le Menu Déroulant (L. 380)** : `<select v-model="selectedOrganisation" @change="onOrganisationChange">`. La directive `@change` branche littéralement ce menu au clic Javascript.
*   **Le Gâteau Surprise (L. 430)** : `v-if="result_section && show_result"` 
    *   Cette directive magique de Vue.js fait en sorte que toute l'interface grise et blanche du bas avec les gros tableaux reste totalement **cachée** tant que le chargement complet des vérifications n'est pas terminé (le Javascript passe `show_result` à `true` tout à la fin de la fonction d'audit à la ligne 359 !).
*   **Les Lignes de Résultat (L. 529)** : À l'intérieur du grand tableau, tu as une petite pastille de couleur pour l'état du serveur Frontend :
    ```html
    <span class="status-indicator status-up" v-if="serveurs.frontend.etat == 'En ligne'"></span>
    <span class="status-indicator status-warning" v-if="serveurs.frontend.etat != 'En ligne'"></span>
    ```
    *C'est la magie de la "Réactivité" :* la condition `v-if` fait que la pastille Verte s'affiche, et que la pastille de danger s'efface si la variable contient bien le bout de texte `'En ligne'` renvoyé par le backend !
