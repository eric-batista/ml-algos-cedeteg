import builtins
from logging import _STYLES 
from os import path
from time import sleep
from numpy import select
import streamlit as st
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.express as px
from streamlit.legacy_caching.caching import cache
from streamlit.proto.PlotlyChart_pb2 import Figure
from web_scrapping import iee_b3, import_ibov, import_ind
from volatility import ind_graph
#----------------------------------------------------------------#
#                         Variaveis                              #
#----------------------------------------------------------------#
countries = ['brazil', 'united states']  
intervals = ['Daily', 'Weekly', 'Monthly']

start_date = datetime.today()-timedelta(days=30) # data de inicio para o grafico de candle  no caso diminuiu 30 dias # 
end_date = datetime.today()                      # end sendo a data de hoje #
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#               função que importa os dados da B3                #
#----------------------------------------------------------------#
#  @cache para poder puxar os dados apenas uma vez # 
#   função que puxa os dados da B3    #
#@st.cache 
def iE():
    iee = iee_b3()  
    return iee
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#                 função que consulta a ação de                  #
#----------------------------------------------------------------#
#   função que retorna um dataframe  baseados nas datas especificas     #
@st.cache(allow_output_mutation=True)
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(
        stock=stock, country=country, from_date=from_date,
        to_date=to_date, interval=interval)
    return df
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#                   Definindo indicadores                        #              
#----------------------------------------------------------------#
# Indicadores usados para plotar o grafico de pizza #
indicadores = ['DY', 'PL', 'PEG_RATIO', 'P_PV', 'EV_EBITIDA', 'EV_EBIT', 'P_EBITIDA', 'P_EBIT',
               'VPA', 'P_ATIVO', 'LPA', 'S_SR', 'P_CAP_GIRO', 'P_ATIVO_CIRC_LIQ', 'DIV_LIQUIDA_PL',
               'DIV_LIQUIDA_EBITIDA', 'DIV_LIQUIDA_EBIT', 'PL_ATIVOS', 'PASSIVOS_ATIVOS', 'LIQ_CORRENTE',
               'M_BRUTA', 'M_EBITIDA', 'M_EBIT', 'M_LIQUIDA', 'ROE', 'ROA', 'ROIC', 'GIRO_ATIVOS',
               'CAGR_RECEITAS_5_ANOS', 'CAGR_LUCROS_5_ANOS']
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#                      Grafico da pizza                          #
#----------------------------------------------------------------#
# Função grafico de pizza #
#@st.cache
def sun_b(var):

    fig_2 = go.Figure(go.Sunburst(
        labels=[var] + [iee[iee.Empresa == var].Acao.values[0]] +
        [i for i in indicadores],
        parents=[''] + [var] + [var for i in range(len([i for i in indicadores]))]))

    fig_2.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)', },
        autosize=True,
        width=600,
        height=600,)

    return fig_2
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#                       Grafico teste                            #            
#----------------------------------------------------------------#
# Grafico teste usado no dash 2 #
def Graftest(df):
    fig = [go.Scatter(
        x = df.index,
        y = df['Close'])]
    return fig
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#                         Formata a data                         #
#----------------------------------------------------------------#
# função de formatação de data  # 
#@st.cache
def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#           função definida para plotar grafico de candle        #
#----------------------------------------------------------------#
def plotCandleStick(df, acao='ticket'):
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }

    data = [trace1] 
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#                       Definindo o dash 2                       #
#----------------------------------------------------------------#
# Função que define novo dash  # 
def Dash_2():
    st.sidebar.title('Menu 📰 De Notícias  ') # 
    st.sidebar.markdown('---')
    st.title('  Dash 2 ')
    st.markdown('---')
    iee = iee_b3()
    #stock_select_side = st.sidebar.selectbox("Selecione o ativo:", )
    
    col1,col2,= st.columns(2)
    container2 = st.container()
    col_side1, col_side2, col_side3 = st.sidebar.columns(3)
    #stock_select = st.selectbox("Selecione o ativo:", [i for i in iee.Empresa])
    
    container3 = st.container()
    container4 = st.container()
    
    #df1, df2 = import_ind(iee[iee.Empresa == stock_select].loc[0][1])
    stock_select = st.selectbox("Selecione o ativo:", [i for i in iee.Empresa])

    id_df1, id_df2 = import_ind(iee[iee.Empresa == stock_select].Acao.values[0])
    with col1:
        from_date = st.date_input('De:', start_date)  
    with col2:
        to_date = st.date_input('Para:', end_date)
    print(start_date)
    #stock_selec = st.sidebar.selectbox('Escolha a ação')
    #colunas dos valores #
    with container3:
        with col_side1: # Coluna sidebar 1#
            st.metric(label='patrimonio liquido', value=id_df2.loc[0][0], delta='',delta_color="inverse")
            st.metric("Wind", "9", "")
            st.metric("Wind", "9", "")
            st.metric(label="Price", value=4, delta='',delta_color="inverse")
            

        with col_side2: # Coluna sidebar 2 #
            st.metric(label="Vale3", value='12%', delta='',delta_color="off")
            st.metric("Wind", "15", "")
            st.metric("Wind", "9", "")
            st.metric(label="Price", value=4, delta='',delta_color="inverse")
            
        with col_side3: # Coluna sidebar 3#
            st.metric(label="Wind", value=9, delta='', delta_color="off")
            st.metric("Wind", "17", '')
            st.metric(label="Price", value=4, delta='',delta_color="inverse") 
    
            
    #with container4:
    #    with col_side4:
    #        st.metric("Wind", "9", "-8%")
    #    with col_side5:
    #        st.metric("Wind", "15", "+8%")
    #    with col_side6:
    #        st.metric("Wind", "17", '8%')


    fig1, fig2, tabel = ind_graph(iee[iee.Empresa == stock_select].Acao.values[0]+'.SA', str(from_date), str(to_date))
    with container2:
        st.markdown('---')
        
        #df1,df2 = import_ind(iee[iee.Empresa == stock_select].loc[0][1])
        #interval_select = st.selectbox("Selecione o timeframe:", intervals)
        #grafico#
    
    if from_date > to_date:
        st.error('Data de ínicio maior do que data final')
    else:
        df = consultar_acao(iee[iee.Empresa == stock_select].Acao.values[0], 'brazil', format_date(
            from_date), format_date(to_date), 'Daily')
        try : 
            #fig = Graftest(df)
            grafico_candle = st.plotly_chart(fig2, use_container_width=True) 
            grafico_linha = st.plotly_chart(fig1, use_container_width=False, height=1000,width=1000) 
            st.markdown('---')
        except Exception as e:
            st.error(e)  
    st.dataframe(tabel)

    


    
