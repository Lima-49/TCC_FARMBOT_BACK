import pyodbc

class ConfiguracoesTarefasRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        
    def connect(self):
        return pyodbc.connect(self.connection_string)
    
    def add_new_config_job(self, config_tarefa):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO CONFIG_TAREFAS (
                    ID_CLIENTE, TIPO_TAREFA, PRODUTO_DESCR, FORNECEDOR_DESCR,
                    QTD_MINIMA, OFERTA_DESCR, FL_ATIVO, FL_EXECUCAO
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    config_tarefa.id_cliente,         # INT
                    config_tarefa.tipo_tarefa,        # INT
                    config_tarefa.produto_descr,      # VARCHAR
                    config_tarefa.fornecedor_descr,   # VARCHAR
                    config_tarefa.qtd_minima,         # INT
                    config_tarefa.oferta_descr,       # VARCHAR
                    config_tarefa.fl_ativo,           # INT
                    config_tarefa.fl_execucao         # INT
                )
            )
            conn.commit()
            
    def get_config_jobs(self, client_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT
                    ID_CONFIG_TAREFA AS id_config_tarefa,
                    ID_CLIENTE AS id_cliente,
                    TIPO_TAREFA AS tipo_tarefa,
                    PRODUTO_DESCR AS produto_descr,
                    FORNECEDOR_DESCR AS fornecedor_descr,
                    QTD_MINIMA AS qtd_minima,
                    OFERTA_DESCR AS oferta_descr,
                    FL_ATIVO AS fl_ativo,
                    FL_EXECUCAO AS fl_execucao
                FROM
                    CONFIG_TAREFAS
                WHERE
                    ID_CLIENTE = ?
                """,(client_id)
            )
            
            configs = []
            
            for row in cursor.fetchall():
                config_data = {
                    'id_config_tarefa': row[0],
                    'id_cliente': row[1],
                    'tipo_tarefa': row[2],
                    'produto_descr': row[3],
                    'fornecedor_descr': row[4],
                    'qtd_minima': row[5],
                    'oferta_descr': row[6],
                    'fl_ativo': row[7],
                    'fl_execucao': row[8]
                }
                
                configs.append(config_data)
                
            return configs