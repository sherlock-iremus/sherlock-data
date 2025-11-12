export interface OpenthesoConcept {
    "@id": string;
    "@type": string[];
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