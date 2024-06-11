# -*- coding: utf-8 -*-
"""
Created on Thu May 30 22:15:14 2024

@author: Utente1
"""

import pandas as pd
import csv
import os

# CARICAMENTO DEI FILE

file = 'movements_20240611.xlsx'
file_alfabeto = 'lista_completa_11062024.xlsx'
file_cat = 'categorie.csv'
folder_path = r'C:\Users\Utente1\Documents\Python Scripts\files\finance'
os.chdir(folder_path)


df = pd.read_excel(file, skiprows=6) #sheet_name = "BDGT VS ACT", , usecols="A,D:H,M,P:AB")
df_alfabeto = pd.read_excel(file_alfabeto, skiprows=18, usecols="A,B,C,F,H")
df_categorie = pd.read_csv(file_cat, delimiter=';')

# PULIZIA DEI DATI

df['account'] = 'fineco'
df_alfabeto['account'] = 'alfabeto'
df['movements'] = df['Entrate'].fillna(0) + df['Uscite'].fillna(0)
df = df.drop(columns=['Descrizione','Stato','Entrate', 'Uscite'])
df.rename(columns={'Moneymap': 'categoria'}, inplace=True) 
df_alfabeto['Descrizione_Completa'] = df_alfabeto['Operazione'] + ' ' + df_alfabeto['Dettagli']
df_alfabeto = df_alfabeto.drop(columns=['Operazione','Dettagli'])
df_alfabeto.rename(columns={'Categoria ': 'categoria','Importo': 'movements'}, inplace=True) #'Operazione': 'Descrizione_Completa' 

merged_df = pd.concat([df, df_alfabeto], ignore_index=True)

# ORGANIZZO UN CAMPO PER MESE E ANNO

merged_df['Data'] = pd.to_datetime(merged_df['Data'], dayfirst=True)
merged_df['Month_Year'] = merged_df['Data'].dt.to_period('M')

# Convert the 'categoria' column to lowercase
merged_df['categoria'] = merged_df['categoria'].str.lower()


# Iterate over each row in movements_df
for i, row in merged_df.iterrows():
    descrizione_completa = row['Descrizione_Completa']
    found = False
    
    if pd.notna(descrizione_completa):
        descrizione_completa_lower = descrizione_completa.lower()
        for j, cat_row in df_categorie.iterrows():
            keyword = cat_row['descrizione']
            category = cat_row['categoria']
            keyword_lower = keyword.lower()
            
            if keyword_lower in descrizione_completa_lower:
                merged_df.at[i, 'categoria'] = category
                break


csv_summary = 'sintesi_conti.csv'
summary_table = merged_df.groupby(['Month_Year', 'account','categoria'])['movements'].sum().reset_index()
filtered_df = merged_df[merged_df['Month_Year'] == '2024-02']

summary_table.to_csv(csv_summary, index=False, encoding='utf-8')   

csv_file = 'tutti_i_conti.csv'
merged_df.to_csv(csv_file, index=False, encoding='utf-8')
         
total_movements = df['movements'].sum()

print(total_movements.round(2))
print('\nSCRIPT COMPLETATO')