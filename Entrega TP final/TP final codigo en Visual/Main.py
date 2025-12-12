# ==========================
# CARGA DE DATOS
# ==========================

# Librerías para análisis de datos y gráficos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Herramientas para rutas de archivos y leer listas en texto
from pathlib import Path
import ast

# Carga de archivos principales del dataset
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

# ==========================
# LIMPIEZA
# ==========================

# Limpieza básica y columnas nuevas
# Convertir fecha
movies["release_date"] = pd.to_datetime(movies["release_date"], errors="coerce")
movies["year"] = movies["release_date"].dt.year
movies["decade"] = (movies["year"] // 10) * 10

# Reemplazar ceros en budget/revenue
movies["budget"] = movies["budget"].replace(0, np.nan)
movies["revenue"] = movies["revenue"].replace(0, np.nan)

# Calcular ROI
movies["roi"] = movies["revenue"] / movies["budget"]

# ==========================
# PREPARAR GÉNEROS
# ==========================

# Convertir el texto de géneros en listas reales de diccionarios
def extraer_generos(genres_str):
    try:
        generos = ast.literal_eval(genres_str)
        return [g["name"] for g in generos] # Extraer solo nombres
    except:
        return []

# Crear columna con lista de géneros y separar cada género en su propia fila
movies["genre_list"] = movies["genres"].apply(extraer_generos)
movies_exploded = movies.explode("genre_list").rename(columns={"genre_list": "genre"})

# ==========================
# EJE 1 – ROI POR GÉNERO
# ==========================

# Agrupar por género y calcular el ROI promedio
roi_by_genre = (
    movies_exploded
    .dropna(subset=["roi", "genre"])
    .groupby("genre")["roi"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

# Grafico
plt.figure(figsize=(10,5))
sns.barplot(data=roi_by_genre.head(12), x="genre", y="roi")
plt.xticks(rotation=45)
plt.title("ROI promedio por género")
plt.tight_layout()
plt.show()

# ==========================
# EJE 2 – PRESUPUESTO VS RATING
# ==========================

# Filtrar películas que tengan presupuesto y rating válidos
df = movies.dropna(subset=["budget", "vote_average"])

# Calcular correlaciones entre presupuesto y rating
pearson = df["budget"].corr(df["vote_average"], method="pearson")
spearman = df["budget"].corr(df["vote_average"], method="spearman")

# Grafico dispersograma
plt.figure(figsize=(7,5))
sns.scatterplot(data=df, x="budget", y="vote_average", alpha=0.3)
plt.xscale("log") 
plt.title("Relación entre presupuesto y rating")
plt.show()

# ==========================
# EJE 3 – RUNTIME POR DÉCADA (50 años)
# ==========================

# Filtrar películas desde 1970 (o desde 50 años atrás)
df_runtime = movies.dropna(subset=["runtime", "decade"])
df_runtime = df_runtime[df_runtime["decade"] >= 1970]

# Calcular promedio por década
runtime_by_decade = (
    df_runtime
    .groupby("decade")["runtime"]
    .mean()
    .reset_index()
)

# Grafico
plt.figure(figsize=(8,4))
sns.lineplot(data=runtime_by_decade, x="decade", y="runtime", marker="o")
plt.title("Duración promedio por década (últimos 50 años)")
plt.ylabel("Minutos")
plt.show()

# ==========================
# EXPORTACIÓN PARA MINI API
# ==========================

# Exportación (JSON/CSV) para la mini API
Path("salidas").mkdir(exist_ok=True)

roi_by_genre.to_json("salidas/roi_by_genre.json", orient="records")
runtime_by_decade.to_json("salidas/runtime_by_decade.json", orient="records")
df[["budget","vote_average"]].to_json("salidas/budget_rating.json", orient="records")

print("Archivos exportados en la carpeta 'salidas'.")
