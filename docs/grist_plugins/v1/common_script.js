let currentThesaurus = null;
let allThesauri = [];
let cellRef = null;
let currentCol = null;
let currentRecord = null;
let searchconceptList = null;
let gristTable = null;
let uriColumnName = null;
let labelColumnName = null;
let allTableColumns = null;

const CONFIGURATION_COLUMN_NAME = "CONFIG_OPENTHESO";
const input = document.getElementById("searchInput");
const button = document.getElementById("searchBtn");
const outputDiv = document.getElementById("searchResults");

const sidebar = document.getElementById("sidebar");
const openSidebarBtn = document.getElementById("openSidebarBtn");
const selectOtherThesaurusBtn = document.getElementById("selectOtherThesaurusBtn");

const selectedThesaurusLabel = document.getElementById("selectedThesaurusLabel");
const thesaurusLink = document.getElementById("thesaurusLink");
const addIndexationBtn = document.getElementById("addIndexationBtn");

// Ferme le sidebar et affiche le bouton d'ouverture
function closeSidebar() {
    sidebar.classList.add("closed");
    openSidebarBtn.style.display = "block";
    selectOtherThesaurusBtn.style.display = "block";
}

// Ouvre le sidebar et masque le bouton d'ouverture
function openSidebar() {
    sidebar.classList.remove("closed");
    openSidebarBtn.style.display = "none";
    selectOtherThesaurusBtn.style.display = "none";
}

openSidebarBtn.addEventListener("click", openSidebar);
selectOtherThesaurusBtn.addEventListener("click", openSidebar);

const initialize = async () => {
    grist.ready({ requiredAccess: "full" });

    grist.onRecord((record) => {
        console.log("New record selected:", record);
        currentRecord = record;
        displayExistingIndexations(record);

        // Si une recherche est en cours, regénère les selects-options
        if (input.value.trim() && searchconceptList && allTableColumns) {
            displayResults(searchconceptList, allTableColumns);
        }
    });

    gristTable = await grist.getTable();

    getAllTableColumns()
        .then(columns => {
            const configWarningDiv = document.getElementById("configWarning");
            if (!columns.includes(CONFIGURATION_COLUMN_NAME)) {
                console.warn("Configuration column is missing, this will cause issues.");
                configWarningDiv.textContent = `Veuillez créer une colonne qui s'appelle ${CONFIGURATION_COLUMN_NAME}.`
                configWarningDiv.style.display = "block";
            } else {
                configWarningDiv.textContent = "";
                configWarningDiv.style.display = "none";
                console.log("Indexations en cours : ")
                console.log(columns[CONFIGURATION_COLUMN_NAME])
            }
        });

    fetchAndDisplayThesauri();

    button.addEventListener("click", () => searchAndDisplayConcepts(input.value));
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") searchAndDisplayConcepts(input.value);
    });

    document.getElementById("filterInput").addEventListener("input", function () {
        const filterText = this.value.toLowerCase();
        const filtered = allThesauri.filter(th =>
            (th.labels?.find(l => l.lang === "fr")?.title || "").toLowerCase().includes(filterText)
        );
        displayThesauri(filtered);
    });
}

const fetchAndDisplayThesauri = async () => {
    try {
        allThesauri = await fetchThesauri();
        displayThesauri(allThesauri);
    } catch (error) {
        document.getElementById("thesaurusList").innerText = "Erreur de chargement.";
        console.error(error);
    }
}

const displayThesauri = (thesauri) => {
    const listDiv = document.getElementById("thesaurusList");
    listDiv.innerHTML = "";
    thesauri.forEach(th => {
        const item = document.createElement("div");
        item.className = "thesaurus-item";
        item.textContent = th.labels?.find(l => l.lang === "fr")?.title || th.idTheso;
        item.onclick = () => onThesaurusClick(th);
        listDiv.appendChild(item);
    });
}

const searchAndDisplayConcepts = async (query) => {
    if (!query.trim()) return;
    outputDiv.innerHTML = "Recherche...";
    try {
        allTableColumns = await getAllTableColumns();
        searchconceptList = await searchConcepts(currentThesaurus.idTheso, input.value);
        displayResults(searchconceptList, allTableColumns);
    } catch (e) {
        console.error(e);
        outputDiv.innerHTML = "Erreur lors de la recherche.";
    }
}

const getAllTableColumns = async () => {
    const table = await grist.fetchSelectedTable();
    const columns = Object.keys(table)
    console.log("Available columns:", columns);
    return columns;
}

