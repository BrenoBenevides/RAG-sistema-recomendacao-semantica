# Projeto 3 – Sistema de Recomendação Semântica com Embeddings, Banco Vetorial, Filtros de Metadados e IA Generativa
# Módulo da app

# Importa a biblioteca Streamlit para criação da interface web interativa
import streamlit as st

# Importa a classe responsável pela geração de embeddings
from src.embeddings import EmbeddingModel

# Importa a classe responsável pelo banco de dados vetorial
from src.vector_db import VectorDB

# Importa a classe responsável pela interação com o modelo de linguagem
from src.llm_service import LLMService

# Define as configurações gerais da página Streamlit como título, ícone e layout
st.set_page_config(page_title="Data Science Academy", page_icon=":100:", layout="wide")

# Define uma função com cache para carregar recursos pesados apenas uma vez
@st.cache_resource
def load_resources():
    
    # Retorna instâncias do modelo de embeddings, banco vetorial e serviço de LLM
    return EmbeddingModel(), VectorDB(), LLMService()

# Inicializa os recursos cacheados
embed_model, db, llm_service = load_resources()

# Define o título principal da aplicação
st.title("Data Science Academy - Projeto 3")
st.title("Sistema de Recomendação")

# Define o subtítulo da aplicação com foco no assistente inteligente
st.title("🤖 Consultor de Compras Inteligente")

# Exibe uma descrição resumida da abordagem utilizada
st.markdown("Busca Semântica + Filtros de Metadados (Hybrid Search)")

# Define o cabeçalho da barra lateral para filtros
st.sidebar.header("Filtros")

# Define as categorias disponíveis para filtragem
categorias = ["Todas", "Games", "Notebooks", "Áudio"]

# Define as marcas disponíveis para filtragem
marcas = ["Todas", "Sony", "Microsoft", "Apple", "Dell", "JBL"]

# Cria um seletor de categoria na barra lateral
filter_category = st.sidebar.selectbox("Categoria", categorias)

# Cria um seletor de marca na barra lateral
filter_brand = st.sidebar.selectbox("Marca", marcas)

# Cria um slider para definição da faixa de preço
price_range = st.sidebar.slider("Faixa de Preço (R$)", 0, 10000, (0, 10000))

# Cria uma área expansível na barra lateral para informações de suporte
with st.sidebar.expander("🆘 Suporte / Fale conosco", expanded=False):
    
    # Exibe o email de contato do suporte
    st.write("Se tiver dúvidas envie mensagem para suporte@datascienceacademy.com.br")

# Exibe um aviso informativo sobre limitações da IA
st.sidebar.info(
    "Aviso: IA pode gerar respostas imprecisas, incompletas ou erradas. "
    "Sempre verifique informações críticas antes de confiar totalmente no resultado."
)

# Cria um campo de texto para entrada da consulta do usuário
query = st.text_input(
    "O que você está procurando hoje?",
    placeholder = "Ex: Preciso de um notebook bom para trabalhar em viagens"
)

# Cria um botão para iniciar o processo de busca
if st.button("Buscar Recomendações"):
    
    # Verifica se o usuário não digitou nenhuma consulta
    if not query:
        
        # Exibe um aviso solicitando a entrada da consulta
        st.warning("Por favor, digite o que você procura.")
    
    else:
        
        # Exibe um indicador visual de processamento
        with st.spinner("Processando vetores e aplicando filtros..."):
            
            # Converte a consulta do usuário em vetor de embedding
            query_vector = embed_model.get_embedding(query)
            
            # Executa a busca vetorial no banco com filtros de metadados
            search_results = db.search(query_vector = query_vector,
                                       category = filter_category,
                                       brand = filter_brand,
                                       price_min = price_range[0],
                                       price_max = price_range[1],
                                       limit = 3)
            
            # Verifica se nenhum resultado foi encontrado
            if not search_results:
                
                # Exibe mensagem de erro informando ausência de resultados
                st.error("Nenhum produto encontrado com esses filtros e termos.")
            
            else:
                
                # Extrai os payloads dos resultados retornados
                context_products = [hit.payload for hit in search_results]
                
                # Gera a recomendação utilizando o modelo de linguagem
                recommendation = llm_service.generate_recommendation(query, context_products)
                
                # Cria duas colunas para organização da interface
                col1, col2 = st.columns([1, 1])
                
                # Define a primeira coluna para exibição da recomendação
                with col1:
                    
                    # Exibe o subtítulo da recomendação
                    st.subheader("💡 Recomendação da IA")
                    
                    # Exibe o texto gerado pela IA
                    st.write(recommendation)
                
                # Define a segunda coluna para exibição dos produtos recuperados
                with col2:
                    
                    # Exibe o subtítulo da seção de contexto
                    st.subheader("📦 Produtos Recuperados (Contexto)")
                    
                    # Itera sobre os produtos recuperados
                    for prod in context_products:
                        
                        # Cria um expander para cada produto
                        with st.expander(f"{prod['name']} - R$ {prod['price']}"):
                            
                            # Exibe a marca do produto
                            st.write(f"**Marca:** {prod['brand']}")
                            
                            # Exibe a descrição do produto
                            st.write(f"**Descrição:** {prod['description']}")



