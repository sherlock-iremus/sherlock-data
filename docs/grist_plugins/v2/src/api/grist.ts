import { gristTable } from "../state";
import { UpsertFields } from "../types/GristTable";

export const upsertGristRecordApiCall = (fields: UpsertFields, require: {id: number}) => {
    console.log("Upserting Grist record with fields:", fields);
    gristTable.upsert({
        fields,
        require
    }).then(response => console.log(response)).catch(error => console.log(error));
}