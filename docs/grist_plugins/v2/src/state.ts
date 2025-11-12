import { ConfigurationColumnData } from "./types/ConfigurationColumnData";
import { GristTable } from "./types/GristTable";
import { Thesaurus } from "./types/Thesaurus";

export let indexations: ConfigurationColumnData;
export let gristTable: GristTable;
export let thesauri: Thesaurus[];
export let currentThesaurus: Thesaurus;
export let conceptList: OpenthesoConcept[];

export const setIndexations = (newIndexations: ConfigurationColumnData) => {
    indexations = newIndexations;
} 

export const setGristTable = (table: GristTable) => {
    gristTable = table;
}

export const setThesauri = (newThesauri: Thesaurus[]) => {
    thesauri = newThesauri;
}

export const setcurrentThesaurus = (newThesaurus: Thesaurus) => {
    currentThesaurus = newThesaurus;
}

export const setConceptList = (newConceptList: OpenthesoConcept[]) => {
    conceptList = newConceptList;
}