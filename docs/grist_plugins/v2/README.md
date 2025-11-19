# General architecture

There are 3 mains folders : 

- `api/` for interactions with grist plugin API and opentheso API 
- `controller/`, handling events for grist plugin events or user DOM interaction events, and then dispaching to other functions.
- `views/`, all DOM edition should be inside this folder.

Also be careful, we do not use any JS high level library, so the state management is only controlled by `state.ts` 

Plugin initialization is done in `index.ts` file 

To make sure data integrity is secured, we restrained every change of state to handlers.ts file.

DOM cannot be edited by something else than views/ files.
views/ files' methods cannot be called by anything else than controllers.
controllers cannot be called by anything else than handlers.

TODO mercredi 26 : 
re-tester avec les changements d'archi
réécrire ce fichier readme en explicitant bien l'encapsulation de state.ts
