import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.data_cleaning import limpar_dados
import sys 

caminho_arquivo = "c:/Users/Camila Sousa/OneDrive/Área de Trabalho/portifólio/Rendimento_Escolar_Analise/data/rendimento_escolar_2021.xlsx"
abas_esperadas = ["Taxa de aprovação", "Taxa de reprovação", "Taxa de abandono"]

# Função: Gráfico de Linha por Ano
def grafico_linha(df, titulo):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Ano', y='Total', hue='Unidade Geográfica', marker='o')
    plt.title(titulo)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# Função: Gráfico de Barras Empilhadas por Dependência Administrativa
def grafico_barras(df, titulo):
    plt.figure(figsize=(12, 7))
    sns.barplot(data=df, x='Ano', y='Total', hue='Dependência administrativa')
    plt.title(titulo)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# Função: Heatmap para variações regionais
def heatmap(df, titulo):
    dados_pivot = df.pivot_table(values='Total', index='Unidade Geográfica', columns='Ano', aggfunc='sum')
    plt.figure(figsize=(10, 8))
    sns.heatmap(dados_pivot, cmap='YlGnBu', annot=True, fmt=".1f", linewidths=.5)
    plt.title(titulo)
    plt.show()

# Função: Cálculo de Recuperação - Verifica se valores são válidos antes de calcular
def calcular_recuperacao(media_rendimento, ano_base, ano_comparacao):
    # Verificando se o valor do ano base (ano_base) não é zero ou nulo
    if media_rendimento[ano_base] != 0 and pd.notnull(media_rendimento[ano_base]):
        recuperacao = (media_rendimento[ano_comparacao] - media_rendimento[ano_base]) / media_rendimento[ano_base] * 100
        return recuperacao
    else:
        return None  

# Carregar e limpar os dados de cada aba de forma controlada
dados = pd.DataFrame()
for aba in abas_esperadas:
    df_aba = limpar_dados(caminho_arquivo, aba).assign(Aba=aba)
    dados = pd.concat([dados, df_aba])

# Converter a coluna 'Ano' para inteiro, corrigindo possíveis erros
dados['Ano'] = pd.to_numeric(dados['Ano'], errors='coerce')

# Remover valores nulos e filtrar anos esperados (2020, 2021, 2022, 2023)
dados = dados[dados['Ano'].isin([2020, 2021, 2022, 2023])]

# Exibindo os gráficos e insights para cada aba, apenas uma vez
for aba in abas_esperadas:
    df_filtrado = dados[dados['Aba'] == aba]

    # Exibindo gráficos
    grafico_linha(df_filtrado, f'{aba} - Evolução por Ano')
    grafico_barras(df_filtrado, f'{aba} - Comparação por Dependência')
    heatmap(df_filtrado, f'{aba} - Variações Regionais')

    # Média de rendimento por ano
    media_rendimento = df_filtrado.groupby('Ano')['Total'].mean()
    print(f'Média de Rendimento de {aba}:')
    print(media_rendimento)

    # Comparando ano a ano a evolução do rendimento
    incremento_rendimento = media_rendimento.pct_change() * 100
    print(f'Variação Percentual no Rendimento de {aba}:')
    print(incremento_rendimento)

    # Focando na recuperação pós-pandemia: 2022 vs 2021 e 2023 vs 2021
    recup_2022_2021 = calcular_recuperacao(media_rendimento, 2021, 2022)
    recup_2023_2021 = calcular_recuperacao(media_rendimento, 2021, 2023)

    if recup_2022_2021 is not None:
        print(f'Recuperação de 2022 em relação a 2021 em {aba}: {recup_2022_2021:.2f}%')
    else:
        print(f'Recuperação de 2022 em relação a 2021 em {aba}: Dados insuficientes')

    if recup_2023_2021 is not None:
        print(f'Recuperação de 2023 em relação a 2021 em {aba}: {recup_2023_2021:.2f}%')
    else:
        print(f'Recuperação de 2023 em relação a 2021 em {aba}: Dados insuficientes')

sys.exit() 

