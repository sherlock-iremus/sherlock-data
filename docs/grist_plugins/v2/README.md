
# Installation (FR)

Le tutoriel suivant explique comment créer une table d'indexation avec des concepts opentheso grâce au plugin. Si vous avez déjà une table d'indexation et souhaitez uniquement intégrer le plugin, commencer au point 3.

1. Se connecter sur grist -> "Nouveau" ->  "Ajouter table vide".
2. Cliquer sur la première colonne, ouvrir le panneau de création. "Type de colonne : Référence", choisir votre table indexée
3. "Nouveau" ->  "Ajouter une vue à la page" -> "Personnalisés" -> Sélectionner votre table d'indexation -> Ne pas oublier de sélectionner une option dans le menu déroulant "Select by".
4. Menu "Choisir un widget personnalisé", sélectionner l'option "Ajouter votre propre widget URL personnalisée", et remplir avec l'URL https://sherlock-iremus.github.io/sherlock-data/grist_plugins/v2/dist/index.html
5. "Le widget a besoin de full access à ce document."  -> "Accepter"
6. Créer une colonne `CONFIG_OPENTHESO`
7. Renommer et donner le nom "uuid" à la colonne qui contient votre ressource indexée.
8. Pour chacun des types d'indexation, créer deux colonnes : `<type_indexation>` et `<type_indexation_prefLabel>`. Exemple `technique_utilisee` et `technique_utilisee_prefLabel`, qui recevront des concepts d'un thesaurus des techniques de gravure. 

⚠️ Chaque colonne ajoutée **après** installation du plugin se sera pas visible par défaut par le plugin. Pour ce faire, cliquez sur la vue du plugin, dans le panneau de création onglet "Personnalisée" -> "Colonnes cachées".

⚠️ Vous pouvez cacher les colonnes de votre table d'indexation (comme `CONFIG_OPENTHESO` par exemple) en cliquant dessus, onglet "Table" -> "Colonnes visibles". Cela n'affectera pas le bon fonctionnement du plugin.


# Technical architecture

Main file is `src/handlers.ts`.

### `src/handlers.ts`

It contains handlers for :

- User DOM interactions
- Grist plugin events
- Opentheso API feedback

### `src/state.ts`

Global variables that should only be mutated in `src/handlers.ts`.

### `src/views/`

All DOM edition should be inside this folder.

### `src/controllers/`

Controllers are called by handlers and dispatch orders to views and api

### Good practices

We followed next rules in this plugin development, for data integrity :
 
- Every change of state is in `src/handlers.ts` file.
- DOM cannot be edited by something else than `src/views/` files.
- `src/views/` cannot be called by anything else than controllers
- `src/controllers/` cannot be called by anything else than handlers


# Plugin edition

`git clone https://github.com/sherlock-iremus/sherlock-data`

`cd sherlock-data/docs/grist_plugins/v2`

`npm run dev`

Do your modification

`npm run build`, then push on your github.

If your project is hosted on github and in the sub-folder `docs/`, the plugin should be accessible and integrable at the URL : `https://sherlock-iremus.github.io/sherlock-data/grist_plugins/v2/dist/index.html`