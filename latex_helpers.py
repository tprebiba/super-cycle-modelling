def df_to_latextable(df, filename, 
                     column_format, 
                     rotate_columns = False, drop_columns_if_empty = False):
    '''
    Writes a pandas dataframe to a latex table.
    '''

    if drop_columns_if_empty:
        for column in df.iloc[0,:].keys():
            if ((len(set(df[column].values))==1) and (type(df[column].values[0])==str)):
                df = df.drop(labels=column, axis=1)
    
    if rotate_columns:
        for column in df.iloc[0,:].keys():
            df.rename(columns = {column:'\rot{%s}'%column}, inplace = True)
    
    # to replace _ with \textunderscore
    for column in df.iloc[0,:].keys():
        if '_' in column:
            df.rename(columns = {column:'%s\textunderscore %s'%(column.split('_')[0], column.split('_')[1])}, inplace = True)
        
    with open(filename,'w') as tf:
        tf.write(df.to_latex(column_format=column_format, escape=False))