import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import pandas as pd
import streamlit as st
from services.api import *

payload_meses = get_all_meses()
df_meses = pd.DataFrame(payload_meses).transpose()
header = df_meses.iloc[0]
df_meses = df_meses[1:]
df_meses.columns = header
df_meses["Label"] = df_meses.apply(lambda row: row["Month"][:3] + str(row["Year"])[-2:],axis=1)
meses = df_meses["Label"].to_list()


#meses = ["Jan/26","Dez/25"]
filtro = st.selectbox("Selecione o mês para ver",options=meses)

if "df" not in st.session_state:
   data = get_lancamentos()
   st.session_state.df = pd.DataFrame(data)
   st.session_state.df["id"] = st.session_state.df["id"].astype(int)
columns = st.session_state.df.columns.to_list()[1:]
print(columns)


#data = get_lancamentos()
#df_original = pd.DataFrame(data)
#df_original["id"] = df_original["id"].astype(int)

edited_df = st.data_editor(
    st.session_state.df,
    num_rows="dynamic",
    width='stretch',
    key="editor",
    column_config={
       "id":st.column_config.NumberColumn(disabled=True)
       },
    column_order = {*columns}
)
#st.session_state.df = 


if st.button("💾 Salvar alterações"):
   edited_df = pd.DataFrame(edited_df)
   st.session_state.df = pd.DataFrame(st.session_state.df)
   print(edited_df)
   print(st.session_state.df)
   

   updated_rows = edited_df.merge(
    st.session_state.df,
    on="id",
    how="inner",
    suffixes=("_new", "_old")
   )
   print(updated_rows)
   st.success("Sincronizando com o banco...")
   
   for _, row in updated_rows.iterrows():
      changed = False
      payload = {}
      for col in ["data", "descricao", "categoria", "status", "valor"]:
         if row[col+"_new"] != row[col+"_old"]:
              payload[col] = row[f"{col}_new"]
              changed = True
      if changed:
          update_lancamento(row["id"], payload)
   
   #print(updated_rows)


   new_rows = edited_df[edited_df["id"].isna()]

   for _, row in new_rows.iterrows():
       payload = row.drop("id").to_dict()
       create_lancamento(payload)

   deleted_ids = set(st.session_state.df["id"]) - set(edited_df["id"].dropna())

   for id in deleted_ids:
       delete_lancamento(id)
   st.rerun()
