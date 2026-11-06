# Airbnb Superhost Analytics | Dados Reais + Python + IA

### Análise de dados reais do meu Airbnb em Ubatuba, onde conquistei o status de Superhost.

## Sobre o projeto

Este projeto nasceu da minha experiência administrando uma acomodação no Airbnb, em Ubatuba (SP), durante a temporada de verão de 2025/2026.

Além de conquistar o status de **Superhost**, utilizei os dados reais da operação para desenvolver uma solução de análise de negócios com Python, Streamlit e classificação de textos.

O objetivo foi transformar informações de reservas, receitas e avaliações de hóspedes em indicadores úteis para compreender o desempenho da hospedagem e identificar oportunidades de melhoria.

## Objetivos

- Analisar receita, reservas e ocupação durante a alta temporada.
- Investigar padrões de sazonalidade e variação de preços.
- Identificar os aspectos mais valorizados pelos hóspedes.
- Classificar comentários automaticamente por temas.
- Comparar os resultados de um classificador local com uma análise assistida pelo ChatGPT.
- Apresentar os resultados em um dashboard interativo.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Processamento e análise de dados |
| Pandas | Limpeza, organização e transformação dos dados |
| Streamlit | Desenvolvimento do dashboard |
| Matplotlib | Visualização de dados |
| Expressões regulares | Classificação automática de comentários |
| ChatGPT | Revisão temática assistida por IA generativa |
| Git e GitHub | Versionamento e publicação do projeto |

## Principais indicadores

**Temporada analisada:** 31/12/2025 a 28/02/2026

| Indicador | Resultado |
|---|---:|
| Reservas comerciais | 16 |
| Noites ocupadas via Airbnb | 16 |
| Noites de uso não comercial | 2 |
| Ocupação comercial | 26,7% |
| Ocupação total estimada | 30,0% |
| Receita bruta da temporada | R$ 4.542,03 |
| Receita após taxas da plataforma | R$ 4.335,25 |
| Avaliações recebidas | 11 |
| Nota de custo-benefício | 4,91/5 |

A ocupação considera 60 noites disponíveis. As estadias não comerciais foram contabilizadas separadamente das reservas remuneradas.

Os valores após taxas da plataforma não representam lucro líquido, pois não incluem todos os custos operacionais.

## Análise de avaliações com IA

Foram analisados 11 comentários públicos anonimizados, identificando temas como:

- Atendimento e comunicação
- Limpeza
- Conforto
- Flexibilidade de check-in
- Localização
- Comodidades
- Custo-benefício

O projeto utiliza duas abordagens complementares.

**1. Classificador local**

Identifica temas por meio de regras explícitas e expressões regulares, sem dependência de serviços externos.

**2. Análise assistida pelo ChatGPT**

Revisão dos comentários realizada fora da aplicação, com resultados estruturados e importados por CSV.

As duas abordagens são comparadas no dashboard para identificar concordâncias e divergências. A revisão assistida pelo ChatGPT não é tratada como referência absoluta.

A aplicação não exige uma chave de API para funcionar.

## Resultados e aprendizados

O projeto permitiu:

- Consolidar dados financeiros e operacionais em uma única aplicação.
- Diferenciar ocupação comercial de uso não comercial.
- Organizar avaliações qualitativas em categorias mensuráveis.
- Comparar métodos de classificação textual.
- Identificar limitações de qualidade e disponibilidade dos dados.
- Desenvolver um dashboard reproduzível a partir de arquivos CSV.

## Privacidade e limitações

Os dados publicados foram anonimizados para evitar a exposição de informações pessoais dos hóspedes.

O conjunto de dados corresponde a uma única acomodação e a um período limitado. Por isso, os resultados são descritivos e não permitem estabelecer relações causais ou generalizações sobre o mercado de hospedagens.

As avaliações detalhadas da plataforma e as menções encontradas nos comentários são métricas distintas e não devem ser confundidas.

## Como executar

Clone o repositório:

```bash
git clone https://github.com/homerocamargo/airbnb-superhost-analytics.git
cd airbnb-superhost-analytics
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute o dashboard:

```bash
python -m streamlit run app.py
```

Abra o endereço local informado pelo Streamlit no navegador.

## Autor

**Homero Camargo**

Estudante de Ciência de Dados, com interesse em inteligência artificial, automação e desenvolvimento de soluções orientadas a dados.

[GitHub](https://github.com/homerocamargo)