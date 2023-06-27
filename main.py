import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = FastAPI()

df_movies_limpio = pd.read_csv("movies_dataset_limpio.csv")
df_credits_limpio = pd.read_csv("credits_limpio.csv")
df_movies_limpio['release_date'] = pd.to_datetime(df_movies_limpio['release_date'], errors='coerce').dt.strftime('%Y-%m-%d').astype('datetime64')

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes):
    month_dict = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }
    
    mes_numero = month_dict.get(mes.lower())
    if mes_numero is None:
        return JSONResponse(content={"mensaje": f"No se reconoce {mes}. Asegúrese de estar escribiéndolo correctamente."})
    
    count = df_movies_limpio[df_movies_limpio['release_date'].dt.month == mes_numero].shape[0]
    return JSONResponse(content={"mes": mes, "filmaciones": count})

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia):
    day_dict = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miércoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sábado': 'Saturday',
        'domingo': 'Sunday'
    }
    
    dia_buscar = day_dict.get(dia.lower())
    if dia_buscar is None:
        return JSONResponse(content={"mensaje": f"No se reconoce {dia}. Asegúrese de estar escribiéndolo correctamente."})
    
    count = df_movies_limpio[df_movies_limpio['release_date'].dt.day_name() == dia_buscar].shape[0]
    return JSONResponse(content={"día": dia ,"filmaciones": count})

@app.get("/score_title/{titulo}")
def score_titulo(titulo):
    movie = df_movies_limpio[df_movies_limpio['title'] == titulo]
    if movie.empty:
        return JSONResponse(content={"mensaje": f"El título {titulo} no fue encontrado en nuestra base de datos. Asegúrese de estar escribiéndolo correctamente."})
    
    popularity = round(movie['popularity'].iloc[0], 2)
    return JSONResponse(content={"titulo": titulo, "año_estreno": int(movie['release_year'].iloc[0]), "popularidad": popularity})

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo):
    movie = df_movies_limpio[df_movies_limpio['title'] == titulo]
    if movie.empty:
        return JSONResponse(content={"mensaje": f"El título {titulo} no fue encontrado en nuestra base de datos. Asegúrese de estar escribiéndolo correctamente."})
    
    vote_count = int(movie['vote_count'].iloc[0])
    vote_average = movie['vote_average'].iloc[0]
    
    if vote_count > 2000:
        return JSONResponse(content={"mensaje": f"La película {titulo} fue estrenada en el año {movie['release_year'].iloc[0]}. Cuenta con un total de {vote_count} valoraciones y un promedio de {vote_average}"})
    else:
        return JSONResponse(content={"mensaje": f"La película {titulo} fue estrenada en el año {movie['release_year'].iloc[0]}. Tiene menos de 2000 valoraciones por lo tanto no se muestra su promedio"})

@app.get("/get_actor/{nombre_actor_o_actriz}")
def get_actor(nombre_actor_o_actriz):
    actor_movies = df_credits_limpio[df_credits_limpio['names_cast'].str.contains(nombre_actor_o_actriz, na=False, case=False)]
    if actor_movies.empty:
        return JSONResponse(content={"mensaje": f"El nombre {nombre_actor_o_actriz} no fue encontrado en nuestra base de datos. Asegúrese de estar escribiéndolo correctamente."})
    
    actor_ids = actor_movies['id'].tolist()
    actor_movies_data = df_movies_limpio[df_movies_limpio['id'].isin(actor_ids)]
    
    total_films = actor_movies_data.shape[0]
    total_return = round(actor_movies_data['return'].sum(), 2)
    average_return = round(actor_movies_data['return'].mean(), 2)
    
    return JSONResponse(content={"mensaje": f"El actor {nombre_actor_o_actriz} ha participado en {total_films} filmaciones. Su retorno total es de {total_return} con un promedio de {average_return} por filmación."})

@app.get("/get_director/{nombre_director_o_directora}")
def get_director(nombre_director_o_directora):
    director_movies = df_credits_limpio[df_credits_limpio['director'].str.lower() == nombre_director_o_directora.lower()]
    if director_movies.empty:
        return JSONResponse(content={"mensaje": f"{nombre_director_o_directora} no fue encontrado en nuestra base de datos. Asegúrese de estar escribiéndolo correctamente."})

    movie_ids = director_movies['id'].tolist()
    director_movies_data = df_movies_limpio[df_movies_limpio['id'].isin(movie_ids)]
    
    director_movies_data['ganancia'] = director_movies_data['revenue'] - director_movies_data['budget']
    director_movies_data = director_movies_data.round({'return': 2, 'promedio': 2, 'ganancia': 2})
    
    movie_titles = director_movies_data['title'].tolist()
    release_years = director_movies_data['release_year'].tolist()
    returns = director_movies_data['return'].tolist()
    revenues = director_movies_data['revenue'].tolist()
    budgets = director_movies_data['budget'].tolist()
    ganancias = director_movies_data['ganancia'].tolist()
    
    return_total = sum(returns)
    
    movies_info = []
    for i in range(len(movie_titles)):
        movie_info = {
            'nombre': movie_titles[i],
            'año': release_years[i],
            'retorno': returns[i],
            'revenue': revenues[i],
            'budget': budgets[i],
            'ganancia': ganancias[i]
        }
        movies_info.append(movie_info)
    
    return JSONResponse(content={"retorno_total": return_total, "peliculas": movies_info})

columnas_modelo = ['title', 'overview']
df_modelo = df_movies_limpio[columnas_modelo].dropna()

# Instancio TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Creo la matriz
tfidf_matrix = tfidf_vectorizer.fit_transform(df_modelo['overview'])

# Creo una función para preprocesar el texto de la columna 'overview'
def preprocess_text(text):
    # Elimino caracteres especiales y números
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    
    # Convierto el texto a minúsculas
    text = text.lower()
    
    # Tokenización de palabras
    tokens = word_tokenize(text)
    
    # Elimino palabras vacías
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Uno las palabras preprocesadas en una cadena de texto
    processed_text = ' '.join(tokens)
    
    return processed_text

# Aplico la función en la columna
df_modelo['overview'] = df_modelo['overview'].apply(preprocess_text)

# Vectorizo
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df_modelo['overview'])

# Cálculo de similitud del coseno
cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

@app.get("/recomendacion/{titulo}")
def recomendacion(titulo):
    # Obtener el índice de la película correspondiente al título
    indices = pd.Series(df_modelo.index, index=df_modelo['title']).drop_duplicates()
    if titulo not in indices:
        return {'error': f'No se encontró la película con el título "{titulo}" en nuestra base de datos.'}

    idx = indices[titulo]

    try:
        # Obtener los puntajes de similitud de la película con todas las demás
        similarity_scores = list(enumerate(cosine_similarities[idx]))

        # Ordenar las películas según los puntajes de similitud en orden descendente
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    except ValueError:
        return {'error': f'No se encontró la película con el título "{titulo}" en nuestra base de datos.'}

    # Obtener los índices de las películas recomendadas
    recommended_indices = [i[0] for i in similarity_scores[1:6]]  # Se obtienen las primeras 5 películas recomendadas

    # Devolver los títulos de las películas recomendadas en orden decreciente
    recomendaciones = df_modelo['title'].iloc[recommended_indices[::-1]].tolist()  # Se invierte el orden de la lista y se convierte a una lista
    
    return {'recomendaciones': recomendaciones}
