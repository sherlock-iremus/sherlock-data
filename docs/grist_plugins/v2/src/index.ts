import { logConsoleWelcomeMessage } from "./utils/logConsoleWelcomeMessage"
import { handlePluginInitialization } from "./handlers";

const initialize = async () => {
    logConsoleWelcomeMessage();
    handlePluginInitialization();
}

initialize();