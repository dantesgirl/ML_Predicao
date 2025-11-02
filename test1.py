import pickle 
with open('fire_model.pkl', 'rb') as f:
    rf_intensity = pickle.load(f)
import pandas as pd
import numpy as np
from datetime import datetime

def predict_fire(latitude, longitude, month, day, year=2026,
                 brightness=None, confidence=None, time_of_day='D'):
    if brightness is None: 
        if month in [12, 1, 2]:
            brightness = 340.0
        elif month in [6, 7, 8]:
            brightness = 315.0
        else:
            brightness = 328.0

    if confidence is None:
        confidence = 80

    date = datetime(year, month, day)
    day_of_year = date.timetuple().tm_yday
    week_of_year = date.isocalendar()[1]
    quarter = (month - 1) // 3 + 1

    if month in [12, 1, 2]:
        season = 3
        season_name = "Verão"
        risk_level = "Muito Alto"
    elif month in [9, 10, 11]:
        season = 2
        season_name = "Primavera"
        risk_level = "Alto"
    elif month in [3, 4, 5]:
        season = 1
        season_name = "Outono"
        risk_level = "Médio"
    else:
        season = 0
        season_name = "Inverno"
        risk_level = "Baixo"

    daynight_encoded = 0 if time_of_day == 'D' else 1
    satellite_encoded = 0
    bright_t31 = brightness - 25.0

    input_data = pd.DataFrame({
        'latitude': [latitude],
        'longitude': [longitude],
        'brightness': [brightness],
        'bright_t31': [bright_t31],
        'confidence': [confidence],
        'scan': [1.5],
        'track': [1.2],
        'month': [month],
        'day_of_year': [day_of_year],
        'season': [season],
        'quarter': [quarter],
        'week_of_year': [week_of_year],
        'daynight_encoded': [daynight_encoded],
        'satellite_encoded': [satellite_encoded]
    })

    prediction = rf_intensity.predict(input_data)[0]
    intensity = "Alto" if prediction == 1 else "Baixo"

    result = {
        'date': f"{year}-{month:02d}-{day:02d}",
        'location': f"({latitude:.2f}, {longitude:.2f})",
        'season': season_name,
        'fire_risk':  risk_level,
        'predicted_intensity': intensity,
        'brightness': brightness,
        'confidence': confidence, 
        'time_of_day': 'Day' if time_of_day == 'D' else 'Night'
    }

    return result

def predict_monthly_risk(latitude, longitude, year=2026):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jun', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    results = []

    for month_num in range(1, 13):
        result = predict_fire(latitude, longitude, month_num, 15, year)
        results.append({
            'Month': months[month_num - 1],
            'Season': result['season'],
            'Fire Risk': result['fire_risk'],
            'Predicted Intensity': result['predicted_intensity']
        })
    return pd.DataFrame(results)
def find_high_risk_periods(latitude, longitude, year=2026):
    high_risk_months = []
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    for month_num in range(1, 13):
        result = predict_fire(latitude, longitude, month_num, 15, year)
        if result['fire_risk'] in ['High', 'Very High']:
            high_risk_months.append(months[month_num - 1])
    return high_risk_months

print("\Entrada do usuario:")
print("  Localização: Sydney (-33.87, 151.21)")
print("  Data: 15 de Janeiro, 2026 (Verão)")

prediction = predict_fire(
    latitude=-33.87,
    longitude=151.21,
    month=1,
    day=15,
    year=2026
)

print("\Resultado das predições:")
for key, value in prediction.items():
    print(f"  {key.replace('_', ' ').title()}: {value}")
print("Exemplo 2: No inverno (Mesmo local)")

print("\nEntrada do usuario:")
print("  Localização: Sydney (-33.87, 151.21)")
print("  Data: 15 de Janeiro, 2026 (Inverno)")

prediction2 = predict_fire(
    latitude=-33.87,
    longitude=151.21,
    month=7,
    day=15,
    year=2026
)

print("\nResultados:")
for key, value in prediction.items():
    print(f"  {key.replace('_', ' ').title()}: {value}")

print("Exemplo 3: Analise mensal dos riscos de 2026")
monthly_df = predict_monthly_risk(-25.0, 135.0, 2026)
print("\nPredição mensal:")
print(monthly_df.to_string(index=False))

print("Exemplo 4: Risco alto - predição")
print("\nAchando meses de alto riscos de fogo...")
print("Localização: Melbourne (-37.81, 144.96)")

high_risk = find_high_risk_periods(-37.81, 144.96, 2026)
print(f"\nMeses de alto riscos ({len(high_risk)}):")
for month in high_risk:
    print(f"  - {month}")

print("Exemplo 5: Teste de varios lugares (Janeiro 2026)")
locations = [
    ("Sydney", -33.87, 151.21),
    ("Melbourne", -37.81, 144.96),
    ("Brisbane", -27.47, 153.03),
    ("Perth", -31.95, 115.86),
    ("Adelaide", -34.93, 138.60)
]

print("\nComparação:")
print(f"{'City':<12} {'Location':<20} {'Risk Level':<12} {'Intensity'}")
for city, lat, lon in locations:
    pred = predict_fire(lat, lon, 1, 15, 2026)
    print(f"{city:<12} ({lat:.2f}, {lon:.2f})     {pred['fire_risk']:<12} {pred['predicted_intensity']}")

def user_prediction_simple():
    print("Predição de risco de fogo")
latitude = -25.0
longitude = 135.0
month = 12
day = 25
year = 2026

print(f"\n  Latitude: {latitude}")
print(f"  Longitude: {longitude}")
print(f"  Data: {year}-{month:02d}-{day:02d}")
result = predict_fire(latitude, longitude, month, day, year)

print(f"\nLocalização: {result['location']}")
print(f"Data: {result['date']}")
print(f"Estação: {result['season']}")
print(f"Risco de fogo: {result['fire_risk']}")
print(f"Presição de fogo: {result['predicted_intensity']}")
print(f"Temperatura: {result['brightness']} C")
