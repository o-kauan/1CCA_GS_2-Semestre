"""Conversa com o cidadão, guarda o histórico e calcula os indicadores."""

import csv
import json
import os
import shutil
import time
from datetime import datetime

from base_conhecimento import LIMIAR_ALTA, LIMIAR_MEDIA

CAMPOS_CSV = ["data", "origem", "pergunta", "id_orientacao", "encontrou", "ajudou",
              "tentativas", "tempo_segundos", "viagem_evitada", "sessao", "nota_facilidade"]

def _entrada(mensagem):
    try:
        return input(mensagem).strip()
    except EOFError:
        return None

def ler_texto(mensagem):
    """Lê um texto. Se a entrada fechar, devolve '0' (voltar)."""
    texto = _entrada(mensagem)
    return "0" if texto is None else texto

def ler_sn(mensagem):
    while True:
        resposta = _entrada(mensagem)
        if resposta is None:
            return False
        resposta = resposta.lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Entrada inválida. Digite s (sim) ou n (não).")


def ler_opcao(mensagem, minimo, maximo, se_acabar_a_entrada=0):
    while True:
        resposta = _entrada(mensagem)
        if resposta is None:
            return se_acabar_a_entrada
        try:
            valor = int(resposta)
        except ValueError:
            print(f"Opção inválida. Digite um número de {minimo} a {maximo}.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"Opção fora da faixa. Digite um número de {minimo} a {maximo}.")


def contem_dado_pessoal(texto):
    """Bloqueia as respostas de 8 ou mais dígitos (CPF, telefone...) ou o sinal @ (e-mail)."""
    quantidade_de_digitos = sum(1 for caractere in texto if caractere.isdigit())
    return quantidade_de_digitos >= 8 or "@" in texto


# Lógica booleana do "Vale a viagem?" que pegamos da matéria Computer Science
# Toda a lógica foi construida no desafio proposto da matéria, desde as variaveis booleanas até o mapa de karnaught
# O assunto e a lógica cabem perfeitamente na nossa ideia principal do projeto Bridge AI
# Se quiser saber mais, está explicando no nosso README

def regra_vale_a_viagem(P, D, U):
    """S = P · (D + U)
    P = o serviço exige presença?   D = você tem todos os documentos?   U = o caso é urgente?
    Vale a viagem (S = 1) quando exige presença E (tem os documentos OU é urgente)."""
    return int(bool(P) and (bool(D) or bool(U)))


# Assistente

class Assistente:
    def __init__(self, nome, base, caminho_historico="data/historico.json",
                 caminho_csv="data/atendimentos.csv"):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.caminho_csv = caminho_csv
        self.sessao = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # identifica esta execução
        self.atendimentos_da_sessao = 0
        self.historico = self._carregar_historico()

    def _carregar_historico(self):
        """le data/historico.json"""
        try:
            with open(self.caminho_historico, encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError("o histórico deve ser uma lista")
            return [item for item in dados if isinstance(item, dict)]
        except FileNotFoundError:
            return []
        except (ValueError, OSError) as erro:
            print(f"Aviso: o histórico não pôde ser lido ({erro}). Começando um histórico novo.")
            try:
                shutil.copyfile(self.caminho_historico, self.caminho_historico + ".bak")
            except OSError:
                pass
            return []

    def _salvar_historico(self):
        try:
            pasta = os.path.dirname(self.caminho_historico)
            if pasta:
                os.makedirs(pasta, exist_ok=True)
            with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)
        except OSError as erro:
            print(f"Aviso: não foi possível salvar o histórico ({erro}).")

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou,
                  tentativas, tempo, viagem_evitada):
        """guarda um atendimento em data/historico.json"""
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo,
            "viagem_evitada": viagem_evitada, # True / False / None (se não encontrou)
            "sessao": self.sessao,
            "nota_facilidade": None, # preenchida ao sair, ajuda na avaliacao do projeto
        }
        self.historico.append(atendimento)
        self.atendimentos_da_sessao += 1
        self._salvar_historico()

    def perguntar(self):
        inicio = time.time()
        tentativas = 0
        ultima_pergunta = ""

        while True:
            texto = ler_texto("\nDigite sua dúvida (0 para voltar): ")

            if texto == "0":
                if tentativas > 0:   # a pessoa tentou e desistiu: registra como não resolvida
                    self.registrar("pergunta", ultima_pergunta, None, False, False,
                                   tentativas, round(time.time() - inicio, 1), None)
                return
            if texto == "":
                print("  Resposta vazia. Escreva sua dúvida ou digite 0 para voltar.")
                continue
            if contem_dado_pessoal(texto):
                # Não conta como tentativa e NÃO é registrada no sistema
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            ultima_pergunta = texto
            resultados = self.base.buscar(texto) # lista de tuplas (pontos, orientacao)

            if not resultados or resultados[0][0] < LIMIAR_MEDIA:
                self._mostrar_nao_encontrei()
                continue

            pontos, orientacao = resultados[0]
            confianca = "ALTA" if pontos >= LIMIAR_ALTA else "MÉDIA"
            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
            alternativas = [t for t in resultados[1:3] if t[0] >= LIMIAR_MEDIA]
            self._apresentar(orientacao, "pergunta", texto, tentativas, inicio, alternativas)
            return

    def _mostrar_nao_encontrei(self):
        print("\nNão encontrei uma orientação para essa dúvida.")
        exemplos = [o.palavras_chave[0] for o in self.base.orientacoes[:3] if o.palavras_chave]
        if exemplos:
            print("Tente outras palavras, por exemplo: " + ", ".join(f"'{e}'" for e in exemplos) + ".")
        print("Ou use a navegação por categorias (opção 2 do menu): " + ", ".join(self.base.categorias()) + ".")


    # navegação por categorias

    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("A base de conhecimento está vazia.")
            return
        while True:
            print("\nCategorias:")
            for numero, categoria in enumerate(categorias, start=1):
                print(f"  {numero}. {categoria}")
            print("  0. Voltar")
            escolha = ler_opcao("Escolha uma categoria: ", 0, len(categorias))
            if escolha == 0:
                return
            self._navegar_categoria(categorias[escolha - 1])

    def _navegar_categoria(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        while True:
            inicio = time.time()
            print(f"\n{categoria}:")
            for numero, orientacao in enumerate(orientacoes, start=1):
                print(f"  {numero}. {orientacao.titulo}")
            print("  0. Voltar")
            escolha = ler_opcao("Escolha uma orientação: ", 0, len(orientacoes))
            if escolha == 0:
                return
            orientacao = orientacoes[escolha - 1]
            self._apresentar(orientacao, "categoria", f"[{categoria}] {orientacao.titulo}", 1, inicio, [])

    def _apresentar(self, orientacao, origem, pergunta, tentativas, inicio, alternativas):
        tempo = round(time.time() - inicio, 1)   # tempo até a orientação aparecer
        orientacao.exibir()
        if alternativas:
            print("\nOutras orientações parecidas:")
            for pontos, outra in alternativas:
                print(f"  - {outra.titulo} ({pontos} pontos)")
        viagem_evitada = self.vale_a_viagem(orientacao)
        ajudou = ler_sn("\nEssa orientação respondeu sua dúvida? (s/n): ")
        self.registrar(origem, pergunta, orientacao.id, True, ajudou, tentativas, tempo, viagem_evitada)
        if not ajudou:
            print("Tente reescrever a dúvida com outras palavras ou use a navegação por categorias.")

    def vale_a_viagem(self, orientacao):
        """Irá devolver True se a viagem foi evitada."""
        print("\n--- Vale a viagem? ---")
        P = orientacao.exige_presenca
        if not P:
            print("Não precisa ir: dá para resolver à distância.")
            if orientacao.alternativa_remota:
                print(f"Faça por: {orientacao.alternativa_remota}")
            return True

        print("Este serviço exige presença. Responda para saber se já vale ir:")
        D = ler_sn("Você tem todos os documentos listados acima? (s/n): ")
        U = ler_sn("O caso é urgente (prazo vencendo)? (s/n): ")
        if regra_vale_a_viagem(P, D, U):
            print(f"Vale a viagem. Vá a: {orientacao.onde}")
            if not D:
                print("Como faltam documentos, leve o que tiver e confirme antes no órgão responsável.")
            return False
        print("Não vá ainda: reúna os documentos antes de se deslocar, para não perder a viagem.")
        return True

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("Ainda não há atendimentos registrados.")
            return {}

        encontrados = [r for r in self.historico if r.get("encontrou")]
        ajudaram = [r for r in self.historico if r.get("ajudou")]
        tempos = [r["tempo_segundos"] for r in encontrados if isinstance(r.get("tempo_segundos"), (int, float))]
        tentativas = [r["tentativas"] for r in self.historico if isinstance(r.get("tentativas"), (int, float))]

        notas_por_sessao = {}
        for r in self.historico:
            if r.get("nota_facilidade") is not None:
                notas_por_sessao[r.get("sessao")] = r["nota_facilidade"]
        notas = list(notas_por_sessao.values())

        com_viagem = [r for r in self.historico if r.get("viagem_evitada") is not None]
        evitadas = [r for r in com_viagem if r["viagem_evitada"]]

        sem_solucao = []
        for r in self.historico:
            if (not r.get("encontrou") or not r.get("ajudou")) and r.get("pergunta"):
                motivo = "não encontrada" if not r.get("encontrou") else "não ajudou"
                linha = f"{r['pergunta']} ({motivo})"
                if linha not in sem_solucao:
                    sem_solucao.append(linha)

        resultado = {
            "total": total,
            "encontrada_pct": round(100 * len(encontrados) / total, 1),
            "acerto_pct": round(100 * len(ajudaram) / total, 1),
            "tempo_medio": round(sum(tempos) / len(tempos), 1) if tempos else None,
            "tentativas_media": round(sum(tentativas) / len(tentativas), 2) if tentativas else None,
            "facilidade_media": round(sum(notas) / len(notas), 2) if notas else None,
            "viagens_evitadas_pct": round(100 * len(evitadas) / len(com_viagem), 1) if com_viagem else None,
            "sem_solucao": sem_solucao,
        }

        print("\n===== Indicadores =====")
        print(f"Atendimentos registrados: {resultado['total']}")
        print(f"Resposta encontrada: {resultado['encontrada_pct']}%")
        print(f"Taxa de acerto (a pessoa disse que ajudou): {resultado['acerto_pct']}%")
        print("Tempo médio para encontrar: "
              + (f"{resultado['tempo_medio']} s" if tempos else "sem dados"))
        print(f"Tentativas por atendimento: {resultado['tentativas_media']}")
        print("Facilidade de uso (1 a 5): "
              + (f"{resultado['facilidade_media']} ({len(notas)} nota(s))" if notas else "sem notas ainda"))
        print("Orientações que evitaram uma viagem: "
              + (f"{resultado['viagens_evitadas_pct']}%" if com_viagem else "sem dados"))
        print("Dúvidas sem solução:")
        if sem_solucao:
            for linha in sem_solucao:
                print(f"  - {linha}")
        else:
            print("  (nenhuma)")
        return resultado

    def exportar_csv(self):
        if not self.historico:
            print("Ainda não há atendimentos para exportar.")
            return False
        try:
            pasta = os.path.dirname(self.caminho_csv)
            if pasta:
                os.makedirs(pasta, exist_ok=True)
            with open(self.caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV, extrasaction="ignore")
                escritor.writeheader()
                for registro in self.historico:
                    linha = dict(registro)
                    for campo in ("encontrou", "ajudou", "viagem_evitada"):
                        valor = linha.get(campo)
                        linha[campo] = "" if valor is None else ("s" if valor else "n")
                    escritor.writerow(linha)
        except OSError as erro:
            print(f"Não foi possível exportar o CSV ({erro}).")
            return False
        print(f"CSV exportado com {len(self.historico)} atendimento(s): {self.caminho_csv}")
        return True

    # saída

    def encerrar(self):
        if self.atendimentos_da_sessao > 0:
            nota = ler_opcao("\nDê uma nota de facilidade de uso, de 1 (difícil) a 5 (muito fácil): ",
                             1, 5, se_acabar_a_entrada=None)
            if nota is not None:
                for registro in self.historico:
                    if registro.get("sessao") == self.sessao:
                        registro["nota_facilidade"] = nota
                self._salvar_historico()
        print("Obrigado por usar o Bridge AI. Lembre-se: este assistente não é um canal oficial.")