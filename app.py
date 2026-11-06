"""Dashboard de dados reais anonimizados de uma acomodação em Ubatuba."""
from pathlib import Path
import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parent
INICIO = pd.Timestamp('2025-12-31')
FIM_EXCLUSIVO = pd.Timestamp('2026-03-01')
AMIGOS_INICIO = pd.Timestamp('2026-01-09')
AMIGOS_FIM = pd.Timestamp('2026-01-11')

st.set_page_config(page_title='Airbnb Analytics | Ubatuba', page_icon='🏡', layout='wide')
st.title('🏡 Airbnb Analytics — Ubatuba')
st.caption('Projeto de portfólio | Dados reais anonimizados | Temporada 2025/2026')

@st.cache_data
def carregar():
    return pd.read_csv(BASE / 'reservas_anonimizadas.csv', parse_dates=['checkin','checkout'])

reservas = carregar()
reservas['noites_na_temporada'] = reservas.apply(
    lambda r: max(0, (min(r.checkout, FIM_EXCLUSIVO) - max(r.checkin, INICIO)).days), axis=1
)
temporada = reservas.loc[reservas.noites_na_temporada > 0].copy()

# Cada noite é contada uma única vez, mesmo que duas estadias tenham datas sobrepostas.
noites_airbnb = set()
for r in temporada.itertuples():
    ini, fim = max(r.checkin, INICIO), min(r.checkout, FIM_EXCLUSIVO)
    noites_airbnb.update(pd.date_range(ini, fim - pd.Timedelta(days=1), freq='D'))
noites_amigos = set(pd.date_range(AMIGOS_INICIO, AMIGOS_FIM - pd.Timedelta(days=1), freq='D'))
sobrepostas = noites_airbnb & noites_amigos
noites_unicas = noites_airbnb | noites_amigos
noites_disponiveis = (FIM_EXCLUSIVO-INICIO).days

st.subheader('Visão geral da temporada')
a,b,c,d = st.columns(4)
a.metric('Reservas comerciais', len(temporada))
b.metric('Noites Airbnb', len(noites_airbnb))
c.metric('Noites ocupadas distintas', len(noites_unicas))
d.metric('Ocupação física estimada', f'{len(noites_unicas)/noites_disponiveis:.1%}')

if sobrepostas:
    datas = ', '.join(d.strftime('%d/%m/%Y') for d in sorted(sobrepostas))
    st.warning(f'⚠️ Conflito de calendário: amigos e Airbnb aparecem na(s) mesma(s) noite(s): {datas}. '
               'Verifique as datas antes de usar a taxa de ocupação como resultado definitivo.')

x,y,z = st.columns(3)
x.metric('Receita bruta', f'R$ {temporada.receita_bruta_brl.sum():,.2f}')
y.metric('Após taxas Airbnb', f'R$ {temporada.recebido_apos_taxa_brl.sum():,.2f}')
z.metric('Receita bruta por noite Airbnb', f'R$ {temporada.receita_bruta_brl.sum()/len(noites_airbnb):,.2f}')
st.caption('Receita após taxas da plataforma não é lucro; custos de água/luz e outros gastos não foram integralmente medidos.')

st.subheader('Receita por mês de check-in')
mensal = temporada.assign(mes=temporada.checkin.dt.strftime('%Y-%m')).groupby('mes', as_index=False).agg(
    reservas=('id_reserva','count'), receita_bruta=('receita_bruta_brl','sum'),
    receita_apos_taxas=('recebido_apos_taxa_brl','sum')
)
st.bar_chart(mensal.set_index('mes')[['receita_bruta','receita_apos_taxas']])

st.subheader('Calendário diário da temporada')
cal = pd.DataFrame({'data': pd.date_range(INICIO, FIM_EXCLUSIVO-pd.Timedelta(days=1), freq='D')})
def status(d):
    if d in sobrepostas: return 'CONFLITO: Airbnb + amigos'
    if d in noites_airbnb: return 'Airbnb'
    if d in noites_amigos: return 'Amigos (não comercial)'
    return 'Sem ocupação registrada'
