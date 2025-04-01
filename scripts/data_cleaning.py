import pandas as pd

def limpar_dados(caminho_arquivo, aba):
    # Carregar os dados
    df = pd.read_excel(caminho_arquivo, sheet_name=aba)

    # 1. Remover valores nulos
    df = df.dropna(subset=['Ano', 'Total', 'Unidade Geográfica', 'Dependência administrativa'], how='any')

    # 2. Corrigir tipos de dados
    df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')  
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce') 
    
    # 3. Remover duplicatas
    df = df.drop_duplicates()

    # 4. Filtrar os anos
    df = df[df['Ano'].isin([2020, 2021, 2022, 2023])]  

    # 5. Substituir valores inconsistentes 
    df['Dependência administrativa'] = df['Dependência administrativa'].replace({
        'Pública': 'Pública',
        'Privada': 'Privada'
       
    })
    
    return df



