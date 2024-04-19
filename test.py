import pandas

data = pandas.read_csv('COVIDATA.csv')
data.dropna(inplace=True)
l = set(data['Country'])

for x in l:
    print(f"'{x}',")