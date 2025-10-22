const addConceptToColumn = async (record, conceptId, label, targetLabelColumn) => {
    const configuration = record?.[CONFIGURATION_COLUMN_NAME] ? JSON.parse(record?.[CONFIGURATION_COLUMN_NAME]) : {}

    targetUriColumn = targetLabelColumn.replace(LABEL_COLUMN_SUFFIX, '')
    
    if (!Array.isArray(configuration[targetUriColumn])) {
        configuration[targetUriColumn] = [];
    }
    
    if (! configuration[targetUriColumn].some(item => item.uri_concept === conceptId)) {
        configuration[targetUriColumn].push({
            uri_concept: conceptId,
            label_concept: label,
        })
    }
    upsertGristRecord(record, configuration);
}

const removeConceptFromColumn = async (record, conceptId, targetLabelColumn) => {
    targetUriColumn = targetLabelColumn.replace(LABEL_COLUMN_SUFFIX, '')

    const configuration = JSON.parse(record?.[CONFIGURATION_COLUMN_NAME])
    configuration[targetUriColumn] = configuration[targetUriColumn].filter(item => item.uri_concept !== conceptId);

    upsertGristRecord(record, configuration);
}

const upsertGristRecord = (record, configuration) => {
    labelFields = {}
    for (const [col, indexationsByConcept] of Object.entries(configuration)) {
        labelFields[col] = (indexationsByConcept || []).map(idx => idx.uri_concept).join(' ; ');
        labelFields[col + LABEL_COLUMN_SUFFIX] = (indexationsByConcept || []).map(idx => idx.label_concept).join(' ; ');
    }

    gristTable.upsert({
        fields: { 
            [CONFIGURATION_COLUMN_NAME]: JSON.stringify(configuration), ...labelFields },
        require: { id: record.id }
    }).then(response => console.log(response)).catch(error => console.log(error));
}