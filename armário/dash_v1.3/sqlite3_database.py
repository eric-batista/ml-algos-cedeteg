def sql_data_to_df(table_name):
    """
    -> Função que retorna um dataframe importado da função iee_b3 do arquivo web_scrapping
    -> Esses dados são inseridos em uma tabela SQL e transformados em um dataframe novamente
    -> Desta forma fazemos o processamento dos dados nesta função e não no dashboard
    :param table_name: nome da tabela que será criada no database
    :return: retorna um dataframe com os novos dados
    """
    
    # ╔════════════════════════════════════════════════════════════════════════════════════════════╗ 
    # ║ Importação das bibliotecas                                                                 ║
    # ╚════════════════════════════════════════════════════════════════════════════════════════════╝
    import sqlite3
    import pandas as pd
    import web_scrapping as ws
    
    # ╔════════════════════════════════════════════════════════════════════════════════════════════╗ 
    # ║ Atribui ao dataframe 'df' os dados obtidos da função 'iee_b3' do arquivo web_scrapping     ║
    # ╚════════════════════════════════════════════════════════════════════════════════════════════╝
    df = ws.iee_b3()
    
    # ╔════════════════════════════════════════════════════════════════════════════════════════════╗ 
    # ║ Função que estabelece uma conexão com o banco de dados passando o nome do banco como       ║
    # ║ parâmetro                                                                                  ║
    # ╚════════════════════════════════════════════════════════════════════════════════════════════╝
    def connect_database(database_name):
        return sqlite3.connect(f'{database_name}')
    
    # ╔════════════════════════════════════════════════════════════════════════════════════════════╗ 
    # ║ Atribui a variável 'conn' os dados obtidos da função descrita acima                        ║
    # ║ Será criado um banco de dados com o nome que foi passado como parâmetro                    ║
    # ╚════════════════════════════════════════════════════════════════════════════════════════════╝
    conn = connect_database('dash_database')
    
    # ╔════════════════════════════════════════════════════════════════════════════════════════════╗ 
    # ║ Transforma os dados do dataframe em uma tabela do banco                                    ║
    # ║ O nome da tabela é passada como parâmetro na chamada da função                             ║
    # ╚════════════════════════════════════════════════════════════════════════════════════════════╝
    df.to_sql(name=f'{table_name}', con=conn, if_exists='replace')
    
    # ╔════════════════════════════════════════════════════════════════════════════════════════════╗ 
    # ║ Passamos a consulta em SQL que queremos dentro da variável 'query'                         ║
    # ║ Neste caso efetuamos uma consulta que retorna todos os dados presentes na tabela           ║
    # ╚════════════════════════════════════════════════════════════════════════════════════════════╝
    query = f"""
                SELECT *
                FROM {table_name};
            """

    # ╔════════════════════════════════════════════════════════════════════════════════════════════╗ 
    # ║ Retornamos os dados da tabela no banco para um novo dataframe                              ║
    # ║ Desta forma, conseguimos retornar o mesmo dataframe obtido com a função 'iee_b3'           ║
    # ╚════════════════════════════════════════════════════════════════════════════════════════════╝
    df = pd.read_sql(query, con=conn, index_col="index")
    
    # ╔════════════════════════════════════════════════════════════════════════════════════════════╗ 
    # ║ Encerra a conexão com o banco de dados, desta forma evitando o desperdício de memória      ║
    # ╚════════════════════════════════════════════════════════════════════════════════════════════╝
    conn.close()
    
    # ╔════════════════════════════════════════════════════════════════════════════════════════════╗ 
    # ║ Retornamos um dataframe com os dados recém obtidos, porém assim o trabalho 'pesado' é      ║
    # ║ feito pela função e não pelo dashboard                                                     ║
    # ╚════════════════════════════════════════════════════════════════════════════════════════════╝
    return df