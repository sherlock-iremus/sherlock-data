const CONCEPT_URI_COLUMN = "ConceptURI"
const CONCEPT_LABEL_COLUMN = "ConceptLabel"

let currentThesaurus = null;
let allThesauri = [];
let cellRef = null;
let currentCol = null;
let currentRecord = null;
let gristTable = null;
let uriColumnName = null;
let labelColumnName = null;

const input = document.getElementById("searchInput");
const button = document.getElementById("searchBtn");
const outputDiv = document.getElementById("searchResults");

const sidebar = document.getElementById("sidebar");
const openSidebarBtn = document.getElementById("openSidebarBtn");
const selectOtherThesaurusBtn = document.getElementById("selectOtherThesaurusBtn");

const selectedThesaurusLabel = document.getElementById("selectedThesaurusLabel");
const thesaurusLink = document.getElementById("thesaurusLink");

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
    grist.ready({ requiredAccess: "full", columns: [CONCEPT_URI_COLUMN, CONCEPT_LABEL_COLUMN] });

    grist.onRecord((record, mappings) => {
        console.log("New record selected:", record);
        uriColumnName = mappings[CONCEPT_URI_COLUMN];
        labelColumnName = mappings[CONCEPT_LABEL_COLUMN];
        currentRecord = record;
    });

    fetchAndDisplayThesauri();

    gristTable = await grist.getTable();

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
        const concepts = await searchConcepts(currentThesaurus.idTheso, input.value);
        displayResults(concepts);
    } catch (e) {
        if (currentThesaurus && currentThesaurus.idTheso) {
            console.error("Erreur lors de la recherche dans le thésaurus", currentThesaurus.idTheso, e);
            outputDiv.innerHTML = "Erreur lors de la recherche dans le thésaurus.";
        } else {
            console.error("Veuillez d'abord sélectionner un thésaurus");
            outputDiv.innerHTML = "Veuillez d'abord sélectionner un thésaurus.";
        }
    }
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

function displayResults(concepts) {
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
          <th style="padding:4px;">Action</th>
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
            // Remplace domaine si besoin
            try {
                // Récupère la partie query string
                const url = new URL(broaderUriRaw, window.location.origin);
                const params = new URLSearchParams(url.search);
                // idc = idConcept, idt = idTheso
                console.log("params", params);
                broaderId = params.get("idc") || "";
                idTheso = params.get("idt") || idTheso;
            } catch (e) {
                // fallback : ancienne méthode
                broaderId = broaderUri.split('/').pop();
            }
        }

        const conceptId = "https://opentheso.huma-num.fr" + concept["@id"].split('/').pop();

        row.innerHTML = `
        <td style="padding:4px;"><button>Ajouter</button></td>
        <td style="padding:4px;">${label}<a href="${conceptId}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a></td>
        <td style="padding:4px;" class="broader-cell">${broaderId ? "Chargement..." : ""}</td>
      `;

        if (broaderId && idTheso) {
            getConceptLabels(idTheso, broaderId)
            .then(data => {
                let broaderLabel = data.label;
                row.querySelector(".broader-cell").innerHTML =
                    `${broaderLabel}<a href="https://opentheso.huma-num.fr/?idc=${broaderId}&idt=${idTheso}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a>`;
            })
            .catch(() => {
                row.querySelector(".broader-cell").innerHTML =
                    `Pas de label<a href="https://opentheso.huma-num.fr/?idc=${broaderId}&idt=${idTheso}" target="_blank" rel="noopener"><img src="./up-right-from-square.svg"/></a>`;
            })
        }

        row.querySelector("button").addEventListener("click", () => {
            if (currentRecord) {
                gristCallback(currentRecord, conceptId, label);
            } else {
                alert("Impossible d'ajouter.");
            }
        });
        tbody.appendChild(row);
    });

    outputDiv.innerHTML = "";
    outputDiv.appendChild(table);
}

openSidebar();
initialize();