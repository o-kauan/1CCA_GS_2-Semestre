# 🌾 Bridge AI — Da cidade ao campo

> **Global Solution 2026.2 · FIAP · 1º ano de Ciência da Computação**
> Desafio **CitizenTech**: *"Da cidade ao campo, tecnologia para a vida cotidiana."*

---

## 👥 Equipe

| Integrante | RM |
|---|---|
| **Thiago Soalheiro Diamantino** | 569316 |
| **Kauan Damasceno de Lima** | 573727 |

---

## 🎯 O desafio

Criar uma solução **CitizenTech** capaz de melhorar a vida das pessoas nas cidades, no campo ou nas comunidades. O case norteador é o **Bridge AI**: um assistente digital introdutório que facilita o acesso de cidadãos a informações úteis do cotidiano (serviços, documentos, direitos e orientações comunitárias), com:

- um conjunto **verificável** de informações;
- respostas claras com **referências** e **avisos sobre limitações**;
- navegação simples, acessibilidade básica e tratamento de entradas inválidas;
- **sem coletar dados pessoais desnecessários** e **sem se apresentar como canal oficial**;
- protótipo **testável com usuários**, com indicadores de acerto, tempo para achar a informação e facilidade de uso.

**Prazo máximo de entrega das avaliações: 19/11.** A Global Solution pode ser feita em trio, dupla ou individualmente. Para concorrer ao prêmio, enviar também um **vídeo pitch de até 3 minutos** pelo portal para o Scrum Master.

---

## O problema real

A população rural brasileira **está envelhecendo**: a proporção de moradores e produtores com mais de 55 e 65 anos cresce a cada levantamento, enquanto os jovens migram para as cidades em busca de estudo, trabalho e conectividade. Muitos idosos permanecem no campo, em parte pela estabilidade da aposentadoria rural.

Consequências no dia a dia de quem fica:

- resolver burocracia, benefício ou saúde exige **ir à cidade**, às vezes com horas de deslocamento;
- **internet fraca ou ausente** e pouca familiaridade com telas;
- falta de clareza sobre **quais documentos levar** e se a ida é realmente necessária;
- maior exposição a **golpes** envolvendo benefícios e empréstimos;
- o jovem que migrou fica distante e sem forma simples de ajudar.

---

## 🛠️ A solução - Assistente por conversa escrita ou chat de voz

### Núcleo: "Vale a viagem?"

O maior custo do morador rural é **ir à cidade à toa**. O assistente responde:

> *Dá para resolver sem ir? Se precisar ir, quais documentos levar, qual o melhor dia e horário, qual o tempo estimado de espera e qual ônibus pegar?*

- Regras de decisão: *precisa de presença? tem todos os documentos?*
- Checklist personalizado de documentos por serviço.
- Estimativa de espera no atendimento (fila virtual).
- Orientação de transporte (horários e regiões atendidas).
- Toda resposta com **fonte, data e aviso de limitação**; quando não houver certeza, o assistente diz **"não sei"** e orienta onde procurar.

#### Como a decisão é tomada (lógica booleana)

Quem decide se vale a viagem é uma **regra lógica**, não um modelo de linguagem. Isso torna a resposta **previsível, testável e auditável**: a mesma situação sempre gera a mesma orientação, o que importa quando há prazo de benefício em jogo. A IA fica com o que ela faz bem (entender a pergunta e explicar em linguagem simples); a decisão fica com a regra.

> **S = P · (D + U)**
> Vale a viagem (**S**) quando o serviço **exige presença (P)** E (você **tem todos os documentos (D)** OU o caso é **urgente (U)**).

| P (exige presença) | D (tem documentos) | U (urgente) | S (vale a viagem) |
|---|---|---|---|
| 0 | x | x | **0** — resolva à distância |
| 1 | 0 | 0 | **0** — reúna os documentos antes |
| 1 | 0 | 1 | **1** |
| 1 | 1 | 0 | **1** |
| 1 | 1 | 1 | **1** |

