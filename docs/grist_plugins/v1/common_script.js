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

const CONFIGURATION_COLUMN_NAME = "CONFIG_OPENTHESO"; // Colonne contenant les indexations sous forme d'objet JSON
const RESOURCE_COLUMN_NAME = "uuid"; // Colonne contenant l'URI de la ressource dans Grist
const LABEL_COLUMN_SUFFIX = "_prefLabel"; // Suffixe qui appaire une colonne de labels d'indexations à sa colonne d'indexation liée
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
            if (!columns.map(col => col.id).includes(CONFIGURATION_COLUMN_NAME)) {
                console.warn("Configuration column is missing, this will cause issues.");
                configWarningDiv.textContent = `Veuillez créer une colonne qui s'appelle ${CONFIGURATION_COLUMN_NAME}.`
                configWarningDiv.style.display = "block";
            } else if (!columns.map(col => col.id).includes(RESOURCE_COLUMN_NAME)) {
                console.warn("Resource URI column is missing, this will cause issues.");
                configWarningDiv.textContent = `Veuillez créer une colonne qui s'appelle ${RESOURCE_COLUMN_NAME} et qui contient l'URI des ressources.`
                configWarningDiv.style.display = "block";
            } else {
                configWarningDiv.textContent = "";
                configWarningDiv.style.display = "none";
                console.log("Indexations en cours : ")
                console.log(columns.find(col => col.id === CONFIGURATION_COLUMN_NAME))
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
    const technicalTableId = await gristTable.getTableId();
    console.log("technicalTableId : ", technicalTableId)

    const gristTables = await grist.docApi.fetchTable("_grist_Tables")
    currentTableIndex = gristTables.tableId.indexOf(technicalTableId);
    currentTableId = gristTables.id[currentTableIndex]
    console.log("gristTableId : ", currentTableId)

    const gristTableColumns = await grist.docApi.fetchTable("_grist_Tables_column")
    console.log("gristTableColumns : ", gristTableColumns)

    const currentTableColumnsIds = [];

    let index = gristTableColumns.parentId.indexOf(currentTableId);
    while (index !== -1) {
        currentTableColumnsIds.push(index);
        index = gristTableColumns.parentId.indexOf(currentTableId, index + 1);
    }

    console.log("currentTableColumnsIds", currentTableColumnsIds)
    console.log("currentTableColumns", gristTableColumns.colId.filter((col, idx) => currentTableColumnsIds.includes(idx)))
    console.log("currentTableColumns", gristTableColumns.label.filter((col, idx) => currentTableColumnsIds.includes(idx)))

    const columnsTable = await grist.docApi.fetchTable(tableId);
    console.log("Current table :", columnsTable);

    // Filtre pour ne garder que celles de la table courante
    const columns = columnsTable.records
        .filter(col => col.parent.id === tableId)
        .map(col => ({
            id: col.id,
            label: col.label || col.id
        }));
    return columns;
};

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
            if (col.id === CONFIGURATION_COLUMN_NAME || col.id === RESOURCE_COLUMN_NAME) return;
            const configuration = !!currentRecord[CONFIGURATION_COLUMN_NAME] ? JSON.parse(currentRecord[CONFIGURATION_COLUMN_NAME]) : {};
            if (configuration[col.id] && configuration[col.id].some(item => item.uri_concept === conceptId)) {
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

        const actionCell = document.createElement("td");
        actionCell.style.padding = "4px";
        actionCell.appendChild(select);
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
    container.innerHTML = "<h3 style='font-size:1em;margin-bottom:6px;'>Liste des indexations existantes</h3>";

    const indexations = record?.[CONFIGURATION_COLUMN_NAME] ? JSON.parse(record?.[CONFIGURATION_COLUMN_NAME]) : {};

    // Si aucune indexation
    if (!Object.keys(indexations).length) {
        container.innerHTML += "<div style='font-size:0.95em;'>Aucune indexation existante.</div>";
        return;
    }

    // Suppose que allTableColumns est bien à jour et contient [{id, label}]
    Object.entries(indexations).forEach(([colId, indexationsByConcept]) => {
        if (!Array.isArray(indexationsByConcept) || indexationsByConcept.length === 0) return;

        // Trouve le label de la colonne
        const colObj = allTableColumns.find(c => c.id === colId);
        const colLabel = colObj ? colObj.label : colId;

        // Ligne unique pour le type et ses concepts
        const lineDiv = document.createElement("div");
        lineDiv.style.display = "flex";
        lineDiv.style.alignItems = "center";
        lineDiv.style.flexWrap = "wrap";
        lineDiv.style.gap = "6px";
        lineDiv.style.fontSize = "0.95em";
        lineDiv.style.marginBottom = "2px";

        // Nom de la colonne (type d'indexation)
        const colSpan = document.createElement("span");
        colSpan.style.fontWeight = "bold";
        colSpan.style.fontSize = "0.95em";
        colSpan.textContent = colLabel + " :";
        lineDiv.appendChild(colSpan);

        // Concepts, séparés par ";"
        indexationsByConcept.forEach((indexation, idx) => {
            const conceptSpan = document.createElement("span");
            conceptSpan.style.display = "inline-flex";
            conceptSpan.style.alignItems = "center";
            conceptSpan.style.fontSize = "0.95em";

            // Label
            const labelSpan = document.createElement("span");
            labelSpan.textContent = indexation.label_concept;

            // Lien
            const link = document.createElement("a");
            link.href = indexation.uri_concept;
            link.target = "_blank";
            link.rel = "noopener";
            link.style.display = "inline-flex";
            link.style.alignItems = "center";
            link.innerHTML = `<img src="./up-right-from-square.svg" style="width:1em;height:1em;vertical-align:middle;margin-left:2px;" />`;

            // Poubelle
            const deleteBtn = document.createElement("button");
            deleteBtn.title = "Supprimer";
            deleteBtn.style.background = "none";
            deleteBtn.style.border = "none";
            deleteBtn.style.cursor = "pointer";
            deleteBtn.style.display = "inline-flex";
            deleteBtn.style.alignItems = "center";
            deleteBtn.innerHTML = `<svg width="15" height="15" fill="none" stroke="#b33" stroke-width="2" viewBox="0 0 24 24" style="vertical-align:middle;"><line x1="5" y1="6" x2="19" y2="6"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/><rect x="6" y="6" width="12" height="14" rx="2"/></svg>`;
            deleteBtn.onclick = () => {
                removeConceptFromColumn(currentRecord, indexation.uri_concept, colId);
            };

            conceptSpan.appendChild(labelSpan);
            conceptSpan.appendChild(link);
            conceptSpan.appendChild(deleteBtn);

            lineDiv.appendChild(conceptSpan);

            // Ajoute le séparateur ";" sauf après le dernier
            if (idx < indexationsByConcept.length - 1) {
                const sep = document.createElement("span");
                sep.textContent = " ;";
                lineDiv.appendChild(sep);
            }
        });

        container.appendChild(lineDiv);
    });
}

openSidebar();
initialize();