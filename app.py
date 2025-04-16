import streamlit as st
from streamlit_folium import folium_static
import folium

# Configuração da página (corrigido)
PAGE_CONFIG = {
    "page_title": "Aplicação de Mapas",
    "page_icon": ":smiley:",
    "layout": "centered"
}
st.set_page_config(**PAGE_CONFIG)  # Corrigido: adicionado ** para desempacotar

def main():
    st.title("Como adicionar mapas no Streamlit")
    st.subheader("Cabe nos cadernos do Colab")  # Preservando o texto original
    menu = ["Menu", "Mapa"]
    
    # Corrigido: st.sidebar.selectbox
    choice = st.sidebar.selectbox("Menu", menu)  
    
    if choice == "Menu":  # Corrigido: operador de comparação ==
        st.subheader("Página inicial 1")
    elif choice == "Mapa":  # Corrigido: operador de comparação ==
        st.subheader("Visualizar Mapa")  # Interpretação de "Ismailzar Mapa"
        
        # Criando o mapa (corrigido conforme comentário linha 17)
        m = folium.Map(
            location=[-25.5, -49.3],  # Coordenadas aproximadas de Curitiba
            zoom_start=11
        )
        
        # Adicionando um marcador de exemplo
        folium.Marker(
            location=[-25.5, -49.3],
            popup="Localização exemplo"
        ).add_to(m)
        
        with st.container():  # Corrigido: st.container() em vez de st.scho()
            folium_static(m)  # Exibindo o mapa
    else:
        st.subheader("")

if __name__ == "__main__":  # Corrigido: sintaxe correta
    main()
