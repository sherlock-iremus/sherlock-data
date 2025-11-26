/**
 * All handlers are centralized here. 
 * Each handler calls the appropriate controller function.
 * 
 * The handler is the only part of the code that has access to the state.
 * The handler is the only part of the code that has access to the controllers
 */

import { displayErrorsIfAnyConfigurationColumnMissing, fetchTableColumns } from "./controller/gristController";
import { addConceptToColumn, removeConceptFromColumn, renderSelectedRecord } from "./controller/recordController";
import { initializeAndFetchThesauri, renderSearchResults, renderSelectedThesaurus, renderThesauriList, searchConcepts } from "./controller/thesaurusController";
import { gristTable, setColumns, setConceptList, setCurrentRecord, setcurrentThesaurus, setGristTable, setIndexations, setThesauri } from "./state";
import { GristRecord } from "./types/GristRecord";
import { OpenthesoConcept } from "./types/OpenthesoConcept";
import { Thesaurus } from "./types/Thesaurus";

export const handleNewRecord = (record: GristRecord) => {
    console.log("New record selected:", record);
    setCurrentRecord(record);
    setIndexations(record && record.CONFIG_OPENTHESO ? JSON.parse(record.CONFIG_OPENTHESO) : {});
    renderSelectedRecord();
}

export const handleDeleteIndexationButtonClick = (uri_concept: string, colId: string) => {
    console.log("Removing concept from column:", uri_concept, colId);
    removeConceptFromColumn(uri_concept, colId);
}

export const handleSelectOptionChange = (conceptId: string, label: string, selectedCol: string) => {
    if (!selectedCol) {
        alert("Veuillez sélectionner une colonne.");
        return;
    }

    console.log("Add concept to column", selectedCol, conceptId, label);
    addConceptToColumn(conceptId, label, selectedCol);
}

export const handlePluginInitialization = async () => {
    initializeAndFetchThesauri();
    
    grist.ready({ requiredAccess: "full" });
    setGristTable(await grist.getTable());
    setColumns(await fetchTableColumns(gristTable))
    displayErrorsIfAnyConfigurationColumnMissing();
    
    grist.onRecord((record: GristRecord) => {
        handleNewRecord(record);
    });
}

export const handleThesaurusClick = (thesaurus: Thesaurus) => {
    console.log("Thesaurus selected:", thesaurus);
    setcurrentThesaurus(thesaurus);
    renderSelectedThesaurus();
}

export const handleSearchButtonClick = (query: string) => {
    console.log("Searching concepts with query:", query);
    searchConcepts(query);
}

export const handleSearchInputKeydown = (e: KeyboardEvent, query: string) => {
    console.log("Searching concepts with query:", query);
    if (e.key === "Enter") searchConcepts(query);
}

export const handleThesauriFetched = (fetchedThesauri: Thesaurus[]) => {
    console.log("Thesauri fetched:", fetchedThesauri);
    setThesauri(fetchedThesauri);
    renderThesauriList();
}

export const handleSearchConceptsFetched = (concepts: OpenthesoConcept[]) => {
    console.log("Concepts fetched with search:", concepts);
    setConceptList(concepts);
    renderSearchResults();
}