import { FormattedGristColumn } from "../types/FormattedGristColumn";
import { CONFIGURATION_COLUMN_NAME, LABEL_COLUMN_SUFFIX, RESOURCE_COLUMN_NAME } from "../utils/consts";
import { pluginConfigurationDiv } from "../views/pluginHTMLElements";

export const displayConfigurationColumnMissing = () => {
    pluginConfigurationDiv.textContent = `Veuillez créer une colonne qui s'appelle ${CONFIGURATION_COLUMN_NAME}.`
    pluginConfigurationDiv.style.display = "block";
}

export const displayResourceColumnMissing = () => {
    pluginConfigurationDiv.textContent = `Veuillez créer une colonne qui s'appelle ${RESOURCE_COLUMN_NAME} et qui contient l'URI des ressources.`
    pluginConfigurationDiv.style.display = "block";
}

export const displayColumnsWithoutLabelMissing = (columnsMissingLabelDisplay: FormattedGristColumn[]) => {
    pluginConfigurationDiv.innerHTML = `Les colonnes suivantes n'ont pas de colonne de labels associée (suffixe ${LABEL_COLUMN_SUFFIX}) : <strong>${columnsMissingLabelDisplay.map(col => col.label).join(", ")}</strong>.<br/>Veuillez créer les colonnes de labels associées.`
    pluginConfigurationDiv.style.display = "block";
}

export const displayConfigurationOK = () => {
    pluginConfigurationDiv.textContent = "";
    pluginConfigurationDiv.style.display = "none";
}