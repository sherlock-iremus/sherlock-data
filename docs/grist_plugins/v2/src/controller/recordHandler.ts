import { setIndexations, indexations } from "../state";
import { FormattedGristColumn } from "../types/FormattedGristColumn";
import { GristRecord } from "../types/GristRecord";
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

    displayExistingIndexations(record, columns, indexations);
}