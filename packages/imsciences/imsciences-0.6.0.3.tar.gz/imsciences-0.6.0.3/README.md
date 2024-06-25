# IMS Package Documentation

The IMS package is a python library for processing incoming data into a format that can be used for projects. IMS processing offers a variety of functions to manipulate and analyze data efficiently. Here are the functionalities provided by the package:

## Data Processing

### 1. `get_wd_levels(levels)`
- **Description**: Get the working directory with the option of moving up parents.
- **Usage**: `get_wd_levels(levels)`

### 2. `remove_rows(data_frame, num_rows_to_remove)`
- **Description**: Removes a specified number of rows from a pandas DataFrame.
- **Usage**: `remove_rows(data_frame, num_rows_to_remove)`

### 3. `aggregate_daily_to_wc_long(df, date_column, group_columns, sum_columns, wc, aggregation='sum', include_totals=False)`
- **Description**: Aggregates daily data into weekly data, grouping and summing specified columns, starting on a specified day of the week. In the long format.
- **Usage**: `aggregate_daily_to_wc_long(df, date_column, group_columns, sum_columns, wc, aggregation='sum', include_totals=False)`

### 4. `convert_monthly_to_daily(df, date_column)`
- **Description**: Converts monthly data in a DataFrame to daily data by expanding and dividing the numeric values.
- **Usage**: `convert_monthly_to_daily(df, date_column)`

### 5. `plot_two(df1, col1, df2, col2, date_column, same_axis=True)`
- **Description**: Plots specified columns from two different DataFrames using a shared date column. Useful for comparing data.
- **Usage**: `plot_two(df1, col1, df2, col2, date_column, same_axis=True)`

### 6. `remove_nan_rows(df, col_to_remove_rows)`
- **Description**: Removes rows from a DataFrame where the specified column has NaN values.
- **Usage**: `remove_nan_rows(df, col_to_remove_rows)`

### 7. `filter_rows(df, col_to_filter, list_of_filters)`
- **Description**: Filters the DataFrame based on whether the values in a specified column are in a provided list.
- **Usage**: `filter_rows(df, col_to_filter, list_of_filters)`

### 8. `plot_one(df1, col1, date_column)`
- **Description**: Plots a specified column from a DataFrame.
- **Usage**: `plot_one(df1, col1, date_column)`

### 9. `week_of_year_mapping(df, week_col, start_day_str)`
- **Description**: Converts a week column in 'yyyy-Www' or 'yyyy-ww' format to week commencing date.
- **Usage**: `week_of_year_mapping(df, week_col, start_day_str)`

### 10. `exclude_rows(df, col_to_filter, list_of_filters)`
- **Description**: Removes rows from a DataFrame based on whether the values in a specified column are not in a provided list.
- **Usage**: `exclude_rows(df, col_to_filter, list_of_filters)`

### 11. `rename_cols(df, cols_to_rename)`
- **Description**: Renames columns in a pandas DataFrame.
- **Usage**: `rename_cols(df, cols_to_rename)`

### 12. `merge_new_and_old(old_df, old_col, new_df, new_col, cutoff_date, date_col_name='OBS')`
- **Description**: Creates a new DataFrame with two columns: one for dates and one for merged numeric values.
- **Usage**: `merge_new_and_old(old_df, old_col, new_df, new_col, cutoff_date, date_col_name='OBS')`

### 13. `merge_dataframes_on_date(dataframes, common_column='OBS', merge_how='outer')`
- **Description**: Merge a list of DataFrames on a common column.
- **Usage**: `merge_dataframes_on_date(dataframes, common_column='OBS', merge_how='outer')`

### 14. `merge_and_update_dfs(df1, df2, key_column)`
- **Description**: Merges two dataframes on a key column, updates the first dataframe's columns with the second's where available, and returns a dataframe sorted by the key column.
- **Usage**: `merge_and_update_dfs(df1, df2, key_column)`

