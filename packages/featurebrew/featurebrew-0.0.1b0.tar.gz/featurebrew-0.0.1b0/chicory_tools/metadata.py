import shutil
import sqlite3
import json
import os
import pandas as pd

from chicory_tools.api_config import initialize_services
from chicory_tools.s3 import AmazonS3, S3Downloader


def create_tables_json(input_path, output_file, dataset_name):
    tables_jsons = []
    tables_json = {}

    # Check if input_path is a SQLite database
    # if input_path.endswith('.sqlite'):
    if os.path.isdir(input_path) and any(file.endswith('.sqlite') for file in os.listdir(input_path)):
        tables_json = process_sqlite_db(input_path, dataset_name)

    # Check if input_path is a folder containing CSV files
    elif os.path.isdir(input_path) and any(file.endswith('.csv') for file in os.listdir(input_path)):
        tables_json = process_csv_xlsx_folder(input_path, dataset_name)

    # Check if input_path is a folder containing Excel (XLSX) files
    elif os.path.isdir(input_path) and any(file.endswith('.xlsx') for file in os.listdir(input_path)):
        tables_json = process_csv_xlsx_folder(input_path, dataset_name)

    else:
        print("Invalid input path or format.")
        return

    tables_jsons.append(tables_json)

    with open(output_file, "w") as f:
        json.dump(tables_jsons, f, indent=4)

def process_sqlite_db(db_path, dataset_name):
    if os.path.isdir(db_path):
        for root, _, files in os.walk(db_path):
            for file in files:
                if file.endswith(('.sqlite')):
                    db_path = os.path.join(db_path, file)
                    break

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get database name
    cursor.execute("SELECT name FROM sqlite_master WHERE type='database'")
    # db_name = cursor.fetchone()[0]

    # Get table names and columns
    tables = []
    table_names = []
    table_names_original = []
    column_names = []
    column_names_original = []
    column_types = []
    foreign_keys_candidates = []
    foreign_keys = []
    primary_keys = []

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names_original = [row[0] for row in cursor.fetchall()]

    column_names.insert(0, [-1, "*"])
    column_names_original.insert(0, [-1, "*"])
    column_types.insert(0, "TEXT")
    table_col_dict = {}
    overall_col_counter = 1
    total_column_count = 0
    max_column_count = 0

    for i, table_name in enumerate(table_names_original):
        table_names.append(table_name.lower().replace('_', ' '))
        columns = []
        columns_original = []
        cursor.execute(f"PRAGMA table_info('{table_name}')")
        column_count = 0

        for j, row in enumerate(cursor.fetchall()):
            column_name = row[1]
            column_type = row[2]
            is_primary_key = row[5]

            columns.append([overall_col_counter, column_name])
            columns_original.append([overall_col_counter, column_name])
            column_names.append([i, column_name.lower().replace('_', ' ')])
            column_names_original.append([i, column_name])
            column_types.append(column_type)
            if is_primary_key:
                primary_keys.append(overall_col_counter)
            table_col_dict[f"{table_name}.{column_name}"] = overall_col_counter
            overall_col_counter += 1
            column_count += 1

        total_column_count += column_count
        if column_count > max_column_count:
            max_column_count = column_count

        cursor.execute(f"PRAGMA foreign_key_list('{table_name}')")
        for row in cursor.fetchall():
            foreign_key = [f"{table_name}.{row[3]}", f"{row[2]}.{row[4]}"]
            foreign_keys_candidates.append(foreign_key)

    for foreign_keys_candidate in foreign_keys_candidates:
        (from_var, to_var) = foreign_keys_candidate
        from_var_index = table_col_dict[from_var]
        to_var_index = table_col_dict[to_var]
        foreign_keys.append([from_var_index, to_var_index])

    conn.close()

    table_count = len(table_names_original)
    avg_column_count = total_column_count / table_count if table_count else 0

    return {
        "db_id": dataset_name,
        "table_names": table_names,
        "table_names_original": table_names_original,
        "column_names": column_names,
        "column_names_original": column_names_original,
        "column_types": column_types,
        "foreign_keys": foreign_keys,
        "primary_keys": primary_keys,
        "table_count": table_count,
        "max_column_count": max_column_count,
        "total_column_count": total_column_count,
        "avg_column_count": avg_column_count
    }


