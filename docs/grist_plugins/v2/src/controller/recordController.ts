import { upsertGristRecordApiCall } from "../api/grist";
import { setIndexations, indexations, gristTable } from "../state";
import { ConfigurationColumnData } from "../types/ConfigurationColumnData";
import { FormattedGristColumn } from "../types/FormattedGristColumn";
import { GristRecord } from "../types/GristRecord";
import { UpsertFields } from "../types/GristTable";
import { LABEL_COLUMN_SUFFIX } from "../utils/consts";
import { displayExistingIndexations, displayNoExistingIndexations, displayNoResourceSelected } from "../views/selectedRecordView";

export const handleNewRecord = (record: GristRecord, columns: FormattedGristColumn[]) => {
    console.log("New record selected:", record);
    if (!record) {
        displayNoResourceSelected();
        return;
    }
    
    setIndexations(record.CONFIG_OPENTHESO ? JSON.parse(record.CONFIG_OPENTHESO) : {});

    if (!Object.keys(indexations).length) {
        displayNoExistingIndexations();
        return;
    }

    displayExistingIndexations(record, columns);
}


export const removeConceptFromColumn = (record: GristRecord, conceptId: string, targetLabelColumn: string) => {
    const targetUriColumn = targetLabelColumn.replace(LABEL_COLUMN_SUFFIX, '')

    indexations[targetUriColumn] = indexations[targetUriColumn].filter(item => item.uri_concept !== conceptId);

    upsertGristRecord(record, indexations);
}

const upsertGristRecord = (record: GristRecord, indexations: ConfigurationColumnData) => {
    const labelFields: UpsertFields = {};
    for (const [col, indexationsByConcept] of Object.entries(indexations)) {
        labelFields[col] = (indexationsByConcept || []).map(idx => idx.uri_concept).join(' ; ');
        labelFields[col + LABEL_COLUMN_SUFFIX] = (indexationsByConcept || []).map(idx => idx.label_concept).join(' ; ');
    }

    upsertGristRecordApiCall({CONFIG_OPENTHESO: JSON.stringify(indexations), ...labelFields }, { id: record.id })
}

