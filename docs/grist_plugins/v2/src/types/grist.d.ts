import { GristRecord } from "./GristRecord";

export {};

declare global {
  /**
   * Objet global injecté par Grist dans index.html.
   */
  const grist: {
    onRecord: (callback: (record: GristRecord) => void) => void;
    ready: (permissions: any) => void;
    getTable: () => Promise<GristTable>;
    fetchSelectedTable: (options: { format: "columns" | "records" }) => Promise<SelectedTableColumns>;
    docApi: {
      fetchTable: <T extends string>(
        tableId: T
      ) => Promise<
        T extends "_grist_Tables"
          ? GristTables
          : T extends "_grist_Tables_column"
            ? GristTablesColumns
            : any[]
      >;
    };

  };
}

interface GristTables {
  tableId: string[];
  id: number[];
}

export interface GristTablesColumns {
  parentId: number[];
  colId: string[];
  label: string[];
}

interface SelectedTableColumns {
  [key: string]: any[];
}