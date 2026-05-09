import boto3
import psycopg2
import csv

# --- CONFIGURACIÓN DE TU BASE DE DATOS ---
DB_HOST = "localhost"
DB_NAME = "universidad"
DB_USER = "tu_usuario"
DB_PASS = "tu_password"
DB_PORT = "5432"

# --- CONFIGURACIÓN DE AWS ACADEMY (Copia de "AWS Details") ---
ACCESS_KEY = 'ASIAXYKJVVDMV7IJ6OUS'
SECRET_KEY = 'LEIJho9RcPKkyvIBd9GyBM9K1F54OhnUeEBhf2k0'
SESSION_TOKEN = 'IQoJb3JpZ2luX2VjECAaCXVzLXdlc3QtMiJGMEQCICOQN9/J5x7HbmpDVkWjjXocYSkkYbdT9333nIby9fL9AiAy0igscwQ6d82l74ihCJXfDjYjBjxB29jPyqCwm1+5WCq7Agjp//////////8BEAAaDDUzMzI2NzMyNzE5MyIMXx/EpS1H1bX+ZB0TKo8CcTlmxpgC3lCFuHz6nGRKpMDHhStr1VPm63I/hgfbtbDj1MXgbk+hkinLE8h075zjWnBh5MzC2A8EAfFs0iaISU2+vy/ugzweYbuaZ4tI0SR9xVJzH3TW1IzPX20qs085GBgX4/aKyOWEVsWmRpdK6GWMGFpcpbbnFpWOg9hj4D37i46M3aeK5cWUfrnhzbZPlZ0/Uds4X3rG5D1AkVn/256fSGJpIQdDLnkvnf92bmzFpQHcv2CZfkkTO1CkV75JA4Dks2qnPJ3r+k+e6eM5BYJPn8+B5EuueU4QKZhgESXqvmxmwiYhbE1q87zYzgnrnAl/1u8+7ZHzy9POConi7V+jrDigxjzLYmPW/wnuczDdrv3PBjqeAbFAargQbSR/myqSidRlSXQPkeMYeVKbfdrC2wSvVBG0FB7ulnf8xDsK7LQefmESJYsHedSIN+OfAW3DWAGVA61FQSXcJ7GGbAmtDCTDjA4+SiNMM/bXy1DqBVQnpaNUwnhOl5LEuOvDtVE3UMiICxJSqE4IucweBJhkjCgNL86ZSMRkxZKZ08DDkQXbD0zwxy100PuC5Tae0aDM8Mrf'
BUCKET_NAME = "jlts-output-011"

def ejecutar_reto():
    try:
        # 1. Conectar a la base de datos
        print("Conectando a la base de datos...")
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # 2. Extraer datos de la tabla alumnos
        cursor.execute("SELECT * FROM alumnos")
        filas = cursor.fetchall()

        # 3. Guardar en un archivo CSV local
        fichero_csv = "datos_extraidos.csv"
        with open(fichero_csv, "w", newline="") as f:
            writer = csv.writer(f)
            # Escribir las cabeceras de las columnas
            writer.writerow([i[0] for i in cursor.description])
            # Escribir los datos
            writer.writerows(filas)
        
        print(f"Archivo {fichero_csv} creado exitosamente.")

        # 4. Subir el archivo a S3
        print("Subiendo a AWS S3...")
        s3 = boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            aws_session_token=SESSION_TOKEN,
            region_name='us-east-1'
        )

        s3.upload_file(fichero_csv, BUCKET_NAME, fichero_csv)
        print(f"¡Reto cumplido! Archivo subido al bucket: {BUCKET_NAME}")

    except Exception as e:
        print(f"Hubo un error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    ejecutar_reto()
