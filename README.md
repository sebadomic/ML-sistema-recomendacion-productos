# Proyecto de Recomendación de Productos
Este proyecto consiste en un sistema de recomendación de productos basado en la similitud entre comercios que compran productos dentro de una misma categoría en una determinada comuna. Utiliza técnicas de Machine Learning como el cálculo de similitud de coseno para encontrar comercios similares y generar recomendaciones basadas en patrones de compra.

# Archivos en el proyecto
1. Challenge_Tecnico_DS_Sebastian_Ramirez.py: Contiene el código fuente del sistema de recomendación de productos.
2. README.md: que describe la metodología y pasos para ejecutar el proyecto.
3. commerces.csv; products.csv; transactions.csv: archivos con la data necesaria para desarrollar el modelo.
4. EDA_Challenge_Sebastian_Ramirez.py: Archivo con el análisis inicial y prueba del modelo.

# Requisitos previos
Para poder ejecutar este proyecto, necesitas tener instalado:

1. Python 3.x
Librerías de Python como:
2. pandas: para la manipulación de datos y creación de tablas dinámicas.
3. sklearn: para el escalamiento de los datos y cálculo de similitudes.
También necesitarás un entorno Conda configurado con las librerías necesarias.

# Metodología de trabajo
### 1. Preparación de Datos: 
El sistema de recomendación comienza filtrando los datos para una categoría de producto y una comuna específica, que se seleccionan a partir de la entrada del usuario.

### 2. Cálculo de Similitud de Comercios
Se crea una matriz de compras (comercio vs producto) a partir de los datos filtrados. Esta matriz se normaliza utilizando MinMaxScaler, escalando los valores entre 0 y 1, lo que permite tratar de manera uniforme los comercios con diferentes volúmenes de compras. Luego, se utiliza la similitud de coseno (cosine_similarity) para medir la similitud entre los comercios.

### 3. Selección de Comercios Similares
Una vez calculada la similitud, se seleccionan aquellos comercios que comparten la misma comuna que el comercio objetivo y cuya similitud es mayor a un umbral de 0.85.

### 4. Recomendación de Productos
Finalmente, se recorre la lista de comercios similares y se acumulan las cantidades compradas de cada producto. Los productos con mayor cantidad comprada se recomiendan al comercio objetivo.

### 5. Interacción con el Usuario
El sistema interactúa con el usuario solicitando la selección de su número de comercio y la categoría de productos que le interesa. Con base en esta información, se generan recomendaciones de productos.

# Estructura del código
### Funciones principales:
### 1. similitud_comercios(categoria, comuna)
Esta función calcula la matriz de similitud entre comercios para una determinada categoría y comuna, utilizando la similitud de coseno.

### 2. recomendar_productos()
Esta función gestiona la interacción con el usuario. Solicita el número de comercio y la categoría de productos, y luego genera una lista de recomendaciones basadas en los comercios más similares.
