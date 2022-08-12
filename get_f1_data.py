import pandas as pd

# list of drivers
all_drivers = ['Alexander Albon', 'Fernando Alonso', 'Valtteri Bottas', 'Pierre Gasly',
              'Lewis Hamilton', 'Nico Hulkenberg', 'Charles Leclerc', 'Nicholas Latifi',
              'Kevin Magnussen', 'Lando Norris', 'Esteban Ocon', 'Sergio Perez', 'Daniel Ricciardo',
              'George Russell', 'Carlos Sainz', 'Mick Schumacher', 'Lance Stroll', 'Yuki Tsunoda',
              'Max Verstappen', 'Sebastian Vettel', 'Guanyu Zhou']

# empty list for driver DataFrames
driver_df_list = []

# get and append individual driver dfs
for i in range(len(all_drivers)):
    name = all_drivers[i].split()
    tag = name[0][:3].upper() + name[1][:3].upper() + '01'
    # Mick Schumacher and Nicholas Latifi don't follow the same url convention as all other drivers
    if name == ['Mick', 'Schumacher']:
        tag = 'MICSCH02'
    if name == ['Nicholas', 'Latifi']:
        tag = 'NICLAF01'
    driver = pd.read_html('https://www.formula1.com/en/results.html/2022/drivers/'
                          + tag + '/' + name[0].lower() + '-' + name[1].lower() + '.html')
    driver = driver[0].drop(['Unnamed: 0', 'Unnamed: 6'], axis=1)
    driver['Driver'] = all_drivers[i]
    driver['Date'] = pd.to_datetime(driver['Date'])
    driver['Total PTS'] = driver['PTS'].cumsum()
    driver.rename(columns={'Grand Prix': 'Race'}, inplace=True)
    # treat DNF as 20 (last)
    driver['Race Position'] = driver['Race Position'].replace(to_replace='DNF', value=20)
    driver_df_list.append(driver)
    
#group and export to csv    
race_results = pd.concat(driver_df_list)
race_results.to_csv('race_results.csv', index=False)

# lists of races and qualifying results    
races = ['Bahrain', 'Saudi Arabia', 'Australia', 'Emilia Romagna', 'Miami', 'Spain',
         'Monaco', 'Azerbaijan', 'Canada', 'Great Britain', 'Austria', 'France', 'Hungary']

qualifying_results = ['https://www.formula1.com/en/results.html/2022/races/1124/bahrain/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1125/saudi-arabia/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1108/australia/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1109/italy/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1110/miami/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1111/spain/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1112/monaco/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1126/azerbaijan/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1113/canada/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1114/great-britain/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1115/austria/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1116/france/qualifying.html',
                      'https://www.formula1.com/en/results.html/2022/races/1117/hungary/qualifying.html']

# edit and group all qualifying results
all_qualifying = pd.DataFrame()

for i in range(len(races)):
    quali = pd.read_html(qualifying_results[i])
    quali = quali[0]
    quali = quali[['Pos', 'Driver', 'Car']]
    quali['Driver'] = quali['Driver'].str.slice(start=0, stop=-4)
    quali['Race'] = races[i]
    # treat no qualification as 20 (last)
    quali['Pos'] = quali['Pos'].replace(to_replace='NC', value=20)
    quali.rename(columns={'Pos': 'Quali Position'}, inplace=True)
    all_qualifying = all_qualifying.append(quali)

#export to csv
all_qualifying.to_csv('all_qualifying.csv', index=False)

