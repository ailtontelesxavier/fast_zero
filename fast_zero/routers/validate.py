import re


def validate_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != int(11) or cpf == cpf[0] * len(cpf):
        return False
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
        check = ((value * 10) % 11) % 10
        if check != int(cpf[i]):
            return False
    return True


def validate_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != int(14) or cnpj == cnpj[0] * len(cnpj):
        return False
    for i in range(12, 14):
        value = sum(
            (
                int(cnpj[num]) * ((i - 7 if num >= i - 8 else i + 1) - num)
                for num in range(0, i)
            )
        )
        check = ((value * 10) % 11) % 10
        if check != int(cnpj[i]):
            return False
    return True
