import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import requests
import tempfile
import os
from folium.plugins import MarkerCluster, HeatMap, MeasureControl

st.set_page_config(page_title="Mapa Bancário", layout="wide")

st.title("Visualização de Sistemas Bancários por Bairro")

# URLs dos arquivos GeoJSON no GitHub
BAIRROS_URL = "https://raw.githubusercontent.com/Analissoares/teste/main/data/bairros.geojson"
SB_URL = "https://raw.githubusercontent.com/Analissoares/teste/main/data/dados_SB.geojson"

# Função para carregar e salvar o GeoJSON antes de ler
def load_gdf_from_url(url):
    with tempfile.NamedTemporaryFile(suffix=".geojson", delete=False) as tmp:
        response = requests.get(url)
        if response.status_code == 200:  # Confirma se o arquivo foi baixado corretamente
            tmp.write(response.content)
            tmp_path = tmp.name
            gdf = gpd.read_file(tmp_path)
            os.remove(tmp_path)
            return gdf
        else:
            st.error(f"Erro ao baixar arquivo: {url}")
            return None

# Carrega os dados
bairros_data = load_gdf_from_url(BAIRROS_URL)
df_sb = load_gdf_from_url(SB_URL)

if bairros_data is None or df_sb is None:
    st.error("Erro ao carregar os dados GeoJSON. Verifique os arquivos.")
else:
    # Converte ambos para o mesmo CRS (WGS 84)
    bairros_data = bairros_data.to_crs(epsg=4326)
    df_sb = df_sb.to_crs(epsg=4326)

    # Spatial join para contar sistemas bancários por bairro
    join = gpd.sjoin(bairros_data, df_sb, how="left", predicate="contains")
    counts = join.groupby(join.index).size()
    bairros_data["sistemas_bancarios"] = counts.reindex(bairros_data.index, fill_value=0)

    # Cria mapa base
    m = folium.Map(location=[-25.5, -49.3], tiles='OpenStreetMap', zoom_start=12)

    # Adiciona camada dos bairros
    folium.GeoJson(
        bairros_data,
        name='Bairros',
        style_function=lambda feature: {
            'fillColor': '#FFF8DC',
            'color': 'black',
            'weight': 1.5,
            'fillOpacity': 0.6
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["NOME", "sistemas_bancarios"],
            aliases=["Bairro:", "Qtd. de Sistemas Bancários:"],
            localize=True,
            sticky=False,
            labels=True,
            style=("background-color: white; color: black; font-family: arial; font-size: 12px; padding: 5px;")
        )
    ).add_to(m)

    # Adiciona marcadores agrupados
    locations = [[geom.y, geom.x] for geom in df_sb.geometry if geom.geom_type == 'Point']
    marker_cluster = MarkerCluster(name='Sistemas Bancários (pontos)')
    for loc in locations:
        folium.Marker(location=loc).add_to(marker_cluster)
    marker_cluster.add_to(m)

    # Adiciona mapa de calor
    HeatMap(locations, name='Mapa de Calor').add_to(m)

    # Controles
    folium.LayerControl().add_to(m)
    m.add_child(MeasureControl())

    # Exibe o mapa no Streamlit
    folium_static(m)
