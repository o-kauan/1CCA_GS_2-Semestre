#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *TIPOS[6] = {"RG", "CPF", "CNH", "Titulo de eleitor", "Certidao", "Outro"};

const char *CATEGORIAS[5] = {"Identidade", "Transito", "Eleitoral", "Registro civil", "Outros"};

int CATEGORIA_DO_TIPO[6] = {0, 0, 1, 2, 3, 4};

typedef struct Documento {
    int id;                    // automatico, unico
    char titular[100];         // digitado: "Maria Silva"
    int tipo;                  // indice em TIPOS
    int categoria;             // indice em CATEGORIAS (preenchido sozinho)
    char numero[50];           // digitado: "101653218"
    struct Documento *proximo; // proximo no da lista
} Documento;

int proximoId = 1;

/* ---------------------------------------------------------
   FUNCOES AUXILIARES DE LEITURA
   --------------------------------------------------------- */
 
void ler_string(char *destino, int tamanho) {
    fgets(destino, tamanho, stdin);
    int n = strlen(destino);
    if (n > 0 && destino[n - 1] == '\n') {
        destino[n - 1] = '\0';
    }
}
 
int ler_inteiro() {
    char linha[50];
    int valor;
    fgets(linha, sizeof(linha), stdin);
    if (sscanf(linha, "%d", &valor) != 1) {
        return -1;
    }
    return valor;
}

int conferir_nome_valido(char *texto) {
    int letras = 0;
    for (int i = 0; texto[i] != '\0'; i++) {
        unsigned char c = texto[i];
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c > 127) {
            letras++;              
        } else if (c != ' ') {
            return 0;              
        }
    }
    return letras > 0;             
}

int conferir_numero_valido(char *texto) {
    if (texto[0] == '\0') {
        return 0;
    }
    for (int i = 0; texto[i] != '\0'; i++) {
        if (texto[i] < '0' || texto[i] > '9') {
            return 0;
        }
    }
    return 1;
}

/* ---------------------------------------------------------
   FUNCOES DA LISTA ENCADEADA
   --------------------------------------------------------- */

Documento *criarNo(char *titular, int tipo, char *numero) {
    Documento *novo = (Documento *) malloc(sizeof(Documento));
    if (novo == NULL) {
        printf("Erro: memoria insuficiente.\n");
        return NULL;
    }
    novo->id = proximoId;
    proximoId++;
    
    strcpy(novo->titular, titular);
    novo->tipo = tipo;
    
    novo->categoria = CATEGORIA_DO_TIPO[tipo];   
    strcpy(novo->numero, numero);
    novo->proximo = NULL;
    return novo;
}

void inserir_fim(Documento **cabeca, Documento *novo) {
    if (*cabeca == NULL) {          
        *cabeca = novo;
        return;
    }
    Documento *atual = *cabeca;
    while (atual->proximo != NULL) {
        atual = atual->proximo;
    }
    atual->proximo = novo;
}

void liberar_lista(Documento **cabeca) {
    Documento *atual = *cabeca;
    while (atual != NULL) {
        Documento *proximo = atual->proximo;
        free(atual);
        atual = proximo;
    }
    *cabeca = NULL;
}

int existe_duplicado(Documento *cabeca, char *titular, int tipo, int ignorar_id) {
    Documento *atual = cabeca;
    while (atual != NULL) {
        if (atual->id != ignorar_id && strcmp(atual->titular, titular) == 0 && atual->tipo == tipo) {
            return 1;
        }
        atual = atual->proximo;
    }
    return 0;
}

/* ---------------------------------------------------------
   FUNCOES DO SISTEMA
   --------------------------------------------------------- */

void imprimir_lista(Documento *d) {
    printf("ID: %d | Titular: %s | Tipo: %s | Categoria: %s | Numero: %s\n",
           d->id, d->titular, TIPOS[d->tipo], CATEGORIAS[d->categoria], d->numero);
}

void listar_todos(Documento *cabeca) {
    if (cabeca == NULL) {
        printf("Nenhum documento cadastrado.\n");
        return;
    }
    Documento *atual = cabeca;
    while (atual != NULL) {
        imprimir_lista(atual);
        atual = atual->proximo;
    }
}

