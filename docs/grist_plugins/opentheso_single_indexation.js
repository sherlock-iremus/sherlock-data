const gristCallback = async (record, conceptId, label) => {
    // TODO: use gristTable.update() when doc is fully written
    // https://support.getgrist.com/code/interfaces/DocApiTypes.AddOrUpdateRecord/
    //gristTable.update([{currentRecord}]).then(response => console.log(response)).catch(error => console.log(error));
    gristTable.upsert({ fields: { [uriColumnName]: conceptId, [labelColumnName]: label }, require: { id: record.id } }).then(response => console.log(response)).catch(error => console.log(error));
}