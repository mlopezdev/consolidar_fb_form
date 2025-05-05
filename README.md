# Normalizador de Datos de Clientes

Este script de Python está diseñado para procesar y consolidar datos de clientes desde múltiples archivos CSV, normalizando la información y eliminando duplicados.

## Características

- Procesa automáticamente archivos CSV con diferentes codificaciones (UTF-8, UTF-16, etc.)
- Normaliza números de teléfono (elimina prefijos 'p:', espacios y caracteres especiales)
- Unifica nombres de columnas entre diferentes archivos
- Elimina registros duplicados basándose en email, teléfono y nombre
- Mantiene un historial de archivos procesados
- Genera un archivo consolidado con todos los registros únicos

## Requisitos

```bash
pip install -r requirements.txt
```

## Estructura del Proyecto

```
.
├── normalize_customer_data.py   # Script principal
├── requirements.txt            # Dependencias del proyecto
├── consolidated_customers.csv  # Archivo consolidado (generado)
└── procesados/                # Directorio de archivos procesados
```

## Uso

1. **Preparación**:
   - Coloca los archivos CSV a procesar en el directorio principal
   - Los archivos pueden tener diferentes nombres de columnas y formatos

2. **Ejecución**:
   ```bash
   python normalize_customer_data.py
   ```

3. **Resultados**:
   - Los archivos procesados se moverán a la carpeta `procesados/` con timestamp
   - Se generará/actualizará `consolidated_customers.csv` con los datos unificados
   - Se mostrarán estadísticas del proceso en la consola

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
   - Elimina duplicados basándose en email, teléfono y nombre
   - Mantiene el registro más reciente en caso de duplicados

## Notas Importantes

- Los archivos originales se conservan en la carpeta `procesados/` con timestamp
- El script es idempotente: puede ejecutarse múltiples veces sin duplicar datos
- Se recomienda hacer respaldo del archivo consolidado periódicamente

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