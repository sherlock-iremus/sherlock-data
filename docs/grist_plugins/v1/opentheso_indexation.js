const gristCallback = async (record, conceptId, label, targetColumn) => {
    const configuration = record?.[CONFIGURATION_COLUMN_NAME] ? JSON.parse(record?.[CONFIGURATION_COLUMN_NAME]) : {}

    if (!Array.isArray(configuration[targetColumn])) {
        configuration[targetColumn] = [];
    }
    
    if (! configuration[targetColumn].some(item => item.uri === conceptId)) {
        configuration[targetColumn].push({
            uri_concept: conceptId,
            label_concept: label,
            uri_theso: 'todo',
            label_theso: 'todo',
            broaderLabel: 'todo'
        })
    }

    labelFields = {}
    for (const [col, indexationsByConcept] of Object.entries(configuration)) {
        labelFields[col] = (indexationsByConcept || []).map(idx => idx.label_concept).join(' ; ');
    }

    console.log("payload grist")
    console.log({ 
            [CONFIGURATION_COLUMN_NAME]: JSON.stringify(configuration), ...labelFields })


    gristTable.upsert({
        fields: { 
            [CONFIGURATION_COLUMN_NAME]: JSON.stringify(configuration), ...labelFields },
        require: { id: record.id }
    }).then(response => console.log(response)).catch(error => console.log(error));
}