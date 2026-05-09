import boto3
import psycopg2
import csv

# 1. Configuración (Tus datos de casa)
DB_HOST = "localhost"
DB_NAME = "universidad"
DB_USER = "tu_usuario"
DB_PASS = "tu_password"
DB_PORT = "5432"

# 2. AWS Academy (Actualiza estas llaves si ya pasaron más de 2 horas)
ACCESS_KEY = 'TU_ACCESS_KEY'
SECRET_KEY = 'TU_SECRET_KEY'
SESSION_TOKEN = 'TU_SESSION_TOKEN'
BUCKET_NAME = "jlts-output-011"

try:
    # --- PASO A: EXTRAER ---
    print("Conectando a PostgreSQL local...")
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumnos")
    filas = cursor.fetchall()

    # --- PASO B: TRANSFORMAR A CSV ---
    fichero_csv = "datos_extraidos.csv"
    with open(fichero_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([i[0] for i in cursor.description]) # Cabeceras
        writer.writerows(filas)
    print(f"Éxito: Se extrajeron {len(filas)} registros al archivo CSV.")

    # --- PASO C: CARGAR A S3 ---
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, aws_session_token=SESSION_TOKEN)
    s3.upload_file(fichero_csv, BUCKET_NAME, fichero_csv)
    print(f"Éxito: Archivo subido al bucket {BUCKET_NAME}")

except Exception as e:
    print(f"Error en el proceso: {e}")
finally:
    if 'conn' in locals(): conn.close()
