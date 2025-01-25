import os
import re
import hashlib
import base64
import psycopg2
from datetime import datetime
import requests


def calculate_sha256(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def is_file_processed(cursor, checksum):
    cursor.execute(f"SELECT id FROM processed_files WHERE sha256='{checksum}'")
    return cursor.fetchone()


def save_file_to_postgres(cursor, file_path, file_name, checksum, file_content_base64):
    query=f"""
        INSERT INTO processed_files (file_path, file_name, sha256, file_content_base64, processed_at)
        VALUES ('{file_path}','{file_name}','{checksum}','{str(file_content_base64)}','{datetime.now()}')
        """
    cursor.execute(query)
            
def save_scan_to_postgres(cursor, checksum, yara_matches, parser_output, scanned_at):
    query=f"""
        INSERT INTO scan_results(sha256, yara_matches, parser_output, scanned_at)
        VALUES ('{checksum}', '{str(yara_matches)}', '{str(parser_output)}', '{datetime.now()}')
        """
    cursor.execute(query)



def process_files(search_dir, db_config, api_url, override=False):
    print(f"scanning beginning in '{search_dir}'")
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    ignore_extensions = ('.zip', '.tar', '.rar','.gz','.iso')
    for root, directories, files in os.walk(search_dir):
        filtered_files = [f for f in files if not f.endswith(ignore_extensions)]
        print("scanning root '{root}'")
        for file in filtered_files:
            file_path = os.path.join(root,file)
            checksum = calculate_sha256(file_path)
            if override:
                pass
            elif is_file_processed(cursor,checksum):
                print(f"already processed '{checksum}' at '{file_path}', skipping")
                continue
            print(f"processing file {file_path}")
            with open(file_path, 'rb') as f:
                file_content = f.read()
            file_content_base64 = base64.b64encode(file_content).decode()

            try:
                response = requests.post(api_url, files={"data":open(file_path,'rb').read()})
                results = response.json()
                print(f"Api results: {results}")
            except Exception as e:
                print(f"Failed to process file '{file_path}': {e}")
                continue
            #save the file to DB
            if not override:
                save_file_to_postgres(cursor, file_path, file, checksum, file_content_base64)
            #extrapolate scan results, and save to DB
            yara_matches = [s for s in results.get('debug') if "Matched" in s]
            tab_seperated_yara_matches = "\t".join(yara_matches)
            save_scan_to_postgres(cursor, checksum, tab_seperated_yara_matches, base64.b64encode(results.get('output_text').encode("utf-8")).decode('utf-8'), datetime.now())

            print(f"File '{file}' processed")

    conn.commit()
    cursor.close()
    conn.close()



