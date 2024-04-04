### **Movies**

Este es el primer proyecto individual de labs (siguiente etapa luego de finalizar el bootcamp) de la carrera data science en Soy Henry. Soy estudiante de la cohorte DSPT01, o sea la primera en modalidad part time.

Para este proyecto nos entregaban unos dataset con data sobre películas (año de lanzamiento, duración, productoras, género, popularidad, etc.) y en una primera etapa debíamos realizar el ETL (extracción, transformación y carga) para dejar la data limpia y preparada, lista como para la etapa siguiente. Lo más complicado fue desanidar algunas columnas cuyos valores eran diccionarios o incluso listas de diccionarios. Luego de infinitos intentos fue el método ast.literal_eval el gran salvador.

Luego debíamos generar una api utilizando la librería fastAPI creando varias funciones específicas con la info de la data limpia. Las mismas son:

*-def cantidad_filmaciones_mes( Mes )*: Devuelve la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.

*-def cantidad_filmaciones_dia( Dia )*: Devuelve la cantidad de películas que fueron estrenadas en el día consultado en la totalidad del dataset.

*-def score_titulo( titulo_de_la_filmación )*: Devuelve el título, el año de estreno y la popularidad de la película consultada.

*-def votos_titulo( titulo_de_la_filmación )*: Devuelve el título, la cantidad de votos y el valor promedio de las votaciones de esa película, con la excepción de que si la cantidad de votos es menor a 2000 debe retornar un mensaje avisando que no cumple esa condición y por ende no devolver la otra información.

*-def get_actor( nombre_actor )*: Devuelve el éxito del actor o la actriz solicitado/a medido a través del retorno(facturación sobre presupuesto). Además, la cantidad de películas que en las que ha participado y el promedio de retorno.

*-def get_director( nombre_director )*: Devuelve el éxito del director o la directora solicitado/a medido a través del retorno y el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.

Luego de crear esas funciones venía otra parte complicada (debo reconocer que en estos procesos de aprendizaje las partes complicadas son las que más nos hacen sufrir en el momento pero al mismo tiempo las que nos hacen aprender a la fuerza y nos dejan grandes enseñanzas): Debíamos hacer el deployment a través de la página render.com.

Superados los obstáculos y con el bendito link de render funcionando correctamente se venía otra etapa complicada (sí, ya sé, todas las etapas lo fueron, al menos para mí!). Realizar el famoso EDA (análisis exploratorio de datos) para dar comienzo a la realización de la función de recomendación. En esta parte del proyecto hice muchos gráficos y análisis pero al final lo que me resultó más práctico fue un reporte en formato html que generé con la librería pandas profiling.

Finalmente decidí que mi sistema de recomendación se basara en la columna Overview, cuyos valores eran cadenas de texto con pequeños resúmenes de las películas, sobre la que apliqué cosine_similarity (método para calcular la similitud entre vectores). Por supuesto que antes de hacerlo de esta forma tuve muchos otros intentos e ideas pero en algunos casos el tamaño del dataset (45000 registros aproximadamente) imposibilitaba ciertos métodos y en otros el obstáculo era el límite de memoria de render.com. Incluso finalmente para que la función de recomendación no colapse el render tuve que achicar el dataset a sólo los primeros 4500 registros.

Debido al límite de GitHub para el tamaño de los archívos en los repositorios, sólo subí los datasets limpios. Así que dejo aquí los links a los archivos originales por si alguien quiere acceder a ellos:
https://drive.google.com/file/d/1NsemqaN83nSCiXJAK-Zpg-yb2iC0NMgu/view?usp=sharing (movies.csv)
https://drive.google.com/file/d/1ILLlv0zh9o32_bQTaGeRSVj5rpf1yzs6/view?usp=sharing (credits.csv)

**Link al video en Youtube mostrando el correcto funcionamiento de la API:**
https://www.youtube.com/watch?v=auPKicg8sS0

**Link para hacer consultas a la API:**
https://proyecto-movies-w8zf.onrender.com

Funciones de consulta:
/cantidad_filmaciones_mes/{mes}
/cantidad_filmaciones_dia/{dia de la semana}
/score_title/{Nombre de una película}
/votos_titulo/{Nombre de una película}
/get_actor/{nombre actor o actriz}
/get_director/{nombre director o directora}
/recomendacion/{Nombre de una película}


Creo que esto es lo más importante como para entender lo que hice pero por cualquier duda, consulta, sugerencia, reclamo, etc. dejo mis mails:

szklaradrian@gmail.com  
szklaradriandatos@gmail.com