#### Exemplo real no protótipo

- **Prova de vida do INSS:** segundo a página oficial do INSS, hoje ela é feita principalmente por **cruzamento de dados** e, em geral, não exige ir ao banco nem à agência. O Bridge AI responde com a fonte e conclui: **"Não precisa ir: dá para resolver à distância. Faça por: Meu INSS (app ou site) ou telefone 135."** Uma viagem evitada.
- **Alerta de golpe:** a mesma página informa que o INSS não faz prova de vida na casa do beneficiário nem por SMS. O assistente traz isso como orientação própria ("é golpe") com a fonte.
- **Cadastro Único (CadÚnico):** exige ir pessoalmente. O assistente lista os documentos, pergunta se a pessoa os tem e se o caso é urgente, e então diz se **vale a viagem** ou se é melhor **reunir os documentos antes**.

### Diferencial técnico: funcionar sem internet

O verdadeiro problema do campo é o sinal.

- Base de conhecimento **local** (ChromaDB roda na própria máquina), com respostas offline e sincronização quando houver conexão.
- Possível implantação como **quiosque** em associação de moradores, posto de saúde ou escola rural.
- **Modo baixa conexão:** respostas curtas, sem imagens pesadas, versão em texto simples e **cartão impresso** com as perguntas mais comuns.
- **No protótipo em Python,** a base é um arquivo JSON local, então o assistente já **funciona sem internet**.

### Módulo clima e risco para quem vive da terra

- Alertas de geada, seca e chuva forte com dados abertos (Open-Meteo, em Python).
- O assistente traduz o dado em orientação prática: *"amanhã há risco de geada, proteja a plantação X"*.
- Usa regressão (ML) e conecta com o tema de energia.
- Na orientação sobre **alertas da Defesa Civil**, o protótipo ensina a receber avisos de chuva forte, enchente e vendaval por **SMS** (sem internet).

### Acessibilidade

- Linguagem simples, letra grande, opção de **voz** (áudio de entrada e saída) como recurso de acessibilidade, não como ideia principal.
- Canal futuro de implantação: WhatsApp. O protótipo da entrega é em **Gradio**.
- **Evolução pensada para quem não tem smartphone:** atendimento por **ligação de telefone comum** (menu por teclas e, depois, voz), que funciona até em celular de teclas.

### Modo família

Um parente na cidade recebe o **resumo do que foi orientado** e pode ajudar. O idoso não entrega dados pessoais ao assistente.

---

## 🧪 O que já está no protótipo × visão futura

O protótipo entregue na disciplina de Python é um assistente **no terminal, baseado em regras**. O restante é a evolução do projeto.

| ✅ No protótipo (Python, terminal) | 🔭 Visão futura |
|---|---|
| Base de conhecimento em **JSON**, com 12 orientações verificadas, 4 categorias, fonte oficial e data de conferência | Base maior e atualizada de tempos em tempos, com RAG (ChromaDB + LangChain) |
| **Busca por pontuação** (+3 por palavra-chave, +1 por palavra do título) com confiança ALTA, MÉDIA ou "não encontrei" | Busca semântica com embeddings |
| Módulo **"Vale a viagem?"** com a regra `S = P · (D + U)` | Estimativa de fila, horários de ônibus e agendamento |
| **Bloqueio de dados pessoais** (8 ou mais dígitos ou `@` são recusados e não registrados) | Guardrails de escopo e prompt injection |
| Navegação por categorias, entradas inválidas tratadas e arquivo ausente ou corrompido sem travar | Interface em Gradio e WhatsApp |
| **Histórico, indicadores e exportação em CSV** | Voz por ligação de telefone, modo família, módulo clima integrado |
| Funciona **sem internet** (base local) | Sincronização quando houver conexão |

