"""Bridge AI Energy - Energia e Sustentabilidade (Global Solution 2026.2)

Modelo comparativo para uma propriedade rural: motobomba a combustao,
bombeamento solar direto e sistema fotovoltaico hibrido com bateria.

Execucao: python calculos_comparacao_atualizado.py

[FONTE] = dado apoiado em fonte publica indicada no relatorio.
[EST]   = estimativa de caso-modelo, a validar localmente.

Os resultados sao estimativas, nao substituem projeto eletrico/hidraulico,
medicao da propriedade, orcamentos ou simulacao de bateria.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Optional

# ---------------------------------------------------------------------------
# 1. PREMISSAS DO CASO-MODELO
# ---------------------------------------------------------------------------
DIAS_MES = 30
G = 9.81
RHO = 1000.0

# Demanda de agua [EST]
VOLUME_DIA_M3 = 3.0
ALTURA_MANOMETRICA_M = 40.0
RENDIMENTO_GLOBAL_BOMBA = 0.35

# Consumo residencial [EST]
CONSUMO_CASA_KWH_MES = 150.0

# Precos usados no cenario [EST]/[FONTE]
TARIFA_KWH = 0.95  # R$/kWh 
PRECO_GASOLINA = 6.53  # R$/L
PRECO_DIESEL_S10 = 6.90  # R$/L

# Custo minimo equivalente usado no modelo (monofasico) [FONTE/EST]
CUSTO_DISPONIBILIDADE_EQUIV_KWH = 30.0

# Alternativa A - motobomba a combustao [EST]
HORAS_MOTOBOMBA_DIA = 1.0
CONSUMO_GASOLINA_L_H = 0.9  # motobomba aproximada de 2 cv
CONSUMO_DIESEL_L_H = 0.7    # motobomba aproximada de 3 cv
MANUTENCAO_COMBUSTAO_MES = 35.0
TROCA_MOTOBOMBA_5_ANOS = 1800.0
PERDAS_QUEDAS_MES = 20.0

# Alternativa B - bombeamento solar direto, sem bateria [EST]
POTENCIA_B_KWP = 1.1  # 2 modulos de aproximadamente 550 Wp
INVEST_B = 9100.0
MANUT_B_MES = 10.0

# Alternativa C - sistema solar hibrido residencial [EST]
POTENCIA_C_KWP = 2.2
HSP = 4.5
PERFORMANCE_RATIO = 0.75
INVEST_C_ITENS: Dict[str, float] = {
    "Modulos FV 4 x 550 Wp (2,2 kWp)": 3300.0,
    "Inversor hibrido 3 kW": 6000.0,
    "Bateria LFP 5 kWh": 8500.0,
    "Estrutura, cabos e protecoes": 2500.0,
    "Bomba 0,5 cv e caixa d'agua 1.000 L": 1900.0,
    "Instalacao, mao de obra e projeto": 3500.0,
}
INVEST_C = sum(INVEST_C_ITENS.values())
FRACAO_CASA_REDE = 0.20  # 20% do consumo residencial ainda vem da rede [EST]
MANUT_C_MES = 15.0

# Reajustes anuais do cenario com inflacao [EST]
REAJUSTE_ENERGIA = 0.06
REAJUSTE_COMBUSTIVEL = 0.04

# Fatores de emissao [FONTE]/[EST]
FE_REDE_KG_CO2_KWH = 0.0385  # 38,5 kg/MWh; fator medio SIN de 2023 [FONTE]
FE_GASOLINA_KG_CO2_L = 1.6   # parcela fossil aproximada da gasolina C [EST]
FE_DIESEL_KG_CO2_L = 2.3     # parcela fossil aproximada do diesel B [EST]
FE_FV_CICLO_VIDA_KG_CO2_KWH = 0.045  # ponto medio de faixa indicativa 40-50 g/kWh [EST]


# ---------------------------------------------------------------------------
# 2. FUNCOES DE CALCULO
# ---------------------------------------------------------------------------
def arredondar_brl(valor: float) -> int:
    """Arredonda valores monetarios para inteiro pelo criterio comercial."""
    return int(Decimal(str(valor)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def energia_hidraulica_kwh_dia() -> float:
    """Energia potencial da agua: rho*g*H*V, convertida para kWh."""
    return RHO * G * ALTURA_MANOMETRICA_M * VOLUME_DIA_M3 / 3_600_000.0


def energia_bomba_kwh_dia() -> float:
    return energia_hidraulica_kwh_dia() / RENDIMENTO_GLOBAL_BOMBA


def geracao_fv_kwh_mes(kwp: float, hsp: float = HSP, pr: float = PERFORMANCE_RATIO) -> float:
    return kwp * hsp * pr * DIAS_MES


def custo_mensal_A(combustivel: str = "gasolina") -> Dict[str, float]:
    if combustivel == "gasolina":
        litros = HORAS_MOTOBOMBA_DIA * CONSUMO_GASOLINA_L_H * DIAS_MES
        preco = PRECO_GASOLINA
    elif combustivel == "diesel":
        litros = HORAS_MOTOBOMBA_DIA * CONSUMO_DIESEL_L_H * DIAS_MES
        preco = PRECO_DIESEL_S10
    else:
        raise ValueError("Combustivel deve ser 'gasolina' ou 'diesel'.")

    custo_combustivel = litros * preco
    custo_rede = CONSUMO_CASA_KWH_MES * TARIFA_KWH
    total = custo_combustivel + MANUTENCAO_COMBUSTAO_MES + custo_rede + PERDAS_QUEDAS_MES
    return {
        "litros": litros,
        "combustivel": custo_combustivel,
        "manutencao": MANUTENCAO_COMBUSTAO_MES,
        "rede": custo_rede,
        "perdas": PERDAS_QUEDAS_MES,
        "total": total,
    }


def custo_mensal_B() -> Dict[str, float]:
    # A casa permanece na rede e continua sujeita as perdas por interrupcao.
    custo_rede = CONSUMO_CASA_KWH_MES * TARIFA_KWH
    total = custo_rede + PERDAS_QUEDAS_MES + MANUT_B_MES
    return {"rede": custo_rede, "perdas": PERDAS_QUEDAS_MES,
            "manutencao": MANUT_B_MES, "total": total}


def custo_mensal_C() -> Dict[str, float]:
    # O modelo adota 20% da energia residencial importada da rede (30 kWh).
    # A cobranca real depende do enquadramento e das regras atuais do SCEE.
    rede_kwh_modelada = max(
        CONSUMO_CASA_KWH_MES * FRACAO_CASA_REDE,
        CUSTO_DISPONIBILIDADE_EQUIV_KWH,
    )
    custo_rede = rede_kwh_modelada * TARIFA_KWH
    total = custo_rede + MANUT_C_MES
    return {"rede_kwh_modelada": rede_kwh_modelada,
            "rede": custo_rede, "manutencao": MANUT_C_MES, "total": total}


def payback_meses(
    investimento: float,
    economia_fixa: float,
    economia_combustivel: float = 0.0,
    economia_energia: float = 0.0,
    com_reajuste: bool = False,
    limite: int = 240,
) -> Optional[int]:
    acumulado = 0.0
    for mes in range(limite):
        ano = mes // 12
        fator_combustivel = (1 + REAJUSTE_COMBUSTIVEL) ** ano if com_reajuste else 1.0
        fator_energia = (1 + REAJUSTE_ENERGIA) ** ano if com_reajuste else 1.0
        acumulado += (
            economia_fixa
            + economia_combustivel * fator_combustivel
            + economia_energia * fator_energia
        )
        if acumulado >= investimento:
            return mes + 1
    return None


def custo_acumulado(
    meses: int,
    custo_fixo_mensal: float,
    combustivel_mensal: float,
    energia_mensal: float,
    investimento: float = 0.0,
    extra: float = 0.0,
    com_reajuste: bool = False,
) -> float:
    total = investimento + extra
    for mes in range(meses):
        ano = mes // 12
        fator_energia = (1 + REAJUSTE_ENERGIA) ** ano if com_reajuste else 1.0
        fator_combustivel = (1 + REAJUSTE_COMBUSTIVEL) ** ano if com_reajuste else 1.0
        total += (
            custo_fixo_mensal
            + combustivel_mensal * fator_combustivel
            + energia_mensal * fator_energia
        )
    return total


def emissao_mensal_kg_co2(cenario: str, combustivel: str = "gasolina") -> float:
    energia_bomba_mes = energia_bomba_kwh_dia() * DIAS_MES
    if cenario == "A":
        a = custo_mensal_A(combustivel)
        fator = FE_GASOLINA_KG_CO2_L if combustivel == "gasolina" else FE_DIESEL_KG_CO2_L
        return a["litros"] * fator + CONSUMO_CASA_KWH_MES * FE_REDE_KG_CO2_KWH
    if cenario == "B":
        return (
            CONSUMO_CASA_KWH_MES * FE_REDE_KG_CO2_KWH
            + energia_bomba_mes * FE_FV_CICLO_VIDA_KG_CO2_KWH
        )
    if cenario == "C":
        c = custo_mensal_C()
        energia_fv_modelada = (
            CONSUMO_CASA_KWH_MES * (1 - FRACAO_CASA_REDE) + energia_bomba_mes
        )
        return (
            c["rede_kwh_modelada"] * FE_REDE_KG_CO2_KWH
            + energia_fv_modelada * FE_FV_CICLO_VIDA_KG_CO2_KWH
        )
    raise ValueError("Cenario deve ser A, B ou C.")


# ---------------------------------------------------------------------------
# 3. RELATORIO NO TERMINAL
# ---------------------------------------------------------------------------
def main() -> None:
    a_gas = custo_mensal_A("gasolina")
    a_diesel = custo_mensal_A("diesel")
    b = custo_mensal_B()
    c = custo_mensal_C()

    bomba_dia = energia_bomba_kwh_dia()
    demanda_total_mes = CONSUMO_CASA_KWH_MES + bomba_dia * DIAS_MES
    geracao_b = geracao_fv_kwh_mes(POTENCIA_B_KWP)
    geracao_c = geracao_fv_kwh_mes(POTENCIA_C_KWP)

    economia_b = a_gas["total"] - b["total"]
    economia_c = a_gas["total"] - c["total"]

    print("=== ENERGIA E DEMANDA ===")
    print(f"Energia hidraulica: {energia_hidraulica_kwh_dia():.3f} kWh/dia")
    print(f"Energia eletrica estimada da bomba: {bomba_dia:.3f} kWh/dia; "
          f"{bomba_dia * DIAS_MES:.1f} kWh/mes")
    print(f"Demanda total (casa + bomba): {demanda_total_mes:.1f} kWh/mes")
    print(f"Geracao teorica B (1,1 kWp): {geracao_b:.1f} kWh/mes; "
          "nao significa energia armazenada ou disponivel fora do sol")
    print(f"Geracao teorica C (2,2 kWp): {geracao_c:.1f} kWh/mes")
    print(f"Investimento B: R$ {arredondar_brl(INVEST_B):,}")
    print(f"Investimento C: R$ {arredondar_brl(INVEST_C):,}")

    print("\n=== CUSTO MENSAL ===")
    for label, dados in (("A gasolina", a_gas), ("A diesel", a_diesel), ("B solar direto", b), ("C hibrido", c)):
        print(f"{label:16s}: R$ {arredondar_brl(dados['total']):,} "
              f"(valor sem arredondar: R$ {dados['total']:.2f})")
    print(f"Economia mensal B vs A gasolina: R$ {arredondar_brl(economia_b):,}")
    print(f"Economia mensal C vs A gasolina: R$ {arredondar_brl(economia_c):,}")

    pb_b = payback_meses(INVEST_B, economia_b)
    pb_c = payback_meses(INVEST_C, economia_c)
    pb_b_reaj = payback_meses(
        INVEST_B,
        a_gas["manutencao"] - MANUT_B_MES,
        a_gas["combustivel"],
        0.0,
        com_reajuste=True,
    )
    pb_c_reaj = payback_meses(
        INVEST_C,
        (a_gas["manutencao"] + a_gas["perdas"]) - MANUT_C_MES,
        a_gas["combustivel"],
        a_gas["rede"] - c["rede"],
        com_reajuste=True,
    )
    print("\n=== PAYBACK SIMPLES ===")
    print(f"B: {pb_b} meses ({pb_b / 12:.1f} anos); com reajustes: "
          f"{pb_b_reaj} meses ({pb_b_reaj / 12:.1f} anos)")
    print(f"C: {pb_c} meses ({pb_c / 12:.1f} anos); com reajustes: "
          f"{pb_c_reaj} meses ({pb_c_reaj / 12:.1f} anos)")

    print("\n=== CUSTO ACUMULADO (A gasolina, B e C) ===")
    for meses, rotulo in ((1, "1 mes"), (12, "1 ano"), (60, "5 anos"), (120, "10 anos")):
        for reajuste in (False, True):
            a_total = custo_acumulado(
                meses,
                a_gas["manutencao"] + a_gas["perdas"],
                a_gas["combustivel"],
                a_gas["rede"],
                extra=TROCA_MOTOBOMBA_5_ANOS if meses >= 60 else 0.0,
                com_reajuste=reajuste,
            )
            b_total = custo_acumulado(
                meses,
                b["manutencao"] + b["perdas"],
                0.0,
                b["rede"],
                investimento=INVEST_B,
                com_reajuste=reajuste,
            )
            c_total = custo_acumulado(
                meses,
                c["manutencao"],
                0.0,
                c["rede"],
                investimento=INVEST_C,
                com_reajuste=reajuste,
            )
            rotulo_reaj = "com reajuste" if reajuste else "sem reajuste"
            print(f"{rotulo:8s} | {rotulo_reaj:13s} | "
                  f"A R$ {arredondar_brl(a_total):,} | "
                  f"B R$ {arredondar_brl(b_total):,} | "
                  f"C R$ {arredondar_brl(c_total):,}")

    print("\nSensibilidade: se a bateria de R$ 8.500 for substituida dentro dos 10 anos:")
    for reajuste in (False, True):
        c10 = custo_acumulado(
            120, c["manutencao"], 0.0, c["rede"],
            investimento=INVEST_C, com_reajuste=reajuste,
        )
        print(f"C em 10 anos + bateria: R$ {arredondar_brl(c10 + 8500.0):,} "
              f"({'com' if reajuste else 'sem'} reajuste)")

    print("\n=== SENSIBILIDADE DE GERACAO FOTOVOLTAICA (C) ===")
    for hsp in (4.0, 4.5, 5.0, 5.5):
        print(f"HSP {hsp:.1f}: {geracao_fv_kwh_mes(POTENCIA_C_KWP, hsp):.1f} kWh/mes")

    print("\n=== EMISSOES INDICATIVAS (kg CO2/mes) ===")
    emissoes = {
        "A gasolina": emissao_mensal_kg_co2("A", "gasolina"),
        "A diesel": emissao_mensal_kg_co2("A", "diesel"),
        "B": emissao_mensal_kg_co2("B"),
        "C": emissao_mensal_kg_co2("C"),
    }
    for nome, valor in emissoes.items():
        print(f"{nome:12s}: {valor:.2f} kg/mes; {valor * 12:.1f} kg/ano")
    for baseline in ("A gasolina", "A diesel"):
        for alternativa in ("B", "C"):
            reducao = emissoes[baseline] - emissoes[alternativa]
            print(f"Reducao {baseline} -> {alternativa}: {reducao:.2f} kg/mes; "
                  f"{reducao * 12:.1f} kg/ano; {reducao * 60 / 1000:.2f} t em 5 anos")

    print("\n=== CENARIO SEM REDE ===")
    litros_gerador = 4.0 * 0.7 * DIAS_MES
    custo_gerador = litros_gerador * PRECO_GASOLINA + 50.0
    total_a2 = a_gas["combustivel"] + a_gas["manutencao"] + custo_gerador
    total_c2 = MANUT_C_MES + 30.0  # reserva estimada para apoio ocasional [EST]
    pb_c2 = payback_meses(INVEST_C + 2500.0, total_a2 - total_c2)
    print(f"Gerador: {litros_gerador:.0f} L/mes; custo com manutencao R$ {custo_gerador:.2f}")
    print(f"A2: R$ {total_a2:.2f}/mes; C2: R$ {total_c2:.2f}/mes")
    print(f"Payback C2: {pb_c2} meses ({pb_c2 / 12:.1f} anos)")
    emissao_combustivel_a2 = (a_gas["litros"] + litros_gerador) * FE_GASOLINA_KG_CO2_L
    print(f"Emissao direta estimada de gasolina em A2 (bomba + gerador): "
          f"{emissao_combustivel_a2:.1f} kg CO2/mes")


if __name__ == "__main__":
    main()
