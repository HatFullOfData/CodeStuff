# Power Query - Compare Tables

## Problem

Need to compare 2 tables, Current and Update, with a common unique id column and compare values in selected columns

ColumnNames needs to be a list of column names to compare, IDColumnName needs to be the name of the common unique column in both tables.

## Working Example

[Excel file](<Sample Files/Compare Tables Example.xlsx>)

## Code

```
= (Current as table, Update as table, IDColumnName as text, ColumnNames as list) as table => let
        // Create list IDColumnName + ColumnNames
        KeepColumns = List.Combine( { {IDColumnName} , ColumnNames } ),

        //Limit Current and Update to only the KeepColumns
        CurrentCols = Table.SelectColumns(Current,KeepColumns),
        UpdateCols = Table.SelectColumns(Update,KeepColumns),

        // Load and unpivot the update table and rename columns to start with update
        UpdateUnpivot = Table.UnpivotOtherColumns(UpdateCols, {IDColumnName}, "Attribute", "Value"),
        UpdateUnpivotRename = Table.RenameColumns(UpdateUnpivot,{{IDColumnName, "Update.ID"}, {"Attribute", "Update.Attribute"}, {"Value", "Update.Value"}}),

        // Load and unpivot the current table
        CurrentUnpivot = Table.UnpivotOtherColumns(CurrentCols, {IDColumnName}, "Attribute", "Value"),
        
        // Merge the unpivoted tables and expand Current, adding on current as a prefix
        MergedTables = Table.NestedJoin(UpdateUnpivotRename, {"Update.ID", "Update.Attribute"}, CurrentUnpivot, {IDColumnName, "Attribute"}, "Current", JoinKind.FullOuter),
        ExpandedCurrent = Table.ExpandTableColumn(MergedTables, "Current", {IDColumnName, "Attribute", "Value"}, {"Current.ID", "Current.Attribute", "Current.Value"}),

        // Add a CompareNum column - numbers so we can use Max summary later
        // 1 = Same
        // 2 = Updated
        // 3 = New
        // 4 = Missing
        AddedCompareNum = Table.AddColumn(ExpandedCurrent, "CompareNum", each if [Update.ID] = null then 4 else if [Current.ID] = null then 3 else if [Update.Value] = [Current.Value] then 1 else 2),
        // Get an ID from Update or Current
        AddedID = Table.AddColumn(AddedCompareNum, IDColumnName, each if [Update.ID] = null then [Current.ID] else [Update.ID]),
        // Group by ID and calc max on the CompareNum
        GroupedRows = Table.Group(AddedID, {IDColumnName}, {{"CompareNum", each List.Max([CompareNum]), type number}}),
        // Convert CompareNum into text
        FinalResult = Table.AddColumn(GroupedRows, "Compare", each if [CompareNum] = 1 then "Same" else if [CompareNum] = 2 then "Updated" else if [CompareNum] = 3 then "New" else "Missing")
    in
        FinalResult
    ```

    
    