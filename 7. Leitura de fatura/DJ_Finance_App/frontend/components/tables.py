import streamlit as st
import pandas as pd
from typing import Dict, List
def base_table(df: pd.DataFrame,
               title: str | None = None,
               height: int| None = None
):
   """Define a tabela base para construção do sistema"""   
   if title:
      st.subheader(title)
   st.dataframe(
         df,
         use_container_width=True,
         hide_index = True,
         height = height
         )
"""
Componentes de tabelas estilizadas e editáveis
"""
def tabela_editavel_entradas(entradas: List[Dict], mes: str) -> pd.DataFrame:
    """
    Renderiza tabela editável de ENTRADAS (Receitas)
    
    Args:
        entradas: Lista de receitas
        mes: Nome do mês
        
    Returns:
        DataFrame editado pelo usuário
    """
    st.markdown(f"### 💵 Entradas - {mes}")
    
    if not entradas:
        st.info("📭 Nenhuma entrada registrada neste período")
        return pd.DataFrame()
    
    # Converter para DataFrame
    df = pd.DataFrame(entradas)
    
    # Reordenar colunas conforme o print
    df = df[['id', 'especificacao', 'data', 'categoria', 'status', 'custo']]
    
    # Configurar editor
    edited_df = st.data_editor(
        df,
        column_config={
            'id': st.column_config.NumberColumn(
                'ID',
                disabled=True,
                width='small'
            ),
            'especificacao': st.column_config.TextColumn(
                'Especificação da entrada',
                width='large',
                required=True
            ),
            'data': st.column_config.DateColumn(
                'Data da entrada',
                format='DD/MM/YYYY',
                width='medium'
            ),
            'categoria': st.column_config.SelectboxColumn(
                'Categoria da entrada',
                options=['Salário', 'Freelance', 'Investimento', 'Outros'],
                width='medium'
            ),
            'metodo_pagamento': st.column_config.SelectboxColumn(
                'Método de Pagamento',
                options=['PIX', 'CREDITO_NUBANK', 'CREDITO_BRB', 'CREDITO_MERCADO_PAGO', 'CREDITO_C&A', 'PREVISIONADO'],
                width='medium'
            ),
            'custo': st.column_config.NumberColumn(
                'Custo',
                format='R$ %.2f',
                width='medium'
            )
        },
        num_rows='dynamic',
        use_container_width=True,
        hide_index=True,
        key=f'editor_entradas_{mes}'
    )
    
    # Mostrar total
    total = edited_df['custo'].sum()
    st.markdown(f"**Total de Entradas:** :green[R$ {total:,.2f}]")
    
    return edited_df


def tabela_editavel_saidas(saidas: List[Dict], mes: str) -> pd.DataFrame:
    """
    Renderiza tabela editável de SAÍDAS (Despesas)
    
    Args:
        saidas: Lista de despesas
        mes: Nome do mês
        
    Returns:
        DataFrame editado pelo usuário
    """
    st.markdown(f"### 💸 Saídas - {mes}")
    
    if not saidas:
        st.info("📭 Nenhuma saída registrada neste período")
        return pd.DataFrame()
    
    # Converter para DataFrame
    df = pd.DataFrame(saidas)
    
    # Reordenar colunas conforme o print
    df = df[['id', 'especificacao', 'data', 'categoria', 'status', 'custo']]
    
    # Configurar editor
    edited_df = st.data_editor(
        df,
        column_config={
            'id': st.column_config.NumberColumn(
                'ID',
                disabled=True,
                width='small'
            ),
            'especificacao': st.column_config.TextColumn(
                'Especificação da saída',
                width='large',
                required=True
            ),
            'data': st.column_config.DateColumn(
                'Data da saída',
                format='DD/MM/YYYY',
                width='medium'
            ),
            'categoria': st.column_config.SelectboxColumn(
                'Categoria da saída',
                options=['Alimentação', 'Transporte', 'Moradia', 'Saúde', 'Lazer', 'Outros'],
                width='medium'
            ),
            'status': st.column_config.TextColumn(
                'Status da saída',
                disabled=True,
                width='small'
            ),
            'custo': st.column_config.NumberColumn(
                'Custo',
                format='R$ %.2f',
                width='medium'
            )
        },
        num_rows='dynamic',
        use_container_width=True,
        hide_index=True,
        key=f'editor_saidas_{mes}'
    )
    
    # Mostrar total
    total = edited_df['custo'].sum()
    st.markdown(f"**Total de Saídas:** :red[R$ {total:,.2f}]")
    
    return edited_df


def processar_alteracoes(df_original: pd.DataFrame, df_editado: pd.DataFrame):
    """
    Processa alterações entre DataFrame original e editado
    
    Returns:
        dict: Dicionário com novos, atualizados e deletados
    """
    # Converter para listas de dicts
    original = df_original.to_dict('records') if not df_original.empty else []
    editado = df_editado.to_dict('records') if not df_editado.empty else []
    
    # IDs originais e editados
    ids_originais = set(r['id'] for r in original if pd.notna(r.get('id')))
    ids_editados = set(r['id'] for r in editado if pd.notna(r.get('id')))
    
    # Novos (sem ID ou ID NaN)
    novos = [r for r in editado if pd.isna(r.get('id'))]
    
    # Deletados (estavam no original, não estão no editado)
    deletados = list(ids_originais - ids_editados)
    
    # Atualizados (estão nos dois mas com valores diferentes)
    atualizados = []
    for row_editado in editado:
        if pd.notna(row_editado.get('id')):
            row_original = next(
                (r for r in original if r['id'] == row_editado['id']),
                None
            )
            if row_original and row_original != row_editado:
                atualizados.append(row_editado)
    
    return {
        'novos': novos,
        'atualizados': atualizados,
        'deletados': deletados
    }
