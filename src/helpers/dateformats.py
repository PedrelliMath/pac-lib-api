import datetime

def calcular_data_devolucao():
        data_devolucao = datetime.datetime.now() + datetime.timedelta(days=15)
        if data_devolucao.weekday() == 5:  # 5 = sábado
            data_devolucao += datetime.timedelta(days=2)  # Avança para segunda-feira
        elif data_devolucao.weekday() == 6:  # 6 = domingo
            data_devolucao += datetime.timedelta(days=1)  # Avança para segunda-feira
        return data_devolucao