> O projeto **não se apresenta como inteligência artificial generativa**: no protótipo, a "inteligência" é de regras. Isso é uma escolha de segurança (o desafio proíbe inventar informação), e não uma limitação escondida.

---

## 🧩 Como o projeto conecta as disciplinas

| Disciplina | Como entra no Bridge AI |
|---|---|
| **Python (PCP)** | Código do assistente: classes `Orientacao`, `BaseConhecimento` e `Assistente`, busca por pontuação, histórico e indicadores |
| **Computer Science** | Regra `S = P · (D + U)` do "Vale a viagem?": tabela-verdade, simplificação algébrica e mapa de Karnaugh; implementada em `regra_vale_a_viagem()` |
| **Modelagem Linear (ML)** | Análise de dados climáticos (Open-Meteo): regressão e relatório sobre risco climático para o produtor rural, base do módulo de clima |
| **Modelagem Matemática e Computacional** | Sistemas lineares e transformação linear aplicados a um problema de deslocamento e distribuição de recursos (frota de ônibus) |

---

## 💡 Nossa narrativa

**O jovem que migrou para a cidade continua ligado ao campo.**

- O **idoso fica no campo**; o filho ou neto foi estudar ou trabalhar na cidade.
- O assistente serve ao idoso **e** ao **familiar na cidade**, que ajuda à distância: confere documentos, recebe o resumo do que foi orientado e organiza a ida quando for necessária.
- O êxodo rural e o envelhecimento são o **problema**; a **conexão entre gerações** é a solução.

É o sentido literal de **"da cidade ao campo"**.

---

## ❓ Respostas às perguntas do desafio

**Quem participará do ecossistema?**
Idosos rurais, familiares na cidade, agentes comunitários de saúde, sindicatos rurais, associações de moradores e os órgãos que publicam as informações.

**Quem é o cidadão beneficiado?**
Idosos de comunidades rurais com acesso limitado a internet e a atendimento presencial, e as famílias que os apoiam à distância.

**Como a solução vai funcionar?**
O usuário pergunta por texto ou áudio. O sistema busca em uma base de documentos verificada, responde com fonte e data e, se não tiver certeza, diz "não sei" e orienta onde procurar. Em seguida, o módulo "Vale a viagem?" diz se a pessoa precisa ir ou se resolve à distância. Funciona offline com base local e sincroniza quando há conexão.

**Quais tecnologias serão usadas?**
Python, RAG (ChromaDB + LangChain), embeddings, reconhecimento e síntese de voz, Gradio, C (estruturas de dados), álgebra booleana, regressão (ML), dados abertos de clima e guardrails (LGPD, escopo, prompt injection). No protótipo em Python: JSON, orientação a objetos, busca por pontuação e álgebra booleana.

**Qual problema será resolvido?**
A dificuldade de acessar informação confiável e de resolver pendências sem deslocamentos desnecessários até a cidade, além da exposição a golpes.

**Quais resultados pode gerar?**
Menos viagens à toa, menos tempo perdido, menos exposição a golpes e mais autonomia para o idoso, medidos pelos indicadores abaixo.

---

## 🌍 ODS relacionados

- **ODS 1** (Erradicação da pobreza): orientação sobre benefícios como o BPC e o CadÚnico.
- **ODS 3** (Saúde e bem-estar): Cartão SUS, vacinação e Farmácia Popular.
- **ODS 9** (Indústria, inovação e infraestrutura): solução que funciona offline, com base local.
- **ODS 10** (Redução das desigualdades): menos distância de acesso entre o campo e a cidade.
- **ODS 16** (Paz, justiça e instituições eficazes): informação clara, com fonte, e alerta contra golpes.

---

## 📊 Indicadores de sucesso

O case pede protótipo testável com usuários. Vamos testar com **no mínimo 5 idosos reais** (familiares, vizinhos, conhecidos do interior) e medir:

