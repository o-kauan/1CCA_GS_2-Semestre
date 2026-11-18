import textwrap

AVISO = "Aviso: este assistente NÃO é um canal oficial. Confirme a informação no órgão responsável."


class Orientacao:
    """Guarda os dados de uma orientação e se exibe na tela."""

    CAMPOS_OBRIGATORIOS = ("id", "categoria", "titulo", "palavras_chave", "resposta",
                           "documentos", "onde", "fonte", "verificado_em")

    def __init__(self, id, categoria, titulo, palavras_chave, resposta,
                 documentos, onde, fonte, verificado_em,
                 exige_presenca=True, alternativa_remota=""):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave # lista de strings
        self.resposta = resposta
        self.documentos = documentos # lista de strings
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em
        # módulo "Vale a viagem?":
        self.exige_presenca = exige_presenca # True = precisa ir; False = dá para resolver à distância
        self.alternativa_remota = alternativa_remota

    @classmethod
    def de_dicionario(cls, dados):
        if not isinstance(dados, dict):
            raise ValueError("o registro não é um dicionário")
        faltando = [campo for campo in cls.CAMPOS_OBRIGATORIOS if campo not in dados]
        if faltando:
            raise ValueError("faltam os campos: " + ", ".join(faltando))
        if not isinstance(dados["palavras_chave"], list) or not isinstance(dados["documentos"], list):
            raise ValueError("'palavras_chave' e 'documentos' devem ser listas")
        return cls(
            id=dados["id"],
            categoria=dados["categoria"],
            titulo=dados["titulo"],
            palavras_chave=dados["palavras_chave"],
            resposta=dados["resposta"],
            documentos=dados["documentos"],
            onde=dados["onde"],
            fonte=dados["fonte"],
            verificado_em=dados["verificado_em"],
            exige_presenca=bool(dados.get("exige_presenca", True)),
            alternativa_remota=dados.get("alternativa_remota", ""),
        )

    def exibir(self):
        """Mostra a orientação na tela: resposta, documentos, onde, fonte, data e aviso..."""
        print(f"\n>> {self.titulo} [{self.categoria}]")
        print(textwrap.fill(self.resposta, width=90))
        print("Documentos necessários:")
        if self.documentos:
            for documento in self.documentos:
                print(textwrap.fill(f"- {documento}", width=90, initial_indent="  ",
                                    subsequent_indent="    "))
        else:
            print("  - Nenhum documento específico")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print(AVISO)