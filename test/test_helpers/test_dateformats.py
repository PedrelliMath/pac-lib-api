import pytest
import datetime
from freezegun import freeze_time

from src.helpers.dateformats import calcular_data_devolucao

@pytest.mark.parametrize(
    'data_atual, data_esperada',
    [
        (datetime.datetime(2024, 6, 28), datetime.datetime(2024, 7, 15)),  # Sexta-feira, sem ajuste
        (datetime.datetime(2024, 6, 29), datetime.datetime(2024, 7, 15)),  # Sábado, ajusta para segunda-feira
        (datetime.datetime(2024, 6, 30), datetime.datetime(2024, 7, 15)),  # Domingo, ajusta para segunda-feira
    ]
)
def test_calcular_data_devolucao(data_atual, data_esperada):
    with freeze_time(data_atual):
        resultado = calcular_data_devolucao()
    assert resultado == data_esperada, f"Esperado {data_esperada}, mas obteve {resultado}"
