import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Cargamos los archivos
comercios = pd.read_csv("commerces.csv", sep=",")
productos = pd.read_csv("product.csv", sep=",")
ventas = pd.read_csv("transactions.csv", sep=",")

# Hacemos join a los datasets para tener toda la informacion
df = ventas.merge(comercios, how='left', on='id_commerce')\
        .merge(productos, how='left', on='id_product')\
            .rename(columns={'price_x':'precio_total',
                             'price_y':'precio_unitario'})

# Armamos la funcion para obtener la similitud entre los comercios de la categoria y comuna seleccionadas
def similitud_comercios(categoria, comuna):
    df_temp = df[(df['category'] == categoria) & (df['district'] == comuna)]
    
    # Crear la matriz de compras (comercio vs producto)
    matriz_compras = df_temp.pivot_table(index='id_commerce', columns='id_product', values='quantity', aggfunc='sum').fillna(0)
    
    # Aplicar MinMaxScaler para escalar los valores entre 0 y 1
    scaler = MinMaxScaler()
    matriz_compras_scaled = scaler.fit_transform(matriz_compras)
    
    # Calcular la similitud entre comercios
    similitud_comercios = cosine_similarity(matriz_compras_scaled)
    
    # Convertir la similitud en un DataFrame
    similitud_comercios_df = pd.DataFrame(similitud_comercios, index=matriz_compras.index, columns=matriz_compras.index)
    
    return similitud_comercios_df


# Función para recomendar productos basados en la popularidad en comercios similares
def recomendar_productos():
    # Damos la bienvenida al sistema
    print("¡Bienvenido al sistema de recomendación de productos!")
    print("\n")
    
    # Buscamos el listado de comercios, categorias y solicitamos el número de comercio al cliente
    listado_comercios = comercios['id_commerce'].unique()
    listado_categorias = productos['category'].unique()
    listado_metricas = ['Unidades', 'Ventas']
    
    numero_comercio = int(input("Por favor indique su número de comercio: "))
    
    while numero_comercio not in listado_comercios:
        numero_comercio = int(input("Comercio no válido. Por favor ingrese su numero de comercio (1 al 100): "))
    else:
        # Filtrar comercios en la misma comuna
        comuna_comercio = comercios[comercios['id_commerce'] == numero_comercio]['district'].iloc[0]
        comercios_comuna = df[df['district'] == comuna_comercio]['id_commerce'].unique()
        
        # Se selecciona la categoria
        print("\n")
        print("Categorías disponibles:")
        for idx, cat in enumerate(listado_categorias, start=1):
            print(f"{idx}. {cat}")
        
        categoria_seleccionada = str(input("Seleccione una categoria: "))
         
        while categoria_seleccionada not in listado_categorias:
            categoria_seleccionada = str(input("Categoría no válida. Favor seleccionar una categoría disponible: "))
        
        else:
            # Obtenemos la matriz de similitud
            similitud_comercios_df = similitud_comercios(categoria_seleccionada, comuna_comercio)
            
            # Obtener las similitudes de los comercios de la misma comuna
            similitudes_comuna = similitud_comercios_df.loc[numero_comercio, comercios_comuna]
        
            # Filtrar: eliminar el comercio actual y los que tengan una similitud menor a 0.85
            similitudes_comuna = similitudes_comuna[similitudes_comuna.index != numero_comercio]
            similitudes_comuna = similitudes_comuna[similitudes_comuna >= 0.85]
        
            # Ordenar los comercios similares en la misma comuna por similitud (descendente)
            comercios_similares = similitudes_comuna.sort_values(ascending=False).index
                    
            # Inicializar una tabla de conteo de productos
            conteo_productos = pd.Series(dtype='float64')
        
            # Recorrer los comercios similares para acumular las cantidades de productos comprados
            for comercio_similar in comercios_similares:
               
                # Obtenemos los productos más comprados por ese comercio dentro de la categoría
                productos_similares = df[(df['id_commerce'] == comercio_similar) & 
                                         (df['category'] == categoria_seleccionada)][['id_product', 'quantity']]
                          
                # Acumular las cantidades compradas para cada producto
                conteo_productos = conteo_productos.add(productos_similares.groupby('id_product')['quantity']\
                                                        .sum(), fill_value=0)
    
                # Ordenar los productos por la cantidad acumulada de compras
                productos_recomendados = conteo_productos.sort_values(ascending=False).index[:10]
                productos_entregados = productos[productos['id_product'].isin(productos_recomendados)][['name', 'price']]
                        
    return print(f"\n Las recomendaciones de productos para el comercio {numero_comercio}, en la comuna de {comuna_comercio} para la categoria {categoria_seleccionada} son: "), print(productos_entregados)


recomendar_productos()