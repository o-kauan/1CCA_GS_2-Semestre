# Módulo de Inteligência Climática e Prevenção de Riscos — Bridge AI (Citizen Assist AI)

Este repositório contém a documentação e os scripts em Python referentes ao **Módulo de Inteligência Climática e Prevenção de Riscos** do projeto **Bridge AI** (desenvolvido no contexto do desafio *Citizen Tech* da FIAP). 

Esta etapa específica do projeto foca na modelagem linear e estatística aplicada a dados meteorológicos reais para apoiar idosos em zonas rurais e seus familiares na tomada de decisões preventivas.

---

## 1. Contextualização e Justificativa da Base de Dados

Como resposta ao desafio *Citizen Tech*, o projeto **Citizen Assist AI** (denominado **Bridge AI** para esta entrega) consiste no desenvolvimento de um assistente digital inteligente estruturado para suavizar barreiras de acesso a serviços públicos, documentação, direitos fundamentais e orientações comunitárias essenciais. No escopo específico desta avaliação de **Modelagem Linear**, a solução direciona seu foco estratégico para o atendimento de **idosos residentes em zonas rurais** e de seus familiares que os auxiliam à distância.

Consciente de que a infraestrutura de conectividade no campo é frequentemente limitada, o sistema foi concebido para operar de forma híbrida e adaptativa. Para validar a eficácia técnica e o rigor analítico da proposta, a aplicação integra um **Módulo de Inteligência Climática e Prevenção de Riscos**, alimentado por dados meteorológicos geolocalizados em tempo real e históricos (extraídos via API da **Open-Meteo** com coordenadas específicas de zonas agrícolas paulistas).

Na prática, o assistente capta as coordenadas da localidade do usuário — seja no ambiente urbano ou no campo — processando-as por meio de modelos estatísticos e algoritmos de regressão em Python. Dessa forma, a ferramenta traduz dados brutos (temperatura, umidade e precipitação) em inteligência acionável, calculando previsões precisas e emitindo alertas preventivos automatizados (contra geadas ou chuvas extremas). Com isso, o *Citizen Assist AI* otimiza o planejamento de deslocamentos, evita viagens desnecessárias aos centros urbanos e protege a agricultura familiar e a segurança da comunidade rural.

Este relatório responde a uma pergunta central: **que relações entre temperatura, umidade e chuva a base mostra, e quanto confiar nelas para alertar o usuário?**

### Resumo dos Dados Utilizados

* **Fonte:** Open-Meteo (`open-meteo.com`), arquivo CSV armazenado no repositório.
* **Local:** Interior de São Paulo.
* **Período e Frequência:** 168 registros horários (7 dias completos), a partir de 06/11/2026 00:00.
* **Variáveis Principais:**
  * `temperature_2m` (°C): Temperatura do ar a 2 metros de altura.
  * `relative_humidity_2m` (%): Umidade relativa do ar.
  * `precipitation` (mm/h): Volume de precipitação por hora.
* **Variável Descartada:** `rain (mm)`, pois apresentou correlação de 0,85 com a precipitação, sendo tratada como redundante.

> *Nota:* Esta análise fornece a base estatística climática do módulo; ela não mede o envelhecimento da população rural nem o uso do assistente, que são tratados em outras etapas e matérias do projeto.

---

## 2. Técnicas e Escopo Estatístico

O pipeline estatístico foi implementado inteiramente em **Python**, utilizando bibliotecas como `pandas`, `SciPy`, `statsmodels`, `scikit-learn` e `seaborn`. As análises seguiram o nível de significância padrão de alfa = 5%, salvo quando especificado o contrário.

| Item | Técnica Aplicada | Variáveis Envolvidas |
| :--- | :--- | :--- |
| **02** | Probabilidade com distribuição normal | Temperatura |
| **03** | Teste Z para a média (alfa = 6% e 9%) | Temperatura |
| **04** | Regressão linear simples, correlação de Pearson, R² e Teste F | Temperatura (Y) e Umidade (X) |
| **05** | Regressão linear múltipla | Temperatura (Y); Umidade e Precipitação (X) |
| **06** | Regressão logística binária | Chuva (1 se precipitação > 0,1 mm/h); Temperatura e Umidade (X) |

### Estatísticas Descritivas Básicas
* **Temperatura:** Varia entre cerca de 15 °C e 31 °C na semana, com média de **21,46 °C** e mediana de **20,95 °C**. A diferença de 0,51 °C aponta leve assimetria à direita.
  * Desvio-padrão amostral: 3,80 °C (Variância: 14,44).
* **Umidade Relativa:** Média de aproximadamente **78%**, com valores entre 53% e 100% (distribuição quase uniforme).
  * Desvio-padrão amostral: 12,82% (Variância: 164,35).
* **Precipitação:** Apenas 28 das 168 horas (16,7%) registraram mais de 0,1 mm; o máximo observado foi de cerca de 2,6 mm/h.
  * Desvio-padrão amostral: 0,57 mm/h (Variância: 0,32).
* **Normalidade:** A suposição de distribuição normal é aceitável como aproximação para a temperatura (embora com histograma achatado) e fraca para a precipitação devido à forte concentração de zeros.

---

## 3. Análise com Distribuição Normal de Probabilidade

Ajustando uma distribuição normal à temperatura (média de 21,46 °C e desvio-padrão de 3,80 °C):

