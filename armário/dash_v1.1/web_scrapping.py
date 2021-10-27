def iee_b3():
    '''Funca para importar dados do site da B3 sobre a ibov, os dados no fim serão organizados em um dataframe para podermos usá-los futuramente'''
    # Importando bibliotecas
    from selenium import webdriver # Usado para importar os dados da url
    import time # usado para gerar um tempo de espera enquanto se utiliza o selenium
    from bs4 import BeautifulSoup # manipular o html
    import pandas as pd # criar a DF que será trabalhada
    from selenium.webdriver.chrome.options import Options
    
    # definindo a url da b3
    url = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IEEX?language=pt-br"
    
    # iniciando o webdriver, que deve estar com o driver na pasta do arquivo para funcionar, nesse caso será utilizado do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    
    # Entrando na url informada
    browser.get(url)
    browser.find_element_by_id('segment').send_keys('Setor de Atuação')
    time.sleep(.5)
    html = browser.page_source

    browser.close() 
    
    # Usando o beatiful soup e convertendo o arquivo para podermos selecionar os dados que precisamos
    bs = BeautifulSoup(html, 'html.parser')
    
    # Criando as listas onde iremos armazenar os dados do html
    setor, cod, acao, tipo, qtde_t, part, part_a = [], [], [], [], [], [], []
    
    # Usando a função find_all para selecionarmos apenas 'td' que contém os dados que usaremos e armazenando eles na variável linhas
    linhas = bs.find_all('td')
    
    # Criando uma variável que será usada no while loop abaixo
    i = 0
    
    # While loop para podermos armazenar os dados em suas respectivas colunas, onde:
    # temos 7 colunas então pegamos o primeiro elemento 0 e somando 1 até chegarmos ao último elemento para a coluna [i+6] = ao setimo elemento
    # por fim somando 7 para pularmos para a próxima linhas e seguir a lógica
    # o loop só irá para quando o número de linhas for maior do que o que os dados apresentados, para isso usados o lógica len(linhas) que nos entrega a quantia de dados
    # e como i é somado de 7 a cada iteração o loop só irá para quando todos os dados forem indexidaodos nas suas devidas colunas
    while i < (len(linhas)):
        setor.append(linhas[i].text)
        cod.append(linhas[i+1].text)
        acao.append(linhas[i+2].text)
        tipo.append(linhas[i+3].text)
        qtde_t.append(linhas[i+4].text)
        part.append(linhas[i+5].text)
        part_a.append(linhas[i+6].text)
        i += 7
        
    # Criando um df para armazearmos os dados    
    df = pd.DataFrame({'Setor': setor[:-1],
                  'Acao': cod[:-1],
                  'Empresa': acao[:-1],
                  'Qntd_teorica': qtde_t[:-1],
                  'Part_%': part[:-1]}) # filtramos para eliminar as últimas linhas, pois a b3 entrega uma soma ao final que não queremos
    # Separando os setores e subsetores em colunas
    df['SubSetor'] = df['Setor'].apply(lambda s: s[s.rfind('/')+1:].strip())
    df['Setor'] = df['Setor'].apply(lambda s: s[:s.rfind('/')])
    
    # Convertendo os valores de string para int
    df['Qntd_teorica'] = df['Qntd_teorica'].apply(lambda s: s.replace(".", ""))
    df['Qntd_teorica'] = pd.to_numeric(df['Qntd_teorica'])
    df['Part_%'] = df['Part_%'].apply(lambda s: s.replace(",", ""))
    df['Part_%'] = pd.to_numeric(df['Part_%'])/1000
    df.sort_values('Part_%', ascending = False, inplace = True)
    
    # Criando uma colunas com a % acumulada
    df['Part_%_acum'] = df['Part_%'].cumsum()
    
    # Resetando o index
    df.reset_index(drop = True, inplace = True)
    
    # fim
    return df

