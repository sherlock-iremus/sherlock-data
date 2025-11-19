import { fetchThesauri, getConceptLabels, searchConceptsInThesaurus } from "../api/opentheso";
import { handleSearchConceptsFetched, handleThesauriFetched } from "../handlers";
import { currentRecord, currentThesaurus, thesauri } from "../state";
import { getBroaderIdForConcept, OpenthesoConcept } from "../types/OpenthesoConcept";
import { displayError, displayLoading, displaySearchResults } from "../views/thesaurusSearchConceptsView";
import { closeSidebar, displaySelectedThesaurus, displayThesauri, initializeThesauriView, showThesauriLoadingError } from "../views/thesaurusSelectionView";

export const initializeAndFetchThesauri = async () => {
    try {
        initializeThesauriView();
        fetchThesauri().then(fetchedThesauri => handleThesauriFetched(fetchedThesauri));
    } catch (error) {
        showThesauriLoadingError();
        console.error(error);
    }
};

export const renderThesauriList = () => {
    displayThesauri(thesauri);
}

export const renderSelectedThesaurus = () => {
    displaySelectedThesaurus();
    closeSidebar();
}

export const searchConcepts = async (query: string) => {
    if (!query.trim()) return;
    displayLoading()
    try {
        const concepts: OpenthesoConcept[] = await searchConceptsInThesaurus(currentThesaurus.idTheso, query);
        await Promise.all(concepts.map(async concept => {
            const broaderId = getBroaderIdForConcept(concept);
            if (broaderId) concept.broaderLabel = (await getConceptLabels(currentThesaurus.idTheso, broaderId)).label;
            return concept;
        }))
        handleSearchConceptsFetched(concepts);
    } catch (e) {
        let error
        if (!currentRecord) {
            error = "Veuillez d'abord sélectionner une ressource."
            console.error(error, currentThesaurus.idTheso, e);
        }
        else if (currentThesaurus && currentThesaurus.idTheso) {
            error = "Erreur lors de la recherche dans le thésaurus."
            console.error(error, currentThesaurus.idTheso, e);
        } else {
            error = "Veuillez d'abord sélectionner un thésaurus."
            console.error(error);
        }
        displayError(error)
    }
}
        
export const renderSearchResults = () => {
    displaySearchResults();
}