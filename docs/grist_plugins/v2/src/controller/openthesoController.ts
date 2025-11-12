import { fetchThesauri, searchConcepts } from "../api/opentheso";
import { conceptList, currentThesaurus, setConceptList, setcurrentThesaurus, setThesauri, thesauri } from "../state";
import { Thesaurus } from "../types/Thesaurus";
import { displayError, displayLoading, displayResults } from "../views/thesaurusSearchConceptsView";
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
        setConceptList(await searchConcepts(currentThesaurus.idTheso, query));
        displayResults(conceptList);
    } catch (e) {
        let error
        if (currentThesaurus && currentThesaurus.idTheso) {
            error = "Erreur lors de la recherche dans le thésaurus."
            console.error(error, currentThesaurus.idTheso, e);
        } else {
            error = "Veuillez d'abord sélectionner un thésaurus."
            console.error(error);
        }
        displayError(error)
    }
}
