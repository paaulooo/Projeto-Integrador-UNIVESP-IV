from dataclasses import dataclass
from datetime import date, timedelta
from collections import Counter
@dataclass
class RegraRes:
    nome: str
    disparada: bool
    peso: float
    detalhe: str
    data_ocorrida: date
    
def regra_perc_falta(registros: list[dict], dias: int = 30, lim: float = 0.025) -> RegraRes:
    ### Dispara se as faltas do aluno forem X% do total de aulas
    hoje = date.today()
    inicio: date = hoje - timedelta(days=dias)
    
    recentes = [r for r in registros if r['data'] >= inicio]
    if not recentes: return RegraRes("percentual_faltas", False, 0.0, "Nenhum registro encontrado.", data_ocorrida=hoje)
    faltas: int = sum(1 for r in recentes if not r["presente"] and not r["justificada"])
    percentual = faltas / len(recentes)
    
    return RegraRes(
        nome="percentual_faltas",
        disparada=(percentual >= lim),
        peso=percentual,
        detalhe=f"{faltas} faltas de {len(recentes)} aulas ({percentual:.2%})",
        data_ocorrida=max(r["data"] for r in recentes)
    )
    
def regra_faltas_consecutivas(registros: list[dict], lim: int = 3) -> RegraRes:
    # Dispara se o aluno tiver K ou mais faltas seguidas
    ordenados = sorted(registros, key=lambda r: r["data"])
    if not ordenados: return RegraRes("faltas_consecutivas", False, 0.0, "Nenhum registro encontrado.", data_ocorrida=date.today())

    sequencia_atual = 0
    maior_sequencia = 0

    for r in ordenados:
        if not r["presente"] and not r["justificada"]:
            sequencia_atual += 1
        else:
            maior_sequencia = max(maior_sequencia, sequencia_atual)
            sequencia_atual = 0
    maior_sequencia = max(maior_sequencia, sequencia_atual)

    return RegraRes(
        nome="faltas_consecutivas",
        disparada=(maior_sequencia >= lim),
        peso=float(maior_sequencia),
        detalhe=f"{maior_sequencia} faltas consecutivas",
        data_ocorrida=max(r["data"] for r in ordenados)
    )
    
def regra_identificar_padrão_falta(registros: list[dict]) -> RegraRes:
    # Identifica padrões de faltas (ex: faltas sempre na segunda-feira) WIP
    pass


def calculo_risco(registros: list[dict]) -> dict:
    ### Calcula um score baseado no histórico de faltas
    pass


    
    