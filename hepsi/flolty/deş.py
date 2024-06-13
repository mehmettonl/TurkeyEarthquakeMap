import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from datetime import datetime, timedelta
import unidecode

# JSON dosyasının tam yolunu belirleme
file_path = "C:\\Users\\onalm\\Desktop\\ikinci.json"

# JSON dosyasını okuma
df = pd.read_json(file_path)

# Oluş tarihi ve zamanı birleştirme ve datetime formatına dönüştürme
df["Olus"] = pd.to_datetime(df["Olus tarihi"] + " " + df["Olus zamani"])

# 'Mw' sütununda NaN değerleri olan satırları kaldırma
df = df.dropna(subset=["Mw"])

# Türkiye'deki 81 il
turkey_cities = ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin",
                 "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa",
                 "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum",
                 "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir",
                 "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir",
                 "Kilis", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir",
                 "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Şanlıurfa", "Şırnak",
                 "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"]

# Şehir isimlerini küçük harfe ve Türkçe karakterlerden arındırma fonksiyonu
def normalize_city_name(city):
    return unidecode.unidecode(city).lower()

# Şehir isimlerini ayıklama fonksiyonu
def contains_city(yers, city):
    normalized_city = normalize_city_name(city)
    return normalized_city in normalize_city_name(yers)

# Dash uygulaması oluşturma
app = Dash(__name__)

# Arayüz oluşturma
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "Türkiye Deprem Atlası",
                    style={
                        "marginTop": "200px",
                        "textAlign": "center",
                        "marginBottom": "2px",
                        "color": "#f0f8ff",
                        "fontFamily": "Helvetica",
                        "margin-top": "50px",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label(
                                            "Başlangıç Tarihi",
                                            style={
                                                "fontWeight": "bold",
                                                "color": "#f0f8ff",
                                                "fontSize": 20,
                                                "fontFamily": "Helvetica",
                                                "marginRight": "20px",
                                            },
                                        ),
                                        dcc.DatePickerSingle(
                                            id="start-date-picker",
                                            min_date_allowed=df["Olus"].min().date(),
                                            max_date_allowed=df["Olus"].max().date(),
                                            initial_visible_month=df["Olus"].min().date(),
                                            date=df["Olus"].min().date(),
                                            display_format="DD MMM YYYY",
                                            style={
                                                "marginBottom": "20px",
                                                "borderRadius": "10px",
                                            },
                                        ),
                                    ]
                                ),
                            ],
                            style={"marginBottom": "20px", "display": "inline-block"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label(
                                            "Bitiş Tarihi",
                                            style={
                                                "fontWeight": "bold",
                                                "color": "#f0f8ff",
                                                "fontSize": 20,
                                                "fontFamily": "Helvetica",
                                                "marginRight": "20px",
                                            },
                                        ),
                                        dcc.DatePickerSingle(
                                            id="end-date-picker",
                                            min_date_allowed=df["Olus"].min().date(),
                                            max_date_allowed=df["Olus"].max().date(),
                                            initial_visible_month=df["Olus"].max().date(),
                                            date=df["Olus"].max().date(),
                                            display_format="DD MMM YYYY",
                                            style={
                                                "marginBottom": "20px",
                                                "borderRadius": "10px",
                                            },
                                        ),
                                    ],
                                    style={
                                        "marginBottom": "20px",
                                        "display": "inline-block",
                                    },
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Büyüklük Aralığı",
                                    style={
                                        "fontWeight": "bold",
                                        "color": "#f0f8ff",
                                        "fontSize": 20,
                                        "fontFamily": "Helvetica",
                                        "marginBottom": "20px",
                                    },
                                ),
                                html.Div(
                                    [
                                        dcc.Input(
                                            id="min-magnitude-input",
                                            type="number",
                                            min=df["Mw"].min(),
                                            max=df["Mw"].max(),
                                            step=0.1,
                                            value=df["Mw"].min(),
                                            style={
                                                "marginRight": "10px",
                                                "width": "100px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="max-magnitude-input",
                                            type="number",
                                            min=df["Mw"].min(),
                                            max=df["Mw"].max(),
                                            step=0.1,
                                            value=df["Mw"].max(),
                                            style={"width": "100px"},
                                       ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "justifyContent": "center",
                                    },
                                ),
                            ],
                            style={"textAlign": "center",
                            "marginBottom": "30px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Şehir",
                                    style={
                                        "fontWeight": "bold",
                                        "color": "#f0f8ff",
                                        "fontSize": 20,
                                        "fontFamily": "Helvetica",
                                    },
                                ),
                            ],
                            style={"marginBottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    id="city-dropdown",
                                    options=[
                                        {"label": city, "value": city}
                                        for city in turkey_cities
                                    ],
                                    value=None,
                                    placeholder="Şehir Seçin",
                                    style={"color": "f0f8ff", "marginBottom": "20px"},
                                ),
                            ],
                            style={"marginBottom": "20px"},
                        ),
                    ],
                    style={"padding": "20px", "borderRadius": "10px"},
                ),  # "width": "300px", "height": "400px"
            ],
            style={
                "backgroundColor": "#045174",
                "flex": "1",
                "padding": "10px",
                "border": "2px solid #045174",
                "borderRadius": "50px",
                "margin-top": "100px",
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "center",
                "alignItems": "center",
                "height": "400px",
            },
        ),
        html.Div(
            [
                dcc.Graph(
                    id="map-graph",
                    style={
                        "borderRadius": "20px",  # Border radius eklendi
                        "height": "99%",
                        "width": "100%",
                        "border": "2px solid #045174",
                        "borderRadius": "10px",
                        "margin": "auto",
                        "backgroundColor": "white",  # Arka plan rengi eklendi
                    },
                    figure={},  # Başlangıçta herhangi bir veri gösterme
                )
            ],
            style={
                "flex": "3",
                "padding": "10px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "maxWidth": "80vw",
                "maxHeight": "70vh",
                "marginTop": "90px",
                "overflow": "hidden",  # Kenarlık nedeniyle içeriği sığdırmak için
                "borderRadius": "10px",  # Bu stil de eklendi
            },
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
        "maxWidth": "100%",
        "margin": "0",
        "position": "relative",
        "height": "100vh",
    },
)