def import_ibov():
    '''Funca para importar dados do site da B3 sobre a ibov, os dados no fim serão organizados em um dataframe para podermos usá-los futuramente'''
    # Importando bibliotecas
    from selenium import webdriver # Usado para importar os dados da url
    import time # usado para gerar um tempo de espera enquanto se utiliza o selenium
    from bs4 import BeautifulSoup # manipular o html
    import pandas as pd # criar a DF que será trabalhada
    from selenium.webdriver.chrome.options import Options

    # definindo a url da b3
    url = "https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br"
    
    # iniciando o webdriver, que deve estar com o driver na pasta do arquivo para funcionar, nesse caso será utilizado do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)    
    # Entrando na url informada
    browser.get(url)
    
    # Encontrando o elemento no html para filtrarmos os dados que precisamos
    browser.find_element_by_id('segment').send_keys('Setor de Atuação')
    
    # Aguardando 1 segundo para a página atualizar
    time.sleep(1)
    
    # Agora selecionando o o menu para podermos ver todas as ações disponíveis
    browser.find_element_by_id('selectPage').send_keys('120')
    
    # Aguardando 1 segundo para o página atualizar
    time.sleep(1)
    
    # IMportando o html inteiro para o Python na variável html
    html = browser.page_source
    
    # Fechando o navegador
    browser.close() 
    
    # Usando o beatiful soup e convertendo o arquivo para podermos selecionar os dados que precisamos
    bs = BeautifulSoup(html, 'html.parser')
    
    # Criando as listas onde iremos armazenar os dados do html
    setor, cod, acao, tipo, qtde_t, part, part_a = [], [], [], [], [], [], []
    
    # Usando a função find_all para selecionarmos apenas 'td' que contém os dados que usaremos e armazenando eles na variável linhas
    linhas = bs.find_all('td')
    
    # Criando uma variável que será usada no while loop abaixo
    i = 0
    
    # While loop para podermos armazenar os dados em suas respectivas colunas, onde:
    # temos 7 colunas então pegamos o primeiro elemento 0 e somando 1 até chegarmos ao último elemento para a coluna [i+6] = ao setimo elemento
    # por fim somando 7 para pularmos para a próxima linhas e seguir a lógica
    # o loop só irá para quando o número de linhas for maior do que o que os dados apresentados, para isso usados o lógica len(linhas) que nos entrega a quantia de dados
    # e como i é somado de 7 a cada iteração o loop só irá para quando todos os dados forem indexidaodos nas suas devidas colunas
    while i < (len(linhas)):
        setor.append(linhas[i].text)
        cod.append(linhas[i+1].text)
        acao.append(linhas[i+2].text)
        tipo.append(linhas[i+3].text)
        qtde_t.append(linhas[i+4].text)
        part.append(linhas[i+5].text)
        part_a.append(linhas[i+6].text)
        i += 7
        
    # Criando um df para armazearmos os dados    
    df = pd.DataFrame({'Setor': setor[:-1],
                  'Acao': cod[:-1],
                  'Empresa': acao[:-1],
                  'Qntd_teorica': qtde_t[:-1],
                  'Part_%': part[:-1]}) # filtramos para eliminar as últimas linhas, pois a b3 entrega uma soma ao final que não queremos
    # Separando os setores e subsetores em colunas
    df['SubSetor'] = df['Setor'].apply(lambda s: s[s.rfind('/')+1:].strip())
    df['Setor'] = df['Setor'].apply(lambda s: s[:s.rfind('/')])
    
    # Convertendo os valores de string para int
    df['Qntd_teorica'] = df['Qntd_teorica'].apply(lambda s: s.replace(".", ""))
    df['Qntd_teorica'] = pd.to_numeric(df['Qntd_teorica'])
    df['Part_%'] = df['Part_%'].apply(lambda s: s.replace(",", ""))
    df['Part_%'] = pd.to_numeric(df['Part_%'])/1000
    df.sort_values('Part_%', ascending = False, inplace = True)
    
    # Criando uma colunas com a % acumulada
    df['Part_%_acum'] = df['Part_%'].cumsum()
    
    # Resetando o index
    df.reset_index(drop = True, inplace = True)
    
    # fim
    return df

