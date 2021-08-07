import numpy as np 
import pandas as pd
from sklearn.svm import LinearSVC 
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import MetaTrader5 as mt
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.linear_model import Lasso
import warnings 
warnings.filterwarnings('ignore')

#### aqui tamos importando o arquivo ####
df = pd.read_csv('wdo_2019_2020.csv', delimiter = '\t').rename(columns = {'<DATE>': 'data', '<OPEN>': 'Open', '<HIGH>': 'High', '<LOW>': 'Low', '<CLOSE>':'Close'}).drop(columns = ['<TICKVOL>', '<VOL>', '<SPREAD>',])

#### atualizando a data ####
df.data = pd.to_datetime(df.data)

#### ta puchando uma DataFrame para y_data ###

y_data = pd.DataFrame()
trade_logic = []


#### X_data recebe no cado colunas de tipos como abertura presços altos e baixos e o fechamento #####
X_data = df[['Open', 'High', 'Low', 'Close']]
y_data = df['Close'] = df['Close'].shift(-1)


#####################################################
#### Aqui ta fazendo os sinais do trade logic ou seja dando o sinal para o robo #####
for i in range(len(X_data['Close'])):
    if X_data['Close'][i] > y_data['Close'][i]:
        trade_logic.append(1)
    elif X_data['Close'][i] < y_data['Close'][i]:
        trade_logic.append(0)
    else:
        trade_logic.append(-1)
        
X_data['Signal'] = trade_logic  

#####################################
#### Pega um sinal da um drop  para poder testar o modele #####

y = X_data['Signal']

X = X_data.drop('Signal', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3369, random_state=42)

##### aqui no caso pega o penutimo elemento do fechamento e compara suas média assim cria uma nova coluna pro target   ####
for i in  range(1,len (X)):
    if X['Close'].iloc[i-1] < X['EMA'].iloc[i-1] and X['EMA'].iloc[i] > X['Close'].iloc[i]:
        X['target'].iloc[i] = 1
    elif X['Close'].iloc[i - 1] > X['EMA'].iloc[i] and X['EMA'].iloc[i] < X['Close'].iloc[i]:
        X['target'].iloc[i] =0
    else:
        X['target'].iloc[i] = -2     
y = pd.DataFrame()

lasso = Lasso()
lasso.fit(X_train,y_train)

y_predict_lasso = lasso.predict(np.array(X_test))

lasso.score(X_test,y_test) 

print(f'Mean_Squared_ERROR: {mean_squared_error(np.array(y_test), y_predict_lasso)}')

#########################################
#### se metaTrader inicializar A conecção #####

if not mt.initialize():
    mt.shutdown()
else:
    print(f'Connected')

#########################################
## Definindo a função compra ####

def buy():
    price = mt.symbol_info_tick('WINQ21').ask

    sl  = price - 200.0*mt.symbol_info('WDO$N').point
    tp  = price + 200.0*mt.symbol_info('WDO$N').point

    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": "WDO$N",
        "volume": float(1.0),
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
################################################
## definindo a função venda     ######

def sell():
    price = mt.symbol_info_tick('WDO$N').bid

    sl  = price + 200.0*mt.symbol_info('WDO$N').point
    tp  = price - 200.0*mt.symbol_info('WDO$N').point

    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": "WINQ21",
        "volume": float(1.0),
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

####################################################
#### pega os valores do meta trader     #####

last_price = mt.copy_rates_from_pos('WDO$N', mt.TIMEFRAME_D1, 0, 1)
open_price = last_price[0][1] # Open
high_price = last_price[0][2] # High
low_price = last_price[0][3]  # Low
close_price = last_price[0][4] # Close

prices = [open_price, high_price, low_price, close_price]

while True:
    predict_result = lasso.predict([prices])

    if mt.positions_get(symbol="WDO$N") == ():
        if predict_result == 1:
            buy()
        elif predict_result == 0:
            sell()
        else:
            print('Nao pode dar predict')  