def process_csv_xlsx_folder(folder_path, dataset_name):
    tables = []
    table_names = []
    table_names_original = []
    column_names = []
    column_names_original = []
    column_types = []

    total_column_count = 0
    max_column_count = 0

    for file in os.listdir(folder_path):
        if file.endswith('.csv') or file.endswith('.xlsx'):
            table_name = os.path.splitext(file)[0]
            table_names.append(len(table_names))
            table_names_original.append(table_name)

            if file.endswith('.csv'):
                df = pd.read_csv(os.path.join(folder_path, file))
            elif file.endswith('.xlsx'):
                df = pd.read_excel(os.path.join(folder_path, file))

            columns = []
            columns_original = []
            column_count = 0
            for i, column in enumerate(df.columns):
                columns.append([i, column])
                columns_original.append([i, column])
                column_names.append([len(table_names) - 1, column.lower().replace('_', ' ')])
                column_names_original.append([len(table_names) - 1, column])
                column_types.append(str(df[column].dtype))
                column_count += 1

            total_column_count += column_count
            if column_count > max_column_count:
                max_column_count = column_count

            tables.append({
                "table_name": len(table_names) - 1,
                "columns": columns,
                "columns_original": columns_original
            })

    column_names.insert(0, [-1, "*"])
    column_names_original.insert(0, [-1, "*"])

    table_count = len(table_names_original)
    avg_column_count = total_column_count / table_count if table_count else 0

    return {
        "db_id": dataset_name,
        "table_names": table_names,
        "table_names_original": table_names_original,
        "column_names": column_names,
        "column_names_original": column_names_original,
        "column_types": column_types,
        "tables": tables,
        "foreign_keys": [],
        "primary_keys": [],
        "table_count": table_count,
        "max_column_count": max_column_count,
        "total_column_count": total_column_count,
        "avg_column_count": avg_column_count
    }


def create_dataset_metadata_json(source_type, persist_path, dataset_id, source_path):
    """
    :return:
    """
    dataset_info = {
        "ds_id": dataset_id,
        "type": None,
        # "query": query_w_context,
        "sources": {
            "type": source_type,
            "paths": []
        }
    }

    for root, _, files in os.walk(source_path):
        for file in files:
            if file.endswith(('.csv', '.xlsx', '.sqlite')):
                file_type = file.split('.')[-1]
                if dataset_info["type"] is None:
                    dataset_info["type"] = file_type
                dataset_info["sources"]["paths"].append({file: os.path.join(root, file)})

    dataset_json_path = os.path.join(persist_path, "datasets", dataset_id, 'dataset.json')
    with open(dataset_json_path, 'w') as json_file:
        json.dump(dataset_info, json_file, indent=4)

    return dataset_info


def _set_env(services):
    s3_aws_access_key_id = services["integration"]["s3"]["aws_access_key_id"]
    s3_aws_secret_access_key = services["integration"]["s3"]["aws_secret_access_key"]
    os.environ['AWS_ACCESS_KEY_ID'] = s3_aws_access_key_id
    os.environ['AWS_SECRET_ACCESS_KEY'] = s3_aws_secret_access_key
    os.environ['USER_AGENT'] = 'chicory-ai-feature-brew-agent'

    s3_openai_api_key = services["system"]["openai"]["open_api_key"]
    os.environ['OPENAI_API_KEY'] = s3_openai_api_key

    s3_openai_model = services["system"]["openai"]["model"]
    os.environ['MODEL'] = s3_openai_model

    storage_path = services["system"]["persistence"]["storage_path"]
    os.environ['STORAGE_PATH'] = storage_path


