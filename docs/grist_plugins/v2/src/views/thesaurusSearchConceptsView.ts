import { handleSelectOptionChange } from "../handlers";
import { columns, conceptList, currentThesaurus, indexations } from "../state";
import { FormattedGristColumn } from "../types/FormattedGristColumn";
import { getBroaderIdForConcept, OpenthesoConcept } from "../types/OpenthesoConcept";
import { LABEL_COLUMN_SUFFIX } from "../utils/consts";
import { searchResults } from "./pluginHTMLElements";

export const displayLoading = () => {
    searchResults.innerHTML = "Recherche...";
}

export const displayError = (error: string) => {
    searchResults.innerHTML = error;
}

export const displaySearchResults = () => {
    if (!Array.isArray(conceptList) || conceptList.length === 0) {
        searchResults.innerHTML = "Aucun résultat.";
        return;
    }

    const table = document.createElement("table");
    table.className = "concepts-table";
    table.border = "1";
    table.innerHTML = `
      <thead>
        <tr>
          <th style="padding:4px;">Indexation</th>
          <th style="padding:4px;">skos:prefLabel</th>
          <th style="padding:4px;">Terme plus générique</th>
        </tr>
      </thead>
      <tbody></tbody>
    `;


    const tbody = table.querySelector("tbody");

    tbody && conceptList.forEach(concept => {
        tbody.appendChild(getRowForConcept(concept));
    });

    searchResults.innerHTML = "";
    searchResults.appendChild(table);
}

const getRowForConcept = (concept: OpenthesoConcept) => {
    const row = document.createElement("tr");

    const label = getLabelForConcept(concept)
    const broaderId = getBroaderIdForConcept(concept);
    const conceptId = getConceptIdForConcept(concept);
    let idTheso = currentThesaurus.idTheso;


    row.appendChild(getActionCellForConcept(conceptId, label));
    row.appendChild(getConceptLabelCell(conceptId, label));

    const broaderCell = document.createElement("td");
    broaderCell.className = "broader-cell";
    broaderCell.textContent = broaderId ? "Chargement..." : "";
    row.appendChild(broaderCell);

    if (concept.broaderLabel)
        broaderCell.innerHTML =
            `${concept.broaderLabel} <a href="https://opentheso.huma-num.fr/?idc=${broaderId}&idt=${idTheso}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a>`;
    else
        broaderCell.innerHTML =
            `Pas de label <a href="https://opentheso.huma-num.fr/?idc=${broaderId}&idt=${idTheso}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a>`;

    return row;
}

const getLabelForConcept = (concept: OpenthesoConcept) => {
    return concept["http://www.w3.org/2004/02/skos/core#prefLabel"]?.find(l => l["@language"] === "fr")?.["@value"] || "(Sans label)";
}

const getConceptIdForConcept = (concept: OpenthesoConcept) => {
    return "https://opentheso.huma-num.fr" + concept["@id"].split('/').pop();
}

const getIndexableLabelColumnsForConcept = (conceptId: string): FormattedGristColumn[] => {
    return columns
        .filter(c => c.id.endsWith(LABEL_COLUMN_SUFFIX))
        .filter(c => !indexations[c.id.replace(LABEL_COLUMN_SUFFIX, '')]?.some(item => item.uri_concept === conceptId));
}

const getAlreadyIndexedLabelColumns = (conceptId: string): FormattedGristColumn[] => {
    return columns
        .filter(c => c.id.endsWith(LABEL_COLUMN_SUFFIX))
        .filter(c => indexations[c.id.replace(LABEL_COLUMN_SUFFIX, '')]?.some(item => item.uri_concept === conceptId));
}

const getOptionForColumn = (col: FormattedGristColumn) => {
    const opt = document.createElement("option");
    opt.value = col.id;
    opt.textContent = col.label;
    return opt;
}

const getActionCellForConcept = (conceptId: string, label: string) => {
    const labelColumnsIndexable = getIndexableLabelColumnsForConcept(conceptId);
    const alreadyIndexedLabelColumns = getAlreadyIndexedLabelColumns(conceptId);

    const select = document.createElement("select");
    select.className = "concepts-select";
    select.innerHTML = `<option value="">Sélectionner...</option>`;
    labelColumnsIndexable.forEach(col => {
        select.appendChild(getOptionForColumn(col));
    });

    select.addEventListener("change", () => {
        handleSelectOptionChange(conceptId, label, select.value);
    });


    const plural = alreadyIndexedLabelColumns.length > 1 ? 's' : ''
    const infoDiv = document.createElement("div");
    infoDiv.className = "concepts-info";
    infoDiv.textContent = `${alreadyIndexedLabelColumns.length} colonne${plural} sélectionnée${plural}.`


    const actionCell = document.createElement("td");
    actionCell.className = "concepts-action-cell";
    actionCell.appendChild(select);
    actionCell.appendChild(infoDiv);
    return actionCell;
}

const getConceptLabelCell = (conceptId: string, label: string) => {
    const labelCell = document.createElement("td");
    labelCell.className = "concepts-label-cell";
    labelCell.innerHTML = `${label} <a href="${conceptId}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a>`;
    return labelCell;
}

