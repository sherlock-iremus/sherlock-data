async function fetchThesauri() {
    const response = await fetch("https://opentheso.huma-num.fr/openapi/v1/thesaurus", {
        headers: { accept: "application/json;charset=utf-8" }
    });
    return await response.json();
}

async function searchConcepts(thesaurusId, query) {
    const response = await fetch(`https://opentheso.huma-num.fr/openapi/v1/concept/${thesaurusId}/search?q=${encodeURIComponent(query)}`, {
        headers: { accept: "application/ld+json;charset=utf-8" }
    });
    return await response.json();
}

async function getConceptLabels(thesaurusId, conceptId) {
    const response = await fetch(`https://opentheso.huma-num.fr/openapi/v1/concept/${thesaurusId}/${conceptId}/labels`, {
        headers: { accept: "application/json;charset=utf-8" }
    });
    return await response.json();
}