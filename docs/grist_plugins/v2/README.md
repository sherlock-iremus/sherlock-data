# General architecture

There are 3 mains folders : 

- `api/` for interactions with grist plugin API and opentheso API 
- `controller/`, handling events for grist plugin events or user DOM interaction events, and then dispaching to other functions.
- `views/`, all DOM edition should be inside this folder.

Also be careful, we do not use any JS high level library, so the state management is only controlled by `state.ts` 

Plugin initialization is done in `index.ts` file 