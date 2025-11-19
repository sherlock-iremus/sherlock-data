export interface OpenthesoConcept {
    "@id": string;
    "@type": string[];
    broaderLabel?: string; // After-fetched property
    "http://www.w3.org/2004/02/skos/core#prefLabel": Array<{
        "@language": string;
        "@value": string;
    }>;
    "http://www.w3.org/2004/02/skos/core#broader"?: Array<{
        "@id": string;
    }>;
    "http://www.w3.org/2004/02/skos/core#inScheme": Array<{
        "@id": string;
    }>;
    "http://www.w3.org/2004/02/skos/core#notation"?: Array<{
        "@value": string;
    }>;
    "http://purl.org/dc/terms/created"?: Array<{
        "@value": string;
        "@type": string;
    }>;
    "http://purl.org/dc/terms/identifier"?: Array<{
        "@value": string;
    }>;
    "http://purl.org/dc/terms/creator"?: Array<{
        "@value": string;
    }>;
}

export const getBroaderIdForConcept = (concept: OpenthesoConcept) => {
    const broaderUriRaw = concept["http://www.w3.org/2004/02/skos/core#broader"]?.[0]?.["@id"];
    if (!broaderUriRaw) return null;

    try {
        const url = new URL(broaderUriRaw, window.location.origin);
        const params = new URLSearchParams(url.search);
        return params.get("idc") || null;
    } catch (e) {
        return null
    }
}