# Airbnb Analytics V4 — análise gratuita, local e auditável

Dashboard Streamlit com dados anonimizados de uma acomodação em Ubatuba. A V4 mantém os indicadores financeiros e de ocupação e acrescenta classificação **automática baseada em regras**, comparação com anotações manuais provisórias e exportação CSV. **Não usa API, chave, créditos, serviços pagos ou IA generativa.**

## Como executar (Windows, VS Code)

1. Extraia o ZIP e abra a pasta `airbnb_analytics_v4_gratis` no VS Code.
2. No terminal, execute:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

3. Abra o endereço local mostrado no terminal (geralmente http://localhost:8501). Se a V3 ainda estiver rodando, o Streamlit pode usar outra porta. Para parar a versão anterior, clique no terminal dela e pressione Ctrl+C uma vez.
4. Desça até **V4 — Classificação local e avaliação**. Use o botão para baixar as classificações em CSV.

## Arquivos

- `app.py`: dashboard Streamlit.
- `classificador_local.py`: regras de classificação transparentes e reproduzíveis.
- `avaliacoes_publicas.csv`: 11 comentários públicos anonimizados, adaptados dos textos compartilhados; precisam de conferência antes da publicação.
- `classificacoes_v4.csv`: resultados da classificação local, já calculados, para inspeção.
- `reservas_anonimizadas.csv`: reservas sem dados identificáveis.
- `caracteristicas_avaliacoes.csv` e `indicadores_avaliacoes.csv`: características e notas agregadas informadas pelo Airbnb.
- `analise.py`: análise tabular da versão anterior.

## Metodologia e limitações

- O algoritmo local detecta temas por padrões de palavras, e sentimento por pistas textuais. **Não chame esta etapa de classificação por LLM ou IA generativa.** É um *baseline* heurístico, útil para aprender avaliação e validar um pipeline.
- A referência manual é provisória, elaborada a partir de comentários adaptados; não é verdade-terreno validada independentemente. As métricas micro de precisão, revocação e F1 medem concordância com essa referência e não a satisfação dos hóspedes.
- Cada comentário pode receber mais de um tema. As 11 avaliações não são o denominador das características agregadas fornecidas pela plataforma.
- A nota 4,91/5 refere-se a custo-benefício, não à nota geral do imóvel.
- As duas noites de amigos foram 9 e 10 de janeiro. Disponibilidade presumida: 31/12/2025 a 28/02/2026, 60 noites. Receita após taxas não equivale a lucro.
- Não publique nomes, mensagens privadas, identificadores de reservas ou documentos financeiros originais.

## Evolução futura

Para experimentar um **LLM gratuito e local**, é possível usar um modelo aberto com ferramentas como Ollama, dependendo da memória e da capacidade do computador. Essa etapa exigirá configuração adicional e não faz parte da V4.
