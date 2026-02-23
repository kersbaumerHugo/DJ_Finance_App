import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from tables.tables import financial_table

# OBS: Não podemos testar base_table diretamente porque usa st.dataframe (UI)
# Vamos testar apenas a lógica de transformação de dados


class TestFinancialTable:
    """Testes para formatação de tabelas financeiras"""

    def test_financial_table_formats_valor_column(self, sample_dataframe):
        """Testa se a coluna 'valor' é formatada corretamente"""
        # Arrange
        df = sample_dataframe.copy()

        # Mock do Streamlit para não tentar renderizar
        with patch("tables.tables.base_table") as mock_base_table:
            # Act
            financial_table(df, title="Test Table")

            # Assert
            # Verifica se base_table foi chamada
            assert mock_base_table.called

            # Captura o DataFrame que foi passado para base_table
            called_df = mock_base_table.call_args[0][0]

            # Verifica se valores foram formatados
            assert isinstance(called_df["valor"].iloc[0], str)
            assert "R$" in called_df["valor"].iloc[0]

    def test_financial_table_preserves_other_columns(self, sample_dataframe):
        """Testa se outras colunas não são alteradas"""
        # Arrange
        df = sample_dataframe.copy()

        with patch("tables.tables.base_table") as mock_base_table:
            # Act
            financial_table(df, title="Test")

            # Assert
            called_df = mock_base_table.call_args[0][0]
            assert "id" in called_df.columns
            assert "descricao" in called_df.columns
            assert "categoria" in called_df.columns

    def test_financial_table_handles_missing_valor_column(self):
        """Testa comportamento quando coluna 'valor' não existe"""
        # Arrange
        df = pd.DataFrame({"id": [1, 2], "descricao": ["A", "B"]})

        with patch("tables.tables.base_table") as mock_base_table:
            # Act
            financial_table(df, title="Test")

            # Assert
            # Não deve dar erro, apenas não formatar nada
            assert mock_base_table.called
