# Bridge AI — Base de dados de documentos para idosos rurais

Global Solution 2026.2 · FIAP · Data Structures and Algorithms (DSA) · Turma 1CC-FEV

## Equipe

| Integrante | RM |
|---|---|
| Thiago Soalheiro Diamantino | 569316 |
| Kauan Damasceno de Lima | 573727 |

---

*Menu principal do programa em execução no terminal.*

<img width="604" height="378" alt="image" src="https://github.com/user-attachments/assets/fa39c2b8-eaa1-4368-89b9-2d34ebde3d1c" />

---

## Sumário

1. [Contextualização](#1-contextualização)
2. [Objetivo](#2-objetivo)
3. [Compilação e execução](#3-compilação-e-execução)
4. [Modelo de dados](#4-modelo-de-dados)
5. [Lista encadeada](#5-lista-encadeada)
6. [Menu e funcionalidades](#6-menu-e-funcionalidades)
7. [Ordenação](#7-ordenação)
8. [Conclusão](#8-conclusão)

---

## 1. Contextualização

O Bridge AI é um assistente digital que ajuda cidadãos a encontrar informações úteis do cotidiano, como serviços, documentos e direitos. O projeto adota o recorte **Documentação e Cidadania** e tem como público principal o idoso que vive em região rural, que costuma enfrentar deslocamentos longos até a cidade, pouca familiaridade com tecnologia e dúvida sobre quais documentos são necessários em cada atendimento.

Este módulo, desenvolvido em C, não é o chatbot. Ele implementa a **base de dados de documentos** que o assistente consultaria: um cadastro em memória, organizado em lista encadeada, com operações de cadastro, consulta, pesquisa, atualização, exclusão, ordenação e indicadores.

## 2. Objetivo

Construir uma base de dados de documentos voltada para idosos de região rural, aplicando estruturas de dados e algoritmos estudados na disciplina:

- armazenar múltiplos registros em uma **lista encadeada** própria, com alocação e liberação dinâmica de memória;
- consultar e pesquisar registros por **titular**, **tipo de documento** ou **identificador**, com algoritmo de busca linear;
- organizar os registros com o algoritmo **Insertion Sort**, por critérios definidos pelo usuário;
- atualizar e excluir registros preservando a integridade da lista;
- tratar opções inválidas, entradas inválidas, duplicidade, consultas sem resultado e lista vazia.

Os tipos de documento cadastráveis refletem a realidade do público-alvo. Além dos documentos pessoais comuns (RG, CPF, CNH, título de eleitor, certidões e cartão do SUS), o sistema inclui a Carteira do Idoso, a Autodeclaração Rural (segurado especial), a Matrícula do Imóvel Rural e o CCIR.

## 3. Compilação e execução

### Execução direta (Windows)
 
1. No repositório do GitHub, clique em **Code > Download ZIP** e extraia o arquivo.
2. Entre na pasta `Data Structures and Algorithms` e abra a pasta `output`.
3. Abra o Prompt de Comando ou o PowerShell dentro dessa pasta. No Prompt de Comando, execute `main.exe`; no PowerShell, execute `.\main.exe`. Também é possível dar dois cliques no arquivo, mas a janela fecha assim que o programa é encerrado.
O executável foi compilado para Windows. Se o sistema exibir um aviso de segurança, clique em "Mais informações" e depois em "Executar assim mesmo". Em Linux ou macOS, compile a partir do código-fonte.
 
### Compilação a partir do código-fonte
 
O programa usa apenas as bibliotecas padrão `stdio.h`, `stdlib.h` e `string.h`, sem dependências externas. Requer um compilador C com suporte ao padrão C99 ou superior (por exemplo, o GCC).
 
Os comandos abaixo devem ser executados dentro da pasta `Data Structures and Algorithms`, onde está o arquivo `main.c`. Como o nome da pasta tem espaços, use aspas ao entrar nela:
 
```bash
cd "Data Structures and Algorithms"
```
 
**Linux e macOS**
 
```bash
gcc -Wall -Wextra -o citizen_assist main.c
./citizen_assist
```
 
**Windows (GCC/MinGW)**
 
```bash
gcc -Wall -Wextra -o citizen_assist.exe main.c
.\citizen_assist.exe
```
 
As mensagens do programa são escritas sem acentos para evitar problemas de codificação em terminais diferentes. A interação é feita pelo teclado: o usuário digita o número da opção e confirma com Enter.

## 4. Modelo de dados

### 4.1 Registro

Cada nó da lista representa um documento de uma pessoa e é declarado pela estrutura `Documento`:

```c
typedef struct Documento {
    int id;
    char titular[100];
    int tipo;
    int categoria;
    char numero[50];
    struct Documento *proximo;
} Documento;
```

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | `int` | Identificador único, gerado automaticamente pelo contador global `proximoId`. O usuário nunca digita o ID. Após uma exclusão, o número não é reaproveitado. |
| `titular` | `char[100]` | Nome da pessoa a quem o documento pertence. Aceita apenas letras e espaços. |
| `tipo` | `int` | Posição do tipo de documento no vetor `TIPOS`. |
| `categoria` | `int` | Posição da categoria no vetor `CATEGORIAS`. É calculada a partir do tipo e preenchida automaticamente. |
| `numero` | `char[50]` | Número do documento ou número de protocolo pelo qual o registro completo é localizado. Aceita apenas dígitos. É armazenado como texto para preservar zeros à esquerda e comportar números longos. |
| `proximo` | `struct Documento *` | Ponteiro para o próximo nó da lista. Vale `NULL` no último nó. |

A lista guarda documentos de várias pessoas, e uma mesma pessoa pode ter vários registros. Por isso o `id` identifica o **registro**, e não a pessoa: o nome não serve como chave única, porque existem homônimos e a mesma pessoa aparece em mais de um registro.

### 4.2 Tabelas de apoio

O tipo e a categoria são escolhidos entre opções fixas, guardadas em vetores. O nó armazena apenas o **índice** da opção, e não o texto. Isso traz quatro vantagens: a ordenação por tipo vira uma comparação de inteiros (a ordem do vetor é a ordem de ordenação), a validação se resume a conferir um intervalo, a contagem dos indicadores usa o índice como posição em um vetor de contadores, e não há risco de grafias diferentes para o mesmo tipo.

Os vetores paralelos `CATEGORIA_DO_TIPO` e `PODE_REPETIR` são indexados pelo tipo e completam a informação de cada um:

| Nº no menu | Tipo | Categoria | Pode repetir para o mesmo titular |
|---|---|---|---|
| 1 | RG - Registro Geral | Identidade | Não |
| 2 | CPF - Cadastro de Pessoas Fisicas | Identidade | Não |
| 3 | CNH - Carteira Nacional de Habilitacao | Transito | Não |
| 4 | Titulo de Eleitor | Eleitoral | Não |
| 5 | Certidao de Nascimento | Registro Civil | Não |
| 6 | Certidao de Casamento | Registro Civil | Não |
| 7 | Cartao Nacional de Saude (Cartao do SUS) | Saude | Não |
| 8 | Carteira do Idoso | Beneficios e Previdencia | Não |
| 9 | Autodeclaracao Rural (Segurado Especial) | Beneficios e Previdencia | Sim |
| 10 | Matricula do Imovel Rural | Terra Rural | Sim |
| 11 | CCIR - Certificado de Cadastro de Imovel Rural | Terra Rural | Sim |

O número exibido no menu é a posição no vetor mais um. O programa converte a escolha do usuário para o índice com `escolha - 1`.

### 4.3 Validações e casos especiais

| Situação | Tratamento |
|---|---|
| Opção de menu inválida ou texto no lugar de número | `ler_inteiro` devolve `-1`, que cai no `default` do `switch` (ou no laço de validação do submenu), e o programa informa o erro. |
| Nome do titular | `conferir_nome_valido` aceita apenas letras, letras acentuadas e espaços, com ao menos uma letra. O programa repete a pergunta até a entrada ser válida. |
| Número do documento | `conferir_numero_valido` aceita apenas dígitos e rejeita entrada vazia. O programa repete a pergunta até a entrada ser válida. |
| Tipo de documento | A escolha precisa estar entre 1 e 11. |
| Identificador duplicado | Não ocorre por construção: o ID é gerado por um contador que só cresce. |
| Documento duplicado | Tratado por `existe_duplicado`, conforme a regra abaixo. |
| Lista vazia | Pesquisar, atualizar, excluir, listar, ordenar e indicadores verificam `cabeca == NULL` e exibem "Nenhum documento cadastrado.". |
| Consulta sem resultado | As pesquisas exibem "Nenhum documento encontrado...". |
| ID inexistente | Atualizar e excluir informam que nenhum documento foi encontrado com o ID digitado. |

**Regra de duplicidade.** Dois registros são duplicados quando pertencem ao mesmo titular e ao mesmo tipo, com uma exceção. Os tipos marcados como repetíveis (Autodeclaração Rural, Matrícula do Imóvel Rural e CCIR) podem existir mais de uma vez para a mesma pessoa, pois um idoso rural pode ter mais de um imóvel. Para esses tipos, o registro só é duplicado se o **número também for igual**.

## 5. Lista encadeada

A lista é o único local onde os dados ficam armazenados. Não existe vetor com os registros: cada nó é alocado com `malloc` e ligado ao seguinte pelo campo `proximo`.

```
cabeca
  |
  v
[id=1 | Maria | RG] -> [id=2 | Maria | Matricula] -> [id=3 | Joao | CPF] -> NULL
```

A variável `Documento *cabeca`, declarada em `main`, guarda o endereço do primeiro nó. Uma lista vazia é representada por `cabeca == NULL`.

| Operação | Função | Descrição |
|---|---|---|
| Inserção | `inserir_fim` | Liga o novo nó ao final da lista. |
| Percurso | `listar_todos`, funções de pesquisa, `exibir_indicadores` | Seguem `proximo` a partir da cabeça até encontrar `NULL`. |
| Remoção | `remover_por_id` | Religa o nó anterior ao seguinte e libera o nó removido. |
| Liberação total | `liberar_lista` | Libera todos os nós ao encerrar o programa. |

**Alocação e liberação dinâmica.** A alocação ocorre em um único ponto, `criarNo`. A liberação ocorre em `remover_por_id` (um nó) e em `liberar_lista` (todos os nós).

**Ponteiro para ponteiro.** As funções que podem mudar o endereço do primeiro nó recebem `Documento **cabeca`: `inserir_fim` (a lista vazia passa a ter uma cabeça), `remover_por_id` (a cabeça pode ser removida) e `ordenar_lista` (a cabeça muda após a ordenação). Com um ponteiro simples, a alteração ocorreria em uma cópia local e a variável `cabeca` de `main` continuaria apontando para o endereço antigo. As funções que apenas leem a lista ou alteram campos de um nó recebem `Documento *`.

## 6. Menu e funcionalidades

O menu fica dentro de um laço `do ... while (opcao != 0)`, o que permite executar várias operações em sequência com a lista mantida em memória.

| Opção | Funcionalidade | Funções principais |
|---|---|---|
| 1 | Cadastrar | `cadastrar_documento` |
| 2 | Pesquisar (titular, tipo ou ID) | `pesquisar_documentos`, `pesquisar_por_titular`, `pesquisar_por_tipo`, `pesquisar_por_id` |
| 3 | Atualizar | `atualizar_documento`, `atualizar_titular`, `atualizar_tipo`, `atualizar_numero` |
| 4 | Excluir | `excluir_documento`, `remover_por_id` |
| 5 | Listar | `listar_todos` |
| 6 | Ordenar | `ordenar_documentos`, `ordenar_lista`, `comparar` |
| 7 | Indicadores | `exibir_indicadores` |
| 0 | Sair | `liberar_lista` |

### 6.1 Funções compartilhadas

Estas funções são usadas por mais de uma opção do menu.

| Função | Funcionamento |
|---|---|
| `ler_string(destino, tamanho)` | Lê uma linha com `fgets` (aceita espaços e respeita o tamanho do vetor) e troca o `'\n'` final por `'\0'`. |
| `ler_inteiro()` | Lê a linha como texto com `fgets` e converte com `sscanf`. Devolve o número lido ou `-1` se a conversão falhar. Ler como texto evita deixar lixo no buffer e laço infinito quando o usuário digita letras. |
| `conferir_nome_valido(texto)` | Percorre a string e devolve 1 se todos os caracteres forem letras, letras acentuadas ou espaço, com ao menos uma letra. |
| `conferir_numero_valido(texto)` | Devolve 1 se a string não for vazia e todos os caracteres forem dígitos de `'0'` a `'9'`. |
| `criarNo(titular, tipo, numero)` | Aloca um nó com `malloc`, atribui o próximo ID, copia os dados, calcula a categoria por `CATEGORIA_DO_TIPO[tipo]` e define `proximo = NULL`. Devolve `NULL` se a alocação falhar. |
| `inserir_fim(&cabeca, novo)` | Se a lista está vazia, o novo nó vira a cabeça. Caso contrário, percorre até o último nó e liga o novo nó a ele. |
| `liberar_lista(&cabeca)` | Percorre a lista guardando o próximo nó antes de cada `free`, libera todos os nós e define `*cabeca = NULL`. |
| `existe_duplicado(cabeca, titular, tipo, numero, ignorar_id)` | Devolve 1 se existir outro nó com o mesmo titular e tipo. Para tipos repetíveis (`PODE_REPETIR`), exige também número igual. O nó com `id == ignorar_id` é desconsiderado, para que um registro não seja duplicado dele mesmo na atualização (no cadastro, passa-se `0`). |
| `mostrar_duplicado(titular, tipo, numero)` | Exibe a mensagem de duplicidade, incluindo o número quando o tipo é repetível. |
| `imprimir_lista(d)` | Exibe um registro: ID, titular, tipo, categoria e número. |
| `buscar_por_id(cabeca, id)` | Percorre a lista e devolve o ponteiro do nó com aquele ID, ou `NULL` se não existir. Devolve o endereço do nó real (e não uma cópia), o que permite alterá-lo diretamente. |
| `para_minusculo(origem, destino)` | Copia a string trocando as letras de `A` a `Z` por minúsculas (soma 32 ao código ASCII). |

### 6.2 Opção 1 — Cadastrar

`cadastrar_documento` coleta os dados em sequência, validando cada um:

1. lê o titular e repete a pergunta até `conferir_nome_valido` aceitar;
2. exibe os tipos a partir de `TIPOS`, lê a escolha e repete até estar entre 1 e 11;
3. lê o número e repete até `conferir_numero_valido` aceitar;
4. chama `existe_duplicado`. Se houver duplicidade, exibe o aviso com `mostrar_duplicado` e cancela;
5. cria o nó com `criarNo`, liga-o com `inserir_fim` e exibe o ID gerado e a categoria atribuída.

**Funções utilizadas:** `ler_string`, `ler_inteiro`, `conferir_nome_valido`, `conferir_numero_valido`, `existe_duplicado`, `mostrar_duplicado`, `criarNo`, `inserir_fim`.

### 6.3 Opção 2 — Pesquisar

A opção abre um submenu para escolher o campo da pesquisa: titular, tipo, ID ou voltar. Todas as pesquisas usam **busca linear**: percorrem a lista do início até `NULL`, comparam o campo de cada nó com o valor procurado e exibem os que correspondem, junto com a contagem de resultados. Quando nada corresponde, exibem mensagem de "nenhum resultado".

| Função | Funcionamento |
|---|---|
| `pesquisar_documentos` | Exibe o submenu, valida a opção e chama a função do campo escolhido. |
| `pesquisar_por_titular` | Lê o termo, valida como nome e converte para minúsculo. Para cada nó, converte o titular para minúsculo e usa `strstr` para verificar se o termo está contido nele. A busca é parcial: "mar" encontra "Maria Silva" e "Mario". |
| `pesquisar_por_tipo` | Exibe os tipos, valida a escolha e exibe todos os nós cujo `tipo` é igual ao escolhido. |
| `pesquisar_por_id` | Lê o ID (deve ser maior que zero) e usa `buscar_por_id`. Como o ID é único, o resultado é um só registro. |

O `strstr(texto, termo)` devolve um ponteiro para a primeira ocorrência de `termo` dentro de `texto`, ou `NULL` se não houver. O programa só testa se o resultado é diferente de `NULL`.

A pesquisa por titular pode devolver vários registros (por exemplo, todos os documentos de uma pessoa). O ID exibido em cada um é usado para escolher o registro nas opções de atualizar e excluir.

**Funções utilizadas:** `pesquisar_documentos`, `pesquisar_por_titular`, `pesquisar_por_tipo`, `pesquisar_por_id`, `buscar_por_id`, `para_minusculo`, `conferir_nome_valido`, `ler_string`, `ler_inteiro`, `imprimir_lista`.

### 6.4 Opção 3 — Atualizar

Como o usuário não conhece os IDs, o fluxo começa por uma pesquisa:

1. `atualizar_documento` chama `pesquisar_documentos` para o usuário localizar o registro e ver o ID;
2. pede o ID do registro (0 cancela) e localiza o nó com `buscar_por_id`;
3. exibe o registro e um submenu para alterar o nome, o tipo ou o número, repetindo até o usuário escolher "Concluir". Assim é possível alterar mais de um campo na mesma operação.

| Função | Funcionamento |
|---|---|
| `atualizar_titular` | Lê e valida o novo nome. Antes de gravar, chama `existe_duplicado` com o novo nome, o tipo e o número do registro. Se houver duplicidade, nada é alterado. |
| `atualizar_tipo` | Exibe os tipos e valida a escolha. Se for igual ao tipo atual, nada muda. Verifica duplicidade com o novo tipo. Se estiver livre, grava o tipo e **recalcula a categoria** por `CATEGORIA_DO_TIPO`. |
| `atualizar_numero` | Lê e valida o novo número (apenas dígitos). Verifica duplicidade (relevante para os tipos repetíveis) e então grava. |

**Integridade da lista.** A atualização não remove nem recria o nó: apenas os campos de dados são sobrescritos. Os campos `id` e `proximo` nunca são tocados, de modo que as ligações da lista permanecem intactas. A chamada a `existe_duplicado` passa o `id` do próprio registro em `ignorar_id`, evitando que ele seja considerado duplicado dele mesmo.

**Funções utilizadas:** `atualizar_documento`, `atualizar_titular`, `atualizar_tipo`, `atualizar_numero`, `pesquisar_documentos`, `buscar_por_id`, `existe_duplicado`, `mostrar_duplicado`, `conferir_nome_valido`, `conferir_numero_valido`, `ler_string`, `ler_inteiro`, `imprimir_lista`.

### 6.5 Opção 4 — Excluir

O fluxo é semelhante ao da atualização: pesquisa para localizar o registro, escolha do ID (0 cancela) e exibição do registro selecionado. Como a exclusão não pode ser desfeita, `excluir_documento` pede confirmação (`S` ou `N`) e só então chama `remover_por_id`.

`remover_por_id(&cabeca, id)` percorre a lista mantendo dois ponteiros: `atual` (o nó procurado) e `anterior` (o nó imediatamente antes dele). O anterior é necessário porque, para retirar um nó, o nó anterior precisa passar a apontar para o seguinte:

```
antes:   [Ana] -> [Bia] -> [Caio]        remover Bia
depois:  [Ana] ---------> [Caio]         anterior->proximo = atual->proximo
```

Há dois casos:

| Caso | Condição | Ação |
|---|---|---|
| Nó é a cabeça | `anterior == NULL` | `*cabeca = atual->proximo` |
| Nó do meio ou do fim | `anterior != NULL` | `anterior->proximo = atual->proximo` |

Depois do religamento, `free(atual)` devolve a memória do nó removido. A função devolve 1 se removeu e 0 se não encontrou o ID.

**Funções utilizadas:** `excluir_documento`, `remover_por_id`, `pesquisar_documentos`, `buscar_por_id`, `ler_string`, `ler_inteiro`, `imprimir_lista`.

### 6.6 Opção 5 — Listar

`listar_todos` percorre a lista a partir da cabeça e chama `imprimir_lista` para cada nó, na ordem em que a lista está no momento (ordem de cadastro ou a última ordenação aplicada). Com a lista vazia, exibe "Nenhum documento cadastrado.".

**Funções utilizadas:** `listar_todos`, `imprimir_lista`.

### 6.7 Opção 6 — Ordenar

O usuário escolhe o critério (tipo, titular ou ID), `ordenar_documentos` chama `ordenar_lista` e, em seguida, exibe a lista já ordenada. O algoritmo, os critérios e a implementação estão detalhados na [seção 7](#7-ordenação).

**Funções utilizadas:** `ordenar_documentos`, `ordenar_lista`, `comparar`, `comparar_titulares`, `para_minusculo`, `listar_todos`.

### 6.8 Opção 7 — Indicadores

`exibir_indicadores` calcula e exibe:

- **total** de documentos cadastrados;
- **quantidade por tipo**, apenas dos tipos com quantidade maior que zero;
- **quantidade por categoria**, apenas das categorias com quantidade maior que zero;
- **quantidade por titular**.

Em um único percurso, a função incrementa o contador do total e os vetores `por_tipo` e `por_categoria`, usando `tipo` e `categoria` do nó como posição. A contagem por titular é feita à parte: para cada nó, verifica se o nome já apareceu em um nó anterior (`strcmp`); se for a primeira ocorrência, conta quantos nós a partir dele têm o mesmo titular e exibe o resultado.

**Funções utilizadas:** `exibir_indicadores`.

### 6.9 Opção 0 — Sair

Encerra o laço do menu. Antes de terminar, `main` chama `liberar_lista(&cabeca)` para devolver ao sistema a memória de todos os nós.

## 7. Ordenação

O algoritmo implementado é o **Insertion Sort**, aplicado diretamente sobre a lista encadeada.

### 7.1 Teoria

O Insertion Sort divide a sequência em duas partes: uma região **ordenada** e uma região **ainda não processada**. A cada passo, retira um elemento da região não processada e o insere na posição correta dentro da região ordenada. A propriedade que se mantém durante toda a execução é: depois de processar *k* elementos, a região ordenada contém exatamente esses *k* elementos em ordem. Quando todos os elementos foram processados, a sequência inteira está ordenada.

**Estabilidade.** O algoritmo é estável quando um elemento novo é inserido depois dos elementos de chave igual que já estão na região ordenada. Nesse caso, elementos com chaves iguais mantêm a ordem relativa que tinham antes da ordenação.

**Adaptação para lista encadeada.** Em um vetor, inserir na posição correta exige deslocar elementos para abrir espaço, o que depende de acesso por índice. Em uma lista encadeada não há índice nem percurso para trás, mas também não há deslocamento: inserir um nó entre dois outros exige apenas alterar dois ponteiros. Por isso a implementação procura a posição percorrendo a região ordenada a partir da cabeça e faz a inserção por **religamento de ponteiros**. Nenhum dado é copiado e nenhum nó é alocado ou liberado.

### 7.2 Critérios de ordenação

O algoritmo não sabe como os registros são comparados. Essa decisão fica na função `comparar(a, b, criterio)`, que segue a convenção de `strcmp`: devolve **negativo** se `a` deve vir antes de `b`, **zero** se são equivalentes e **positivo** se `a` deve vir depois. Trocar o critério não exige alterar o algoritmo.

| Opção | Critério principal | Desempate |
|---|---|---|
| 1 — Tipo | Posição do tipo no vetor `TIPOS` (RG, CPF, CNH, ...), por `a->tipo - b->tipo` | Titular em ordem alfabética |
| 2 — Titular | Ordem alfabética do titular | Tipo |
| 3 — ID | `a->id - b->id` | Não há (o ID é único) |

```c
int comparar(Documento *a, Documento *b, int criterio) {
    if (criterio == 1) {
        if (a->tipo != b->tipo) {
            return a->tipo - b->tipo;
        }
        return comparar_titulares(a->titular, b->titular);
    }

    if (criterio == 2) {
        int resultado = comparar_titulares(a->titular, b->titular);
        if (resultado != 0) {
            return resultado;
        }
        return a->tipo - b->tipo;
    }

    return a->id - b->id;
}
```

`comparar_titulares` converte os dois nomes para minúsculo com `para_minusculo` e aplica `strcmp`, de modo que "ana" e "Ana" sejam equivalentes na ordenação. Como os IDs crescem na ordem de cadastro, ordenar por ID restaura a ordem original de cadastro.

### 7.3 Implementação

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
            while (posicao->proximo != NULL && comparar(posicao->proximo, atual, criterio) <= 0) {
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

Correspondência entre a teoria e o código:

| Elemento do código | Papel no algoritmo |
|---|---|
| `ordenada` | Cabeça da região ordenada, que começa vazia (`NULL`) e é montada nó a nó. |
| `atual` | Percorre a lista original: é o elemento retirado da região não processada em cada passo. |
| `proximo = atual->proximo` | Guarda a continuação da lista original **antes** de religar, porque `atual->proximo` será sobrescrito durante a inserção. Sem isso, o restante da lista seria perdido. |
| Primeiro `if` | Trata a inserção **no início** da região ordenada: ocorre quando ela está vazia ou quando `atual` deve vir antes da cabeça atual (`comparar < 0`). |
| `posicao` | Percorre a região ordenada procurando o nó **após o qual** `atual` deve entrar. |
| Condição `comparar(posicao->proximo, atual, criterio) <= 0` | Avança enquanto o nó seguinte for menor ou **igual** a `atual`. O `<=` faz o novo elemento entrar depois dos equivalentes que já estão na região ordenada, o que garante a estabilidade. |
| `atual->proximo = posicao->proximo; posicao->proximo = atual;` | Inserção por religamento: `atual` passa a apontar para o sucessor de `posicao`, e `posicao` passa a apontar para `atual`. A ordem dessas duas atribuições é essencial: invertê-la faria `atual` apontar para si mesmo. |
| `*cabeca = ordenada` | Atualiza a cabeça da lista de `main` (por isso o parâmetro é `Documento **`). |

### 7.4 Exemplo passo a passo

Critério: titular. Lista original, na ordem de cadastro: `Carlos -> Ana -> Bia`.

| Passo | `atual` | Comparação | Região ordenada depois do passo |
|---|---|---|---|
| Início | — | — | vazia |
| 1 | Carlos | A região está vazia, então Carlos vira a cabeça. | `Carlos` |
| 2 | Ana | `comparar(Ana, Carlos) < 0`, então Ana vira a nova cabeça. | `Ana -> Carlos` |
| 3 | Bia | `comparar(Bia, Ana) > 0`, então não é a cabeça. `posicao` começa em Ana, e `comparar(Carlos, Bia) > 0` interrompe o avanço. Bia é inserida depois de Ana. | `Ana -> Bia -> Carlos` |

Resultado: `Ana -> Bia -> Carlos`. Ao final, `*cabeca` passa a apontar para Ana.

### 7.5 Observações

- A ordenação **altera a lista de forma permanente**: a opção Listar e as demais operações passam a seguir a nova ordem até outra ordenação ser aplicada.
- Lista vazia é tratada antes da escolha do critério. Com um único elemento, a lista permanece como está.
- Na ordenação por tipo, registros do mesmo tipo são desempatados pelo titular. Por exemplo, com `Bia (CPF)`, `Bia (RG)` e `Ana (CPF)`, o resultado é `Bia (RG)`, `Ana (CPF)`, `Bia (CPF)`.
- Nomes que começam com letra acentuada (por exemplo, "Álvaro") ordenam depois de todos os nomes sem acento, porque o código dos caracteres acentuados é maior que o das letras comuns.

## 8. Conclusão
 
O Bridge AI cumpre o objetivo de oferecer uma base de dados de documentos para idosos de região rural, construída inteiramente sobre uma **lista encadeada** própria, com alocação e liberação dinâmica de memória. O sistema permite cadastrar, pesquisar, atualizar, excluir, listar e ordenar registros, além de exibir indicadores, e trata entradas inválidas, duplicidade, consultas sem resultado e lista vazia, mantendo a integridade da lista em todas as operações.
 
Os algoritmos escolhidos, **busca linear** e **Insertion Sort**, são simples de entender, testar e demonstrar, e adequados ao porte esperado do cadastro. O projeto mostra, na prática, como a escolha da estrutura de dados influencia o funcionamento e o custo de cada operação.
