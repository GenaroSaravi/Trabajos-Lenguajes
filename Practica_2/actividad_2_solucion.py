"""
TP Entrega Practica 2 - Alumno: Saravi Sosa Genaro
"""

#Path y modulos para manejar archivos, fechas y diccionario
from pathlib import Path
import csv
import json
from datetime import datetime
from collections import Counter, defaultdict

# Configuración de rutas
BASE = Path(__file__).parent if "__file__" in globals() else Path(".") #Representa la ruta del archivo/carpeta en py o colab
SRC_CSV = BASE / "actividad_2.csv"
OUT_DIR = BASE / "salida"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Funcion para convertir el formato que tenga el CSV
def try_parse_ts(ts: str) -> datetime:

    # Intenta parsear un timestamp con varios formatos comunes.
    # Devuelve un datetime (naive). Si no puede, lanza ValueError.
    # Convertir el texto(string) a un objeto

    ts = ts.strip() 
    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
    ]
    for fmt in formatos: # Recorre los formatos y pruba uno por uno
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            pass
    try: # Intento final con fromisoformat (formato ISO 8601).
        return datetime.fromisoformat(ts.replace("Z", ""))
    except Exception as e:
        raise ValueError(f"No pude parsear timestamp: {ts!r}") from e


# 0=lunes a 6=domingo
WEEKDAYS_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


# 1 y 2) Leer CSV y Identificar el día de la semana de cada entrenamiento
rows = []
with SRC_CSV.open("r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    # Normalizo claves a minúsculas/strip por si vienen distintas
    field_map = {k: k.strip().lower() for k in reader.fieldnames}
    for raw in reader:
        r = {field_map[k]: (v.strip() if isinstance(v, str) else v) for k, v in raw.items()}
        # Campos mínimos esperados
        # timestamp, campeon, actividad, entrenador
        ts = try_parse_ts(r["timestamp"])
        r["_dt"] = ts
        r["_date"] = ts.date()
        idx = ts.weekday()                  # 0..6 (lunes..domingo)
        r["_weekday_idx"] = idx
        r["_weekday"] = WEEKDAYS_ES[idx]
        rows.append(r) # Lee cada fila del CSV, limpia los datos y convierte la fecha a datetime agregando todo a las filas (rows)


# 3) Día/s con más sesiones
by_weekday = Counter(r["_weekday"] for r in rows)
max_day_count = max(by_weekday.values()) if by_weekday else 0 
dias_mas_sesiones = sorted([d for d, c in by_weekday.items() if c == max_day_count])
# Uso un contador, luego guardo los maximos y los ordeno

# 4) Días entre primer y último entrenamiento
min_dt = min((r["_dt"] for r in rows), default=None)
max_dt = max((r["_dt"] for r in rows), default=None)
dias_entre = (max_dt.date() - min_dt.date()).days if (min_dt and max_dt) else 0 #Resto el dia menos al mayor


# 5) Campeón que más entrenó
by_campeon = Counter(r["campeon"] for r in rows)
max_cam_count = max(by_campeon.values()) if by_campeon else 0
campeones_top = sorted([c for c, n in by_campeon.items() if n == max_cam_count])
# Idem al 3, uso un contador, luego guardo los maximos y los ordeno

# 6) Promedio de entrenamientos por cada día de la semana
counts_per_day = defaultdict(int) # Cuenta sesiones del dia
unique_dates_per_day = defaultdict(set) # Cuenta cuantas fechas unicas en ese dia

for r in rows: #Bucle para contar cuantas sesiones en cada dia
    d = r["_weekday"]
    counts_per_day[d] += 1
    unique_dates_per_day[d].add(r["_date"])

promedios_por_dia = {}
for d in WEEKDAYS_ES: #Bucle para calcular el promedio
    total = counts_per_day.get(d, 0)
    cant_fechas = len(unique_dates_per_day.get(d, set()))
    promedio = (total / cant_fechas) if cant_fechas else 0.0
    promedios_por_dia[d] = round(promedio, 2)


# 7) Campeón que más entrena fines de semana
weekend_set = {"sábado", "domingo"}
by_campeon_weekend = Counter(r["campeon"] for r in rows if r["_weekday"] in weekend_set)
max_we_count = max(by_campeon_weekend.values()) if by_campeon_weekend else 0
campeones_top_weekend = sorted([c for c, n in by_campeon_weekend.items() if n == max_we_count]) if max_we_count > 0 else []


# 8) CSV: cantidad de entrenamientos por campeón
out_csv = OUT_DIR / "entrenamientos_por_campeon.csv" #Ruta de salida del CSV
with out_csv.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["campeon", "cantidad"])
    for campeon, cantidad in sorted(by_campeon.items(), key=lambda x: (-x[1], x[0].lower())): # Lambda para ordenar de mayor a menor y alfabeticamente
        writer.writerow([campeon, cantidad])

# 9) JSON: resumen total y, para cada día, campeones con sus cantidades
per_day_cam = defaultdict(Counter)
for r in rows:
    per_day_cam[r["_weekday"]][r["campeon"]] += 1

por_dia = {}
for d in WEEKDAYS_ES:
    if per_day_cam[d]:
        por_dia[d] = dict(sorted(per_day_cam[d].items(), key=lambda x: (-x[1], x[0].lower())))
    else:
        por_dia[d] = {}

resumen = {  # Creo gran diccionario con el resumen de forma ordenada
    "total_registros": len(rows),
    "primer_entrenamiento": min_dt.isoformat(sep=" ") if min_dt else None,
    "ultimo_entrenamiento": max_dt.isoformat(sep=" ") if max_dt else None,
    "dias_mas_sesiones": dias_mas_sesiones,
    "cantidad_maxima_en_esos_dias": max_day_count,
    "dias_entre_primero_y_ultimo": dias_entre,
    "campeon_es_que_mas_entreno": campeones_top,
    "cantidad_maxima_campeon": max_cam_count,
    "promedios_por_dia": promedios_por_dia,
    "campeon_es_finde": campeones_top_weekend,
    "cantidad_finde": max_we_count,
    "por_dia": por_dia,
}

out_json = OUT_DIR / "resumen_entrenamientos.json" # Declaro la ruta de salida del JSON
with out_json.open("w", encoding="utf-8") as f:
    json.dump(resumen, f, ensure_ascii=False, indent=2)


# X) Resumen por consola
print("=== RESUMEN ===")
print("Días con más sesiones:", ", ".join(dias_mas_sesiones) if dias_mas_sesiones else "-")
print("Cantidad máxima en esos días:", max_day_count)
print("Días entre el primero y el último entrenamiento:", dias_entre)
print("Campeón/es que más entrenó/aron:", ", ".join(campeones_top) if campeones_top else "-",
      f"(total: {max_cam_count})")
print("Promedios por día:", promedios_por_dia)
print("Campeón/es top de fin de semana:", ", ".join(campeones_top_weekend) if campeones_top_weekend else "-",
      f"(total finde: {max_we_count})")
print("Archivos generados:")
print(" -", out_csv)
print(" -", out_json)