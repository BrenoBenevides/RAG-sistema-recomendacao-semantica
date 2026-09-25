# Projeto 3 – Sistema de Recomendação Semântica com Embeddings, Banco Vetorial, Filtros de Metadados e IA Generativa

# Abra o terminal ou prompt de comando, navegue até a pasta com os arquivos e execute o comando abaixo para criar o container com o banco vetorial (lembre-se de abrir a janela do Docker Desktop antes):

docker-compose up -d

# Abra o terminal ou prompt de comando, navegue até a pasta com os arquivos e execute o comando abaixo para criar um ambiente virtual:

conda create --name dsamebvp3 python=3.13

# Ative o ambiente:

conda activate dsamebvp3 (ou: source activate dsamebvp3)

# Instale o pip e as dependências:

conda install pip
pip install -r requirements.txt 

# Teste a instalação do qdrant:

python dsa_testa_qdrant.py

# Execute a ingestão no banco vetorial:

python dsa_ingestao.py

# Execute o script para rodar a aplicação:

streamlit run dsa_app.py

# Para testar a app:

# Preciso de um notebook bom para viagens.
# Qual o melhor headphone com cancelamento de ruído?
# Qual console de games suporta 4k?
# Qual o melhor automóvel com baixo consumo de combustível?

# Use os comandos abaixo para desativar o ambiente virtual e remover o ambiente (opcional):

conda deactivate
conda remove --name dsamebvp3 --all






