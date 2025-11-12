import { OpenthesoConcept } from "../types/OpenthesoConcept";
import { searchResults } from "./pluginHTMLElements";

export const displayLoading = () => {
    searchResults.innerHTML = "Recherche...";
}

export const displayError = (error: string) => {
    searchResults.innerHTML = error;
} 

export const displayResults = (concepts: OpenthesoConcept[]) => {
        if (!Array.isArray(concepts) || concepts.length === 0) {
        searchResults.innerHTML = "Aucun résultat.";
        return;
    }

    const table = document.createElement("table");
    table.border = "1";
    table.style.borderCollapse = "collapse";
    table.style.marginTop = "1em";
    table.style.width = "100%";
    table.style.textWrap = "initial";
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

    concepts.forEach(concept => {
        const configuration = !!currentRecord[CONFIGURATION_COLUMN_NAME] ? JSON.parse(currentRecord[CONFIGURATION_COLUMN_NAME]) : {};
        const row = document.createElement("tr");

        const label = concept["http://www.w3.org/2004/02/skos/core#prefLabel"]?.find(l => l["@language"] === "fr")?.["@value"] || "(Sans label)";
        const broaderUriRaw = concept["http://www.w3.org/2004/02/skos/core#broader"]?.[0]?.["@id"];
        let broaderUri = "";
        let broaderId = "";
        let idTheso = currentThesaurus?.idTheso;

        if (broaderUriRaw) {
            try {
                const url = new URL(broaderUriRaw, window.location.origin);
                const params = new URLSearchParams(url.search);
                broaderId = params.get("idc") || "";
                idTheso = params.get("idt") || idTheso;
            } catch (e) {
                broaderId = broaderUri.split('/').pop();
            }
        }

        const conceptId = "https://opentheso.huma-num.fr" + concept["@id"].split('/').pop();

        const select = document.createElement("select");
        select.style.width = "180px";
        select.innerHTML = `<option value="">Sélectionner...</option>`;
        let columnsIndexedNumber = 0;
        columns.filter(c => c.id.endsWith(LABEL_COLUMN_SUFFIX)).forEach(col => {
            uriColumnId = col.id.replace(LABEL_COLUMN_SUFFIX, '')
            if (configuration[uriColumnId] && configuration[uriColumnId].some(item => item.uri_concept === conceptId)) {
                columnsIndexedNumber += 1;
                return; // Ne pas inclure les colonnes où le concept est déjà indexé
            }
            const opt = document.createElement("option");
            opt.value = col.id;
            opt.textContent = col.label;
            select.appendChild(opt);
        });

        select.addEventListener("change", () => {
            const selectedCol = select.value;
            if (!selectedCol) {
                alert("Veuillez sélectionner une colonne.");
                return;
            }

            addConceptToColumn(currentRecord, conceptId, label, selectedCol);
            console.log("Colonne sélectionnée pour l'indexation :", selectedCol, conceptId, label);
        });

        const plural = columnsIndexedNumber > 1 ? 's' : ''
        const infoDiv = document.createElement("div");
        infoDiv.style.fontSize = "0.85em";
        infoDiv.style.marginTop = "2px";
        infoDiv.textContent = `${columnsIndexedNumber} colonne${plural} sélectionnée${plural}.`


        const actionCell = document.createElement("td");
        actionCell.style.padding = "4px";
        actionCell.appendChild(select);
        actionCell.appendChild(infoDiv);
        row.appendChild(actionCell);

        const labelCell = document.createElement("td");
        labelCell.style.padding = "4px";
        labelCell.innerHTML = `${label} <a href="${conceptId}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a>`;
        row.appendChild(labelCell);

        const broaderCell = document.createElement("td");
        broaderCell.style.padding = "4px";
        broaderCell.className = "broader-cell";
        broaderCell.textContent = broaderId ? "Chargement..." : "";
        row.appendChild(broaderCell);

        if (broaderId && idTheso) {
            getConceptLabels(idTheso, broaderId)
                .then(data => {
                    let broaderLabel = data.label;
                    broaderCell.innerHTML =
                        `${broaderLabel} <a href="https://opentheso.huma-num.fr/?idc=${broaderId}&idt=${idTheso}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a>`;
                })
                .catch(() => {
                    broaderCell.innerHTML =
                        `Pas de label <a href="https://opentheso.huma-num.fr/?idc=${broaderId}&idt=${idTheso}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a>`;
                });
        }

        tbody.appendChild(row);
    });

    searchResults.innerHTML = "";
    searchResults.appendChild(table);
}