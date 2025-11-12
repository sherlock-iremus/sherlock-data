import { handleNewRecord } from "./controller/recordController";
import { fetchTableColumns } from "./controller/pluginController";
import { FormattedGristColumn } from "./types/FormattedGristColumn";
import { GristRecord } from "./types/GristRecord";
import { logConsoleWelcomeMessage } from "./utils/logConsoleWelcomeMessage"
import { gristTable, setGristTable } from "./state";
import { fetchAndDisplayThesauri } from "./controller/openthesoController";

let currentRecord: GristRecord | null = null;
let columns: FormattedGristColumn[];

const initialize = async () => {
    logConsoleWelcomeMessage();
    fetchAndDisplayThesauri();

    grist.ready({ requiredAccess: "full" });
    setGristTable(await grist.getTable());
    columns = await fetchTableColumns(gristTable)

    grist.onRecord((record: GristRecord) => {
        currentRecord = record;
        handleNewRecord(record, columns);
    });
}

initialize();