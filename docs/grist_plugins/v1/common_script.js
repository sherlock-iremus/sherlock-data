let currentThesaurus = null;
let allThesauri = [];
let cellRef = null;
let currentCol = null;
let currentRecord = null;
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
        const columns = await getAllTableColumns();
        const concepts = await searchConcepts(currentThesaurus.idTheso, input.value);
        displayResults(concepts, columns);
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
            
            gristCallback(currentRecord, conceptId, label, selectedCol);
            console.log("Colonne sélectionnée pour l'indexation :", selectedCol, conceptId, label);
        });

        const actionCell = document.createElement("td");
        actionCell.style.padding = "4px";
        actionCell.appendChild(select);
        const indexationsAlreadyDoneDiv = document.createElement("div");
        indexationsAlreadyDoneDiv.innerHTML = currentRecord?.CONFIGURATION?.conceptId != null ? currentRecord.CONFIGURATION.conceptId : '';
        actionCell.appendChild(indexationsAlreadyDoneDiv);
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

    const indexations = JSON.parse(record?.[CONFIGURATION_COLUMN_NAME]) || {};
    const rows = [];

    console.log("Indexations existantes :", indexations);
    for (const [col, indexationsByConcept] of Object.entries(indexations)) {

        for (const indexation of indexationsByConcept) {
        console.log("Indexation :", indexation);
           rows.push({
                colonne_concernée: col,
                thesaurusUri: indexation.uri_theso,
                thesaurusLabel: indexation.label_theso,
                conceptUri: indexation.uri_concept,
                conceptLabel: indexation.label_concept
            });
        }
    }

    if (rows.length === 0) {
        container.innerHTML += "<div>Aucune indexation existante.</div><br/>";
        return;
    }

    const table = document.createElement("table");
    table.border = "1";
    table.style.borderCollapse = "collapse";
    table.style.marginTop = "1em";
    table.style.width = "100%";
    table.innerHTML = `
      <thead>
        <tr>
          <th>id</th>
          <th>colonne_concernée</th>
          <th>thesaurusUri</th>
          <th>thesaurusLabel</th>
          <th>conceptUri</th>
          <th>conceptLabel</th>
          <th>Supprimer</th>
        </tr>
      </thead>
      <tbody></tbody>
    `;
    const tbody = table.querySelector("tbody");

    rows.forEach(row => {
        const tr = document.createElement("tr");
        Object.values(row).forEach(val => {
            const td = document.createElement("td");
            td.textContent = val;
            tr.appendChild(td);
        });
        const tdDelete = document.createElement("td");
        const btn = document.createElement("button");
        btn.textContent = "Supprimer";
        tdDelete.appendChild(btn);
        tr.appendChild(tdDelete);
        tbody.appendChild(tr);
    });

    table.appendChild(tbody);
    container.appendChild(table);
}

openSidebar();
initialize();