### 15. `convert_us_to_uk_dates(df, date_col)`
- **Description**: Convert a DataFrame column with mixed date formats to datetime.
- **Usage**: `convert_us_to_uk_dates(df, date_col)`

### 16. `combine_sheets(all_sheets)`
- **Description**: Combines multiple DataFrames from a dictionary into a single DataFrame.
- **Usage**: `combine_sheets({'Sheet1': df1, 'Sheet2': df2})`

### 17. `pivot_table(df, filters_dict, index_col, columns, values_col, fill_value=0,aggfunc='sum',margins=False,margins_name='Total',datetime_trans_needed=True)`
- **Description**: Dynamically pivots a DataFrame based on specified columns.
- **Usage**: `pivot_table(df, {'Master Include':' == 1','OBS':' >= datetime(2019,9,9)','Metric Short Names':' == 'spd''}, 'OBS', 'Channel Short Names', 'Value', fill_value=0,aggfunc='sum',margins=False,margins_name='Total',datetime_trans_needed=True)`

### 18. `apply_lookup_table_for_columns(df, col_names, to_find_dict, if_not_in_country_dict='Other'), new_column_name='Mapping')`
- **Description**: Equivalent of xlookup in excel. Allows you to map a dictionary of substrings within a column. If multiple columns are need for the LUT then a | seperator is needed.
- **Usage**: `classify_within_column(df, ['campaign type','media type'], {'France Paid Social FB|paid social': 'facebook','France Paid Social TW|paid social': 'twitter'}, 'other','mapping')`

### 19. `aggregate_daily_to_wc_wide(df, date_column, group_columns, sum_columns, wc, aggregation='sum', include_totals=False)`
- **Description**: Aggregates daily data into weekly data, grouping and summing specified columns, starting on a specified day of the week. In the wide format.
- **Usage**: `aggregate_daily_to_wc_wide(df, date_column, group_columns, sum_columns, wc, aggregation='sum', include_totals=False)`

### 20. `merge_cols_with_seperator(self, df, col_names,seperator='_',output_column_name = 'Merged',starting_prefix_str=None,ending_prefix_str=None)`
- **Description**: Merge multiple columns in a dataframe into 1 column with a seperator.Can be used if multiple columns are needed for a LUT.
- **Usage**: `merge_cols_with_seperator(df, ['Campaign','Product'],seperator='|','Merged Columns',starting_prefix_str='start_',ending_prefix_str='_end')`

### 21. `check_sum_of_df_cols_are_equal(df_1,df_2,cols_1,cols_2)`
- **Description**: Checks if the sum of two columns in two dataframes are the same, and provides the sums of each column and the difference between them.
- **Usage**: `check_sum_of_df_cols_are_equal(df_1,df_2,'Media Cost','Spend')`

### 22. `convert_2_df_cols_to_dict(df, key_col, value_col)`
- **Description**: Can be used to create an LUT. Creates a dictionary using two columns in a dataframe.
- **Usage**: `convert_2_df_cols_to_dict(df, 'Campaign', 'Channel')`

### 23. `create_FY_and_H_columns(df, index_col, start_date, starting_FY,short_format='No',half_years='No',combined_FY_and_H='No')`
- **Description**: Used to create a financial year, half year, and financial half year column.
- **Usage**: `create_FY_and_H_columns(df, 'Week (M-S)', '2022-10-03', 'FY2023',short_format='Yes',half_years='Yes',combined_FY_and_H='Yes')`

### 24. `keyword_lookup_replacement(df, col, replacement_rows, cols_to_merge, replacement_lookup_dict,output_column_name='Updated Column')`
- **Description**: Essentially provides an if statement with a xlookup if a value is something. Updates certain chosen values in a specified column of the DataFrame based on a lookup dictionary.
- **Usage**: `keyword_lookup_replacement(df, 'channel', 'Paid Search Generic', ['channel','segment','product'], qlik_dict_for_channel,output_column_name='Channel New')`

