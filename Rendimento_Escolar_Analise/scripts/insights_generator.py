def gerar_insights(df):
    taxa_media_aprovacao = df['Total'].mean()
    melhor_regiao = df.groupby('Unidade Geográfica')['Total'].mean().idxmax()

    insights = f"""
    📊 A taxa média de aprovação é de {taxa_media_aprovacao:.2f}%.
    🌍 A região com maior taxa de aprovação é: {melhor_regiao}.
    """
    return insights
