import { OpenthesoConcept } from "../types/OpenthesoConcept";
import { OpenthesoLabel } from "../types/OpenthesoLabel";
import { Thesaurus } from "../types/Thesaurus";
import { OPENTHESO_API_BASE_URL } from "../utils/consts";

/**
 * 
 * @returns Every thesauri with anonymous user reading permissions.
 */
export const fetchThesauri = async (): Promise<Thesaurus[]> => {
    const response = await fetch(OPENTHESO_API_BASE_URL + "/v1/thesaurus", {
        headers: { accept: "application/json;charset=utf-8" }
    });
    return await response.json();
}

/**
 * 
 * @param idTheso Thesaurus to browse
 * @param query 
 * @returns 
 */
export const searchConceptsInThesaurus = async (idTheso: string, query: string): Promise<OpenthesoConcept[]> => {
    const response = await fetch(OPENTHESO_API_BASE_URL + `/v1/concept/${idTheso}/search?q=${encodeURIComponent(query)}`, {
        headers: { accept: "application/ld+json;charset=utf-8" }
    });
    return await response.json();
}

export const getConceptLabels = async (idTheso: string, conceptId: string): Promise<OpenthesoLabel> => {
    const response = await fetch(OPENTHESO_API_BASE_URL + `/v1/concept/${idTheso}/${conceptId}/labels`, {
        headers: { accept: "application/json;charset=utf-8" }
    });
    return await response.json();
}