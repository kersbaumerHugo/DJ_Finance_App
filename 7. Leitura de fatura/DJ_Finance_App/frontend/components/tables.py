import streamlit as st
import pandas as pd
def base_table(df: pd.DataFrame,
               title: str | None = None,
               height: int| None = None
):
   
   if title:
      st.subheader(title)
   st.dataframe(
         df,
         use_container_width=True,
         hide_index = True
         height = height
         )
def financial_table(df: pd.DataFrame,
                    title
):
    df_fmt = df.copy()

    if "valor" in df_fmt.columns:
        df_fmt["valor"] = df_fmt["valor"].map("R$ {:,.2f}".format)

    base_table(df_fmt, title=title)