cal['status'] = cal.data.map(status)
cal['mes'] = cal.data.dt.strftime('%Y-%m')
mes = st.selectbox('Mês', sorted(cal.mes.unique()), index=1)
sub = cal.loc[cal.mes==mes, ['data','status']].copy()
sub['data'] = sub.data.dt.strftime('%d/%m/%Y')
st.dataframe(sub, hide_index=True, use_container_width=True)

st.subheader('Preços por tipo de dia')
temporada['dia_semana'] = temporada.checkin.dt.dayofweek
temporada['tipo_dia'] = temporada.dia_semana.map(lambda d: 'Fim de semana (sex/sáb)' if d in (4,5) else 'Outros dias')
# Usar apenas reservas de uma noite para comparar tarifas por diária sem rateios imprecisos.
precos = temporada.loc[temporada.noites==1].groupby('tipo_dia').agg(
    reservas=('id_reserva','count'), preco_medio_brl=('receita_bruta_brl','mean')
).reset_index()
st.dataframe(precos, hide_index=True, use_container_width=True)
st.caption('Comparação descritiva: feriados e Ano-Novo podem influenciar preços; não é uma estimativa causal.')

st.subheader('Avaliações — características destacadas pelos hóspedes')
st.caption('Contagens de características exibidas pelo Airbnb e transcritas pelo anfitrião. Não são classificações produzidas por IA.')
caracteristicas = pd.read_csv(BASE / 'caracteristicas_avaliacoes.csv')
indicadores = pd.read_csv(BASE / 'indicadores_avaliacoes.csv')
col_a, col_b, col_c = st.columns(3)
col_a.metric('Avaliações recebidas', 11)
col_b.metric('Nota de custo-benefício', '4,91 / 5')
col_c.metric('Maior contagem individual', '8 menções')
st.info('As contagens representam hóspedes que selecionaram cada característica, conforme informado pelo Airbnb. '
        'Não é possível deduzir quantas pessoas responderam a cada categoria nem calcular porcentagens válidas com denominador 8 ou 11.')
categoria = st.selectbox('Selecione uma categoria de avaliação', caracteristicas.categoria.unique())
filtrado = caracteristicas.loc[caracteristicas.categoria == categoria].sort_values('mencoes', ascending=True)
st.bar_chart(filtrado.set_index('caracteristica')['mencoes'], horizontal=True, x_label='Quantidade de menções')
with st.expander('Ver todas as características e contagens'):
    st.dataframe(caracteristicas, hide_index=True, use_container_width=True)
st.markdown('**Feedback qualitativo contextual**')
st.write('Pontos positivos relatados: anfitrião atencioso, limpeza, conforto, comunicação e flexibilidade de check-in.')
st.write('Uma observação mencionou distância da praia. A nota agregada de custo-benefício informada é 4,91/5.')
st.caption('As avaliações textuais individuais não foram vinculadas às reservas nem classificadas por IA nesta versão. '
           'Não inferimos quantos hóspedes escreveram comentários sobre cada tema a partir das etiquetas.')

st.subheader('Limitações e qualidade dos dados')
st.markdown('''
- **Validação de datas:** a estadia dos amigos foi corrigida para as noites de 09 e 10/01/2026; não há sobreposição com reservas Airbnb na base.
- **Disponibilidade:** 60 noites assumidas com base no relato do anfitrião, não em calendário exportado.
- **Custos:** apenas estimativa informal de até R$ 200 para água e luz em janeiro; não calcular lucro líquido.
- **Visualizações e conversão:** indisponíveis no aplicativo.
- **Amostra pequena:** resultados descritivos, sem previsão confiável ou afirmações de causalidade.
- **Avaliações:** 11 no total; contagens de etiquetas são fornecidas pela plataforma e não devem ser convertidas em percentuais sem o denominador por pergunta. Não há vínculo individual com reservas.
''')
with st.expander('Ver reservas anonimizadas'):
    st.dataframe(temporada.drop(columns=['dia_semana','tipo_dia']), hide_index=True, use_container_width=True)