def amazon_s3_object_list(dataset_id, services, source_bucket):
    s3_svc = AmazonS3(services['integration']['s3']['aws_access_key_id'], services['integration']['s3']['aws_secret_access_key'])
    s3_downloader = S3Downloader(services['integration']['s3']['aws_access_key_id'], services['integration']['s3']['aws_secret_access_key'])
    persist_data_path = services['system']['persistence']['storage_path']
    object_list = {}

    # for bucket in s3_buckets:
    files = s3_svc.list_files(source_bucket)
    if 'Contents' in files:
        for file in files['Contents']:
            if 'Key' in file:
                path = file['Key']
                if "log" in path:
                    continue
                object_dict = s3_downloader.download_dir(source_bucket, path,
                                                         f"{persist_data_path}/datasets/{dataset_id}/source",
                                                         mock_download_dir=False)
                for obj_key, obj_val in object_dict.items():
                    if obj_val != "":
                        object_list[obj_key] = obj_val

    return object_list


def copy_files(src_folder, dst_folder, extensions, dataset_id):
    # Check if the source folder exists
    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return

    # Create the destination folder if it does not exist
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    # Check if the source path is a file or a directory
    if os.path.isfile(src_folder):
        # If it's a file, return it in a list if it has the correct extension
        files = [os.path.basename(src_folder)] if src_folder.endswith(extensions) else []
    else:
        # If it's a directory, list all files in the directory
        # files = [os.path.join(src_folder, file) for file in os.listdir(src_folder) if file.endswith(extensions)]
        files = os.listdir(src_folder)

    # Filter and copy files with the specified extensions
    for file in files:
        if file.endswith(extensions):
            if os.path.isfile(src_folder):
                src_file = src_folder
            else:
                src_file = os.path.join(src_folder, file)
            if file.endswith(".sqlite"):
                dst_file = os.path.join(dst_folder, dataset_id + ".sqlite")
            else:
                dst_file = os.path.join(dst_folder, file)
            shutil.copy2(src_file, dst_file)  # copy2 preserves metadata
            print(f"Copied: {src_file} to {dst_file}")

def create_dataset_metadata(dataset_id, datasource, services):
    """

    :param dataset_id:
    :param datasource:
    :param chicory_config:
    :return:
    """

    persist_path = os.getenv('STORAGE_PATH')
    os.makedirs(os.path.join(persist_path, "datasets"), exist_ok=True)
    os.makedirs(os.path.join(persist_path, "datasets", dataset_id), exist_ok=True)
    os.makedirs(os.path.join(persist_path, "datasets", dataset_id, "source"), exist_ok=True)
    os.makedirs(os.path.join(persist_path, "datasets", dataset_id, "rules"), exist_ok=True)

    persist_data_path = services['system']['persistence']['storage_path']

    if "s3://" in datasource:
        object_list = amazon_s3_object_list(dataset_id, services, datasource)
        create_dataset_metadata_json("s3", persist_path, dataset_id, f"{persist_data_path}/datasets/{dataset_id}/source")
        # for identifier, local in object_list.items():
    else:
        extensions = ('.xlsx', '.csv', '.sqlite')
        copy_files(datasource, f"{persist_data_path}/datasets/{dataset_id}/source", extensions, dataset_id)
        create_dataset_metadata_json("local", persist_path, dataset_id, f"{persist_data_path}/datasets/{dataset_id}/source")

    create_tables_json(f"{persist_data_path}/datasets/{dataset_id}/source",
                            f"{persist_data_path}/datasets/{dataset_id}/tables.json", dataset_id)


if __name__ == "__main__":
    dataset_name = "ml-dataset-internal"
    # Example usage
    # create_tables_json("database.sqlite", "tables.json", dataset_name)
    # create_tables_json("csv_folder", "tables.json", dataset_name)
    # create_tables_json("xlsx_folder", "tables.json", dataset_name)
    services = initialize_services("/Users/sarkarsaurabh.27/Documents/Projects/chicoryai/resources/chicory-config.yaml")
    _set_env(services)
    create_dataset_metadata(dataset_name, "/Users/sarkarsaurabh.27/Documents/Projects/chicoryai/data/di/datasets",
                            services)

    # create_dataset_metadata(dataset_name, "/Users/sarkarsaurabh.27/Documents/Projects/chicoryai/data/datasets/spider/database/perpetrator/perpetrator.sqlite",
    #                         "/Users/sarkarsaurabh.27/Documents/Projects/chicoryai/resources/chicory-config.yaml")