| Indicador | Como medir |
|---|---|
| **Taxa de acerto das orientações** | % de perguntas em que a pessoa conseguiu a informação correta |
| **Tempo para encontrar a informação** | Tempo médio por tarefa, em segundos |
| **Facilidade de uso** | Nota de 1 a 5 dada pelo usuário |
| **Viagens evitadas (estimadas)** | Casos em que o assistente indicou que dava para resolver sem ir |
| **"Não sei" corretos** | % de vezes em que o assistente admitiu não saber em vez de inventar |
| **Resposta encontrada** | % de atendimentos em que existia uma orientação para a dúvida |
| **Tentativas por atendimento** | Quantas vezes a pessoa precisou reescrever a pergunta |

No protótipo em Python, esses indicadores são calculados automaticamente a partir de `data/historico.json` e exportados em `data/atendimentos.csv`. A disciplina de Python exige no mínimo **3 pessoas de fora da equipe e 10 atendimentos**; o nosso objetivo de 5 idosos reais cobre essa exigência.

### Resultados dos testes **[PREENCHER depois dos testes]**

| Indicador | Resultado |
|---|---|
| Pessoas testadas / atendimentos | [PREENCHER] |
| Taxa de acerto (%) | [PREENCHER] |
| Tempo médio para encontrar (s) | [PREENCHER] |
| Facilidade de uso (1 a 5) | [PREENCHER] |
| Viagens evitadas (%) | [PREENCHER] |
| Dúvidas sem solução | [PREENCHER] |
| Melhoria feita a partir do teste | [PREENCHER] |

Registros dos testes ficam em `docs/testes-usuarios/`. Não registrar nomes nem dados das pessoas.

---

## 🔒 Segurança, ética e limites

- **Não é canal oficial.** Todas as respostas trazem aviso e indicam o órgão responsável.
- **Sem dados pessoais desnecessários.** O assistente não pede CPF, endereço ou dados bancários. No protótipo, pergunta com **8 ou mais dígitos** ou com **@** é recusada e **não é registrada**.
- **Toda resposta com fonte e data.** Informação sem fonte verificável não entra na base.
- **Armadilha de contradição/desatualização** documentada na base (exigência da disciplina de IA), com tratamento explícito.
- **Guardrails:** escopo (só responde dentro do tema), prompt injection na fonte e LGPD.
- **Entradas inválidas** tratadas em todos os módulos. Arquivo da base ausente ou corrompido **não trava** o programa.

### ⚠️ Limitações

- No protótipo, a busca é por **palavras-chave e pontuação**: ela só responde o que está na base e pode não entender frases muito diferentes das palavras-chave cadastradas.
- A base tem 12 orientações. As regras dos serviços **mudam**, então as fontes precisam ser reconferidas de tempos em tempos.
- Algumas fontes são **notícias oficiais de 2025** (Cartão SUS, Farmácia Popular, vacina da gripe), e a orientação sobre alertas da Defesa Civil usa a página do **Paraná**; o texto de cada orientação avisa quando é preciso confirmar a informação atual.
- A regra do "Vale a viagem?" **orienta**, mas não confirma direitos nem prazos: a decisão final é sempre da pessoa, junto ao órgão responsável.

---

## 🧠 Banco de ideias

Ideias que surgiram no brainstorm. Algumas viram módulos, outras ficam como possibilidade.

