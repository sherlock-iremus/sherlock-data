import { ConfigurationColumnData } from "./types/ConfigurationoColumnData";
import { GristTable } from "./types/GristTable";

export let indexations: ConfigurationColumnData;
export let gristTable: GristTable;

export const setIndexations = (newIndexations: ConfigurationColumnData) => {
    indexations = newIndexations;
} 

export const setGristTable = (table: GristTable) => {
    gristTable = table;
}