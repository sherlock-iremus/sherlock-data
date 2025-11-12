import { onThesaurusClick, searchAndDisplayConcepts } from "../controller/openthesoController";
import { thesauri } from "../state";
import { Thesaurus } from "../types/Thesaurus";
import { filterInput, openSidebarBtn, searchBtn, searchInput, selectedThesaurusLabel, selectOtherThesaurusBtn, sidebar, thesaurusLink, thesaurusList } from "./pluginHTMLElements";

export const showThesauriLoadingError = () => {
    thesaurusList.innerText = "Erreur de chargement.";
};

export const initializeThesauriView = () => {
    openSidebar();
    openSidebarBtn.addEventListener("click", openSidebar);
    selectOtherThesaurusBtn.addEventListener("click", openSidebar);

    searchBtn.addEventListener("click", () => searchAndDisplayConcepts(searchInput.value));
    searchInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") searchAndDisplayConcepts(searchInput.value);
    });

    filterInput.addEventListener("input", function () {
        const filterText = this.value.toLowerCase();
        const filtered = thesauri.filter(th =>
            (th.labels?.find(l => l.lang === "fr")?.title || "").toLowerCase().includes(filterText)
        );
        displayThesauri(filtered);
    });
}

export const displayThesauri = (thesauri: Thesaurus[]) => {
    thesaurusList.innerHTML = "";
    thesauri.forEach(th => {
        const item = document.createElement("div");
        item.className = "thesaurus-item";
        item.textContent = th.labels?.find(l => l.lang === "fr")?.title || th.idTheso;
        item.onclick = () => onThesaurusClick(th);
        thesaurusList.appendChild(item);
    });
}

export const displaySelectedThesaurus = (thesaurus: Thesaurus) => {
    const label = thesaurus.labels?.find(l => l.lang === "fr")?.title || thesaurus.idTheso;
    selectedThesaurusLabel.textContent = label;
    if (thesaurus.idTheso) {
        thesaurusLink.href = `https://opentheso.huma-num.fr/opentheso/?idt=${encodeURIComponent(thesaurus.idTheso)}`;
        thesaurusLink.style.display = "inline-block";
    } else {
        thesaurusLink.style.display = "none";
    }
}

// Ferme le sidebar et affiche le bouton d'ouverture
export const closeSidebar = () => {
    sidebar.classList.add("closed");
    openSidebarBtn.style.display = "block";
    selectOtherThesaurusBtn.style.display = "block";
}

// Ouvre le sidebar et masque le bouton d'ouverture
export const openSidebar = () => {
    sidebar.classList.remove("closed");
    openSidebarBtn.style.display = "none";
    selectOtherThesaurusBtn.style.display = "none";
}