### 25. `create_new_version_of_col_using_LUT(df, keys_col,value_col, dict_for_specific_changes, new_col_name='New Version of Old Col')`
- **Description**: Creates a new column in a dataframe, which takes an old column and uses a lookup table to changes values in the new column to reflect the lookup table. The lookup is based on a column in the dataframe.
- **Usage**: `keyword_lookup_replacement(df, '*Campaign Name','Campaign Type',search_campaign_name_retag_lut,'Campaign Name New')`

### 26. `convert_df_wide_2_long(df,value_cols,variable_col_name='Stacked',value_col_name='Value')`
- **Description**: Changes a dataframe from wide to long format.
- **Usage**: `keyword_lookup_replacement(df, ['Media Cost','Impressions','Clicks'],variable_col_name='Metric')`

### 27. `manually_edit_data(df, filters_dict, col_to_change, new_value, change_in_existing_df_col='No', new_col_to_change_name='New', manual_edit_col_name=None, add_notes='No', existing_note_col_name=None, note=None)`
- **Description**: Allows the capability to manually update any cell in dataframe by applying filters and chosing a column to edit in dataframe.
- **Usage**: `keyword_lookup_replacement(df, {'OBS':' <= datetime(2023,1,23)','File_Name':' == 'France media''},'Master Include',1,change_in_existing_df_col = 'Yes',new_col_to_change_name = 'Master Include',manual_edit_col_name = 'Manual Changes')`

### 28. `format_numbers_with_commas(df, decimal_length_chosen=2)`
- **Description**: Converts data in numerical format into numbers with commas and a chosen decimal place length.
- **Usage**: `format_numbers_with_commas(df,1)`

### 29. `filter_df_on_multiple_conditions(df, filters_dict)`
- **Description**: Filters dataframe on multiple conditions, which come in the form of a dictionary.
- **Usage**: `filter_df_on_multiple_conditions(df, {'OBS':' <= datetime(2023,1,23)','File_Name':' == 'France media''})`

### 30. `read_and_concatenate_files(folder_path, file_type='csv')`
- **Description**: Read and Concatinate all files of one type in a folder.
- **Usage**: `read_and_concatenate_files(folder_path, file_type='csv')`

### 31. `remove_zero_values(data_frame, column_to_filter)`
- **Description**: Remove zero values in a specified column.
- **Usage**: `remove_zero_values(self, data_frame, column_to_filter)`

## Data Pulling

### 1. `pull_fred_data(data_frame, column_to_filter)`
- **Description**: Get data from FRED by using series id tokens.
- **Usage**: `pull_fred_data(week_commencing, series_id_list)`

### 2. `pull_boe_data(week_commencing)`
- **Description**: Fetch and process Bank of England interest rate data.
- **Usage**: ` pull_boe_data('mon')`

### 3. `pull_ons_data(series_list, week_commencing)`
- **Description**: Fetch and process time series data from the ONS API.
- **Usage**: `pull_ons_data(series_list, week_commencing)`

### 4. `pull_macro(country='GBR', week_commencing='mon')`
- **Description**: Fetch macroeconomic data from OECD and other sources for a specified country.
- **Usage**: `pull_macro(country='GBR', week_commencing='mon')`

### 5. `get_google_mobility_data(country, wc)`
- **Description**: Fetch Google Mobility data for the specified country.
- **Usage**: `get_google_mobility_data(country, wc)`

### 6. `pull_combined_dummies(week_commencing)`
- **Description**: Generate combined dummy variables for seasonality, trends, and COVID lockdowns.
- **Usage**: `pull_combined_dummies(week_commencing)`

### 7. `pull_weather(week_commencing, country)`
- **Description**: Fetch and process historical weather data for the specified country.
- **Usage**: `pull_weather(week_commencing, country)`

