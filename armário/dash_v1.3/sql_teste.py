def sql_data_to_df():
    import sqlite3
    import pandas as pd
    import web_scrapping as ws
    
    df = ws.iee_b3()
    
    def connect_database():
        return sqlite3.connect('dash_database')
    
    conn = connect_database()
    
    df.to_sql(name='iee_b3_table', con=conn, if_exists="replace")
    query = """
            SELECT *
            FROM iee_b3_table;
        """

    df = pd.read_sql(query, con=conn, index_col="index")
    
    conn.close()
    
    return df