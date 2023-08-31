
import sqlite3
import pandas as pd

df = pd.read_csv('fert.csv', encoding='latin-1')
df.columns = df.columns.str.strip()

connection = sqlite3.connect('fertilitet.db')
df.to_sql('Fertilitet', connection, if_exists='replace')

connection.close()