def import_ind(acao):
    """Acao será o nome da ação, deverá ser passada em formato de srt(entre ""). Serão devolvidos dois DataFrames, o primeiro sendo todos os indicadores e o segundo contendo alguns indicadores chaves da empresa"""

    #Importando bibliotecas necessárias
    from selenium import webdriver # Usado para importar os dados da url
    import time # usado para gerar um tempo de espera enquanto se utiliza o selenium
    from bs4 import BeautifulSoup # manipular o html
    import pandas as pd # criar a DF que será trabalhada
    from datetime import date # extrair ano atual
    import warnings
    warnings.filterwarnings("ignore")

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Definindo a url que será usada no web scrapping
    url = f"https://statusinvest.com.br/acoes/{acao.lower()}"

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Iniciando o webdriver (o qual deve estar configurado no computador)

    browser = webdriver.Chrome()

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Entrando na url informada
    browser.get(url)

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Aguardando 2 segundos para a página ser carregada
    time.sleep(3)

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Encontrando o elemento no xpath para podermos mudar seu valor e podermos selecionar o filtro para podermos ter acesso a informações mais completas
    element = browser.find_elements_by_xpath('/html/body/main/div[2]/div/div[6]/div[1]/div/button[2]/div/span')

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Para termos certeza que o elemento será selecionado é criado um for loop para validar a seleção
    for i in element: i.click()

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Aguardando meio segundo para a página atualizar a seleção
    time.sleep(.5)   

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Selecionando agora o elemento para obtermos o maior conjunto de dados históricos possível
    element = browser.find_elements_by_xpath('/html/body/main/div[2]/div/div[6]/div[3]/div[1]/div[2]/div[2]/ul/li[2]/a')

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Como feito anteriormente aqui usamos um for loop para validarmos que será selecionada a opção do xpath

    for i in element: i.click()

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Aguardamos novamente meio segundo para a página atualizar o conteúdo
    time.sleep(.5)

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Agora extraímos toda a url e salvamos ela na variável 'html'
    html = browser.page_source

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Fechando o navegador
    browser.close() 

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Usando o beatiful soup e convertendo o arquivo para podermos selecionar os dados que precisamos
    bs = BeautifulSoup(html, 'html.parser')



    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Usando a função find_all do BeatifulSoup para encontrarmos todos os valores dentro do div na classe que precisamos,
    # a classe foi selecionada em uma análise do html da página para identificar qual a classe em que os dados necessários estavam
    cols = bs.find_all('div', class_='th w-100') # contém os anos de cada tabela
    lines = bs.find_all('div', class_='td w-100') # contém todos os dados de todas as tabelas

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Convertendo os dados de html das colunas para str
    cols_data = []
    for coluna in cols:  cols_data.append(coluna.text)

    lines_data = []
    for i in lines: lines_data.append(i.text)   

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Criando um whiel loop para identificarmos os interválos onde temos a palavra 'ATUAL' para assim substituirmos ela pelo ano atual
    while True:
        i = 0
        interval = []
        while i < len(lines):
            try: 
                if cols_data.index('ATUAL', i) == i: # aqui é verificado se 'ATUAL' está no index na posição i, se for verdade ele salva a posição
                    interval.append(i)
            except ValueError: # se a verificação não for verdadeira ele irá somar 1 no loop e não irá salvar a posição
                break 
            i += 1
        break

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Usando o argumento anterior iremos criar duas variáveis x e y onde:
    # bgn = início do intervalo dos anos nas colunas
    # end = final do intervalor dos anos nas colunas
    # Assim obtemos os intervalos onde os anos estão
    while True:
        i = 0
        bgn = []
        end = []
        try:
            while i < len(interval):
                bgn.append(interval[i]), end.append(interval[i+1]) #usamos 'bgn' como o inicial em intervalos e 'end' com i+1 para pegarmos o final do intervalo
                i += 1
            break
        except IndexError:
            end.append(len(lines)) # como vamos encontrar um erro no loop usamos esse erro para o ultimo valor em 'end' ser o lenght de intervalo, esse sendo o último valor para o intervalo
        break

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Alterando a coluna chamada 'ATUAL' para o ano atual    
    for i in interval: cols_data[i] = str(date.today().year)

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Criando uma variável cols_table que contém todos os anos pela numeração das colunas (de 1 a 5)
    cols_table = {}
    for i in range(1, len(bgn)+1): cols_table[f'{i}'] = cols_data[bgn[i-1]:end[i-1]]

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Criando um dicionário que irá conter todas as informações
    obj = {}
    for i in range(1, len(max(cols_table.values()))+1): obj[max(cols_table.values())[i-1]] = []

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    #Criando um while loop para inserir todas os dados conforme necessário, se adaptando ao formato do site e número de anos por coluna
    while True:
        _a = 0 # variável para limite de iterações
        _b = 0 # variável para definição do início do range que será usado
        _1 = (len(cols_table['1']))*14 # variável da quantia de dados a serem importados da tabela 1
        _2 = (len(cols_table['2']))*6 + _1 # variável da quantia de dados a serem importados da tabela 1
        _3 = (len(cols_table['3']))*4 + _2 # variável da quantia de dados a serem importados da tabela 2
        _4 = (len(cols_table['4']))*4 + _3 # variável da quantia de dados a serem importados da tabela 3
        _5 = (len(cols_table['5']))*2 + _4 # variável da quantia de dados a serem importados da tabela 4

        # iteração na primeira tabela
        while _a < len(obj): # definindo que o código irá percorrer todas as colunas e indexar os valores
            obj[f'{max(cols_table.values())[_a]}'].append(lines_data[_b: _1 :(len(cols_table['1']))] if _a+1 <= len(cols_table['1']) else [0*i for i in range(14)])

            # 1.0 -> temos acima a função  obj[f'{max(cols_table.values())[_a]}'] que irá trazer o elemento _a do dicionário obj, onde:
                # max(cols_table.values())[_a] nos entrega o range máximo de anos que podemos ter no site;

            # 2.0 -> usamos append para inserir os valores onde:

                # 2.1 -> (lines_data[_b: _1 :(len(cols_table['1']))] if _a+1 <= len(cols_table['1']) else [0*i for i in range(14)]);

                    # 2.1.1 -> (lines_data[_b: _1 :(len(cols_table['1']))], onde:

                        # 2.1.1.1 -> pegamos a lista 'lines_data' e determinamos o range ['inicio', 'fim', 'intervalo']:
                            # 2.1.1.1.1 -> bgn = _b, conforme definimos acima será o reponsável pelo ínicio do range;
                            # 2.1.1.1.2 -> end = _1, conforme definimos acima será o reponsável pelo fim do range;
                            # 2.1.1.1.3 -> intervalo = (len(cols_table['1'])), entrega a quantia de colunhas da tabela, 
                                            #assim indexando somente os elementos pertencentes a coluna da iteração

                    # 2.1.2 -> usamos if para case a table aque estamos trabalhando tenha um shape diferente das demais 
                                        #(estamos adotando o maior comprimento de colunas para criarmos o df futuramente)

                    # 2.1.3 -> _a+1 <= len(cols_table['1']) else [0*i for i in range(14)], onde:
                        # 2.1.3.1 ->  _a+1 <= len(cols_table['1']) nos entrega a lógica para verificarmos se a coluna da iteração possui dados

                    # 2.1.4 -> else [0*i for i in range(14)], caso o argumento acima seja falso ele irá retornar 0 vezes a quantia de lines para a coluna não informar dados incorretos
                        # 2.1.4.1 -> 14 se dá pela quantia de features na tabela, por isso será a única constante que temos
            _a += 1
            _b += 1

        # Os seguintes while loops seguem a mesma lógica do primeiro, onde somente estão mudando para cada tabela
        _a = 0
        _b = _1     
        while _a < len(obj):
            obj[f'{max(cols_table.values())[_a]}'].append(lines_data[_b: _2 :(len(cols_table['2']))] if _a+1 <= len(cols_table['2']) else [0*i for i in range(6)])
            _a += 1
            _b += 1

        _a = 0
        _b = _2     
        while _a < len(obj):
            obj[f'{max(cols_table.values())[_a]}'].append(lines_data[_b: _3 :(len(cols_table['3']))] if _a+1 <= len(cols_table['3']) else [0*i for i in range(4)])
            _a += 1
            _b += 1    

        _a = 0
        _b = _3     
        while _a < len(obj):
            obj[f'{max(cols_table.values())[_a]}'].append(lines_data[_b: _4 :(len(cols_table['4']))] if _a+1 <= len(cols_table['4']) else [0*i for i in range(4)])
            _a += 1
            _b += 1  

        _a = 0
        _b = _4     
        while _a < len(obj):
            obj[f'{max(cols_table.values())[_a]}'].append(lines_data[_b: _5 :(len(cols_table['5']))] if _a+1 <= len(cols_table['5']) else [0*i for i in range(2)])
            _a += 1
            _b += 1      
        break 
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #

    for i in max(cols_table.values()): obj[f'{i}'].append([acao.upper()])

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Definindo nome dos indicadores
    indicadores = ['DY', 'PL','PEG_RATIO', 'P_PV', 'EV_EBITIDA', 'EV_EBIT', 'P_EBITIDA', 'P_EBIT',
          'VPA', 'P_ATIVO', 'LPA', 'S_SR', 'P_CAP_GIRO', 'P_ATIVO_CIRC_LIQ', 'DIV_LIQUIDA_PL',
          'DIV_LIQUIDA_EBITIDA', 'DIV_LIQUIDA_EBIT', 'PL_ATIVOS', 'PASSIVOS_ATIVOS', 'LIQ_CORRENTE',
          'M_BRUTA', 'M_EBITIDA', 'M_EBIT', 'M_LIQUIDA', 'ROE', 'ROA', 'ROIC', 'GIRO_ATIVOS',
          'CAGR_RECEITAS_5_ANOS', 'CAGR_LUCROS_5_ANOS']

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Criando um dicionário com os indicadores
    ind = {'indicadores':indicadores}

    # Usando a função update na variável ind para criarmos um dicionário com as informações
    ind.update({ f'{i}':obj[f'{i}'][0] + obj[f'{i}'][1] + obj[f'{i}'][2] + obj[f'{i}'][3] + obj[f'{i}'][4] for i in max(cols_table.values())})
        # Usamos um for loop dentro do update para indexarmos os valores no dicionário iterando nas colunas

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Criando o dataframe    
    df = pd.DataFrame(ind) 
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # Retorna outros indicadores em um novo DF
    
    # Criando uma lista para anexarmos os valores
    res = []
    
    # Iterando na lista para termos somente os valores em formato de texto
    for i in bs.find_all('strong', class_='value'): res.append(i.text)
    
    # Criando uma lista com os indicadores
    ind_2 = ['patrimonio_liquido', 'ativos', 'ativo_circulante', 'divida_bruta', 'disponibilidade', 'divida_liquida', 'valor_de_mercado', 'valor_de_firma', 'n_total_de_papeis', 'segmento_de_listagem', 'free_float']
    
    # Iterando na lista para anexar os valores nos indicadores apropriados
    while True:
        x = 0
        obj_2 = {}
        while x < len(ind_2):
            obj_2[ind_2[x]] = res[res.index('\n\n\n()\n\n')+1+x:res.index('\n\n\n()\n\n')+2+x]
            # acima usa-se a funação index() para identificarmos em qual posição está o elemento ('\n\n\n()\n\n') na lista,
            # pois o que o segue será o valor que buscamos.
            x += 1
        break

    # Transformamos a lista em um DF
    df_2 = pd.DataFrame(obj_2)    
    
    # Retorna os DFs
    return df, df_2