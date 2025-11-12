export interface GristTable {
    getTableId: () => Promise<string>; // Technical table ID
    upsert: (payload: {
        fields: UpsertFields;
        require: { id: number }
    }) => Promise<any[]>;
}

export interface UpsertFields {
    [key: string]: string;
}