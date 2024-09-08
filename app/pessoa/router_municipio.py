"""
def save_states_and_citys():
    # salva stados e cidades via api ibge
    list_uf = getStates()
    for _uf in list_uf:
        unidade = Uf.objects.get_or_create(
            id=_uf.get('id'),
            sigla=_uf.get('sigla'),
            nome=_uf.get('nome')
            )
        Regiao.objects.get_or_create(
            id=_uf.get('regiao').get('id'),
            nome=_uf.get('regiao').get('nome'),
            sigla=_uf.get('regiao').get('sigla')
        )
        list_city = getCityforState(_uf.get('sigla'))
        for city in list_city:
            Municipio.objects.get_or_create(
                id=city.get('id'),
                nome=city.get('nome'),
                uf=unidade[0]
            )

"""