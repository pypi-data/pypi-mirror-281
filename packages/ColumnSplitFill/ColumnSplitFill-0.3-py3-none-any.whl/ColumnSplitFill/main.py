import pandas as pd

def process_data(df, column_to_split, separator):
    columns_to_fill = df.columns.difference([column_to_split])
    
    df_expanded = df[column_to_split].str.split(separator, expand=True).stack().reset_index(level=1, drop=True)
    df_expanded.name = column_to_split 
    
    df = df.drop(columns=[column_to_split]).join(df_expanded)
    
    df[columns_to_fill] = df[columns_to_fill].ffill()
    
    return df
