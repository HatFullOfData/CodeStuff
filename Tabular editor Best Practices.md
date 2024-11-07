# Tabular Editor Best Practices Scripts

When you run Best Practice Analyzer in Tabular Editor using the standard set of tests from [https://github.com/TabularEditor/BestPracticeRules](https://github.com/TabularEditor/BestPracticeRules) you get lots of translation issues. Editing each field would be hell and boring so I wrote a script.

Download it here [Script File](<Sample Files/Tabular Editor Set Default Translations Script.csx>)

Or copy it from here

```C#
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

```
