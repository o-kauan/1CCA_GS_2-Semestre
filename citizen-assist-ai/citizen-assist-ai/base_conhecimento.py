"""Irá ler o JSON, listar categorias e buscar a melhor orientação por pontuação."""

import json

from orientacao import Orientacao

PONTOS_PALAVRA_CHAVE = 3     # palavra-chave da orientação que aparece na pergunta
PONTOS_PALAVRA_TITULO = 1    # palavra da pergunta (4+ letras) que aparece no título
LIMIAR_ALTA = 6              # 6 pontos ou mais  -> confiança ALTA
LIMIAR_MEDIA = 3             # 3 a 5 pontos      -> confiança MÉDIA ; menos de 3 -> "não encontrei"

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

# Palavras comuns que não ajudam a achar o assunto:
# elas não ganham o ponto extra do título
PALAVRAS_COMUNS = {"como", "para", "fazer", "mais", "anos", "contra", "sobre", "quero",
                   "preciso", "pode", "onde", "qual", "quais", "tenho", "minha", "pelo",
                   "pela", "esse", "essa", "isso", "esta", "este", "isto", "quando"}

def normalizar(texto):
    """Minúsculas, sem acentos e sem pontuação. Devolve com um espaço nas pontas,
    o que permite procurar palavras inteiras com 'in'."""
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "

class BaseConhecimento:

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        """Lê o JSON e cria os objetos Orientacao."""
        self.orientacoes = []
        try:
            with open(self.caminho, encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"Erro: o arquivo da base de conhecimento não foi encontrado ({self.caminho}).")
            return False
        except json.JSONDecodeError as erro:
            print(f"Erro: o arquivo da base está corrompido (linha {erro.lineno}, coluna {erro.colno}).")
            return False
        except (OSError, UnicodeDecodeError) as erro:
            print(f"Erro ao ler a base de conhecimento: {erro}")
            return False

        if not isinstance(dados, list):
            print("Erro: o JSON da base deve ser uma lista de orientações.")
            return False

        for numero, item in enumerate(dados, start=1):
            try:
                self.orientacoes.append(Orientacao.de_dicionario(item))
            except (ValueError, TypeError) as erro:
                print(f"Aviso: o registro {numero} foi ignorado ({erro}).")

        if not self.orientacoes:
            print("Erro: nenhuma orientação válida foi encontrada na base.")
            return False
        return True

    def categorias(self):
        """Lista as categorias na ordem certa, sem repetir."""
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        return lista

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        """Calcula os pontos de UMA orientação para a pergunta."""
        texto = normalizar(pergunta)
        pontos = 0

        # +3 para cada palavra-chave que aparece na pergunta
        for palavra_chave in orientacao.palavras_chave:
            if normalizar(palavra_chave) in texto:
                pontos += PONTOS_PALAVRA_CHAVE

        # +1 para cada palavra da pergunta (4+ letras) que aparece no título
        palavras_do_titulo = set(normalizar(orientacao.titulo).split())
        for palavra in set(texto.split()):
            if len(palavra) >= 4 and palavra not in PALAVRAS_COMUNS and palavra in palavras_do_titulo:
                pontos += PONTOS_PALAVRA_TITULO
        return pontos

    def buscar(self, pergunta):
        """lista de tuplas (pontos, orientacao), da maior para a menor pontuação"""
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        resultados.sort(key=lambda tupla: (-tupla[0], tupla[1].id))  # caso dê empate: menor id primeiro
        return resultados