# Importações de bibliotecas

from sklearn.model_selection import train_test_split
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np

import MetaTrader5 as mt

import warnings
warnings.filterwarnings('ignore') # Ignorar os warnings do código

# Definição das variáveis de entrada
ativo = 'PETR3' # ou PETR4
lote = 100 # minimo de 100 para ações (1 para mercado fracionário)

# Ler os dados dentro de um data frame         dropar algumas colunas, considerando apenas OHLC
df = pd.read_csv(f'./Data/{ativo}_Daily_data.csv').drop(columns = ['Tickvol', 'Vol', 'Spread'])

df['Date'] = pd.to_datetime(df['Date'])
df['Adj Close'] = df['Close']

# Definição da função do indicador
# Média Móvel curta de 9 períodos e de 10 períodos

trade_logic = []

def moving_average(df):
    dados = df.copy()

    dados['MA9'] = dados['Adj Close'].rolling(9).mean()
    dados['MA10'] = dados['Adj Close'].rolling(10).mean()

    dados = dados.dropna()

    for i in range(len(dados)):
        if dados['MA9'].iloc[i-1] < dados['MA10'].iloc[i-1] and \
        dados['MA9'].iloc[i] > dados['MA10'].iloc[i]:
            trade_logic.append(1)
        elif dados['MA9'].iloc[i-1] > dados['MA10'].iloc[i-1] and \
        dados['MA9'].iloc[i] < dados['MA10'].iloc[i]:
            trade_logic.append(0)
        else:
            trade_logic.append(-1)
        
    dados['Signal'] = trade_logic
        
    return dados
	
# Definindo as variáveis de treino e de teste

df = moving_average(df)

y = df['Signal']
X = df.drop('Signal', axis=1)
                                                            #.3369 = 2 anos de treino e 1 ano de teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3369, random_state=42)

# Definição do modelo RidgeClassifier

rc = RidgeClassifier()
rc.fit(X_train, y_train)
y_pred_rc = rc.predict(np.array(X_test))

rc.score(X_test, y_test)

print(f'Mean_Squared_ERROR: {mean_squared_error(np.array(y_test), y_pred_rc)}')

# Conecxão com o Meta Trader 5

mt.initialize()
mt.terminal_info()

print('Connected')
    
dados = pd.DataFrame()
rates = mt.copy_rates_from_pos(ativo, mt.TIMEFRAME_M5, 0, 20)
print('Copying the values...')

mt.shutdown()
print('Desconnected')

open_price  = rates[0][1]  # Open
high_price  = rates[0][2]  # High
low_price   = rates[0][3]  # Low
close_price = rates[0][4]  # Close

# Definindo a função de Compra

def buy():
    price = mt.symbol_info_tick(ativo).ask

    sl  = price - 200.0*mt.symbol_info(ativo).point
    tp  = price + 200.0*mt.symbol_info(ativo).point

    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": ativo,
        "volume": lote,
        "type": mt.ORDER_TYPE_BUY,
        "sl": sl,
        "tp": tp,
        "magic": 124512,
        "deviation": 0,
        "comment": "Buy Order",
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_FOK,
    }

    result = mt.order_send(request)

    print(f'OrderSended buy: {result}')
	
# Definindo a função de Venda

def sell():
    price = mt.symbol_info_tick(ativo).bid
    
    sl = price + 200.0*mt.symbol_info(ativo).point
    tp = price - 200.0*mt.symbol_info(ativo).point

    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": ativo,
        "volume": lote,
        "type": mt.ORDER_TYPE_SELL,
        "sl": sl,
        "tp": tp,
        "magic": 124512,
        "deviation": 0,
        "comment": "Sell Order",
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_FOK,
    }

    result = mt.order_send(request)
    
    print(f'OrderSended sell: {result}')
	
# Efetuando as ordens de compra e de venda a mercado

mt.initialize()
prices = [open_price, high_price, low_price, close_price]
mt.initialize()

while True:
    predict_result = rc.predict([prices])

    if mt.positions_get(symbol=ativo) == ():
        if predict_result == 1:
            buy()
        elif predict_result == 0:
            sell()
        else:
            print('Can not predict')
    else:
        print('ERROR! - Financial Asset is incorrect')
    break