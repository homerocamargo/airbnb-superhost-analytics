"""Classificador local de referência: regras explícitas, sem API e sem LLM."""
import re
import unicodedata

TEMAS = ["Atendimento", "Limpeza", "Conforto", "Flexibilidade",
         "Localização", "Comodidades", "Custo-benefício"]

PADROES = {
    "Atendimento": [
        r"anfitriao", r"host", r"atencios", r"prestativ", r"solicit",
        r"educad", r"amigav", r"compreensiv", r"ajud", r"great host",
    ],
    "Limpeza": [
        r"limp", r"impecav", r"organiza", r"bem cuidad",
    ],
    "Conforto": [
        r"aconchegant", r"acolhedor", r"confortav", r"tranquil",
        r"ambiente familiar", r"casa boa",
    ],
    "Flexibilidade": [
        r"flexib", r"check.in de madrugada", r"ultima hora",
        r"mesmo dia", r"check.out",
    ],
    "Localização": [
        r"localiz", r"longe da praia", r"perto", r"proxim",
        r"mercado", r"posto de combustivel",
    ],
    "Comodidades": [
        r"garagem", r"internet", r"tudo que precis", r"casa completa",
        r"tinha tudo", r"casa equipada",
    ],
    "Custo-benefício": [
        r"valeu muito a pena", r"custo.beneficio", r"preco", r"valor cobrado",
    ],
}

NEGATIVOS = [r"longe da praia", r"nao gostei", r"ruim", r"sujo",
             r"caro", r"problema", r"pessim"]
POSITIVOS = [r"excelent", r"otim", r"adorei", r"amam", r"amamos",
             r"impecav", r"aconchegant", r"confortav", r"atencios",
             r"prestativ", r"educad", r"great", r"nice", r"voltare",
             r"recomend", r"limp", r"agradavel", r"valeu muito a pena",
             r"boa", r"bom", r"tranquil"]

def normalizar(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", str(texto).lower())
                   if not unicodedata.combining(c))

def classificar(texto):
    base = normalizar(texto)
    temas = []
    evidencias = {}
    for tema, padroes in PADROES.items():
        achados = [p for p in padroes if re.search(p, base)]
        if achados:
            temas.append(tema)
            evidencias[tema] = ", ".join(achados)
    pos = any(re.search(p, base) for p in POSITIVOS)
    neg = any(re.search(p, base) for p in NEGATIVOS)
    sentimento = ("misto" if pos and neg else "positivo" if pos
                  else "negativo" if neg else "inconclusivo")
    return {"temas": temas, "sentimento": sentimento, "padroes_detectados": evidencias}

def temas_referencia(texto):
    return {p.strip() for p in str(texto).split(";") if p.strip()}