#----------------------------------------------------------------#
#                        Dash 3                                  #
#----------------------------------------------------------------#
# Função que define novo dash  # 
def dash_3():
    
    st.markdown(' ## Novo Dash 3 - Gráficos')
    c = st.container()
    c.markdown(' # Grafico 1')
    c.markdown(' # Grafico 2')
    c.markdown(' # Grafico 3')
#----------------------------------------------------------------#



#----------------------------------------------------------------#
#                    Variaveis usadas no dash 1                  #
#----------------------------------------------------------------#
carregar_dados = 0
iee = iE() #carregadno dados  da função iE # 
dash = ['Dash 1', 'Dash 2', 'Dash 3']   # variavel dash recebe uma lista de dash  # 

newDash = st.sidebar.selectbox('Selecione o  Dash', dash) # newDash recebe um seletor de caixa  #
formatacao1   = st.sidebar.markdown("---")
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#------------------------- dash main ----------------------------#
#----------------------------------------------------------------#
    # if que é usado para fazer um novo dash    #
if newDash == 'Dash 2' :
    Dash_2() # Função Dash 2#
elif newDash == 'Dash 3':
    dash_3()    # Função Dash 3
#   Caso contrario motrar o dash 1   #    
else:
    barra_lateral = st.sidebar.title('Menu 🌫️   ')
    barra_lateral = st.sidebar.empty()
    formatacao1   = st.sidebar.markdown("---")
    
    stock_select = st.selectbox("Selecione o ativo:", [i for i in iee.Empresa]) # stock select recebe um seletor de ativo  # 
    formatacao13   = st.markdown("---")
    from_date = st.sidebar.date_input('De:', start_date)  
    to_date = st.sidebar.date_input('Para:', end_date)
    interval_select = st.sidebar.selectbox("Selecione o timeframe:", intervals)
    formatacao2 = st.sidebar.markdown("---")
    grafico_line = st.empty()   #Grafico de linha  recebendo vazio   #
    grafico_candle = st.empty() #Grafico de candle recebendo vazio   #
    grafico_pizza = st.empty()  #Grafico de pizza recebendo vazio    #
    if from_date > to_date:     #Se from data for maior que to date  #
        st.sidebar.error('Data de ínicio maior do que data final') 
    else:
        df = consultar_acao(iee[iee.Empresa == stock_select].Acao.values[0], 'brazil', format_date(
            from_date), format_date(to_date), interval_select) #  dataframa recebe a função consultar ação com da iee  com as datas selecionada  # 
        try:
            fig = plotCandleStick(df) # fig recebe a função que mostra o grafico de 
            figpizza = sun_b(stock_select)  # figurapizza com a variavel stock_select que foi selecionada pelo usuario  #
            
            grafico_pizza = st.plotly_chart(figpizza, use_container_width=True) # Grafico de pizza usando a variavel figpizza em que o dataframe foi transformado em figura#

            #grafico_line = st.line_chart(df.Close)  #pegando apenas os dados de df.Close para usar no grafico de linhas#

            container = st.container() 
            with container:
                grafico_candle = st.plotly_chart(fig, use_container_width=True)     # plotando o grafico de candle  #
                carregar_dados = st.sidebar.checkbox('Carregar Dados')  #  caixa de carregar dados  #

            if carregar_dados == 1:  #Se carregar dados for True então faça#
                st.subheader('Dados')
                dados = st.dataframe(df) #Mostra o dataframe de df com seus especificos dados #
                stock_select = st.sidebar.checkbox #    #

        except Exception as e:
            st.error(e)  
#----------------------------------------------------------------#