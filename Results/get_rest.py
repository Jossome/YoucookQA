import pandas as pd
import os

taste = ['taste_filtered.csv']
order = ['order_filtered.csv']

ytid_taste = []
for csv in taste:
    df = pd.read_csv(csv)
    ytid_taste += list(df['Input.ytid'])

ytid_order = []
for csv in order:
    df = pd.read_csv(csv)
    ytid_order += list(df['Input.ytid'])


df_all_taste = pd.read_csv('taste_rest.csv')
df_all_order = pd.read_csv('order_rest.csv')
df_taste = df_all_taste[~df_all_taste['ytid'].isin(ytid_taste)]
df_order = df_all_order[~df_all_order['ytid'].isin(ytid_order)]

df_taste.to_csv('taste_rest_rest.csv', index=None)
df_order.to_csv('order_rest_rest.csv', index=None)
