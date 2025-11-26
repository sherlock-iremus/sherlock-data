import { columns } from "../state";
import { FormattedGristColumn } from "../types/FormattedGristColumn";
import { GristTablesColumns } from "../types/grist";
import { GristTable } from "../types/GristTable";
import { CONFIGURATION_COLUMN_NAME, LABEL_COLUMN_SUFFIX, RESOURCE_COLUMN_NAME } from "../utils/consts";
import { displayColumnsWithoutLabelMissing, displayConfigurationColumnMissing, displayConfigurationOK, displayResourceColumnMissing } from "../views/pluginConfigurationView";

/**
 * Plugin initialization, get all columns of the current table.
 * 
 * There is only one way to get current table LABELS.
 * It is to fetch the special _grist_Tables and _grist_Tables_column tables from the docApi,
 * and then to match the column parentId to the current table id.
 * 
 * @param gristTable grist table api object
 * @returns all columns of the current table with their id and label 
 */
export const fetchTableColumns = async (gristTable: GristTable): Promise<FormattedGristColumn[]> => {
    // All columns from your workspace
    const gristTableColumns = await grist.docApi.fetchTable("_grist_Tables_column")
    console.log("gristTableColumns : ", gristTableColumns)

    // All columns from current table
    const currentTableColumnsIds = await fetchCurrentTableColumnsFromDocApi(gristTable, gristTableColumns)
    console.log("currentTableColumnsIds : ", currentTableColumnsIds)

    // We also have to filter out columns that are not in the current table view, such as "sortBy, filterBy, etc."
    // We can do so since those columns are not included in from grist.fetchSelectedTable().
    const directlyFetchedTableColumns = Object.keys(await grist.fetchSelectedTable({ format: "columns" }));
    console.log("directlyFetchedTableColumns : ", directlyFetchedTableColumns)

    return currentTableColumnsIds
        .filter(idx => directlyFetchedTableColumns.includes(gristTableColumns.colId[idx]))
        .map(idx => ({ id: gristTableColumns.colId[idx], label: gristTableColumns.label[idx] }))
}

const fetchCurrentTableColumnsFromDocApi = async (gristTable: GristTable, gristTableColumns: GristTablesColumns) => {
    const technicalTableId = await gristTable.getTableId();
    console.log("technicalTableId : ", technicalTableId)

    const gristTables = await grist.docApi.fetchTable("_grist_Tables")
    const currentTableIndex = gristTables.tableId.indexOf(technicalTableId);
    const currentTableId = gristTables.id[currentTableIndex]
    console.log("gristTableId : ", currentTableId)


    const currentTableColumnsIds = [];

    let index = gristTableColumns.parentId.indexOf(currentTableId);
    while (index !== -1) {
        currentTableColumnsIds.push(index);
        index = gristTableColumns.parentId.indexOf(currentTableId, index + 1);
    }
    return currentTableColumnsIds;
}

export const displayErrorsIfAnyConfigurationColumnMissing = () => {
    const columnsMissingLabelDisplay = columns.filter(
        column => !column.id.endsWith(LABEL_COLUMN_SUFFIX) &&
            column.id !==CONFIGURATION_COLUMN_NAME &&
            column.id !== RESOURCE_COLUMN_NAME &&
            columns.filter(col => col.id === (column.id + LABEL_COLUMN_SUFFIX)).length === 0
    );

    if (!columns.map(col => col.id).includes(CONFIGURATION_COLUMN_NAME)) {
        console.warn("Configuration column is missing, this will cause issues.");
        displayConfigurationColumnMissing();
    } else if (!columns.map(col => col.id).includes(RESOURCE_COLUMN_NAME)) {
        console.warn("Resource URI column is missing, this will cause issues.");
        displayResourceColumnMissing();
    } else if (columnsMissingLabelDisplay.length) {
        console.warn("Some columns are missing their label display column, this will cause issues.", columnsMissingLabelDisplay);
        displayColumnsWithoutLabelMissing(columnsMissingLabelDisplay);
    } else {
        displayConfigurationOK();
    }
}