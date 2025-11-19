import { OpenthesoConcept } from "../types/OpenthesoConcept";
import { OpenthesoLabel } from "../types/OpenthesoLabel";
import { Thesaurus } from "../types/Thesaurus";

export const fetchThesauri = async (): Promise<Thesaurus[]> => {
    const response = await fetch("https://opentheso.huma-num.fr/openapi/v1/thesaurus", {
        headers: { accept: "application/json;charset=utf-8" }
    });
    return await response.json();
}

export const searchConcepts = async (idTheso: string, query: string): Promise<OpenthesoConcept[]> => {
    const response = await fetch(`https://opentheso.huma-num.fr/openapi/v1/concept/${idTheso}/search?q=${encodeURIComponent(query)}`, {
        headers: { accept: "application/ld+json;charset=utf-8" }
    });
    return await response.json();
}

export const getConceptLabels = async (idTheso: string, conceptId: string): Promise<OpenthesoLabel> => {
    const response = await fetch(`https://opentheso.huma-num.fr/openapi/v1/concept/${idTheso}/${conceptId}/labels`, {
        headers: { accept: "application/json;charset=utf-8" }
    });
    return await response.json();
}