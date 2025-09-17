const gristCallback = async (record, conceptId, label, targetColumn) => {
    if (!record.CONFIGURATION_COLUMN_NAME || typeof record.CONFIGURATION_COLUMN_NAME !== "object") {
        record.CONFIGURATION_COLUMN_NAME = {};
    }

    if (!Array.isArray(record.CONFIGURATION_COLUMN_NAME[targetColumn])) {
        record.CONFIGURATION_COLUMN_NAME[targetColumn] = [];
    }
    
    if (! record.CONFIGURATION_COLUMN_NAME[targetColumn].some(item => item.uri === conceptId)) {
        record.CONFIGURATION_COLUMN_NAME[targetColumn].push({
            uri_concept: conceptId,
            label_concept: label,
            uri_theso: 'todo',
            label_theso: 'todo',
            broaderLabel: 'todo'
        })
    }

    record[targetColumn] = (record[targetColumn] || '') + ` ; ${label}`;
    labelFields = []
    for (const [col, indexationsByConcept] of Object.entries(indexations)) {

        gristTable.upsert({
        fields: { 
            [CONFIGURATION_COLUMN_NAME]: JSON.stringify(record.CONFIGURATION_COLUMN_NAME), [targetColumn]: record[targetColumn] },
        require: { id: record.id }
    }).then(response => console.log(response)).catch(error => console.log(error));
}