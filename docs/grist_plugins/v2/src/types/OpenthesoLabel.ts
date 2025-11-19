export interface OpenthesoLabel {
    id: string;
    label: string;
    altLabel: string[];
    related: string[];
    traduction: { lang: string; title: string }[];
    Alignment: string[];
    definition: string[];
}