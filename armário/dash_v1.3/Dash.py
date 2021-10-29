import builtins
from logging import _STYLES
from os import path
from time import sleep
from ipython_genutils.py3compat import with_metaclass
from numpy import select
import streamlit as st
import investpy as ip
from datetime import datetime, timedelta, date
import plotly.graph_objs as go
import plotly.express as px
from streamlit.legacy_caching.caching import cache
from streamlit.proto.PlotlyChart_pb2 import Figure
from web_scrapping import iee_b3, import_ibov, import_ind
from volatility import ind_graph
from sql_teste import sql_data_to_df
#----------------------------------------------------------------#
#                         Variaveis                              #
#----------------------------------------------------------------#
countries = ['brazil', 'united states']
intervals = ['Daily', 'Weekly', 'Monthly']

# data de inicio para o grafico de candle  no caso diminuiu 30 dias #
start_date = datetime.today()-timedelta(days=30)
end_date = datetime.today()                      # end sendo a data de hoje #
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#               função que importa os dados da B3                #
#----------------------------------------------------------------#
#  @cache para poder puxar os dados apenas uma vez #
#   função que puxa os dados da B3    #

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
@st.cache
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
        x=df.index,
        y=df['Close'])]
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
@st.cache
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

def Dash_2(iee):
    st.sidebar.title('Menu 📰 De Notícias  ')
    st.sidebar.markdown('---')
    st.markdown('---')

    # stock_select_side = st.sidebar.selectbox("Selecione o ativo:", )

    col1, col2, = st.columns(2)
    container2 = st.container()
    col_side1, col_side2 = st.sidebar.columns(2)

    container3 = st.container()
    container4 = st.container()

    # df1, df2 = import_ind(iee[iee.Empresa == stock_select].loc[0][1])
    stock_select = st.selectbox("Selecione o ativo:", [i for i in iee.Empresa])

    with col1:
        from_date = st.date_input(
            'De:', value=start_date, min_value=date(2006, 1, 1))
    with col2:
        to_date = st.date_input('Para:', end_date)

    #with col_side1: # Coluna sidebar 1#
    container4 = st.container()

    options2 = st.sidebar.multiselect(
        'Escolha as ações', iee.Acao, ['ALUP11', 'TRPL4', 'CPFE3', 'ELET3'])
    #st.sidebar.write('You selected:', options2)
    with col_side1:
        st.metric(
            label='Ação: ' + options2[0], value='', delta='')
        st.metric(
            label='Ação: ' + options2[1], value='', delta='')
    with col_side2:
        st.metric(
            label='Ação: ' + options2[2], value='', delta='')
        st.metric(
            label='Ação: ' + options2[3], value='', delta='')

    my_expander_side2 = st.sidebar.expander(label='Example Bottons')
    with my_expander_side2:
        if st.button('Say hello'):
            st.write('Why hello there')
        else:
            st.write('Goodbye')
        genre = st.radio("What's your favorite movie genre",
                         ('Comedy', 'Drama', 'Documentary'))
        if genre == 'Comedy':
            st.write('You selected comedy.')
        else:
            st.write("You didn't select comedy.")
        age = st.slider('How old are you?', 0, 130, 25)
        st.write("I'm ", age, 'years old')
        title = st.text_input('Movie title', 'Life of Brian')
        st.write('The current movie title is', title)

    #iee[iee.Empresa == stock_select].Acao.values[0]#
    fig1, fig2, tabel = ind_graph(
        iee[iee.Empresa == stock_select].Acao.values[0]+'.SA', str(from_date), str(to_date))

    # with container4:
    #    for l in iee.Acao:
    #        st.sidebar.metric(label="[l]")
    # st.sidebar.metric(label=print(l))
    #        sleep(2)

    with container2:
        st.markdown('---')

    if from_date > to_date:
        st.error('Data de ínicio maior do que data final')
    else:
        df = consultar_acao(iee[iee.Empresa == stock_select].Acao.values[0], 'brazil', format_date(
            from_date), format_date(to_date), 'Daily')
        try:
            fig = Graftest(df)
            grafico_candle = st.plotly_chart(fig2, use_container_width=True)
            grafico_linha = st.plotly_chart(
                fig1, use_container_width=False, height=1000, width=1000)
            st.markdown('---')
            st.dataframe(tabel)
            

        except Exception as e:
            st.error(e)


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
iee = iee_b3()  # carregadno dados  da função iE #

