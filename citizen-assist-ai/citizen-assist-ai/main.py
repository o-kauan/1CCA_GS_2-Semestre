"""Bridge AI (Citizen Assist AI)"""

import os

from assistente import Assistente, ler_opcao
from base_conhecimento import BaseConhecimento

PASTA = os.path.dirname(os.path.abspath(__file__))

def caminho(*partes):
    return os.path.join(PASTA, *partes)

def main():
    base = BaseConhecimento(caminho("data", "base_conhecimento.json"))
    if not base.carregar(): # lê o JSON e cria os objetos Orientacao
        print("O assistente não pode iniciar sem a base de conhecimento. "
              "Confira o arquivo data/base_conhecimento.json.")
        return

    assistente = Assistente("Bridge AI", base,
                            caminho("data", "historico.json"),
                            caminho("data", "atendimentos.csv"))

    print("=" * 62)
    print(f" {assistente.nome} - orientação para quem vive no campo")
    print(" Responde dúvidas com informações de fontes oficiais.")
    print(" Este assistente NÃO é um canal oficial e NÃO guarda dados pessoais.")
    print("=" * 62)

    while True:
        print("\nMenu")
        print("  1. Perguntar (digitar sua dúvida)")
        print("  2. Navegar por categorias")
        print("  3. Ver indicadores")
        print("  4. Exportar atendimentos para CSV")
        print("  0. Sair")
        opcao = ler_opcao("Escolha uma opção: ", 0, 4)

        if opcao == 1:
            assistente.perguntar()
        elif opcao == 2:
            assistente.navegar()
        elif opcao == 3:
            assistente.indicadores()
        elif opcao == 4:
            assistente.exportar_csv()
        else:
            assistente.encerrar()
            break

if __name__ == "__main__":
    main()
