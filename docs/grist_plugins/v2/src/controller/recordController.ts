import { gristTable, indexations } from "../state";
import { ConfigurationColumnData } from "../types/ConfigurationoColumnData";
import { GristRecord } from "../types/GristRecord";
import { UpsertFields } from "../types/GristTable";
import { LABEL_COLUMN_SUFFIX } from "../utils/consts";

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

    gristTable.upsert({
        fields: { 
            CONFIG_OPENTHESO: JSON.stringify(indexations), ...labelFields },
        require: { id: record.id }
    }).then(response => console.log(response)).catch(error => console.log(error));
}
