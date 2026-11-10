# Bridge AI — Análise dos Algoritmos (Big-O)

Global Solution 2026.2 · FIAP · Data Structures and Algorithms (DSA) · Turma 1CC-FEV

## Equipe

| Integrante | RM |
|---|---|
| Thiago Soalheiro Diamantino | 569316 |
| Kauan Damasceno de Lima | 573727 |

---

## Sumário

1. [Convenções e notação](#1-convenções-e-notação)
2. [Resumo geral das complexidades](#2-resumo-geral-das-complexidades)
3. [Inserção](#3-inserção)
4. [Busca e pesquisa](#4-busca-e-pesquisa)
5. [Remoção](#5-remoção)
6. [Atualização](#6-atualização)
7. [Ordenação: Insertion Sort em lista encadeada](#7-ordenação-insertion-sort-em-lista-encadeada)
8. [Indicadores](#8-indicadores)
9. [Listagem, liberação e funções auxiliares](#9-listagem-liberação-e-funções-auxiliares)
10. [Complexidade de espaço](#10-complexidade-de-espaço)
11. [Por que Insertion Sort?](#11-por-que-insertion-sort)
12. [Conclusão](#12-conclusão)

---

## 1. Convenções e notação

### 1.1 Variáveis de análise

| Símbolo | Significado |
|---|---|
| `n` | Quantidade de nós (documentos) na lista encadeada. |
| `L` | Tamanho máximo das strings: 99 caracteres úteis para o titular (`char[100]`) e 49 para o número (`char[50]`). |
| `T` | Tamanho do termo digitado em uma pesquisa por nome (no máximo 99). |

### 1.2 Tratamento das constantes

As operações sobre strings (`strcmp`, `strcpy`, `strstr`, `para_minusculo`, `conferir_nome_valido`) dependem de `L`. Como os vetores têm **tamanho fixo e pequeno** (100 e 50 bytes), `L` e `T` são limitados por constantes. Por isso, a análise trata cada operação sobre uma string como **O(1) em relação a `n`**, que é o parâmetro que cresce com a base de dados.

Para ser transparente, as tabelas indicam também a forma completa, com `L` visível, quando ela muda a leitura (por exemplo, `O(n · L)`). O custo constante de `L` pesa na prática, principalmente na ordenação, em que cada comparação de titulares converte duas strings para minúsculo.

### 1.3 Notações usadas

| Notação | Significado |
|---|---|
| `O(f(n))` | Limite superior: o custo nunca cresce mais rápido que `f(n)` (usado para o **pior caso**). |
| `Ω(f(n))` | Limite inferior: o custo nunca cresce mais devagar que `f(n)` (usado para o **melhor caso**). |
| `Θ(f(n))` | Limite justo: o custo cresce exatamente como `f(n)`, em todos os casos. |

### 1.4 Por que a estrutura determina o custo

A lista encadeada guarda apenas o ponteiro `cabeca`. **Não há acesso por índice** e **não há ponteiro para o último nó**. Qualquer operação que precise de um nó específico, inclusive o último, tem de percorrer a lista a partir da cabeça. Essa característica explica a maior parte das complexidades lineares abaixo.

---

## 2. Resumo geral das complexidades

Tempo de cada operação do menu, na implementação efetiva:

| Operação | Função principal | Melhor caso | Caso médio | Pior caso | Espaço extra |
|---|---|---|---|---|---|
| Inserção (cadastro) | `cadastrar_documento` → `inserir_fim` | `Ω(1)` (lista vazia) | `Θ(n)` | `O(n)` | `O(1)` |
| Busca por ID | `buscar_por_id` | `Ω(1)` (1º nó) | `Θ(n)` | `O(n)` | `O(1)` |
| Pesquisa por titular | `pesquisar_por_titular` | `Θ(n)` | `Θ(n)` | `O(n)` | `O(1)` |
| Pesquisa por tipo | `pesquisar_por_tipo` | `Θ(n)` | `Θ(n)` | `O(n)` | `O(1)` |
| Remoção | `remover_por_id` | `Ω(1)` (nó é a cabeça) | `Θ(n)` | `O(n)` | `O(1)` |
| Atualização | `atualizar_*` | `Ω(n)` | `Θ(n)` | `O(n)` | `O(1)` |
| **Ordenação** | `ordenar_lista` | `Ω(n)` | `Θ(n²)` | `O(n²)` | `O(1)` |
| Listagem | `listar_todos` | `Θ(n)` | `Θ(n)` | `Θ(n)` | `O(1)` |
| Indicadores | `exibir_indicadores` | `Ω(n)` | `O(n²)` | `O(n²)` | `O(1)` |
| Liberação total | `liberar_lista` | `Θ(n)` | `Θ(n)` | `Θ(n)` | `O(1)` |

Espaço total da estrutura: `Θ(n)`, com um nó por documento.

---

## 3. Inserção

### 3.1 Como funciona

O cadastro (`cadastrar_documento`) executa, em ordem:

1. leitura e validação do titular, do tipo e do número;
2. `existe_duplicado`, que percorre a lista;
3. `criarNo`, que aloca um nó com `malloc` e copia os dados;
4. `inserir_fim`, que liga o nó ao final da lista.

### 3.2 Análise de cada parte

| Parte | Custo | Justificativa |
|---|---|---|
| Leitura e validação de entrada (`ler_string`, `conferir_*`) | `O(L)` por tentativa, `O(1)` em relação a `n` | Percorrem no máximo 100 ou 50 caracteres. Não dependem da lista. |
| `existe_duplicado` | `O(n)` | Percorre a lista inteira no pior caso (nenhum duplicado). Em cada nó faz um `strcmp` de custo limitado. |
| `criarNo` | `O(1)` | Um `malloc`, um incremento de `proximoId` e cópias de tamanho fixo. |
| `inserir_fim` | melhor `O(1)`, pior `O(n)` | Se a lista está vazia, só atribui `*cabeca = novo`. Caso contrário, percorre todos os `n` nós até achar o último (`atual->proximo != NULL`). |

### 3.3 Complexidade da inserção

```
T(inserir_fim)         = O(n)       // percurso até o último nó
T(existe_duplicado)    = O(n)       // percurso completo no pior caso
T(cadastrar_documento) = O(n) + O(n) + O(1) = O(n)
```

- **Melhor caso `Ω(1)`** para `inserir_fim` isolada: lista vazia.
- **Caso médio e pior caso `O(n)`** para o cadastro completo: tanto a verificação de duplicidade quanto a inserção no fim percorrem a lista.

**Justificativa.** A inserção no fim é `O(n)` porque a estrutura guarda só a cabeça. A **inserção no início** seria `O(1)`, mas a lista precisa manter a ordem de cadastro, e a verificação de duplicidade é `O(n)` de qualquer forma. Assim, mesmo uma inserção `O(1)` não baixaria o custo do cadastro como um todo.

---

## 4. Busca e pesquisa

Todas as buscas usam **busca linear** (sequencial): percorrem a lista da cabeça até `NULL`, comparando o campo de cada nó com o valor procurado. A busca binária **não é aplicável**: ela exige acesso direto ao elemento do meio, e a lista encadeada só permite acesso sequencial.

### 4.1 Busca por ID: `buscar_por_id` e `pesquisar_por_id`

```c
while (atual != NULL) {
    if (atual->id == id) return atual;   // para no primeiro resultado
    atual = atual->proximo;
}
return NULL;
```

| Caso | Situação | Comparações | Complexidade |
|---|---|---|---|
| Melhor | O ID está no primeiro nó | 1 | `Ω(1)` |
| Médio | O ID está em posição qualquer (equiprobável) | `(n + 1) / 2` | `Θ(n)` |
| Pior | O ID está no último nó **ou não existe** | `n` | `O(n)` |

**Justificativa.** Como o ID é único, a busca pode parar no primeiro encontro (`return`). Se o ID não existe ("consulta sem resultado"), a lista é percorrida inteira: este é o pior caso. Cada comparação (`atual->id == id`) é `O(1)`.

**Observação.** Como os IDs são gerados em ordem crescente e a lista (sem reordenação) os mantém em ordem, seria possível interromper a busca ao passar de um ID maior que o procurado. A implementação atual não faz essa otimização, e ela deixaria de valer depois de uma ordenação por tipo ou titular.

### 4.2 Pesquisa por tipo: `pesquisar_por_tipo`

A função percorre **todos** os nós e exibe todos os que têm `atual->tipo == tipo`. Como pode haver vários resultados, não existe parada antecipada.

- Comparações: sempre `n` (comparação de inteiros, `O(1)`).
- Complexidade: **`Θ(n)`** em todos os casos (melhor, médio e pior).

### 4.3 Pesquisa por titular: `pesquisar_por_titular`

Para cada nó, a função:

1. converte o titular do nó para minúsculo com `para_minusculo` (`O(L)`);
2. procura o termo dentro do titular com `strstr` (`O(L · T)` no pior caso de uma implementação ingênua; as bibliotecas modernas fazem em tempo linear);
3. imprime o registro se houver correspondência (`O(1)`).

O termo digitado é validado e convertido para minúsculo uma única vez, antes do laço: `O(T)`.

```
T(n) = O(T) + n · ( O(L) + O(L·T) )      →   O(n · L · T)
```

Com `L` e `T` limitados a 100, o fator `L · T` é uma constante e a complexidade em função de `n` é **`Θ(n)`**.

**Justificativa.** A pesquisa é parcial (substring) e pode retornar vários registros, então **sempre percorre a lista inteira**. Não existe melhor caso melhor que o pior: o custo é linear em todos os casos. Esta é também a pesquisa de maior custo constante por nó, por causa da conversão de caixa e da busca de substring.

### 4.4 Resumo das buscas

| Busca | Melhor | Médio | Pior | Para antes do fim? |
|---|---|---|---|---|
| Por ID | `Ω(1)` | `Θ(n)` | `O(n)` | Sim (ID único) |
| Por tipo | `Θ(n)` | `Θ(n)` | `O(n)` | Não (vários resultados) |
| Por titular | `Θ(n)` | `Θ(n)` | `O(n)` | Não (vários resultados) |

Consultas sem resultado (registro inexistente) caem no **pior caso**: percorrem a lista completa e terminam com a mensagem "Nenhum documento encontrado...".

---

## 5. Remoção

### 5.1 Como funciona

`remover_por_id(&cabeca, id)` mantém dois ponteiros durante o percurso: `atual` (o nó procurado) e `anterior` (o nó imediatamente antes). Ao encontrar o nó, religa a lista e libera a memória.

```c
while (atual != NULL && atual->id != id) {
    anterior = atual;
    atual = atual->proximo;
}
if (atual == NULL) return 0;                  // ID inexistente
if (anterior == NULL) *cabeca = atual->proximo;   // remove a cabeça
else anterior->proximo = atual->proximo;          // remove meio/fim
free(atual);
```

### 5.2 Análise

| Parte | Custo |
|---|---|
| Percurso até o nó procurado | melhor `O(1)` (é a cabeça), pior `O(n)` (último nó ou inexistente) |
| Religamento de ponteiros | `O(1)` (uma atribuição) |
| `free(atual)` | `O(1)` |

| Caso | Situação | Complexidade |
|---|---|---|
| Melhor | O nó é a cabeça | `Ω(1)` |
| Médio | O nó está em posição qualquer | `Θ(n)` |
| Pior | O nó é o último ou não existe | `O(n)` |

**Justificativa.** A remoção em si é `O(1)` **depois de localizado o nó**, porque basta alterar um ponteiro (não há deslocamento de elementos, ao contrário de um vetor, onde remover exige mover até `n - 1` posições). O custo `O(n)` vem inteiramente da **localização** do nó, que exige percurso sequencial.

### 5.3 Custo da operação de menu "Excluir"

`excluir_documento` executa antes `pesquisar_documentos` (para o usuário descobrir o ID, `O(n)`), depois `buscar_por_id` (`O(n)`) e por fim `remover_por_id` (`O(n)`):

```
T(excluir) = O(n) + O(n) + O(n) = O(n)
```

A soma de três percursos lineares continua linear. A confirmação S/N é leitura de entrada, `O(1)`.

---

## 6. Atualização

### 6.1 Como funciona

`atualizar_documento` localiza o registro (pesquisa + `buscar_por_id`) e abre um submenu em laço. Cada alteração (`atualizar_titular`, `atualizar_tipo`, `atualizar_numero`) valida a entrada, verifica duplicidade e grava o novo valor **diretamente no nó existente**.

### 6.2 Análise

| Parte | Custo | Justificativa |
|---|---|---|
| `pesquisar_documentos` (localização) | `O(n)` | Busca linear (seção 4). |
| `buscar_por_id` | `O(n)` | Busca linear por ID. |
| `existe_duplicado` (uma por alteração) | `O(n)` | Percorre a lista. |
| Gravação (`strcpy`, atribuição de `tipo`, recálculo de `categoria`) | `O(1)` | Cópia de tamanho fixo e consulta a vetor (`CATEGORIA_DO_TIPO[tipo]`). |

Se o usuário fizer `k` alterações na mesma sessão, o custo é `O(n) + k · O(n) = O(k · n)`. Como `k` é pequeno e limitado pelas três opções do submenu na prática, a atualização completa é **`O(n)`**.

**Integridade da lista.** A atualização **não altera `id` nem `proximo`**: nenhuma ligação é desfeita e nenhum nó é recriado. Por isso a operação de gravação é `O(1)` e a estrutura permanece consistente.

---

## 7. Ordenação: Insertion Sort em lista encadeada

O sistema usa o **Insertion Sort** implementado manualmente, sem funções prontas (`qsort` ou similares), aplicado **diretamente sobre os nós**, por religamento de ponteiros.

### 7.1 Ideia do algoritmo

O Insertion Sort funciona como ordenar cartas de baralho na mão. A cada passo, pega-se **uma carta nova** e a encaixa na **posição certa** entre as cartas que já estão ordenadas.

O algoritmo mantém duas regiões:

- **região ordenada**: nós que já estão em ordem entre si (começa **vazia**);
- **região não processada**: nós que ainda serão examinados (começa com **toda a lista**).

**Invariante do laço:** depois de processar `k` nós, a região ordenada contém exatamente esses `k` nós, em ordem. Quando `k = n`, a lista está ordenada.

### 7.2 Código

```c
void ordenar_lista(Documento **cabeca, int criterio) {
    Documento *ordenada = NULL;
    Documento *atual = *cabeca;

    while (atual != NULL) {
        Documento *proximo = atual->proximo;

        if (ordenada == NULL || comparar(atual, ordenada, criterio) < 0) {
            atual->proximo = ordenada;
            ordenada = atual;
        } else {
            Documento *posicao = ordenada;
            while (posicao->proximo != NULL &&
                   comparar(posicao->proximo, atual, criterio) <= 0) {
                posicao = posicao->proximo;
            }
            atual->proximo = posicao->proximo;
            posicao->proximo = atual;
        }

        atual = proximo;
    }

    *cabeca = ordenada;
}
```

### 7.3 Passo a passo do funcionamento

Em cada iteração do laço externo (`while (atual != NULL)`):

1. **Guardar o resto da lista:** `proximo = atual->proximo`. Isso é necessário porque `atual->proximo` será sobrescrito ao inserir o nó na região ordenada. Sem esse passo, o restante da lista seria perdido.
2. **Escolher entre dois casos de inserção:**
   - **Inserção no início:** se a região ordenada está vazia ou `atual` deve vir antes da cabeça (`comparar < 0`), o nó vira a nova cabeça: `atual->proximo = ordenada; ordenada = atual;`.
   - **Inserção no meio ou no fim:** `posicao` percorre a região ordenada, avançando enquanto o nó seguinte for **menor ou igual** a `atual`. Quando para, `atual` entra logo depois de `posicao`: `atual->proximo = posicao->proximo; posicao->proximo = atual;`.
3. **Avançar:** `atual = proximo`.

Ao final, `*cabeca = ordenada` atualiza a cabeça da lista em `main` (por isso o parâmetro é `Documento **`).

> **Ordem das atribuições.** Na inserção, `atual->proximo = posicao->proximo` deve vir **antes** de `posicao->proximo = atual`. Invertendo a ordem, `atual` apontaria para si mesmo e o restante da região ordenada seria perdido.

### 7.4 Exemplo detalhado (critério: titular)

Lista original: `Carlos -> Ana -> Dani -> Bia`. A tabela mostra a região ordenada e o número de comparações a cada passo.

| Passo | `atual` | O que acontece | Região ordenada depois | Comparações |
|---|---|---|---|---|
| 1 | Carlos | Região vazia: Carlos vira a cabeça. | `Carlos` | 0 (testa `ordenada == NULL`) |
| 2 | Ana | `Ana < Carlos`: vira a nova cabeça. | `Ana -> Carlos` | 1 |
| 3 | Dani | `Dani > Ana`, então não é a cabeça. `posicao = Ana`; `Carlos <= Dani` avança; `posicao->proximo == NULL` para. Dani entra no fim. | `Ana -> Carlos -> Dani` | 2 |
| 4 | Bia | `Bia > Ana`. `posicao = Ana`; `comparar(Carlos, Bia) > 0` para. Bia entra depois de Ana. | `Ana -> Bia -> Carlos -> Dani` | 2 |

Resultado: `Ana -> Bia -> Carlos -> Dani`, com `*cabeca` apontando para Ana.

### 7.5 A função `comparar` e seu custo

O algoritmo é independente do critério: toda decisão passa por `comparar(a, b, criterio)`, que segue a convenção de `strcmp` (negativo: `a` antes de `b`; zero: equivalentes; positivo: `a` depois de `b`).

| Critério | Custo de uma comparação | Justificativa |
|---|---|---|
| 1 — Tipo (desempate por titular) | `O(1)` na maioria das vezes; `O(L)` no desempate | Compara dois inteiros. Só em caso de tipos iguais chama `comparar_titulares`. |
| 2 — Titular (desempate por tipo) | `O(L)` | `comparar_titulares` converte as duas strings para minúsculo (`para_minusculo`, duas vezes) e aplica `strcmp`. |
| 3 — ID | `O(1)` | Subtração de dois inteiros. |

Denominando `C` o custo de uma comparação (`O(1)` ou `O(L)`, com `L` ≤ 99), o tempo total da ordenação é **número de comparações × `C`**. Como `C` é limitada por constante, a análise assintótica em `n` depende apenas do número de comparações.

### 7.6 Análise de complexidade de tempo

#### 7.6.1 Custo de inserir o k-ésimo nó

Ao processar o `k`-ésimo nó, a região ordenada já tem `k - 1` nós. A inserção faz:

- 1 comparação com a cabeça (primeiro `if`);
- se não entrar no início, várias comparações no laço de `posicao`, até encontrar o ponto de inserção.

O número de comparações varia de **1** (entra no início da região ordenada) até **`k - 1`** (entra no fim). Isso é decisivo para entender os casos abaixo.

> **Detalhe importante.** Normalmente o Insertion Sort atua sobre um vetor, a busca pelo ponto de inserção parte do **fim** da região ordenada e recua, então um vetor já ordenado custa `O(n)`. No nosso caso aplicando à lista simplesmente encadeada **não é possível recuar**, e esta implementação percorre a região ordenada **a partir da cabeça**. Por isso o comportamento dos casos extremos é o **inverso** do que seria em um modelo padrão aplicado a um vetor, como mostram os casos abaixo.

#### 7.6.2 Melhor caso: `Ω(n)`

Ocorre quando **cada novo nó é menor que a cabeça atual da região ordenada**, ou seja, a lista de entrada está em **ordem estritamente decrescente** em relação ao critério. Todo nó entra no início após **uma única comparação**:

```
Comparações = 0 (1º nó) + 1 + 1 + ... + 1 = n - 1
T(n) = Θ(n)  →  melhor caso Ω(n)
```

Exemplo (critério titular): `Dani -> Carlos -> Bia -> Ana`.

#### 7.6.3 Pior caso: `O(n²)`

Ocorre quando **cada novo nó é maior que todos os já ordenados**, ou seja, a lista de entrada já está em **ordem crescente** (ou com todos os critérios iguais). Todo nó percorre a região ordenada inteira até o fim:

```
Para o k-ésimo nó (k = 2, ..., n):  comparações = 1 + (k - 2) = k - 1

T(n) = Σ (k - 1) para k = 2..n
     = 1 + 2 + ... + (n - 1)
     = n(n - 1) / 2
     = (n² - n) / 2
     = O(n²)
```

O termo dominante é `n² / 2`, e as constantes são descartadas na notação Big-O.

**Consequência prática.** Como os IDs são gerados em ordem crescente e a lista nasce na ordem de cadastro, **ordenar por ID (critério 3) uma lista na ordem original é o pior caso**. Ordenar de novo uma lista que já está ordenada pelo mesmo critério também é o pior caso. Esse comportamento é uma característica da implementação com percurso a partir da cabeça, e não um erro de lógica: o resultado sai correto, apenas com custo quadrático.

#### 7.6.4 Caso médio: `Θ(n²)`

Com os registros em ordem aleatória, o `k`-ésimo nó entra em uma posição equiprobável entre as `k` posições possíveis da região ordenada. Em média, `posicao` percorre **metade** da região:

```
Comparações esperadas para o k-ésimo nó ≈ k / 2

T(n) ≈ Σ (k / 2) para k = 1..n ≈ n² / 4  →  Θ(n²)
```

O caso médio é cerca de **metade** do pior caso em número de comparações, mas continua **quadrático**: dobrar `n` quadruplica o tempo.

Uma forma equivalente de enxergar o custo: o número de comparações é aproximadamente `n + P`, em que `P` é o número de pares de elementos que **já estão na ordem correta** na entrada. Quanto mais a lista já estiver em ordem crescente, maior `P` e maior o custo. No pior caso, `P = n(n-1)/2`.

#### 7.6.5 Resumo dos casos de tempo

| Caso | Entrada | Comparações | Complexidade |
|---|---|---|---|
| Melhor | Ordem decrescente (cada nó entra na cabeça) | `n - 1` | `Ω(n)` |
| Médio | Ordem aleatória | `≈ n² / 4` | `Θ(n²)` |
| Pior | Ordem crescente (cada nó entra no fim) | `n(n - 1) / 2` | `O(n²)` |

Ilustração do crescimento do pior caso:

| `n` | Comparações no pior caso `n(n-1)/2` | Comparações no melhor caso `n-1` |
|---|---|---|
| 10 | 45 | 9 |
| 100 | 4.950 | 99 |
| 1.000 | 499.500 | 999 |
| 10.000 | 49.995.000 | 9.999 |

#### 7.6.6 Custo dos ajustes de ponteiros

Cada inserção faz um número **constante** de atribuições de ponteiros (duas), e `proximo`/`atual` avançam uma vez por iteração. Esses custos somam `O(n)` e são dominados pelas comparações e pelos avanços de `posicao`. **Nenhum dado é copiado, nenhum nó é alocado e nenhum é liberado**: apenas ponteiros mudam.

### 7.7 Complexidade de espaço: `O(1)`

O algoritmo usa apenas quatro ponteiros auxiliares (`ordenada`, `atual`, `proximo`, `posicao`), independentemente de `n`. Como os nós são **religados**, e não copiados, a ordenação é **in-place** em relação aos dados: espaço extra `O(1)`.

Em um vetor, o Insertion Sort precisa deslocar elementos (`O(n)` movimentos por inserção). Na lista encadeada, a inserção na posição correta custa **dois ponteiros**, sem deslocamento. É uma vantagem real da estrutura, embora o **custo de encontrar a posição** continue linear.

### 7.8 Estabilidade

O algoritmo é **estável**: registros com chave equivalente mantêm a ordem relativa que tinham antes da ordenação.

Isso decorre de duas escolhas na implementação:

- o laço avança enquanto `comparar(posicao->proximo, atual) <= 0`; o `<=` faz o nó novo entrar **depois** dos equivalentes que já estão na região ordenada;
- o teste de inserção na cabeça usa `< 0` (estrito), então um nó equivalente à cabeça **não** passa à frente dela.

Como os nós são processados na ordem original, equivalentes ficam na ordem de chegada.

### 7.9 Correção do algoritmo

- **Invariante:** após cada iteração do laço externo, `ordenada` aponta para uma lista bem formada (terminada em `NULL`) e em ordem não decrescente por `comparar`, contendo todos os nós processados.
- **Inicialização:** `ordenada = NULL` é uma lista vazia, trivialmente ordenada.
- **Manutenção:** a inserção coloca `atual` exatamente antes do primeiro nó estritamente maior, preservando a ordem; os dois ramos mantêm a lista terminada em `NULL`.
- **Término:** a cada iteração `atual` avança um nó da lista original (guardado em `proximo`); após `n` iterações, `atual == NULL` e `ordenada` contém todos os `n` nós.

### 7.10 Casos limite

| Situação | Comportamento |
|---|---|
| Lista vazia | `ordenar_documentos` verifica `*cabeca == NULL` antes e exibe "Nenhum documento cadastrado." Não chama `ordenar_lista`. |
| Lista com 1 nó | Um único passo: o nó vira a cabeça. Nenhuma comparação. Custo `O(1)`. |
| Todos os registros equivalentes | Equivale ao pior caso (cada nó entra no fim), `O(n²)`, e a ordem original é preservada. |
| Critério "Voltar" (0) | `ordenar_documentos` retorna antes de ordenar. |

### 7.11 Custo da operação de menu "Ordenar"

```
T(ordenar_documentos) = T(ordenar_lista) + T(listar_todos)
                      = O(n²) + Θ(n)
                      = O(n²)
```

A listagem final é linear e dominada pelo custo quadrático da ordenação.

---

## 8. Indicadores

`exibir_indicadores` calcula quatro resultados: total, quantidade por tipo, quantidade por categoria e quantidade por titular.

### 8.1 Total, por tipo e por categoria: `Θ(n)`

Em um **único percurso**, a função incrementa `total`, `por_tipo[atual->tipo]` e `por_categoria[atual->categoria]`. Cada incremento é `O(1)`, porque o tipo e a categoria funcionam como **índices** dos vetores de contadores (acesso direto). Depois, dois laços fixos de 11 e 7 posições exibem os contadores: `O(1)`, pois o tamanho não depende de `n`.

```
T = n · O(1) + O(11) + O(7) = Θ(n)
```

Armazenar o **índice** do tipo e da categoria (em vez do texto) é o que permite contar por acesso direto, sem comparar strings.

### 8.2 Quantidade por titular: `O(n²)`

Como o titular é texto livre, não existe vetor de contadores indexado por nome. A função usa dois percursos aninhados:

1. para cada nó `atual`, um laço interno percorre os nós **anteriores** (`anterior` de `cabeca` até `atual`) comparando titulares com `strcmp`, para saber se o nome **já foi contado**;
2. se for a **primeira ocorrência**, outro laço percorre a lista de `atual` até o fim, contando os nós com o mesmo titular.

Análise por nó na posição `i` (de 0 a `n - 1`):

- verificação dos anteriores: até `i` comparações;
- contagem (só para primeira ocorrência): `n - i` comparações.

| Caso | Situação | Custo |
|---|---|---|
| Pior | Todos os titulares são **diferentes**: cada nó faz `i` + `(n - i)` = `n` comparações | `n · n = n²` → `O(n²)` |
| Melhor | Todos os registros são do **mesmo** titular: o 1º nó conta `n`; os demais param na 1ª comparação do laço interno (`ja_contado = 1` com `break`) | `n + (n - 1) = Θ(n)` → `Ω(n)` |

O custo total da função é `Θ(n) + O(n²) = O(n²)`.

**Justificativa.** O trecho quadrático decorre de não haver uma estrutura de busca rápida por nome (como uma tabela hash). Para a escala do projeto (cadastro local de poucos registros) o custo é aceitável, e a abordagem evita estruturas extras, mantendo-se dentro da lista encadeada exigida.

---

## 9. Listagem, liberação e funções auxiliares

| Função | Complexidade | Justificativa |
|---|---|---|
| `listar_todos` | `Θ(n)` | Percorre todos os nós uma vez e chama `imprimir_lista` (`O(1)` por nó). |
| `imprimir_lista` | `O(1)` | Um `printf` com campos de tamanho limitado. |
| `liberar_lista` | `Θ(n)` | Um `free` por nó, guardando o próximo antes de liberar. Sem isso, o ponteiro de continuação se perderia. |
| `criarNo` | `O(1)` | Um `malloc` e cópias de tamanho fixo. |
| `existe_duplicado` | `O(n)` | Percurso da lista com `strcmp` e comparação de inteiros por nó. |
| `mostrar_duplicado` | `O(1)` | Apenas impressão. |
| `ler_string` | `O(L)` | `fgets` + `strlen` sobre no máximo 100 caracteres. |
| `ler_inteiro` | `O(1)` | Linha de no máximo 50 caracteres e um `sscanf`. |
| `conferir_nome_valido` | `O(L)` | Percorre os caracteres da string uma vez. |
| `conferir_numero_valido` | `O(L)` | Percorre os caracteres da string uma vez. |
| `para_minusculo` | `O(L)` | Percorre a string uma vez, copiando e convertendo. |
| `comparar_titulares` | `O(L)` | Duas chamadas a `para_minusculo` + um `strcmp`. |
| `comparar` | `O(1)` ou `O(L)` | Depende do critério (seção 7.5). |

---

## 10. Complexidade de espaço

### 10.1 Espaço da estrutura

Cada nó (`Documento`) ocupa um tamanho fixo:

| Campo | Bytes |
|---|---|
| `id` | 4 |
| `titular[100]` | 100 |
| `tipo` | 4 |
| `categoria` | 4 |
| `numero[50]` | 50 |
| `proximo` (ponteiro, 64 bits) | 8 |
| Preenchimento (alinhamento) | ≈ 6 |
| **Total aproximado** | **≈ 176** |

O tamanho exato depende do compilador e da plataforma, mas o valor é **constante por nó**. Para `n` documentos: **`Θ(n)`** (≈ 176 · `n` bytes), sem desperdício de posições vazias, pois a lista aloca apenas o necessário.

### 10.2 Espaço auxiliar por operação

| Operação | Espaço extra | Justificativa |
|---|---|---|
| Inserção | `O(1)` | Um nó novo (já contado na estrutura) e um ponteiro de percurso. |
| Busca e pesquisa | `O(1)` | Ponteiro de percurso e buffers de tamanho fixo. |
| Remoção | `O(1)` | Dois ponteiros (`atual`, `anterior`). |
| Ordenação | `O(1)` | Quatro ponteiros; os nós são religados, não copiados. |
| Indicadores | `O(1)` | Vetores de contadores de tamanho fixo (11 e 7) e ponteiros. |

Nenhuma operação usa recursão, então não há crescimento de pilha em função de `n`.

---

## 11. Por que Insertion Sort?
 
A tabela compara Selection Sort, Insertion Sort, Merge Sort e Quick Sort:
 
| Algoritmo | Melhor | Médio | Pior | Espaço extra | Estável | Observação em lista encadeada |
|---|---|---|---|---|---|---|
| Selection Sort | `Θ(n²)` | `Θ(n²)` | `Θ(n²)` | `O(1)` | Não (na forma clássica) | Sempre quadrático, mesmo com a lista já ordenada. |
| **Insertion Sort** | `Ω(n)` | `Θ(n²)` | `O(n²)` | `O(1)` | **Sim** | Inserção por religamento, sem deslocamento. |
| Merge Sort | `Θ(n log n)` | `Θ(n log n)` | `Θ(n log n)` | `O(log n)` (recursão) | Sim | Excelente para listas, mas exige dividir a lista e mesclar. |
| Quick Sort | `Θ(n log n)` | `Θ(n log n)` | `O(n²)` | `O(log n)` a `O(n)` | Não | Pior em listas: o acesso ao pivô e a partição são menos eficientes sem índice. |
 
**Justificativa da escolha do Insertion Sort:**
 
O Insertion Sort tem uma ideia simples: a cada passo, pegar um elemento e encaixá-lo na posição certa entre os que já estão ordenados, como se ordena um baralho na mão. Na implementação, isso se traduz em apenas dois laços (um que percorre a lista original e outro que procura a posição de inserção) e duas atribuições de ponteiros, em cerca de vinte linhas de código. O algoritmo não usa recursão, não precisa dividir a lista nem criar estruturas auxiliares e não aloca memória: usa só quatro ponteiros (`ordenada`, `atual`, `proximo` e `posicao`). 
Além disso, toda a lógica de comparação fica isolada na função `comparar`, então trocar o critério (tipo, titular ou ID) não exige mexer no algoritmo. Essa simplicidade facilita acompanhar o código passo a passo, testar com listas pequenas e demonstrar a ideia de funcionamento. Ele também é estável, o que é necessário para os critérios com desempate (tipo + titular) e para manter a ordem de cadastro entre registros equivalentes. 
Por fim, adapta-se bem à lista encadeada: a inserção por religamento de dois ponteiros elimina o ponto fraco do Insertion Sort em vetor (o deslocamento de elementos), sem alocar nem copiar nós.
 
---

## 12. Conclusão

O Bridge AI reúne um conjunto pequeno de algoritmos, todos escritos sobre uma única estrutura de dados: a **lista encadeada**. Cada um responde a uma necessidade do cadastro de documentos:
 
- **Inserção, percurso e remoção na lista encadeada:** sustentam o cadastro, a listagem e a exclusão. A alocação e a liberação dinâmica de memória são feitas sob controle da equipe (`malloc` em um único ponto, `free` na remoção e no encerramento).
- **Busca linear:** é a base da consulta por ID e das pesquisas por tipo e por titular, e também da verificação de duplicidade. É o único algoritmo de busca possível sobre uma lista encadeada, que não permite acesso direto a um elemento do meio.
- **Insertion Sort por religamento de ponteiros:** organiza os registros por tipo, titular ou ID, sem copiar dados e sem alocar memória.
- **Contagem por acesso direto e por varredura:** os indicadores por tipo e por categoria usam vetores de contadores indexados, enquanto o indicador por titular usa varreduras aninhadas.
A tabela final resume a complexidade das operações:

| Operação | Pior caso | Melhor caso | Justificativa curta |
|---|---|---|---|
| **Inserção** | `O(n)` | `Ω(1)` (lista vazia) | Percurso até o último nó + verificação de duplicidade; sem ponteiro para o final. |
| **Busca** | `O(n)` | `Ω(1)` (por ID, 1º nó) | Busca linear; lista encadeada não permite acesso por índice nem busca binária. |
| **Remoção** | `O(n)` | `Ω(1)` (cabeça) | Localizar o nó é `O(n)`; religar e liberar é `O(1)`. |
| **Ordenação** (Insertion Sort) | `O(n²)` | `Ω(n)` | Cada inserção percorre a região ordenada a partir da cabeça. Estável e `O(1)` de espaço extra. |

