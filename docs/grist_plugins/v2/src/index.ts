import { handleNewRecord } from "./controller/recordController";
import { fetchTableColumns } from "./controller/pluginController";
import { GristRecord } from "./types/GristRecord";
import { logConsoleWelcomeMessage } from "./utils/logConsoleWelcomeMessage"
import { gristTable, setColumns, setGristTable } from "./state";
import { fetchAndDisplayThesauri } from "./controller/openthesoController";

const initialize = async () => {
    logConsoleWelcomeMessage();
    fetchAndDisplayThesauri();

    grist.ready({ requiredAccess: "full" });
    setGristTable(await grist.getTable());
    setColumns(await fetchTableColumns(gristTable))

    grist.onRecord((record: GristRecord) => {
        handleNewRecord(record);
    });
}

initialize();