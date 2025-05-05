# Normalización de Datos de Clientes

Este script procesa múltiples archivos CSV con datos de clientes, normaliza la información y maneja duplicados.

## Características

- Detecta automáticamente la codificación de los archivos CSV
- Normaliza nombres de columnas (ej: 'telefono', 'teléfono', 'phone' → 'phone_number')
- Limpia números de teléfono (elimina 'p:' y caracteres no numéricos)
- Maneja archivos con diferentes separadores (coma o tabulador)
- Mueve los archivos procesados a un directorio 'procesados' con timestamp
- Genera dos archivos de salida:
  - `consolidated_customers.csv`: Contiene todos los registros históricos
  - `new_customers.csv`: Contiene solo los registros nuevos del último procesamiento

## Detección de Duplicados

El script identifica duplicados basándose en las siguientes columnas:
- email
- phone_number

Si un registro nuevo tiene el mismo email o número de teléfono que uno existente en el archivo consolidado, se considera duplicado y solo se guarda en el archivo consolidado.

## Uso

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Colocar los archivos CSV a procesar en el mismo directorio que el script

3. Ejecutar el script:
```bash
python normalize_customer_data.py
```

## Estructura de Archivos

- `normalize_customer_data.py`: Script principal
- `requirements.txt`: Dependencias del proyecto
- `consolidated_customers.csv`: Archivo con todos los registros históricos
- `new_customers.csv`: Archivo con solo los registros nuevos del último procesamiento
- `procesados/`: Directorio donde se mueven los archivos procesados

## Notas

- Los archivos procesados se mueven automáticamente al directorio 'procesados' con un timestamp
- El script mantiene un historial completo en `consolidated_customers.csv`
- Los registros nuevos (sin duplicados) se guardan en `new_customers.csv`
- Se recomienda hacer backup del archivo consolidado antes de procesar nuevos archivos

## Proceso de Lectura de Archivos CSV

El script implementa un proceso robusto para manejar archivos CSV con diferentes codificaciones y formatos:

1. **Lectura Binaria y Detección de Codificación**:
   ```python
   def detect_encoding(file_path: str) -> str:
       with open(file_path, 'rb') as file:
           raw_data = file.read()
       result = chardet.detect(raw_data)
       return result['encoding']
   ```
   - Primero se lee el archivo en modo binario
   - Se utiliza `chardet` para detectar automáticamente la codificación
   - Esto permite manejar archivos UTF-8, UTF-16, Latin-1, etc.

2. **Detección de Separadores**:
   ```python
   # Detectar el separador
   first_line = content.split('\n')[0]
   if '\t' in first_line:
       sep = '\t'
   elif ';' in first_line:
       sep = ';'
   else:
       sep = ','
   ```
   - Se analiza la primera línea para detectar el separador
   - Soporta tabulaciones, punto y coma, y comas
   - Evita problemas con archivos exportados de diferentes fuentes

3. **Manejo de BOM (Byte Order Mark)**:
   - Se elimina el BOM automáticamente durante la normalización de columnas
   - Previene problemas con archivos exportados desde Excel

4. **Proceso de Lectura Segura**:
   ```python
   try:
       encoding = detect_encoding(file_path)
       with open(file_path, 'r', encoding=encoding) as f:
           content = f.read()
       df = pd.read_csv(io.StringIO(content), sep=sep)
   ```
   - Lectura en dos pasos para mayor control
   - Uso de `StringIO` para procesar el contenido en memoria
   - Manejo de errores robusto

## Manejo de Columnas

El script normaliza automáticamente los siguientes nombres de columnas:

- Teléfono: `telefono`, `phone`, `celular`, `cel` → `phone_number`
- Nombre: `nombre`, `nombres`, `full_name` → `name`
- Correo: `email`, `correo` → `email`
- Ciudad: `ciudad`, `city` → `city`
- Y otros campos comunes...

## Proceso de Normalización

1. **Detección de Codificación**:
   - Detecta automáticamente la codificación del archivo (UTF-8, UTF-16, etc.)
   - Maneja diferentes separadores (coma, tab, punto y coma)

2. **Normalización de Datos**:
   - Números de teléfono: Elimina prefijos y caracteres especiales
   - Emails: Convierte a minúsculas
   - Nombres: Normaliza formato y convierte a minúsculas

3. **Manejo de Duplicados**:
   - Verifica duplicados contra el archivo consolidado existente
   - Elimina duplicados basándose en email y teléfono
   - Se considera duplicado si el email O el teléfono coinciden
   - Mantiene el registro más reciente en caso de duplicados

## Notas Importantes

- Los archivos originales se conservan en la carpeta `procesados/` con timestamp
- El archivo consolidado (`consolidated_customers.csv`) contiene solo los registros del último procesamiento
- Se recomienda hacer respaldo del archivo consolidado periódicamente si se necesita mantener un historial

## Manejo de Errores

El script maneja varios tipos de errores comunes:
- Archivos con diferentes codificaciones
- Columnas faltantes o con nombres diferentes
- Valores nulos o mal formateados
- Problemas de codificación de caracteres

## Contribución

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request 