def tabela_detalhamento_financeiro(detalhamento: dict, mes: str):
    """
    Renderiza tabela estilizada de detalhamento financeiro
    Inspirada em planilha Excel com cores e hierarquia visual
    
    Args:
        detalhamento: Dados de entradas/saídas detalhados
        mes: Nome do mês para exibição
    """
    entradas = detalhamento['entradas']
    saidas = detalhamento['saidas']
    total_entradas = detalhamento['total_entradas']
    total_saidas = detalhamento['total_saidas']
    saldo_previsto = detalhamento['saldo_previsto']
    
    # CSS customizado para tabela estilizada
    st.markdown("""
    <style>
    .tabela-financeira {
        width: 100%;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .mes-label {
        background-color: #4a4a4a;
        color: white;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border: 2px solid #333;
    }
    
    .secao-header {
        font-size: 18px;
        font-weight: bold;
        padding: 12px;
        text-align: center;
        border: 2px solid #333;
    }
    
    .entrada-header {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    .saida-header {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    
    .categoria-cell {
        background-color: rgba(255,255,255,0.5);
        font-weight: bold;
        padding: 10px;
        text-align: center;
        border: 1px solid #666;
    }
    
    .entrada-categoria {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    .saida-categoria {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    
    .subcategoria-cell {
        padding: 8px 15px;
        text-align: center;
        border: 1px solid #999;
        background-color: white;
    }
    
    .valor-cell {
        padding: 8px 15px;
        text-align: right;
        font-weight: bold;
        border: 1px solid #999;
        background-color: white;
    }
    
    .total-box {
        border: 3px solid #333;
        padding: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        margin: 10px 0;
    }
    
    .montante-box {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    
    .previsto-box {
        background-color: #f8d7da;
        color: #721c24;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Construir HTML da tabela
    html = '<table class="tabela-financeira">'
    
    # Linha do mês
    html += f'''
    <tr>
        <td rowspan="{len(entradas) + len(saidas) + 4}" class="mes-label">
            {mes}
        </td>
    '''
    
    # ========== ENTRADAS ==========
    html += '<td rowspan="{}" class="secao-header entrada-header">ENTRADA</td>'.format(
        sum(len(items) for items in entradas.values()) + len(entradas)
    )
    
    primeira_entrada = True
    for categoria, items in entradas.items():
        if not primeira_entrada:
            html += '<tr>'
        
        html += f'<td rowspan="{len(items)}" class="categoria-cell entrada-categoria">{categoria.upper()}</td>'
        
        # Primeira subcategoria
        if items:
            html += f'''
                <td class="subcategoria-cell">{items[0]['subcategoria']}</td>
                <td class="valor-cell">R$ {items[0]['valor']:,.2f}</td>
            </tr>
            '''
        
        # Demais subcategorias
        for item in items[1:]:
            html += f'''
            <tr>
                <td class="subcategoria-cell">{item['subcategoria']}</td>
                <td class="valor-cell">R$ {item['valor']:,.2f}</td>
            </tr>
            '''
        
        primeira_entrada = False
    
    html += '</tr>'
    
    # ========== SAÍDAS ==========
    html += f'<tr><td rowspan="{sum(len(items) for items in saidas.values()) + len(saidas)}" class="secao-header saida-header">SAÍDA</td>'
    
    primeira_saida = True
    for categoria, items in saidas.items():
        if not primeira_saida:
            html += '<tr>'
        
        html += f'<td rowspan="{len(items)}" class="categoria-cell saida-categoria">{categoria.upper()}</td>'
        
        # Primeira subcategoria
        if items:
            html += f'''
                <td class="subcategoria-cell">{items[0]['subcategoria']}</td>
                <td class="valor-cell">R$ {items[0]['valor']:,.2f}</td>
            </tr>
            '''
        
        # Demais subcategorias
        for item in items[1:]:
            html += f'''
            <tr>
                <td class="subcategoria-cell">{item['subcategoria']}</td>
                <td class="valor-cell">R$ {item['valor']:,.2f}</td>
            </tr>
            '''
        
        primeira_saida = False
    
    html += '</table>'
    
    st.markdown(html, unsafe_allow_html=True)
    
    # Boxes de totais (fora da tabela)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'''
        <div class="total-box montante-box">
            <div style="font-size: 14px;">MONTANTE</div>
            <div style="font-size: 24px;">R$ {total_entradas:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="total-box previsto-box">
            <div style="font-size: 14px;">MONTANTE PREVISIONADO</div>
            <div style="font-size: 24px;">R$ {saldo_previsto:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