# variavel dash recebe uma lista de dash  #
dash = ['Dash 1', 'Dash 2', 'Dash 3']

# newDash recebe um seletor de caixa  #
newDash = st.sidebar.selectbox('Selecione o  Dash', dash)
formatacao1 = st.sidebar.markdown("---")
#----------------------------------------------------------------#


#----------------------------------------------------------------#
#------------------------- dash main ----------------------------#
#----------------------------------------------------------------#
# if que é usado para fazer um novo dash    #
if newDash == 'Dash 2':
    Dash_2(iee)  # Função Dash 2#
elif newDash == 'Dash 3':
    dash_3()    # Função Dash 3
#   Caso contrario motrar o dash 1   #
else:
    barra_lateral = st.sidebar.title('Menu 🌫️ ')
    barra_lateral = st.sidebar.empty()
    formatacao1 = st.sidebar.markdown("---")
    # menu_expander = st.sidebar.expander()
    col_head1, col_head2 = st.columns(2)

    # stock select recebe um seletor de ativo  #
    stock_select = st.selectbox("Selecione o ativo:", [i for i in iee.Empresa])
    formatacao13 = st.markdown("---")

    my_expander_side = st.sidebar.expander(label='Datas')
    with my_expander_side:
        from_date = st.date_input(
            'De:', start_date, min_value=date(2006, 1, 1))
        to_date = st.date_input('Para: ', end_date)

    interval_select = st.sidebar.selectbox("Selecione o intervalo:", intervals)
    formatacao2 = st.sidebar.markdown("---")
    grafico_line = st.empty()  # Grafico de linha  recebendo vazio   #
    grafico_candle = st.empty()  # Grafico de candle recebendo vazio   #
    grafico_pizza = st.empty()  # Grafico de pizza recebendo vazio    #
    if from_date > to_date:  # Se from data for maior que to date  #
        st.sidebar.error('Data de ínicio maior do que data final')
    else:
        df = consultar_acao(iee[iee.Empresa == stock_select].Acao.values[0], 'brazil', format_date(
            from_date), format_date(to_date), interval_select)  # dataframa recebe a função consultar ação com da iee  com as datas selecionada  #
        try:
            container = st.container()
            # fig recebe a função que mostra o grafico de
            fig = plotCandleStick(df)
            with container:
                # with col_head1:
                # figurapizza com a variavel stock_select que foi selecionada pelo usuario  #
                figpizza = sun_b(stock_select)
                # Grafico de pizza usando a variavel figpizza em que o dataframe foi transformado em figura#
                grafico_pizza = st.plotly_chart(
                    figpizza, use_container_width=True)
                # with col_head2:
                grafico_candle = st.plotly_chart(fig, use_container_width=True)
                carregar_dados = st.sidebar.checkbox('Carregar Dados')
            #grafico_line = st.line_chart(df.Close)  #pegando apenas os dados de df.Close para usar no grafico de linhas#

            container = st.container()
            # with container:
            #    grafico_candle = st.plotly_chart(fig, use_container_width=True)     # plotando o grafico de candle  #
            #    carregar_dados = st.sidebar.checkbox('Carregar Dados')  #  caixa de carregar dados  #

            if carregar_dados == 1:  # Se carregar dados for True então faça#
                st.subheader('Dados')
                # Mostra o dataframe de df com seus especificos dados #
                dados = st.dataframe(df)
                stock_select = st.sidebar.checkbox

        except Exception as e:
            st.error(e)
#----------------------------------------------------------------#
