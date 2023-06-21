import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse

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




