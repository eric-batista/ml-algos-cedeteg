####importando as blibliotecas####

import pandas as pd
import numpy as np
import MetaTrader5 as mt

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#### atribuido as variaveis ####

df = pd.read_csv('DI1N_Daily_201801020000_202012300000.csv', delimiter = '\t').rename(columns = {'<DATE>': 'Data', '<OPEN>': 'Open', '<HIGH>': 'High', '<LOW>': 'Low', '<CLOSE>':'Close'}).drop(columns = ['<TICKVOL>', '<VOL>', '<SPREAD>',])
dt = DecisionTreeClassifier(criterion='gini',random_state=1)

coin = 'DI1$N' ## moeda ##
value = 1000    ## valor ##
serial = mt.TIMEFRAME_D1 
X_data = df[['Open', 'High', 'Low', 'Close']]
y_data = pd.DataFrame()
y_data['Close'] = df['Close'].shift(-1) 

y_data = pd.DataFrame()
### metodo de média simples ####
trade_logic = []

X_data = df[['Open', 'High', 'Low', 'Close']]
y_data['Close'] = df['Close'].shift(-1)

for i in range(len(X_data['Close'])):
    if X_data['Close'][i] > y_data['Close'][i]:
        trade_logic.append(1)
    elif X_data['Close'][i] < y_data['Close'][i]:
        trade_logic.append(0)
    else:
        trade_logic.append(-1)

X_data['Signal'] = trade_logic

y = X_data['Signal']
X = X_data.drop('Signal', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
  ############################
### função de treinar o robo ###
def Tuning_Traning(X,y):

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,stratify=y,random_state=1)
    
    dt.fit(X=X_train,y=y_train)
    y_pred = dt.predict(np.array(X_test))
    return y_pred

y_pred = Tuning_Traning(X,y)

def Initialize_MetaTrader():
    if not mt.initialize():
        mt.shutdown()
    else:
        print(f'Connected')

Initialize_MetaTrader()

##### função de compra #####
def Buy(coin):
    price = mt.symbol_info_tick(coin).ask
    sl = price - 200.0 * mt.symbol_info(coin).point
    tp = price + 200.0 * mt.symbol_info(coin).point

    request = {
        'action' : mt.TRADE_ACTION_DEAL,
        'symbol' : coin,
        'volume' : float(1.0),
        'sl' : sl,
        'tp' : tp,
        'magic' : 1378,
        'deviation' : 0,
        'comment' : 'Buy Order',
        'type_time' : mt.ORDER_TIME_GTC,
        'type_filling' : mt.ORDER_FILLING_FOK
    }
    result = mt.order_send(request)

    print(f'OrderSended buy: {result}')

##### função de venda #####

def Sell(coin):
    price = mt.symbol_info_tick(coin).bid
    sl = price + 200.0* mt.symbol_info(coin).point
    tp = price - 200.0* mt.symbol_info(coin).point

    request = {
        'action' : mt.TRADE_ACTION_DEAL,
        'symbol' : coin,
        'volume' : float(1.0),
        'type' : mt.ORDER_TYPE_SELL,
        'sl' : sl,
        'tp' : tp,
        'magic' : 1378,
        'deviation' : 0,
        'comment' : 'Sell Order',
        'type_time' : mt.ORDER_TIME_GTC,
        'type_filling' : mt.ORDER_FILLING_FOK
    }

    result = mt.order.order_send(request)

    print(f'OrderSended sell: {result}')   

### pregando os melhores preços ###

def Relative_Position_Market(coin,serial,value):    
    last_price_cands = mt.copy_rates_from_pos(coin,serial,0,value)
    open_price = last_price_cands[0][1]
    high_price = last_price_cands[0][2]
    low_price = last_price_cands[0][3]
    close_price = last_price_cands[0][3]
    prices = [open_price, high_price, low_price, close_price]
    
    return prices

prices = Relative_Position_Market(coin,serial,value)    

#####  Ações do robo  #####

def Robo_Action(coin):
    v_interetion = 8
    timer_b = 6
    timer_f = mt.TIMEFRAME_D1
    line_ = 3
    volum = 1000
    
    
    var = v_interetion  * 60
    from time import sleep
    
    while var != 0:    
        sleep(timer_b)
        last_price = dt.predict([prices])
        predict_result = dt.predict([prices])
        #mt.initialize()
        
        if mt.positions_get(symbol = coin) == ():
            if predict_result[-1] == 1 :
                Buy(coin)
                print("compra")
                print(predict_result[-1], '\n')
                #mt.shutdown()
                var -= x_2
                
            elif predict_result[-1] == 0 :
                Sell(coin)
                print("venda")
                #mt.shutdown()
            
            else: 
                print('nao pode dar predict')
                            
        else:
            print('Erro')
            break
Robo_Action(coin)
