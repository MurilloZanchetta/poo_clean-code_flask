import pymysql
from pymysql.cursors import DictCursor
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

class DBConnection(ABC):
    
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close_connection(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass


class MySQLConnection(DBConnection):
    
    def __init__(self):
        
        self.host = os.environ['MYSQL_HOST']
        self.user = os.environ['MYSQL_USER']
        self.password = os.environ['MYSQL_PASSWORD']
        self.db = os.environ['MYSQL_DB']
        self.connection = None

    def connect(self):
        
        if not self.connection:
            try:
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    db=self.db,
                    cursorclass=DictCursor
                )
                logging.info("Conexão bem-sucedida com o MySQL!")
            except Exception as e:
                logging.error(f"Erro ao conectar ao banco de dados: {e}")
                self.connection = None

    def close_connection(self):

        if self.connection:
            self.connection.close()
            self.connection = None
            logging.info("Conexão fechada.")

    def get_connection(self):

        if self.connection is None:
            self.connect()
        return self.connection


### OCP - Open/Closed Principle ###
class BaseDAO(ABC):

    
    def __init__(self, connection, table_name):
        """Inicializa o DAO base com a conexão e o nome da tabela"""
        self.connection = connection
        self._table_name = table_name

    @abstractmethod
    def create_table(self):

        pass

    def insert(self, data):

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {self._table_name} ({columns}) VALUES ({placeholders})"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, tuple(data.values()))
            self.connection.commit()
        except Exception as e:
            logging.error(f"Erro ao inserir dados na tabela '{self._table_name}': {e}")
            raise

    def get_all(self):

        query = f"SELECT * FROM {self._table_name}"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Erro ao buscar registros na tabela '{self._table_name}': {e}")
            return []

    def delete_by_id(self, record_id):

        query = f"DELETE FROM {self._table_name} WHERE id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (record_id,))
            self.connection.commit()
        except Exception as e:
            logging.error(f"Erro ao deletar registro da tabela '{self._table_name}': {e}")
            raise


class PessoaDAO(BaseDAO):


    def __init__(self, connection):

        super().__init__(connection, os.environ['TABLE_NAME'])

    def create_table(self):

        query = f"""
        CREATE TABLE IF NOT EXISTS {self._table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            idade INT NOT NULL
        )
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            logging.error(f"Erro ao criar tabela: {e}")
            raise

    def insert_pessoa(self, nome, idade):

        self.insert({'nome': nome, 'idade': idade})

    def get_all_pessoas(self):

        return self.get_all()

    def delete_pessoa(self, pessoa_id):

        self.delete_by_id(pessoa_id)