| Evento | Probabilidade | Classificação |
| :--- | :--- | :--- |
| P(X < média = 21,46 °C) | 0,5000 (50,0%) | Equiprovável |
| P(X > mediana = 20,95 °C) | 0,5538 (55,4%) | Provável, pouco acima de 50% |

* **Análise:** O primeiro resultado decorre da simetria da normal (a média divide a distribuição ao meio). O segundo difere de 50% porque a mediana amostral fica 0,51 °C abaixo da média (z = -0,14). Como cerca de metade das horas supera a mediana, o modelo normal superestimou essa chance em ~5 pontos percentuais (o custo de assumir normalidade). O uso do desvio-padrão populacional (3,789 °C) difere em apenas 0,3% e não altera as conclusões.

---

## 4. Testes de Hipótese para a Média Amostral

Utilizou-se a referência populacional mu = 21,46 °C e sigma = 3,7998 °C sob diferentes tamanhos de amostra e níveis de significância (alfa).

| Teste | Hipóteses (H0 / H1) | n | alfa | Média Amostral | Estatística Z | Z Crítico | p-valor | Decisão |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **(a)** | H0: mu = mu_0<br>H1: mu < mu_0 | 20 | 6% | 21,96 °C | 0,584 | −1,555 | 0,7204 | Não rejeita H0 |
| **(b)** | H0: mu = mu_0<br>H1: mu > mu_0 | 25 | 9% | 23,02 °C | 2,048 | 1,341 | 0,0203 | Rejeita H0 |

* **Decisão para o assistente:** Esse tipo de teste é empregado para comparar um novo período com uma referência climatológica (por exemplo, confrontar a temperatura da semana corrente contra a média histórica mensal).

---

## 5. Análise Bivariada (Umidade Relativa vs. Temperatura)

* **Covariância:** -18,2018 (indica variação em sentidos opostos / relação inversa).
* **Correlação Linear de Pearson (r):** -0,3737 (correlação linear negativa de intensidade moderada).
* **Equação da Regressão Linear Simples:**
  Temperatura = 30,0641 + (-0,1108 * Umidade)
* **Adequação do Modelo:**
  * Coeficiente de Determinação (R²): **0,1396 (13,96%)** — cerca de 14% da variação da temperatura é explicada linearmente pela umidade relativa.
  * Estatística F: 26,9371 com p-valor = 6,07 * 10^-7 (modelo globalmente significativo e estatisticamente robusto).
* **Exercício de Previsão:** Para uma umidade relativa de 25%, a temperatura prevista pelo sistema é:
  Temperatura = 30,0641 + (-0,1108 * 25) = 27,30 °C

---

## 6. Análise Multivariada (Temperatura, Umidade e Precipitação)

Adicionando a precipitação ao modelo para avaliar o ganho preditivo:

### Matrizes de Covariância e Correlação
* **Matriz de Covariância:**
  * Temperatura x Umidade: -18,2018 | Temperatura x Precipitação: 0,0670
  * Umidade x Precipitação: 2,5255
* **Matriz de Correlação de Pearson:**
  * Temperatura e Umidade: -0,3737
  * Temperatura e Precipitação: 0,0310
  * Umidade e Precipitação: 0,3466 (correlação positiva moderada).

### Resumo dos Coeficientes e Métricas do Modelo Múltiplo
* **Equação:** Temperatura = beta_0 + beta_1(Umidade) + beta_2(Precipitação)
* **R²:** 0,1689 | **R² Ajustado:** 0,1588 (a inclusão da chuva eleva a explicação de 14,0% para 16,9%).
* **Estatística F:** 16,77 (p-valor = 2,35 * 10^-7).
* **Erro-padrão dos resíduos:** 3,49 °C (apenas 8% menor que o desvio-padrão original de 3,80 °C).
* **Fator de Inflação da Variância (VIF):** 1,14 (ausência de multicolinearidade problemática).

---

## 7. Considerações Finais e Recomendações

Os resultados demonstram sólida viabilidade técnica para a implantação do assistente digital **Bridge AI** (*Citizen Assist AI*). Embora o teste piloto de 7 dias tenha caráter demonstrativo, ele comprova que o sistema captura variações térmicas e hídricas relevantes.

Em escalas futuras, o assistente contará com:
1. Séries temporais ampliadas e maior diversidade climática.
2. Refinamento dinâmico de desvios-padrão e comportamentos de precipitação.
3. Suporte a pequenos agricultores no planejamento de irrigação e colheita, além de orientação a moradores urbanos em cenários de instabilidade climática.

---

## Referências

* **Repositório de Dados:** [Open-Meteo CSV (GitHub)](https://raw.githubusercontent.com/o-kauan/1CCA_GS_2-Semestre/refs/heads/main/Modelagem%20Linear/Base%20de%20dados%20Rural/open-meteo-22.74S47.67W526m.csv)
* **FIAP Experience:** *Citizen Tech*. Disponível em: <https://experience.fiap.com.br/global-solution-citizen-tech>.
* **Portal do Envelhecimento:** *O envelhecimento da população rural é um dos desafios da Agricultura Familiar*. Disponível em: <https://portaldoenvelhecimento.com.br/o-envelhecimento-da-populacao-rural-e-um-dos-desafios-da-agricultura-familiar/>.
* **Open-Meteo:** Free Open-Source Weather API. Disponível em: <https://open-meteo.com/>.
* **INMET:** Instituto Nacional de Meteorologia. Disponível em: <https://portal.inmet.gov.br/>.
* **IBGE:** Portal estatístico oficial. Disponível em: <https://www.ibge.gov.br/>.