/*----------------------------------------------------------
  NOVO CADASTRO
  ----------------------------------------------------------*/
void cadastrar_documento(Documento **cabeca) {
    char titular[100];
    char numero[50];
    int escolha;

    printf("\nNome do titular: ");
    ler_string(titular, 100);
    
    while (!conferir_nome_valido(titular)) {
    printf("ERRO (use apenas letras e espacos)\n");
    printf("Tente novamente: ");
    ler_string(titular, 100);
    }

    printf("\nTipos de documento:\n");
    for (int i = 0; i < 6; i++) {
        printf("(%d) %s\n", i + 1, TIPOS[i]);
    }

    printf("Escolha o tipo: ");
    escolha = ler_inteiro();

    while (escolha < 1 || escolha > 6) {
        printf("ERRO (tipo invalido)\n");
        printf("Tente novamente: ");
        escolha = ler_inteiro();
    }
    int tipo = escolha - 1; 

    if (existe_duplicado(*cabeca, titular, tipo, 0)) {
        printf("%s ja possui o documento %s cadastrado.\n", titular, TIPOS[tipo]);
        return;
    }

    printf("\nNumero do documento: ");
    ler_string(numero, 50);
    
    while (!conferir_numero_valido(numero)) {
    printf("ERRO (digite apenas digitos)\n");
    printf("Tente novamente: ");
    ler_string(numero, 50);
    }

    Documento *novo = criarNo(titular, tipo, numero);
    if (novo == NULL) {
        return;
    }
    inserir_fim(cabeca, novo);
    printf("Cadastrado com sucesso! ID: %d (categoria: %s)\n",
           novo->id, CATEGORIAS[novo->categoria]);
}

/* ---------------------------------------------------------
   PESQUISA
   --------------------------------------------------------- */

void para_minusculo(char *origem, char *destino) {
    int i;
    for (i = 0; origem[i] != '\0'; i++) {
        if (origem[i] >= 'A' && origem[i] <= 'Z') {
            destino[i] = origem[i] + 32;
        } else {
            destino[i] = origem[i];
        }
    }
    destino[i] = '\0';
}

Documento *buscar_por_id(Documento *cabeca, int id) {
    Documento *atual = cabeca;
    while (atual != NULL) {
        if (atual->id == id) {
            return atual;
        }
        atual = atual->proximo;
    }
    return NULL;
}

void pesquisar_por_titular(Documento *cabeca) {
    char termo[100];
    char termo_min[100];
    char titular_min[100];
    int encontrados = 0;

    printf("\nNome (ou parte do nome) do titular: ");
    ler_string(termo, 100);

    while (!conferir_nome_valido(termo)) {
        printf("ERRO (use apenas letras e espacos)\n");
        printf("Tente novamente: ");
        ler_string(termo, 100);
    }
    para_minusculo(termo, termo_min);

    printf("\nResultados:\n");
    Documento *atual = cabeca;
    while (atual != NULL) {
        para_minusculo(atual->titular, titular_min);
        if (strstr(titular_min, termo_min) != NULL) {   
            imprimir_lista(atual);
            encontrados++;
        }
        atual = atual->proximo;
    }

    if (encontrados == 0) {
        printf("Nenhum documento encontrado para \"%s\".\n", termo);
    } else {
        printf("%d documento(s) encontrado(s).\n", encontrados);
    }
}

void pesquisar_por_tipo(Documento *cabeca) {
    int escolha;
    int encontrados = 0;

    printf("\nTipo de documento:\n");
    for (int i = 0; i < 6; i++) {
        printf("  (%d) %s\n", i + 1, TIPOS[i]);
    }
    printf("Escolha o tipo: ");
    escolha = ler_inteiro();

    while (escolha < 1 || escolha > 6) {
        printf("ERRO (tipo invalido)\n");
        printf("Tente novamente: ");
        escolha = ler_inteiro();
    }
    int tipo = escolha - 1;

    printf("\nResultados:\n");
    Documento *atual = cabeca;
    while (atual != NULL) {
        if (atual->tipo == tipo) {
            imprimir_lista(atual);
            encontrados++;
        }
        atual = atual->proximo;
    }

    if (encontrados == 0) {
        printf("Nenhum documento do tipo %s encontrado.\n", TIPOS[tipo]);
    } else {
        printf("%d documento(s) encontrado(s).\n", encontrados);
    }
}

