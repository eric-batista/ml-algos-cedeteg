def ind_graph(acao, initial, finish, tempo = 7, destaque='👁️'):
    """Função retorna dois gráficos, o primeiro da volatilidade com os pontos chaves destacados, onde:
        acao
        _________
        :param acao: str, acao que será analisada
        :param initial: str, data de inicio para a análise
        :param finish: str, data de fim da análise
        :param periodo: int, período que será analisado, por padrão 7 dias
        :param destaque: str, icone desejado para ser destacado no gráfico (opcional)
        _________
        retorna um gráfico com a volatilidade
        retorna um gráfico com a volatilidade aplicada em um gráfico de candle stick"""
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #   
    # Importando bibliotecas necessárias
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas_datareader as pdr
    from datetime import datetime
    import math
    import warnings
    warnings.filterwarnings("ignore")
    import plotly.express as px
    import plotly.graph_objects as go
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #    
    # Convertendo datas no formato correto usando a função datetime.strptime()
    initial_date = datetime.strptime(initial, '%M-%d-%Y')
    finish_date = datetime.strptime(finish, '%M-%d-%Y')
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #    
    # Definindo a função para importar as ações (créditos Renan pelo código pronto)
    def get(ticker, startdata, enddate):
        return pdr.get_data_yahoo(ticker, start=startdata, end=enddate)
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #    
    # Importando os dados e armazenando na variável all_data
    all_data = get(f'{acao.upper()}',  initial_date, finish_date)
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #    
    # Criando a coluna "Return" que traz o cálculo da volatilidade, onde é calculada inicial a mudança do valor do dia anterior para o atual
    all_data['Return'] = 100 * (all_data.Close.pct_change())
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #    
    # Calculando o desvio padrão da volatilidade diário, para podermos selecionar o intervalo de análise mais adqueado com a variável "periodo"
    std_daily = all_data.Return.std()
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #    
    # Gerando uma tabela contendo todos os dias que tiveram uma volatilidade elevada (tanto positivamente quanto negativamente)
    filtered = all_data[(all_data.Return >= math.sqrt(tempo) * std_daily) | (all_data.Return <= -1*(math.sqrt(tempo) * std_daily))].sort_values('Return')
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #    
    # Definindo o primeiro gráfico na variável "fig"
    fig = px.line(all_data, x = all_data.index, y = 'Return', height = 800)
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #    
    # Função para inserirmos no gráfico pontos de fácil identificação da volatilidade
    for i in range(len(filtered)):
        fig.add_annotation(x = filtered.index[i], y = filtered.Return[i], text = destaque, showarrow = False, textangle = 0)
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Definindo o segundo gráfico na variável "fig2", agora em candle stick
    fig2 = go.Figure(data=[go.Candlestick(x=all_data.index,
                    open=all_data.Open,
                    high=all_data.High,
                    low=all_data.Low,
                    close=all_data.Close)])
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Utilizando a mesma função para também facilitar a identificação dos pontos de volatilidade
    for i in range(len(filtered)):
        fig2.add_annotation(x = filtered.index[i], y = filtered.Close[i], text = destaque, showarrow = False, textangle = 0)
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #    
    # Retornando os gráficos gerados para sua utilização
    return fig, fig2
    