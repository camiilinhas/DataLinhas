import matplotlib.pyplot as plt
import seaborn as sns

def grafico_taxa(df, titulo, coluna='Total'):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Ano', y=coluna, hue='Unidade Geográfica')
    plt.title(titulo)
    plt.xlabel('Ano')
    plt.ylabel(f'{coluna} (%)')
    plt.grid(True)
    plt.show()
