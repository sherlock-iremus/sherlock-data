import { gristTable } from "../state";
import { UpsertFields } from "../types/GristTable";

/**
 * We should be using gristTable.update, because we will never add a new record here with this plugin.
 * But the endpoint is not working yet, so we use upsert as a workaround.
 *  
 * @param fields fields to upsert, be sure to also include non-changing fields or they will be erased
 * @param require record to update identifier
 */
export const upsertGristRecordApiCall = (fields: UpsertFields, require: {id: number}) => {
    console.log("Upserting Grist record with fields:", fields);
    gristTable.upsert({
        fields,
        require
    }).then(response => console.log(response)).catch(error => console.log(error));
}