void pesquisar_por_id(Documento *cabeca) {
    printf("\nDigite o ID: ");
    int id = ler_inteiro();

    while (id < 1) {
        printf("ERRO (o ID deve ser um numero maior que zero)\n");
        printf("Tente novamente: ");
        id = ler_inteiro();
    }

    Documento *achado = buscar_por_id(cabeca, id);
    printf("\nResultado:\n");
    if (achado == NULL) {
        printf("Nenhum documento encontrado com o ID %d.\n", id);
    } else {
        imprimir_lista(achado);
    }
}

void pesquisar_documentos(Documento *cabeca) {
    if (cabeca == NULL) {
        printf("Nenhum documento cadastrado.\n");
        return;
    }

    printf("\nPesquisar por:\n");
    printf("  (1) Nome do titular\n");
    printf("  (2) Tipo de documento\n");
    printf("  (3) ID\n");
    printf("  (0) Voltar\n");
    printf("Escolha uma opcao: ");
    int campo = ler_inteiro();

    while (campo < 0 || campo > 3) {
        printf("ERRO (opcao invalida)\n");
        printf("Tente novamente: ");
        campo = ler_inteiro();
    }

    switch (campo) {
        case 1:
            pesquisar_por_titular(cabeca);
            break;
        case 2:
            pesquisar_por_tipo(cabeca);
            break;
        case 3:
            pesquisar_por_id(cabeca);
            break;
        case 0:
            break;
    }
}


/* ---------------------------------------------------------
   ATUALIZAR
   --------------------------------------------------------- */

void atualizar_titular(Documento *cabeca, Documento *doc) {
    char novo_titular[100];

    printf("\nNovo nome do titular: ");
    ler_string(novo_titular, 100);

    while (!conferir_nome_valido(novo_titular)) {
        printf("ERRO (use apenas letras e espacos)\n");
        printf("Tente novamente: ");
        ler_string(novo_titular, 100);
    }

    if (existe_duplicado(cabeca, novo_titular, doc->tipo, doc->id)) {
        printf("%s ja possui o documento %s cadastrado. Nada foi alterado.\n",
               novo_titular, TIPOS[doc->tipo]);
        return;
    }

    strcpy(doc->titular, novo_titular);
    printf("Nome atualizado com sucesso.\n");
}

void atualizar_tipo(Documento *cabeca, Documento *doc) {
    printf("\nTipo de documento:\n");
    for (int i = 0; i < 6; i++) {
        printf("(%d) %s\n", i + 1, TIPOS[i]);
    }
    printf("Escolha o novo tipo: ");
    int escolha = ler_inteiro();

    while (escolha < 1 || escolha > 6) {
        printf("ERRO (tipo invalido)\n");
        printf("Tente novamente: ");
        escolha = ler_inteiro();
    }
    int novo_tipo = escolha - 1;

    if (novo_tipo == doc->tipo) {
        printf("O documento ja e do tipo %s. Nada foi alterado.\n", TIPOS[novo_tipo]);
        return;
    }

    if (existe_duplicado(cabeca, doc->titular, novo_tipo, doc->id)) {
        printf("%s ja possui o documento %s cadastrado. Nada foi alterado.\n",
               doc->titular, TIPOS[novo_tipo]);
        return;
    }

    doc->tipo = novo_tipo;
    doc->categoria = CATEGORIA_DO_TIPO[novo_tipo];  
    printf("Tipo atualizado com sucesso (categoria: %s).\n", CATEGORIAS[doc->categoria]);
}

void atualizar_numero(Documento *doc) {
    char novo_numero[50];

    printf("\nNovo numero do documento: ");
    ler_string(novo_numero, 50);

    while (!conferir_numero_valido(novo_numero)) {
        printf("ERRO (digite apenas digitos)\n");
        printf("Tente novamente: ");
        ler_string(novo_numero, 50);
    }

    strcpy(doc->numero, novo_numero);
    printf("Numero atualizado com sucesso.\n");
}