const onThesaurusClick = async (th) => {
    currentThesaurus = th;
    const label = th.labels?.find(l => l.lang === "fr")?.title || th.idTheso;
    selectedThesaurusLabel.textContent = label;
    if (th.idTheso) {
        thesaurusLink.href = `https://opentheso.huma-num.fr/opentheso/?idt=${encodeURIComponent(th.idTheso)}`;
        thesaurusLink.style.display = "inline-block";
    } else {
        thesaurusLink.style.display = "none";
    }
    closeSidebar();
}

function displayResults(concepts, columns) {
    if (!Array.isArray(concepts) || concepts.length === 0) {
        outputDiv.innerHTML = "Aucun résultat.";
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
        select.innerHTML = `<option value="">Sélectionner...</option>`;
        columns.forEach(col => {
            if (col === CONFIGURATION_COLUMN_NAME) return; // Ne pas inclure la colonne de configuration
            const configuration = JSON.parse(currentRecord[CONFIGURATION_COLUMN_NAME])
            if (configuration[col] && configuration[col].some(item => item.uri_concept === conceptId)) {
                return; // Ne pas inclure les colonnes où le concept est déjà indexé
            }
            const opt = document.createElement("option");
            opt.value = col;
            opt.textContent = col;
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

        const actionCell = document.createElement("td");
        actionCell.style.padding = "4px";
        actionCell.appendChild(select);
        row.appendChild(actionCell);

        const labelCell = document.createElement("td");
        labelCell.style.padding = "4px";
        labelCell.innerHTML = `${label}<a href="${conceptId}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a>`;
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
                        `${broaderLabel}<a href="https://opentheso.huma-num.fr/?idc=${broaderId}&idt=${idTheso}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a>`;
                })
                .catch(() => {
                    broaderCell.innerHTML =
                        `Pas de label<a href="https://opentheso.huma-num.fr/?idc=${broaderId}&idt=${idTheso}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a>`;
                });
        }

        tbody.appendChild(row);
    });

    outputDiv.innerHTML = "";
    outputDiv.appendChild(table);
}

function displayExistingIndexations(record) {
    const configDiv = document.getElementById("configWarning");
    let container = document.getElementById("existingIndexationsTable");
    if (!container) {
        container = document.createElement("div");
        container.id = "existingIndexationsTable";
        configDiv.parentNode.insertBefore(container, configDiv.nextSibling);
    }
    container.innerHTML = "<h3>Liste des indexations existantes</h3>";

    const indexations = record?.[CONFIGURATION_COLUMN_NAME] ? JSON.parse(record?.[CONFIGURATION_COLUMN_NAME]) : {};

    // Si aucune indexation
    if (!Object.keys(indexations).length) {
        container.innerHTML += "<div>Aucune indexation existante.</div>";
        return;
    }

    // Affichage groupé par type d'indexation
    Object.entries(indexations).forEach(([col, indexationsByConcept]) => {
        if (!Array.isArray(indexationsByConcept) || indexationsByConcept.length === 0) return;

        // Titre du type d'indexation
        const groupDiv = document.createElement("div");
        groupDiv.style.marginBottom = "1em";
        groupDiv.innerHTML = `<div style="font-weight:bold; margin-bottom:4px;">${col} :</div>`;

        // Liste des concepts pour ce type
        indexationsByConcept.forEach(indexation => {
            const itemDiv = document.createElement("div");
            itemDiv.style.display = "flex";
            itemDiv.style.alignItems = "center";
            itemDiv.style.gap = "8px";
            itemDiv.style.marginBottom = "2px";

            // Label du concept
            const labelSpan = document.createElement("span");
            labelSpan.textContent = indexation.label_concept;

            // Lien vers conceptUri
            const link = document.createElement("a");
            link.href = indexation.uri_concept;
            link.target = "_blank";
            link.rel = "noopener";
            link.innerHTML = `<img src="./up-right-from-square.svg" style="width:1em;height:1em;vertical-align:middle;" />`;

            // Icône poubelle
            const deleteBtn = document.createElement("button");
            deleteBtn.title = "Supprimer";
            deleteBtn.style.background = "none";
            deleteBtn.style.border = "none";
            deleteBtn.style.cursor = "pointer";
            deleteBtn.innerHTML = `<svg width="16" height="16" fill="none" stroke="#b33" stroke-width="2" viewBox="0 0 24 24"><line x1="5" y1="6" x2="19" y2="6"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/><rect x="6" y="6" width="12" height="14" rx="2"/></svg>`;
            deleteBtn.onclick = () => {
                removeConceptFromColumn(currentRecord, indexation.uri_concept, col);
            };

            // (Optionnel) Ajoute ici le handler pour supprimer l'indexation

            itemDiv.appendChild(labelSpan);
            itemDiv.appendChild(link);
            itemDiv.appendChild(deleteBtn);

            groupDiv.appendChild(itemDiv);
        });

        container.appendChild(groupDiv);
    });
}

openSidebar();
initialize();