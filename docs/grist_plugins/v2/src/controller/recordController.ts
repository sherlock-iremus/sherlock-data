import { upsertGristRecordApiCall } from "../api/grist";
import { setIndexations, indexations, currentRecord, setCurrentRecord } from "../state";
import { ConfigurationColumnData } from "../types/ConfigurationColumnData";
import { GristRecord } from "../types/GristRecord";
import { UpsertFields } from "../types/GristTable";
import { LABEL_COLUMN_SUFFIX } from "../utils/consts";
import { displayExistingIndexations, displayNoExistingIndexations, displayNoResourceSelected } from "../views/selectedRecordView";
import { displaySearchResults } from "../views/thesaurusSearchConceptsView";

export const handleNewRecord = (record: GristRecord) => {
    console.log("New record selected:", record);
    setCurrentRecord(record);
    if (!record) {
        displayNoResourceSelected();
        return;
    }
    
    setIndexations(record.CONFIG_OPENTHESO ? JSON.parse(record.CONFIG_OPENTHESO) : {});

    if (!Object.keys(indexations).length) {
        displayNoExistingIndexations();
        return;
    }

    displayExistingIndexations(record);
    displaySearchResults();
}


export const removeConceptFromColumn = (conceptId: string, targetLabelColumn: string) => {
    const targetUriColumn = targetLabelColumn.replace(LABEL_COLUMN_SUFFIX, '')

    indexations[targetUriColumn] = indexations[targetUriColumn].filter(item => item.uri_concept !== conceptId);

    upsertGristRecord(indexations);
}

export const addConceptToColumn = (conceptId: string, label: string, targetLabelColumn: string) => {
    
    const targetUriColumn = targetLabelColumn.replace(LABEL_COLUMN_SUFFIX, '')
    
    if (!Array.isArray(indexations[targetUriColumn])) {
        indexations[targetUriColumn] = [];
    }
    
    if (! indexations[targetUriColumn].some(item => item.uri_concept === conceptId)) {
        indexations[targetUriColumn].push({
            uri_concept: conceptId,
            label_concept: label,
        })
    }
    
    upsertGristRecord(indexations);
}

const upsertGristRecord = (indexations: ConfigurationColumnData) => {
    const labelFields: UpsertFields = {};
    for (const [col, indexationsByConcept] of Object.entries(indexations)) {
        labelFields[col] = (indexationsByConcept || []).map(idx => idx.uri_concept).join(' ; ');
        labelFields[col + LABEL_COLUMN_SUFFIX] = (indexationsByConcept || []).map(idx => idx.label_concept).join(' ; ');
    }

    upsertGristRecordApiCall({CONFIG_OPENTHESO: JSON.stringify(indexations), ...labelFields }, { id: currentRecord.id })
}

