import { fetchThesauri, getConceptLabels, searchConcepts } from "../api/opentheso";
import { currentRecord, currentThesaurus, setConceptList, setcurrentThesaurus, setThesauri, thesauri } from "../state";
import { getBroaderIdForConcept, OpenthesoConcept } from "../types/OpenthesoConcept";
import { Thesaurus } from "../types/Thesaurus";
import { displayError, displayLoading, displaySearchResults } from "../views/thesaurusSearchConceptsView";
import { closeSidebar, displaySelectedThesaurus, displayThesauri, initializeThesauriView, openSidebar, showThesauriLoadingError } from "../views/thesaurusSelectionView";

export const fetchAndDisplayThesauri = async () => {
    try {
        setThesauri(await fetchThesauri());
        initializeThesauriView();
        displayThesauri(thesauri);
    } catch (error) {
        showThesauriLoadingError();
        console.error(error);
    }
};

export const onThesaurusClick = (thesaurus: Thesaurus) => {
    setcurrentThesaurus(thesaurus);
    displaySelectedThesaurus(thesaurus);
    closeSidebar();
}

export const searchAndDisplayConcepts = async (query: string) => {
    if (!query.trim()) return;
    displayLoading()
    try {
        const concepts: OpenthesoConcept[] = await searchConcepts(currentThesaurus.idTheso, query);
        await Promise.all(concepts.map(async concept => {
            const broaderId = getBroaderIdForConcept(concept);
            if (broaderId) concept.broaderLabel = (await getConceptLabels(currentThesaurus.idTheso, broaderId)).label;
            return concept;
        }))

        setConceptList(concepts);
        displaySearchResults();
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