# V4 — análise local e avaliação de concordância, sem custo e sem API
st.subheader("🔎 V4 — Classificação local e avaliação")
st.caption("Execução 100% local, sem chave, internet ou envio de comentários. "
           "O classificador é baseado em regras de palavras-chave: não é um LLM nem uma IA generativa.")
from classificador_local import TEMAS, classificar, temas_referencia
from collections import Counter
from io import StringIO

@st.cache_data
def carregar_comentarios():
    return pd.read_csv(BASE / "avaliacoes_publicas.csv", keep_default_na=False)

avaliacoes = carregar_comentarios()
st.metric("Comentários analisados", len(avaliacoes))
st.warning("Os comentários foram adaptados dos trechos fornecidos pelo anfitrião. "
           "Confirme a transcrição antes de publicar. A codificação manual é provisória.")

registros = []
for r in avaliacoes.itertuples(index=False):
    resultado = classificar(r.comentario_publico)
    manual = temas_referencia(r.temas_referencia_provisorios)
    automatico = set(resultado["temas"])
    registros.append({
        "id_avaliacao": r.id_avaliacao,
        "comentario_publico": r.comentario_publico,
        "temas_manuais_provisorios": "; ".join(sorted(manual)),
        "temas_automaticos": "; ".join(sorted(automatico)),
        "sentimento_automatico": resultado["sentimento"],
        "temas_em_comum": "; ".join(sorted(manual & automatico)),
        "apenas_manual": "; ".join(sorted(manual - automatico)),
        "apenas_automatico": "; ".join(sorted(automatico - manual)),
        "evidencias_regras": str(resultado["padroes_detectados"]),
    })
resultados = pd.DataFrame(registros)

st.markdown("**Comparação de temas: classificação manual provisória × regras automáticas**")
contagens = []
for tema in TEMAS:
    man = sum(tema in temas_referencia(r.temas_referencia_provisorios)
              for r in avaliacoes.itertuples(index=False))
    aut = sum(tema in classificar(r.comentario_publico)["temas"]
              for r in avaliacoes.itertuples(index=False))
    contagens.append({"tema": tema, "Manual provisório": man, "Automático local": aut})
st.bar_chart(pd.DataFrame(contagens).set_index("tema"))

# Avaliação multilabel: pares comentário × tema, não quantidade de hóspedes.
tp = fp = fn = tn = 0
por_tema = []
for tema in TEMAS:
    tpi = fpi = fni = tni = 0
    for r in avaliacoes.itertuples(index=False):
        verdadeiro = tema in temas_referencia(r.temas_referencia_provisorios)
        previsto = tema in classificar(r.comentario_publico)["temas"]
        if verdadeiro and previsto: tpi += 1
        elif previsto: fpi += 1
        elif verdadeiro: fni += 1
        else: tni += 1
    tp += tpi; fp += fpi; fn += fni; tn += tni
    por_tema.append({"tema": tema, "acertos_positivos": tpi,
                     "falsos_positivos": fpi, "nao_detectados": fni})
precisao = tp / (tp + fp) if tp + fp else 0.0
revocacao = tp / (tp + fn) if tp + fn else 0.0
f1 = 2 * precisao * revocacao / (precisao + revocacao) if precisao + revocacao else 0.0
c1, c2, c3 = st.columns(3)
c1.metric("Precisão micro", f"{precisao:.1%}")
c2.metric("Revocação micro", f"{revocacao:.1%}")
c3.metric("F1 micro", f"{f1:.1%}")
st.caption("Métricas de comparação com a referência manual provisória: "
           "11 comentários × 7 temas = 77 decisões binárias. "
           "Não medem satisfação dos hóspedes nem qualidade de um LLM.")
