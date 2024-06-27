import json
from abc import abstractmethod, ABC

import psycopg2
from google.cloud import bigquery


class DatabaseConnector(ABC):
    @abstractmethod
    def get_table_info(self):
        pass

    @abstractmethod
    def get_columns_info(self, table):
        pass

    @abstractmethod
    def get_low_cardinality_columns(self, table, threshold=10):
        pass

    @abstractmethod
    def get_table_logs(self):
        pass

    @abstractmethod
    def get_total_table_count(self):
        pass

    @abstractmethod
    def get_table_name_list(self):
        pass

    @abstractmethod
    def get_df_from_table(self, table):
        pass

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)


class RedshiftConnector(DatabaseConnector):
    def __init__(self, dbname, user, password, host, port):
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cursor = self.connection.cursor()

    def get_table_info(self):
        self.cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');
        """)
        return self.cursor.fetchall()

    def get_columns_info(self, table):
        self.cursor.execute(f"""
            SELECT column_name, data_type, is_nullable, character_maximum_length, numeric_precision, numeric_scale
            FROM information_schema.columns
            WHERE table_name = '{table}';
        """)
        return self.cursor.fetchall()

    def get_low_cardinality_columns(self, table, threshold=10):
        self.cursor.execute(f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{table}';
        """)
        columns = [row[0] for row in self.cursor.fetchall()]

        low_cardinality_columns = {}
        for column in columns:
            self.cursor.execute(f"""
                SELECT COUNT(DISTINCT {column})
                FROM {table};
            """)
            if self.cursor.fetchone()[0] <= threshold:
                self.cursor.execute(f"""
                    SELECT DISTINCT {column}
                    FROM {table};
                """)
                low_cardinality_columns[column] = [row[0] for row in self.cursor.fetchall()]
        return low_cardinality_columns

    def get_table_logs(self):
        # Implement method to fetch table/query logs if applicable
        return "Redshift table/query logs not implemented"

    def get_total_table_count(self):
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');
        """)
        return self.cursor.fetchone()[0]

    def get_table_name_list(self):
        self.cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');
        """)
        return [row[0] for row in self.cursor.fetchall()]

    def get_df_from_table(self, table):
        query = f"SELECT * FROM {table};"
        return pd.read_sql_query(query, self.connection)

    def __del__(self):
        self.cursor.close()
        self.connection.close()


class BigQueryConnector(DatabaseConnector):
    def __init__(self):
        self.client = bigquery.Client()

    def get_table_info(self):
        datasets = list(self.client.list_datasets())
        tables_info = []
        for dataset in datasets:
            tables = list(self.client.list_tables(dataset.dataset_id))
            for table in tables:
                tables_info.append((dataset.dataset_id, table.table_id))
        return tables_info

    def get_columns_info(self, table):
        dataset_id, table_id = table.split('.')
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = self.client.get_table(table_ref)
        return [(field.name, field.field_type, field.mode) for field in table.schema]

    def get_low_cardinality_columns(self, table, threshold=10):
        dataset_id, table_id = table.split('.')
        query = f"""
            SELECT column_name
            FROM `{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
            WHERE table_name = '{table_id}';
        """
        columns = [row['column_name'] for row in self.client.query(query).result()]

        low_cardinality_columns = {}
        for column in columns:
            query = f"""
                SELECT COUNT(DISTINCT {column}) as distinct_count
                FROM `{dataset_id}.{table_id}`;
            """
            result = self.client.query(query).result().to_dataframe()
            if result['distinct_count'][0] <= threshold:
                query = f"""
                    SELECT DISTINCT {column}
                    FROM `{dataset_id}.{table_id}`;
                """
                values = [row[column] for row in self.client.query(query).result()]
                low_cardinality_columns[column] = values
        return low_cardinality_columns

    def get_table_logs(self):
        # Implement method to fetch table/query logs if applicable
        return "BigQuery table/query logs not implemented"

    def get_total_table_count(self):
        query = """
            SELECT COUNT(*)
            FROM `project_id.region-us`.INFORMATION_SCHEMA.TABLES
            WHERE table_type = 'BASE TABLE';
        """
        query_job = self.client.query(query)
        return query_job.result().to_dataframe().iloc[0, 0]

    def get_table_name_list(self):
        query = """
            SELECT table_name
            FROM `project_id.region-us`.INFORMATION_SCHEMA.TABLES
            WHERE table_type = 'BASE TABLE';
        """
        query_job = self.client.query(query)
        return [row['table_name'] for row in query_job.result()]

    def get_df_from_table(self, table):
        query = f"SELECT * FROM `{table}`;"
        return self.client.query(query).to_dataframe()