### Ideias para se destacar
- **"Resolvo sem ir à cidade"** — o que dá para resolver por telefone/canal digital e o que exige presença, com a viagem organizada.
- **Detector de golpe** — o idoso cola uma mensagem suspeita (ex.: "seu benefício foi bloqueado") e recebe uma avaliação de risco com explicação.
- **Modo família** — resumo das orientações enviado a um parente.
- **Saúde e benefícios** — posto de saúde, vacinação, medicamentos de uso contínuo, aposentadoria rural, sempre com fonte.
- **Modo baixa conexão** — texto simples, SMS ou cartão impresso.
- **Atendimento por ligação de telefone** — menu por teclas (1 = sim, 2 = não) e, depois, voz; funciona sem app e sem internet.
- **Contador de impacto** — cada consulta mostra a viagem, o tempo e o dinheiro poupados (como estimativa declarada, com fonte).
- **Ponte humana** — quando a IA não sabe, diz "não sei" e encaminha para um familiar, agente comunitário ou sindicato.
- **Simulador de impacto para o gestor público** — quanto tempo e dinheiro se poupa se mil idosos deixarem de fazer uma viagem desnecessária.

### Outros recortes possíveis
- **Papelada do pequeno produtor** — crédito rural, cadastros e seguro, com checklist de documentos e aviso de prazos.
- **Energia no campo** — comparação solar × rede × diesel para bombear água ou irrigar, com calculadora própria.
- **Contas de água e energia** — entender a conta, tarifa social, vazamentos, como reclamar e economizar.
- **Outros públicos** — imigrantes e refugiados, MEI, pessoas com deficiência, jovens em primeiro emprego.

### Agro com IA (módulo secundário)
Monitoramento da saúde do solo e irrigação existem em abundância no mercado. Neste projeto entram apenas como **apoio** (clima e energia), mantendo o foco nas **pessoas**, que é o espírito do desafio.

---

## 🔗 Fontes

Orientações da base do protótipo, conferidas em páginas oficiais em **11/11/2026** (a data fica no campo `verificado_em` de cada registro):

| Assunto | Fonte |
|---|---|
| Prova de vida do INSS e alerta de golpe | https://www.gov.br/inss/pt-br/noticias/prova-de-vida-nao-foi-suspensa-e-obrigatoria-e-por-cruzamento-de-dados |
| Aposentadoria por idade rural | https://www.gov.br/pt-br/servicos/solicitar-aposentadoria-por-idade-para-trabalhador-rural |
| BPC/LOAS (idoso) e Meu INSS / telefone 135 | https://www.gov.br/pt-br/servicos/solicitar-beneficio-assistencial-ao-idoso |
| Cartão SUS e CPF | https://agenciagov.ebc.com.br/noticias/202509/ministerio-da-saude-comeca-a-emitir-cartao-sus-com-base-no-cpf |
| Vacina contra a gripe (60 anos ou mais) | https://www.gov.br/saude/pt-br/campanhas-da-saude/2025/gripe |
| Farmácia Popular e fraldas geriátricas | https://agenciagov.ebc.com.br/noticias/202503/saiba-como-retirar-medicamentos-e-insumos-pelo-farmacia-popular |
| Cadastro Único (CadÚnico) | https://www.gov.br/pt-br/servicos/inscrever-se-no-cadastro-unico-para-programas-sociais-do-governo-federal |
| CAF (Cadastro Nacional da Agricultura Familiar) | https://www.gov.br/mda/pt-br/acesso-a-informacao/acoes-e-programas/programas-projetos-acoes-obras-e-atividades/cadastro-nacional-da-agricultura-familiar/como-obter-o-caf |
| Alertas da Defesa Civil por SMS (40199) | https://www.parana.pr.gov.br/servicos/Seguranca/Defesa-Civil/Receber-alertas-da-Defesa-Civil-por-SMS-ERrZ4PN6 |

Outras fontes:

- Dados climáticos: **Open-Meteo** (https://open-meteo.com), usados na atividade de Modelagem Linear.
- Números sobre envelhecimento rural: **IBGE (Censo Demográfico e Censo Agropecuário)** e **Embrapa** — **[A CONFIRMAR e citar diretamente]**.
 
## 📄 Aviso
 
Projeto acadêmico da FIAP. O Bridge AI **não é um canal oficial** de nenhum órgão público e não substitui o atendimento oficial. Sempre confirme as informações nas fontes indicadas.
