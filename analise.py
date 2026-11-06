"""Airbnb Analytics: análise descritiva de reservas anonimizadas."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).parent
reservas = pd.read_csv(BASE / 'reservas_anonimizadas.csv', parse_dates=['checkin', 'checkout'])
INICIO = pd.Timestamp('2025-12-31')
FIM_EXCLUSIVO = pd.Timestamp('2026-03-01')  # inclui a noite de 28/02

# Sobreposição de noites, evitando contar noites fora do período
reservas['noites_temporada'] = reservas.apply(
    lambda r: max(0, (min(r['checkout'], FIM_EXCLUSIVO) - max(r['checkin'], INICIO)).days), axis=1
)
temporada = reservas[reservas['noites_temporada'] > 0].copy()
noites_disponiveis = (FIM_EXCLUSIVO - INICIO).days
noites_ocupadas = int(temporada['noites_temporada'].sum())

print('AIRBNB ANALYTICS — TEMPORADA 2025/2026')
print(f'Reservas: {len(temporada)}')
print(f'Noites ocupadas: {noites_ocupadas} / {noites_disponiveis}')
print(f'Ocupação estimada: {noites_ocupadas/noites_disponiveis:.1%}')
print(f'Receita bruta: R$ {temporada["receita_bruta_brl"].sum():,.2f}')
print(f'Receita após taxa Airbnb: R$ {temporada["recebido_apos_taxa_brl"].sum():,.2f}')
print('Nota: não foram descontados custos operacionais.')

# Receita por mês de check-in, para reservas integralmente no período
mensal = temporada.assign(mes=temporada['checkin'].dt.strftime('%Y-%m')).groupby('mes', as_index=False).agg(
    reservas=('id_reserva', 'count'), receita_bruta=('receita_bruta_brl', 'sum')
)
print('\nResumo mensal:')
print(mensal.to_string(index=False))
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(mensal['mes'], mensal['receita_bruta'])
ax.set_title('Receita bruta por mês de check-in')
ax.set_ylabel('Receita bruta (R$)')
ax.set_xlabel('Mês')
fig.tight_layout()
fig.savefig(BASE / 'receita_mensal.png', dpi=160)
plt.close(fig)
mensal.to_csv(BASE / 'resumo_mensal.csv', index=False)