st.dataframe(pd.DataFrame(por_tema), hide_index=True, use_container_width=True)

st.markdown("**Auditoria comentário a comentário**")
st.dataframe(resultados, hide_index=True, use_container_width=True)
st.download_button("📥 Baixar classificações e comparação (CSV)",
    data=resultados.to_csv(index=False).encode("utf-8-sig"),
    file_name="classificacoes_v4.csv", mime="text/csv")

with st.expander("Como funciona a classificação automática?"):
    st.markdown("""
    - Busca expressões relacionadas a cada tema no próprio comentário.
    - Permite múltiplos temas para o mesmo comentário.
    - Usa pistas linguísticas simples para sentimento positivo, negativo, misto ou inconclusivo.
    - **Limitação:** regras podem errar com ironia, negações, contexto e sinônimos.
    - A referência manual é provisória e foi criada a partir de comentários adaptados.
    - A análise não usa modelos de linguagem, nem realiza chamadas a serviços externos.
    """)
st.info("Próxima evolução opcional: usar um modelo de linguagem aberto, executado localmente, "
        "quando houver hardware adequado; manter esta versão como baseline interpretável.")


# Comparação: classificador local x análise do ChatGPT
st.divider()
st.subheader("🤖 Comparação com análise do ChatGPT")

arquivo_ia = BASE / "airbnb_analytics_analise_chatgpt.csv"

if arquivo_ia.exists():
    analise_ia = pd.read_csv(arquivo_ia)

    st.success("Análise dos 11 comentários carregada com sucesso!")

    st.caption(
        "Classificação assistida pelo ChatGPT, realizada fora do "
        "aplicativo e importada por CSV. Não utiliza API."
    )

    st.dataframe(
        analise_ia,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Baixar análise do ChatGPT",
        data=analise_ia.to_csv(index=False).encode("utf-8-sig"),
        file_name="analise_chatgpt.csv",
        mime="text/csv"
    )
else:
    st.warning("Arquivo de análise do ChatGPT não encontrado.")

# Comparação automática: regras locais x revisão do ChatGPT
st.divider()
st.subheader("📊 Avaliação do classificador local")

from classificador_local import classificar

arquivo_chatgpt = BASE / "airbnb_analytics_analise_chatgpt.csv"

if arquivo_chatgpt.exists():
    revisao = pd.read_csv(arquivo_chatgpt).fillna("")

    registros = []

    for _, linha in revisao.iterrows():
        temas_chatgpt = {
            tema.strip()
            for tema in linha["temas_revisados"].split(";")
            if tema.strip()
        }

        resultado_local = classificar(
            linha["comentario_publico_anonimizado"]
        )

        temas_local = set(resultado_local["temas"])

        registros.append({
            "Avaliação": linha["id_avaliacao"],
            "Temas ChatGPT": ", ".join(sorted(temas_chatgpt)),
            "Temas classificador local": ", ".join(sorted(temas_local)),
            "Coincidentes": ", ".join(sorted(temas_chatgpt & temas_local)),
            "Somente ChatGPT": ", ".join(sorted(temas_chatgpt - temas_local)),
            "Somente classificador": ", ".join(sorted(temas_local - temas_chatgpt)),
        })

    comparacao = pd.DataFrame(registros)

    st.dataframe(
        comparacao,
        hide_index=True,
        use_container_width=True
    )

    total_coincidencias = sum(
        len(set(reg["Coincidentes"].split(", ")) - {""})
        for reg in registros
    )

    st.metric(
        "Identificações de temas coincidentes",
        total_coincidencias
    )

    st.download_button(
        "Baixar comparação final",
        data=comparacao.to_csv(index=False).encode("utf-8-sig"),
        file_name="comparacao_classificadores.csv",
        mime="text/csv"
    )
else:
    st.warning("CSV da análise do ChatGPT não encontrado.")