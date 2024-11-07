if(Model.Cultures.Count==1){

    Model.TranslatedNames.SetAll(Model.Name);
    if(!string.IsNullOrEmpty(Model.Description))
    {
        Model.TranslatedDescriptions.SetAll(Model.Description);
    };

    foreach(var item in Model.Tables)
    {
        item.TranslatedNames.SetAll(item.Name);
        // If there is a description
        if(!string.IsNullOrEmpty(item.Description))
        {
            item.TranslatedDescriptions.SetAll(item.Description);
        };
    }

    foreach(var item in Model.AllColumns)
    {
        item.TranslatedNames.SetAll(item.Name);
        // If there is a description
        if(!string.IsNullOrEmpty(item.Description))
        {
            item.TranslatedDescriptions.SetAll(item.Description);
        };
        // If there is a display folder
        if(!string.IsNullOrEmpty(item.DisplayFolder))
        {
            item.TranslatedDisplayFolders.SetAll(item.DisplayFolder);
        };
    };


    foreach(var item in Model.AllMeasures)
    {
        item.TranslatedNames.SetAll(item.Name);
        // If there is a description
        if(!string.IsNullOrEmpty(item.Description))
        {
            item.TranslatedDescriptions.SetAll(item.Description);
        };
        // If there is a display folder
        if(!string.IsNullOrEmpty(item.DisplayFolder))
        {
            item.TranslatedDisplayFolders.SetAll(item.DisplayFolder);
        };
    };

    foreach(var item in Model.Perspectives)
    {
        item.TranslatedNames.SetAll(item.Name);
        // If there is a description
        if(!string.IsNullOrEmpty(item.Description))
        {
            item.TranslatedDescriptions.SetAll(item.Description);
        };
    }
}
else
{ Output("Model contains multiple cultures, this script assumes only 1");}