void atualizar_documento(Documento *cabeca) {
    if (cabeca == NULL) {
        printf("Nenhum documento cadastrado.\n");
        return;
    }

    printf("\nPrimeiro, localize o documento que deseja atualizar.\n");
    pesquisar_documentos(cabeca);

    printf("\nDigite o ID do documento a atualizar (0 para cancelar): ");
    int id = ler_inteiro();
    while (id < 0) {
        printf("ERRO (digite um numero)\n");
        printf("Tente novamente: ");
        id = ler_inteiro();
    }
    if (id == 0) {
        printf("Atualizacao cancelada.\n");
        return;
    }

    Documento *doc = buscar_por_id(cabeca, id);
    if (doc == NULL) {
        printf("Nenhum documento encontrado com o ID %d.\n", id);
        return;
    }

    int opcao;
    do {
        printf("\nDocumento selecionado:\n");
        imprimir_lista(doc);
        printf("\nO que deseja alterar?\n");
        printf("(1) Nome do titular\n");
        printf("(2) Tipo de documento\n");
        printf("(3) Numero do documento\n");
        printf("(0) Concluir\n");
        printf("Escolha uma opcao: ");
        opcao = ler_inteiro();

        switch (opcao) {
            case 1:
                atualizar_titular(cabeca, doc);
                break;
            case 2:
                atualizar_tipo(cabeca, doc);
                break;
            case 3:
                atualizar_numero(doc);
                break;
            case 0:
                printf("Atualizacao concluida.\n");
                break;
            default:
                printf("Opcao invalida. Por favor, tente novamente.\n");
        }
    } while (opcao != 0);
}

/* ---------------------------------------------------------
   EXCLUIR
   --------------------------------------------------------- */
int remover_por_id(Documento **cabeca, int id) {
    Documento *atual = *cabeca;
    Documento *anterior = NULL;

    while (atual != NULL && atual->id != id) {
        anterior = atual;
        atual = atual->proximo;
    }

    if (atual == NULL) {          
        return 0;
    }

    if (anterior == NULL) {       
        *cabeca = atual->proximo;
    } else {                      
        anterior->proximo = atual->proximo;
    }

    free(atual);                  
    return 1;
}

void excluir_documento(Documento **cabeca) {
    if (*cabeca == NULL) {
        printf("Nenhum documento cadastrado.\n");
        return;
    }

    printf("\nPrimeiro, localize o documento que deseja excluir.\n");
    pesquisar_documentos(*cabeca);

    printf("\nDigite o ID do documento a excluir (0 para cancelar): ");
    int id = ler_inteiro();
    while (id < 0) {
        printf("ERRO (digite um numero)\n");
        printf("Tente novamente: ");
        id = ler_inteiro();
    }
    if (id == 0) {
        printf("Exclusao cancelada.\n");
        return;
    }

    Documento *doc = buscar_por_id(*cabeca, id);
    if (doc == NULL) {
        printf("Nenhum documento encontrado com o ID %d.\n", id);
        return;
    }

    printf("\nDocumento selecionado:\n");
    imprimir_lista(doc);
    printf("\nTem certeza que deseja excluir? (S/N): ");
    char resposta[50];
    ler_string(resposta, 50);

    while (!((resposta[0] == 'S' || resposta[0] == 's' ||
              resposta[0] == 'N' || resposta[0] == 'n') && resposta[1] == '\0')) {
        printf("ERRO (digite S ou N)\n");
        printf("Tente novamente: ");
        ler_string(resposta, 50);
    }

    if (resposta[0] == 'N' || resposta[0] == 'n') {
        printf("Exclusao cancelada.\n");
        return;
    }

    if (remover_por_id(cabeca, id)) {
        printf("Documento excluido com sucesso.\n");
    }
}

/* ---------------------------------------------------------
   ORDENAR
   --------------------------------------------------------- */

int comparar_titulares(char *a, char *b) {
    char a_min[100];
    char b_min[100];

    para_minusculo(a, a_min);
    para_minusculo(b, b_min);
    return strcmp(a_min, b_min);
}

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

