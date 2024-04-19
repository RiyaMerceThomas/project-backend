import pandas

data = pandas.read_csv("infection.csv")
new_data = pandas.DataFrame(columns=list(map(lambda x: x.lower().replace(" ","_") ,data.columns.to_list())) + ['infection'])
new_data.drop(['chikungunya','nipah','jaundice'],inplace=True,axis=1)

for index,row in data.iterrows():
    temp_row = []
    for column in data.columns:
        if column not in ['Chikungunya','Nipah','Jaundice']:
            try:
                temp_row.append(row[column].lower())
            except AttributeError:
                temp_row.append(row[column])
    
    if row['Chikungunya'] == 1:
        temp_row.append('chikungunya')
    elif row['Nipah'] == 1:
        temp_row.append('nipah')
    elif row['Jaundice'] == 1:
        temp_row.append('jaundice')
    else:
        temp_row.append('none')

    new_data.loc[index] = temp_row

new_data.to_csv('infection_dataset.csv')