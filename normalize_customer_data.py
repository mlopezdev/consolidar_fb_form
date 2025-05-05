import pandas as pd
import os
import glob
from typing import List, Dict
import re
import io
import chardet
import shutil
from datetime import datetime

def normalize_phone_number(phone: str) -> str:
    """
    Normaliza el número de teléfono eliminando 'p:' y otros caracteres no deseados
    """
    if pd.isna(phone):
        return ''
    phone = str(phone)
    # Eliminar 'p:' y cualquier otro carácter no numérico
    phone = re.sub(r'^p:', '', phone)
    phone = re.sub(r'[^\d+]', '', phone)
    return phone

def clean_column_name(col: str) -> str:
    """
    Limpia y normaliza el nombre de una columna
    """
    # Eliminar BOM y caracteres especiales
    col = col.replace('\ufeff', '').strip()
    
    # Reemplazar caracteres especiales comunes
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N',
        '¿': '', '?': '', '¡': '', '!': '',
        '_': ' '
    }
    
    for old, new in replacements.items():
        col = col.replace(old, new)
    
    # Convertir a minúsculas y reemplazar espacios múltiples
    col = col.lower().strip()
    col = re.sub(r'\s+', '_', col)
    
    return col

def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de las columnas para unificar formatos
    """
    # Diccionario de mapeo de nombres de columnas comunes
    column_mapping = {
        'telefono': 'phone_number',
        'phone': 'phone_number',
        'celular': 'phone_number',
        'cel': 'phone_number',
        'phone_number': 'phone_number',
        'nombre': 'name',
        'nombres': 'name',
        'full_name': 'name',
        'apellido': 'last_name',
        'apellidos': 'last_name',
        'email': 'email',
        'correo': 'email',
        'direccion': 'address',
        'ciudad': 'city',
        'en_que_ciudad_vives': 'city',
        'departamento': 'state',
        'estado': 'state',
        'pais': 'country',
        'platform': 'platform',
        'por_que_deseas_estudiar_este_programa': 'reason',
        'sobre_este_programa': 'program_interest',
        'created_time': 'created_time',
        'id': 'id'
    }
    
    # Limpiar nombres de columnas
    df.columns = [clean_column_name(col) for col in df.columns]
    
    # Aplicar el mapeo de nombres de columnas
    df = df.rename(columns=column_mapping)
    
    return df

def detect_encoding(file_path: str) -> str:
    """
    Detecta la codificación del archivo usando chardet
    """
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def read_csv_with_encoding(file_path: str) -> pd.DataFrame:
    """
    Lee el archivo CSV detectando la codificación y el separador
    """
    try:
        # Detectar la codificación del archivo
        encoding = detect_encoding(file_path)
        print(f"Codificación detectada: {encoding}")
        
        # Leer el archivo como texto
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        
        # Detectar el separador
        first_line = content.split('\n')[0]
        if '\t' in first_line:
            sep = '\t'
        elif ';' in first_line:
            sep = ';'
        else:
            sep = ','
        
        # Procesar el contenido con pandas
        df = pd.read_csv(io.StringIO(content), sep=sep, skipinitialspace=True)
        print(f"Archivo leído exitosamente con separador '{sep}'")
        return df
        
    except Exception as e:
        print(f"Error al leer el archivo: {str(e)}")
        raise Exception(f"No se pudo leer el archivo {file_path}")

def ensure_processed_dir() -> str:
    """
    Asegura que existe el directorio de archivos procesados
    """
    processed_dir = 'procesados'
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    return processed_dir

def move_to_processed(file_path: str, processed_dir: str) -> None:
    """
    Mueve un archivo al directorio de procesados con timestamp
    """
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f"{name}_{timestamp}{ext}"
    new_path = os.path.join(processed_dir, new_filename)
    shutil.move(file_path, new_path)
    print(f"Archivo movido a: {new_path}")

def load_consolidated_base() -> pd.DataFrame:
    """
    Carga el archivo base consolidado si existe
    """
    base_file = 'consolidated_customers.csv'
    if os.path.exists(base_file):
        try:
            df = pd.read_csv(base_file)
            print(f"Archivo base cargado: {base_file} ({len(df)} registros)")
            return df
        except Exception as e:
            print(f"Error al cargar el archivo base: {str(e)}")
    return pd.DataFrame()

def process_csv_files() -> None:
    """
    Procesa todos los archivos CSV en el directorio actual
    """
    # Asegurar que existe el directorio de procesados
    processed_dir = ensure_processed_dir()
    
    # Cargar el archivo base consolidado
    consolidated_df = load_consolidated_base()
    
    # Asegurar tipos de datos consistentes en el archivo base
    if not consolidated_df.empty:
        if 'phone_number' in consolidated_df.columns:
            consolidated_df['phone_number'] = consolidated_df['phone_number'].astype(str).apply(normalize_phone_number)
        if 'email' in consolidated_df.columns:
            consolidated_df['email'] = consolidated_df['email'].astype(str).str.lower()
        if 'name' in consolidated_df.columns:
            consolidated_df['name'] = consolidated_df['name'].astype(str).str.lower()
    
    # Buscar todos los archivos CSV en el directorio actual
    csv_files = glob.glob('*.csv')
    csv_files = [f for f in csv_files if f not in ['consolidated_customers.csv']]  # Excluir el archivo consolidado
    
    if not csv_files:
        print("No se encontraron archivos CSV nuevos para procesar.")
        return
    
    # Lista para almacenar todos los DataFrames nuevos
    new_dfs = []
    
    # Procesar cada archivo CSV
    for file in csv_files:
        try:
            print(f"\nProcesando archivo: {file}")
            df = read_csv_with_encoding(file)
            
            # Normalizar nombres de columnas
            df = normalize_column_names(df)
            
            # Asegurar tipos de datos consistentes
            if 'phone_number' in df.columns:
                df['phone_number'] = df['phone_number'].astype(str).apply(normalize_phone_number)
            if 'email' in df.columns:
                df['email'] = df['email'].astype(str).str.lower()
            if 'name' in df.columns:
                df['name'] = df['name'].astype(str).str.lower()
            
            new_dfs.append(df)
            print(f"Archivo {file} procesado exitosamente")
            print(f"Número de registros en este archivo: {len(df)}")
            print("Columnas encontradas:", ", ".join(df.columns))
            
            # Mover el archivo a procesados
            move_to_processed(file, processed_dir)
            
        except Exception as e:
            print(f"Error procesando el archivo {file}: {str(e)}")
    
    if not new_dfs:
        print("No se pudo procesar ningún archivo nuevo.")
        return
    
    # Concatenar los nuevos DataFrames
    new_data = pd.concat(new_dfs, ignore_index=True)
    
    # Mostrar información sobre las columnas nuevas
    print("\nColumnas en los nuevos datos:")
    for col in new_data.columns:
        print(f"- {col}: {new_data[col].nunique()} valores únicos")
    
    # Si hay datos consolidados previos, verificar duplicados
    if not consolidated_df.empty:
        # Eliminar duplicados basados en columnas clave
        duplicate_columns = ['email', 'phone_number', 'name']
        available_columns = [col for col in duplicate_columns if col in new_data.columns]
        
        if not available_columns:
            print("\nAdvertencia: No se encontraron columnas para identificar duplicados")
            available_columns = new_data.columns.tolist()
        
        # Encontrar duplicados con el archivo base
        duplicates = new_data.merge(consolidated_df, on=available_columns, how='inner')
        if not duplicates.empty:
            print(f"\nSe encontraron {len(duplicates)} registros duplicados con el archivo base")
            # Eliminar duplicados de los nuevos datos
            new_data = new_data.drop_duplicates(subset=available_columns)
            new_data = new_data[~new_data.index.isin(duplicates.index)]
    
    # Concatenar con el archivo base
    consolidated_df = pd.concat([consolidated_df, new_data], ignore_index=True)
    
    # Eliminar duplicados finales
    duplicate_columns = ['email', 'phone_number', 'name']
    available_columns = [col for col in duplicate_columns if col in consolidated_df.columns]
    
    if not available_columns:
        print("\nAdvertencia: No se encontraron columnas para identificar duplicados")
        available_columns = consolidated_df.columns.tolist()
    
    original_count = len(consolidated_df)
    consolidated_df = consolidated_df.drop_duplicates(subset=available_columns)
    duplicates_removed = original_count - len(consolidated_df)
    
    # Guardar el resultado
    output_file = 'consolidated_customers.csv'
    consolidated_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\nArchivo consolidado guardado como: {output_file}")
    print(f"Total de registros antes de eliminar duplicados: {original_count}")
    print(f"Duplicados eliminados (basado en {', '.join(available_columns)}): {duplicates_removed}")
    print(f"Total de registros únicos final: {len(consolidated_df)}")

if __name__ == "__main__":
    process_csv_files() 