void ordenar_documentos(Documento **cabeca) {
    if (*cabeca == NULL) {
        printf("Nenhum documento cadastrado.\n");
        return;
    }

    printf("\nOrdenar por:\n");
    printf("(1) Tipo de documento (RG, CPF, CNH...)\n");
    printf("(2) Nome do titular (A-Z)\n");
    printf("(3) ID (ordem de cadastro)\n");
    printf("(0) Voltar\n");
    printf("Escolha uma opcao: ");
    int criterio = ler_inteiro();

    while (criterio < 0 || criterio > 3) {
        printf("ERRO (opcao invalida)\n");
        printf("Tente novamente: ");
        criterio = ler_inteiro();
    }

    if (criterio == 0) {
        return;
    }

    ordenar_lista(cabeca, criterio);
    printf("\nLista ordenada:\n");
    listar_todos(*cabeca);
}

/* ---------------------------------------------------------
   INDICADORES
   --------------------------------------------------------- */

void exibir_indicadores(Documento *cabeca) {
    if (cabeca == NULL) {
        printf("Nenhum documento cadastrado.\n");
        return;
    }

    int total = 0;
    int por_tipo[6] = {0};
    int por_categoria[5] = {0};

    Documento *atual = cabeca;
    while (atual != NULL) {
        total++;
        por_tipo[atual->tipo]++;
        por_categoria[atual->categoria]++;
        atual = atual->proximo;
    }

    printf("\nTotal de documentos: %d\n", total);

    printf("\nPor tipo:\n");
    for (int i = 0; i < 6; i++) {
        printf("  %s: %d\n", TIPOS[i], por_tipo[i]);
    }

    printf("\nPor categoria:\n");
    for (int i = 0; i < 5; i++) {
        printf("  %s: %d\n", CATEGORIAS[i], por_categoria[i]);
    }

    printf("\nPor titular:\n");
    atual = cabeca;
    while (atual != NULL) {
        int ja_contado = 0;
        Documento *anterior = cabeca;
        while (anterior != atual) {
            if (strcmp(anterior->titular, atual->titular) == 0) {
                ja_contado = 1;
                break;
            }
            anterior = anterior->proximo;
        }

        if (!ja_contado) {
            int quantidade = 0;
            Documento *busca = atual;
            while (busca != NULL) {
                if (strcmp(busca->titular, atual->titular) == 0) {
                    quantidade++;
                }
                busca = busca->proximo;
            }
            printf("  %s: %d\n", atual->titular, quantidade);
        }

        atual = atual->proximo;
    }
}


int main() {
    Documento *cabeca = NULL;  
    int opcao;

    do {
        printf("\n=== CITIZEN ASSIST AI ===\n");
        printf("(1) Cadastrar \n");
        printf("(2) Pesquisar (titular / tipo / ID)\n");
        printf("(3) Atualizar \n");
        printf("(4) Excluir \n");
        printf("(5) Listar \n");
        printf("(6) Ordenar \n");
        printf("(7) Indicadores\n");
        printf("(0) Sair \n");
        printf("Escolha uma opcao: ");
        opcao = ler_inteiro();

        switch (opcao) {
            case 1:
                printf("\n== NOVO CADASTRO ==");
                cadastrar_documento(&cabeca);
                break;
            case 2:
                printf("\n== PESQUISAR ==\n");
                pesquisar_documentos(cabeca);
                break;
            case 3:
                printf("\n== ATUALIZAR ==\n");
                atualizar_documento(cabeca);
                break;
            case 4:
                printf("\n== EXCLUIR ==\n");
                excluir_documento(&cabeca);
                break;
            case 5:
                printf("\n== LISTAR ==\n");
                listar_todos(cabeca);   
                break;
            case 6:
                printf("\n== ORDENAR ==\n");
                ordenar_documentos(&cabeca);
                break;
            case 7:
                printf("\n== INDICADORES ==\n");
                exibir_indicadores(cabeca);
                break;
            case 0:
                printf("Encerrando...\n");
                break;
            default:
                printf("Opcao invalida. Por favor, tente novamente.\n");
        }
    } while (opcao != 0);

    liberar_lista(&cabeca);   
    return 0;
}
