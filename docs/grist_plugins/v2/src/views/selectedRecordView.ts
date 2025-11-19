import { handleDeleteIndexationButtonClick } from "../handlers";
import { columns, currentRecord, indexations } from "../state";
import { ConceptItem } from "../types/ConfigurationColumnData";
import { LABEL_COLUMN_SUFFIX } from "../utils/consts";
import { existingIndexationsList, selectedResourceLabel } from "./pluginHTMLElements";

export const displayNoResourceSelected = () => {
    selectedResourceLabel.textContent = "Pas de ressource sélectionnée";
    existingIndexationsList.innerHTML = "";
}

export const displaySelectedResourceLabel = () => {
    selectedResourceLabel.textContent = currentRecord.uuid || "";
}

export const displayNoExistingIndexations = () => {
    existingIndexationsList.innerHTML = "<div style='font-size:0.95em;'>Aucune indexation existante.</div>";
}

export const displayExistingIndexations = () => {
    existingIndexationsList.innerHTML = "<h3 style='font-size:1em;margin-bottom:6px;'>Liste des indexations existantes</h3>";

    const ul = document.createElement("ul");
    ul.style.paddingLeft = "1.2em";
    ul.style.margin = "0";

    Object.entries(indexations).forEach(([colId, indexationsByConcept]) => {
        if (!Array.isArray(indexationsByConcept) || indexationsByConcept.length === 0) return;

        ul.appendChild(getConceptsAsListItemsByColumn(colId, indexationsByConcept));
    });

    existingIndexationsList.appendChild(ul);

}

const getConceptsAsListItemsByColumn = (
    colId: string,
    indexationsByConcept: ConceptItem[]) => {
    const colObj = columns.find(c => c.id === colId + LABEL_COLUMN_SUFFIX);
    const colLabel = colObj ? colObj.label : colId;

    // Catégorie (type d'indexation) en bullet point
    const li = document.createElement("li");
    li.className = "indexation-type-item";

    // Ligne unique pour le type et ses concepts
    const lineDiv = document.createElement("div");
    lineDiv.className = "indexation-type-line";

    // Nom de la colonne (type d'indexation)
    const colSpan = document.createElement("span");
    colSpan.className = "indexation-type-label";
    colSpan.textContent = colLabel + " :";
    lineDiv.appendChild(colSpan);
    const conceptsDiv = document.createElement("div");
    conceptsDiv.className = "indexation-concept-line";
    lineDiv.appendChild(conceptsDiv);
    // Concepts
    indexationsByConcept.forEach((indexation, idx) => {
        const conceptSpan = getConceptAsSpan(colId, indexation);
        conceptsDiv.appendChild(conceptSpan);
        // Ajoute le séparateur ";" sauf après le dernier
        if (idx < indexationsByConcept.length - 1) {
            const sep = document.createElement("span");
            sep.className = "indexation-concept-separator";
            sep.textContent = " ; ";
            conceptsDiv.appendChild(sep);
        }
    });

    li.appendChild(lineDiv);
    return li;
}

function getConceptAsSpan(colId: string, indexation: ConceptItem) {
    const conceptSpan = document.createElement("span");
    conceptSpan.className = "indexation-concept";

    // Label
    const labelSpan = document.createElement("span");
    labelSpan.className = "indexation-concept-label";
    labelSpan.textContent = indexation.label_concept;

    // Lien
    const link = document.createElement("a");
    link.href = indexation.uri_concept;
    link.target = "_blank";
    link.rel = "noopener";
    link.className = "indexation-concept-link";
    link.innerHTML = `<img src="./up-right-from-square.svg" alt="Ouvrir" />`;

    // Poubelle
    const deleteBtn = document.createElement("button");
    deleteBtn.title = "Supprimer";
    deleteBtn.className = "indexation-concept-delete";
    deleteBtn.innerHTML = `<svg width="15" height="15" fill="none" stroke="#b33" stroke-width="2" viewBox="0 0 24 24"><line x1="5" y1="6" x2="19" y2="6"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/><rect x="6" y="6" width="12" height="14" rx="2"/></svg>`;
    deleteBtn.onclick = () => handleDeleteIndexationButtonClick(indexation.uri_concept, colId);
    
    conceptSpan.appendChild(labelSpan);
    conceptSpan.appendChild(link);
    conceptSpan.appendChild(deleteBtn);
    return conceptSpan;
};