@app.callback(
    Output("map-graph", "figure"),
    [
        Input("start-date-picker", "date"),
        Input("end-date-picker", "date"),
        Input("min-magnitude-input", "value"),
        Input("max-magnitude-input", "value"),
        Input("city-dropdown", "value"),
    ],
)
def update_map(start_date, end_date, min_magnitude, max_magnitude, selected_city):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df_filtreli = df[
        (df["Olus"] >= start_date)
        & (df["Olus"] <= end_date)
        & (df["Mw"] >= min_magnitude)
        & (df["Mw"] <= max_magnitude)
        & (df["Mw"] != 0)  # Mw değeri sıfır olmayan depremleri filtrele
    ]

    if selected_city:
        df_filtreli = df_filtreli[
            df_filtreli["Yer"].apply(contains_city, city=selected_city)
        ]

    # Filtrelenmiş veri seti boşsa boş bir figür döndür
    if df_filtreli.empty:
        return {}

    # Depremleri çizmek için boş bir şekil oluşturalım
    fig = go.Figure()

    # Plotly renk skalası seçimi
    colors = px.colors.qualitative.Plotly

    # Veri noktalarını çizin ve aynı büyüklükteki depremleri birbirine bağlama
    for i, (mw, data) in enumerate(df_filtreli.groupby("Mw")):
        data_sorted = data.sort_values(by="Olus")  # Tarihe göre sıralı veri
        latitudes = data_sorted["Enlem"].tolist()
        longitudes = data_sorted["Boylam"].tolist()
        color = colors[i % len(colors)]  # Her büyüklük için farklı bir renk seçimi
        fig.add_trace(go.Scattermapbox(
            lat=latitudes,
            lon=longitudes,
            mode='lines',
            line=dict(width=2, color=color),
            hoverinfo='skip',  # Hover etkileşimini devre dışı bırakma
        ))

        # Markerlar üzerinde deprem büyüklüğünü gösterin
        fig.add_trace(px.scatter_mapbox(
            data_sorted,
            lat="Enlem",
            lon="Boylam",
            hover_name="Mw",
            color="Mw",
            size="Mw",
            size_max=15,
            zoom=4.9,
            center={"lat": 39.9255, "lon": 35.5565},
            title="Türkiye Deprem Haritası (Filtrelenmiş)",
            color_continuous_scale="YlOrRd",
        ).data[0])

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=510,
        width=1050,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2
        )
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
