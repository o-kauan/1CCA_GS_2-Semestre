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
 
> *"Não comece pela ideia, comece pela vida real."*
 
A população rural brasileira **está envelhecendo**: a proporção de moradores e produtores com mais de 55 e 65 anos cresce a cada levantamento, enquanto os jovens migram para as cidades em busca de estudo, trabalho e conectividade. Muitos idosos permanecem no campo, em parte pela estabilidade da aposentadoria rural.
 
Consequências no dia a dia de quem fica:
 
- resolver burocracia, benefício ou saúde exige **ir à cidade**, às vezes com horas de deslocamento;
- **internet fraca ou ausente** e pouca familiaridade com telas;
- falta de clareza sobre **quais documentos levar** e se a ida é realmente necessária;
- maior exposição a **golpes** envolvendo benefícios e empréstimos;
- o jovem que migrou fica distante e sem forma simples de ajudar.
> ⚠️ **A confirmar:** números exatos (percentual de idosos no campo, índice de envelhecimento rural) devem vir do **Censo Demográfico/Censo Agropecuário do IBGE** e de publicações da **Embrapa**, citados diretamente. Não afirmar que idosos são a "maioria" do campo sem a fonte primária.
 
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
### Diferencial técnico: funcionar sem internet
 
O verdadeiro problema do campo é o sinal.
 
- Base de conhecimento **local** (ChromaDB roda na própria máquina), com respostas offline e sincronização quando houver conexão.
- Possível implantação como **quiosque** em associação de moradores, posto de saúde ou escola rural.
- **Modo baixa conexão:** respostas curtas, sem imagens pesadas, versão em texto simples e **cartão impresso** com as perguntas mais comuns.
### Módulo clima e risco para quem vive da terra
 
- Alertas de geada, seca e chuva forte com dados abertos (Open-Meteo, em Python).
- O assistente traduz o dado em orientação prática: *"amanhã há risco de geada, proteja a plantação X"*.
- Usa regressão (ML) e conecta com o tema de energia.
### Acessibilidade
 
- Linguagem simples, letra grande, opção de **voz** (áudio de entrada e saída) como recurso de acessibilidade, não como ideia principal.
- Canal futuro de implantação: WhatsApp. O protótipo da entrega é em **Gradio**.
### Modo família
 
Um parente na cidade recebe o **resumo do que foi orientado** e pode ajudar. O idoso não entrega dados pessoais ao assistente.

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
O usuário pergunta por texto ou áudio. O sistema busca em uma base de documentos verificada, responde com fonte e data e, se não tiver certeza, diz "não sei" e orienta onde procurar. Funciona offline com base local e sincroniza quando há conexão.
 
**Quais tecnologias serão usadas?**
Python, RAG (ChromaDB + LangChain), embeddings, reconhecimento e síntese de voz, Gradio, C (estruturas de dados), álgebra booleana, regressão (ML), dados abertos de clima e guardrails (LGPD, escopo, prompt injection).
 
**Qual problema será resolvido?**
A dificuldade de acessar informação confiável e de resolver pendências sem deslocamentos desnecessários até a cidade, além da exposição a golpes.
 
**Quais resultados pode gerar?**
Menos viagens à toa, menos tempo perdido, menos exposição a golpes e mais autonomia para o idoso, medidos pelos indicadores abaixo.
 
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
 
Registros dos testes ficam em `docs/testes-usuarios/`.
 
---
 
## 🔒 Segurança, ética e limites
 
- **Não é canal oficial.** Todas as respostas trazem aviso e indicam o órgão responsável.
- **Sem dados pessoais desnecessários.** O assistente não pede CPF, endereço ou dados bancários.
- **Toda resposta com fonte e data.** Informação sem fonte verificável não entra na base.
- **Armadilha de contradição/desatualização** documentada na base (exigência da disciplina de IA), com tratamento explícito.
- **Guardrails:** escopo (só responde dentro do tema), prompt injection na fonte e LGPD.
- **Entradas inválidas** tratadas em todos os módulos.
---
 
## 🧠 Banco de ideias
 
Ideias que surgiram no brainstorm. Algumas viram módulos, outras ficam como possibilidade.
 
### Ideias para se destacar
- **"Resolvo sem ir à cidade"** — o que dá para resolver por telefone/canal digital e o que exige presença, com a viagem organizada.
- **Detector de golpe** — o idoso cola uma mensagem suspeita (ex.: "seu benefício foi bloqueado") e recebe uma avaliação de risco com explicação.
- **Modo família** — resumo das orientações enviado a um parente.
- **Saúde e benefícios** — posto de saúde, vacinação, medicamentos de uso contínuo, aposentadoria rural, sempre com fonte.
- **Modo baixa conexão** — texto simples, SMS ou cartão impresso.
### Outros recortes possíveis
- **Papelada do pequeno produtor** — crédito rural, cadastros e seguro, com checklist de documentos e aviso de prazos.
- **Energia no campo** — comparação solar × rede × diesel para bombear água ou irrigar, com calculadora própria.
- **Contas de água e energia** — entender a conta, tarifa social, vazamentos, como reclamar e economizar.
- **Outros públicos** — imigrantes e refugiados, MEI, pessoas com deficiência, jovens em primeiro emprego.
### Agro com IA (módulo secundário)
Monitoramento da saúde do solo e irrigação existem em abundância no mercado. Neste projeto entram apenas como **apoio** (clima e energia), mantendo o foco nas **pessoas**, que é o espírito do desafio.

---
 
## 🔗 Fontes
 
---
 
## 📄 Aviso
 
Projeto acadêmico da FIAP. O Bridge AI **não é um canal oficial** de nenhum órgão público e não substitui o atendimento oficial. Sempre confirme as informações nas fontes indicadas.
