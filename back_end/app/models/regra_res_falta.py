from dataclasses import dataclass
from datetime import date, timedelta

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
    if not recentes: return RegraRes("percentual_faltas", False, 0.0, "Nenhum registro encontrado.")
    faltas: int = sum(1 for r in recentes if not r["presente"] or r["justificada"])
    percentual = faltas / len(recentes)
    
    return RegraRes(
        nome="percentual_faltas",
        disparada=(percentual >= lim),
        peso=percentual,
        detalhe=f"{faltas} faltas de {len(recentes)} aulas ({percentual:.2%})",
        data_ocorrida=max(r["data"] for r in recentes)
    )