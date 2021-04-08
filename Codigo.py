import sys

print(sys.version)

import simpy
import random
import numpy


def iniciaCenarios(atend_dinheiro, atend_cartao, atend_lanche):
    print('\n \nResultados com {} atendente no dinheiro, {} no cartão e {} no lanche:'.format(atend_dinheiro,
                                                                                              atend_cartao,
                                                                                              atend_lanche))

    # Médias dos valores gerais para cada replicacao
    todasfilaCartao = []
    todasfilaDinheiro = []
    todasfilaLanche = []

    # Médias tempos do fila do cartão para cada intervalo em cada replicacao
    todastempoFilaCartaoAlmoco = []
    todastempoFilaCartaoIntervaloManha = []
    todastempoFilaCartaoIntervaloTarde = []
    todastempoFilaCartaoDuranteAulas = []

    # Médias tempos do fila do dinheiro para cada intervalo em cada replicacao
    todastempoFilaDinheiroAlmoco = []
    todastempoFilaDinheiroIntervaloManha = []
    todastempoFilaDinheiroIntervaloTarde = []
    todastempoFilaDinheiroDuranteAulas = []

    # Médias tempos do fila do lanche para cada intervalo em cada replicacao
    todastempoFilaLancheAlmoco = []
    todastempoFilaLancheIntervaloManha = []
    todastempoFilaLancheIntervaloTarde = []
    todastempoFilaLancheDuranteAulas = []

    replicacoes = 100
    i = 0
    while i < replicacoes:
        semana = 5
        j = 0

        FilaCartaoSemanal = []
        FilaDinheiroSemanal = []
        FilaLancheSemanal = []
        TempoFilaCartaoAlmocoSemanal = []
        TempoFilaCartaoIntervaloManhaSemanal = []
        TempoFilaCartaoIntervaloTardeSemanal = []
        TempoFilaCartaoDuranteAulasSemanal = []
        TempoFilaDinheiroAlmocoSemanal = []
        TempoFilaDinheiroIntervaloManhaSemanal = []
        TempoFilaDinheiroIntervaloTardeSemanal = []
        TempoFilaDinheiroDuranteAulasSemanal = []
        TempoFilaLancheAlmocoSemanal = []
        TempoFilaLancheIntervaloManhaSemanal = []
        TempoFilaLancheIntervaloTardeSemanal = []
        TempoFilaLancheDuranteAulasSemanal = []

        while j < semana:
            env = simpy.Environment()

            dados = dict(
                filaCartao=[],  # Tempos do dia inteiro
                filaDinheiro=[],
                filaLanche=[],
                tempoFilaCartaoAlmoco=[],  # Tempos do fila do cartão para cada intervalo
                tempoFilaCartaoIntervaloManha=[],
                tempoFilaCartaoIntervaloTarde=[],
                tempoFilaCartaoDuranteAulas=[],
                tempoFilaDinheiroAlmoco=[],  # Tempos da fila do dinheiro para cada intervalo
                tempoFilaDinheiroIntervaloManha=[],
                tempoFilaDinheiroIntervaloTarde=[],
                tempoFilaDinheiroDuranteAulas=[],
                tempoFilaLancheAlmoco=[],  # Tempos da fila do lanche para cada intervalo
                tempoFilaLancheIntervaloManha=[],
                tempoFilaLancheIntervaloTarde=[],
                tempoFilaLancheDuranteAulas=[],
            )

            recursos = dict(
                atendenteDinheiro=simpy.Resource(env, capacity=atend_dinheiro),
                atendenteCartao=simpy.Resource(env, capacity=atend_cartao),
                atendenteLanche=simpy.Resource(env, capacity=atend_lanche),
                atendenteAlmoco=simpy.Resource(env, capacity=float('inf'))
                # Capacidade infinita, pois não é o objetivo da simulação
            )
            env.process(chegadas(env, 'cliente', recursos, dados))
            env.run(until=50400)  # Considerado que eles trabalham de 7h as 21h, totalizando 50400 segundos

            FilaCartaoSemanal.append(numpy.mean(dados["filaCartao"]))
            FilaDinheiroSemanal.append(numpy.mean(dados["filaDinheiro"]))
            FilaLancheSemanal.append(numpy.mean(dados["filaLanche"]))

            TempoFilaCartaoAlmocoSemanal.append(numpy.mean(dados["tempoFilaCartaoAlmoco"]))
            TempoFilaCartaoIntervaloManhaSemanal.append(numpy.mean(dados["tempoFilaCartaoIntervaloManha"]))
            TempoFilaCartaoIntervaloTardeSemanal.append(numpy.mean(dados["tempoFilaCartaoIntervaloTarde"]))
            TempoFilaCartaoDuranteAulasSemanal.append(numpy.mean(dados["tempoFilaCartaoDuranteAulas"]))

            TempoFilaDinheiroAlmocoSemanal.append(numpy.mean(dados["tempoFilaDinheiroAlmoco"]))
            TempoFilaDinheiroIntervaloManhaSemanal.append(numpy.mean(dados["tempoFilaDinheiroIntervaloManha"]))
            TempoFilaDinheiroIntervaloTardeSemanal.append(numpy.mean(dados["tempoFilaDinheiroIntervaloTarde"]))
            TempoFilaDinheiroDuranteAulasSemanal.append(numpy.mean(dados["tempoFilaDinheiroDuranteAulas"]))

            TempoFilaLancheAlmocoSemanal.append(numpy.mean(dados["tempoFilaLancheAlmoco"]))
            TempoFilaLancheIntervaloManhaSemanal.append(numpy.mean(dados["tempoFilaLancheIntervaloManha"]))
            TempoFilaLancheIntervaloTardeSemanal.append(numpy.mean(dados["tempoFilaLancheIntervaloTarde"]))
            TempoFilaLancheDuranteAulasSemanal.append(numpy.mean(dados["tempoFilaLancheDuranteAulas"]))

            j += 1

        todasfilaCartao.append(numpy.mean(FilaCartaoSemanal))
        todasfilaDinheiro.append(numpy.mean(FilaDinheiroSemanal))
        todasfilaLanche.append(numpy.mean(FilaLancheSemanal))

        todastempoFilaCartaoAlmoco.append(numpy.mean(TempoFilaCartaoAlmocoSemanal))
        todastempoFilaCartaoIntervaloManha.append(numpy.mean(TempoFilaCartaoIntervaloManhaSemanal))
        todastempoFilaCartaoIntervaloTarde.append(numpy.mean(TempoFilaCartaoIntervaloTardeSemanal))
        todastempoFilaCartaoDuranteAulas.append(numpy.mean(TempoFilaCartaoDuranteAulasSemanal))

        todastempoFilaDinheiroAlmoco.append(numpy.mean(TempoFilaDinheiroAlmocoSemanal))
        todastempoFilaDinheiroIntervaloManha.append(numpy.mean(TempoFilaDinheiroIntervaloManhaSemanal))
        todastempoFilaDinheiroIntervaloTarde.append(numpy.mean(TempoFilaDinheiroIntervaloTardeSemanal))
        todastempoFilaDinheiroDuranteAulas.append(numpy.mean(TempoFilaDinheiroDuranteAulasSemanal))

        todastempoFilaLancheAlmoco.append(numpy.mean(TempoFilaLancheAlmocoSemanal))
        todastempoFilaLancheIntervaloManha.append(numpy.mean(TempoFilaLancheIntervaloManhaSemanal))
        todastempoFilaLancheIntervaloTarde.append(numpy.mean(TempoFilaLancheIntervaloTardeSemanal))
        todastempoFilaLancheDuranteAulas.append(numpy.mean(TempoFilaLancheDuranteAulasSemanal))
        i += 1

    print('\nTempos médios durante todo o expediente:')
    print('Fila do dinheiro: {} ± {}'.format(numpy.mean(todasfilaDinheiro), numpy.std(todasfilaDinheiro)))
    print('Fila do cartao: {} ± {}'.format(numpy.mean(todasfilaCartao), numpy.std(todasfilaCartao)))
    print('Fila do lanche: {} ± {}'.format(numpy.mean(todasfilaLanche), numpy.std(todasfilaLanche)))

    print('\nTempos médios durante o almoço:')
    print('Fila do dinheiro: {} ± {}'.format(numpy.mean(todastempoFilaDinheiroAlmoco), numpy.std(todastempoFilaDinheiroAlmoco)))
    print(
        'Fila do cartao: {} ± {}'.format(numpy.mean(todastempoFilaCartaoAlmoco), numpy.std(todastempoFilaCartaoAlmoco)))
    print(
        'Fila do lanche: {} ± {}'.format(numpy.mean(todastempoFilaLancheAlmoco), numpy.std(todastempoFilaLancheAlmoco)))

    print('\nTempos médios durante o intervalo da manhã:')
    print('Fila do dinheiro: {} ± {}'.format(numpy.mean(todastempoFilaDinheiroIntervaloManha), numpy.std(todastempoFilaDinheiroIntervaloManha)))
    print('Fila do cartao: {} ± {}'.format(numpy.mean(todastempoFilaCartaoIntervaloManha), numpy.std(todastempoFilaCartaoIntervaloManha)))
    print('Fila do lanche: {} ± {}'.format(numpy.mean(todastempoFilaLancheIntervaloManha),numpy.std(todastempoFilaLancheIntervaloManha)))

    print('\nTempos médios durante os intervalos da tarde:')
    print('Fila do dinheiro: {} ± {}'.format(numpy.mean(todastempoFilaDinheiroIntervaloTarde), numpy.std(todastempoFilaDinheiroIntervaloTarde)))
    print('Fila do cartao: {} ± {}'.format(numpy.mean(todastempoFilaCartaoIntervaloTarde), numpy.std(todastempoFilaCartaoIntervaloTarde)))
    print('Fila do lanche: {} ± {}'.format(numpy.mean(todastempoFilaLancheIntervaloTarde), numpy.std(todastempoFilaLancheIntervaloTarde)))

    print('\nTempos médios durante o restante do dia:')
    print('Fila do dinheiro: {} ± {}'.format(numpy.mean(todastempoFilaDinheiroDuranteAulas), numpy.std(todastempoFilaDinheiroDuranteAulas)))
    print('Fila do cartao: {} ± {}'.format(numpy.mean(todastempoFilaCartaoDuranteAulas), numpy.std(todastempoFilaCartaoDuranteAulas)))
    print('Fila do lanche: {} ± {}'.format(numpy.mean(todastempoFilaLancheDuranteAulas), numpy.std(todastempoFilaLancheDuranteAulas)))


def distribuicoesChegadas(env):
    dist = 0
    valores = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5,
               12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5,
               29.5,
               30.5, 31.5, 32.5, 33.5, 34.5, 35.5, 36.5, 37.5, 38.5, 39.5, 40.5, 61, 87.5]
    probabilidades = [0.085, 0.211, 0.106, 0, 0.010, 0, 0, 0, 0, 0.010, 0.031, 0.010, 0.053, 0.010, 0, 0.031, 0.031,
                      0.021, 0.031, 0.010, 0.021, 0.021, 0.021, 0.031, 0, 0.010, 0.010, 0, 0.010, 0.010, 0.031, 0.021,
                      0, 0,
                      0.031, 0, 0.031, 0.010, 0, 0.010, 0, 0.021, 0, 0.010, 0, 0.010, 0, 0, 0.010, 0.021, 0.010]

    if (env.now >= 14400) and (env.now < 23400):  # Horário de almoco entre 11h e 13h30
        x = random.gammavariate(0.315, 1)
        y = random.gammavariate(2.08, 1)
        dist = 108 * x / (x + y)

    elif (env.now >= 7200) and (env.now < 9000):  # Intervalo da manha entre 9h e 9h30
        dist = random.lognormvariate(1.5287, -1.528)

    elif ((env.now >= 27600) and (env.now < 28800)) or ((env.now >= 34200) and (env.now < 35400)) or \
            ((env.now >= 39600) and (
                    env.now < 43200)):  # Intervalos da tarde de 14h40 a 15h, de 16h30 a 16h50 e de 18h às 19h
        dist = numpy.random.choice(valores, 1, p=probabilidades)

    elif ((env.now >= 0) and (env.now < 7200)) or ((env.now >= 9000) and (env.now < 14400)) or (
            (env.now >= 23400) and (env.now < 27600)) \
            or ((env.now >= 28800) and (env.now < 34200)) or ((env.now >= 35400) and (env.now < 39600)) or (
            (env.now >= 43200) and (env.now < 50400)):  # Demais intervalos
        dist = random.weibullvariate(22.8, 0.755)
    return dist


def chegadas(env, entidade, recursos, dados):
    contadorChegadas = 0
    while True:
        yield env.timeout(distribuicoesChegadas(env))
        contadorChegadas += 1
        cliente = dict(
            nome=entidade + str(int(contadorChegadas)),
            servico=random.random(), # Determina valor aleatorio que mandara o cliente para o almoco ou para o lanche no horario de almoco
            pagamento=random.random(),  # Determina valor aleatorio que mandara o cliente pagar em dinheiro ou cartao
            entrada=env.now,
            horario=" ",
            intervalo=" "
        )

        if (cliente['entrada'] >= 14400) and (
                cliente['entrada'] < 23400):  # Marcador que identifica se esta ou nao no horario de almoco
            cliente['horario'] = 'almoco'
        else:
            cliente['horario'] = 'lanche'

        if (cliente['entrada'] >= 14400) and (
                cliente['entrada'] < 23400):  # Marcador que identifica o intervalo de entrada
            cliente['intervalo'] = 'almoco'
        elif (cliente['entrada'] >= 7200) and (cliente['entrada'] < 9000):
            cliente['intervalo'] = 'manha'
        elif ((env.now >= 27600) and (env.now < 28800)) or ((env.now >= 34200) and (env.now < 35400)):
            cliente['intervalo'] = 'tarde'
        elif ((env.now >= 0) and (env.now < 7200)) or ((env.now >= 9000) and (env.now < 14400)) or (
                (env.now >= 23400) and (env.now < 27600)) \
                or ((env.now >= 28800) and (env.now < 34200)) or ((env.now >= 35400) and (env.now < 50400)):
            cliente['intervalo'] = 'restante'

        if cliente['horario'] == 'almoco':
            if cliente['servico'] >= 0.16666:
                env.process(almoco(env, cliente, recursos, dados))
            else:
                env.process(lanche(env, cliente, recursos, dados))
        elif cliente['pagamento'] <= 0.3556:
            env.process(pagamentoDinheiro(env, cliente, recursos, dados))
        elif cliente['pagamento'] >= 0.3556:
            env.process(pagamentoCartao(env, cliente, recursos, dados))


def lanche(env, entidade, recursos, dados):
    inicio = env.now
    with recursos['atendenteLanche'].request() as req_lanche:

        yield req_lanche
        tempo = env.now - inicio
        dados["filaLanche"].append(tempo)
        if entidade['intervalo'] == 'manha':
            dados["tempoFilaLancheIntervaloManha"].append(tempo)
        elif entidade['intervalo'] == 'tarde':
            dados["tempoFilaLancheIntervaloTarde"].append(tempo)
        elif entidade['intervalo'] == 'restante':
            dados["tempoFilaLancheDuranteAulas"].append(tempo)
        elif entidade['intervalo'] == 'almoco':
            dados["tempoFilaLancheAlmoco"].append(tempo)

        yield env.timeout(random.weibullvariate(15.4, 1.45))

        if entidade['horario'] == 'almoco':
            if entidade['pagamento'] <= 0.3556:
                env.process(pagamentoDinheiro(env, entidade, recursos, dados))
            elif entidade['pagamento'] >= 0.3556:
                env.process(pagamentoCartao(env, entidade, recursos, dados))


def almoco(env, entidade, recursos, dados):
    inicio = env.now
    with recursos['atendenteAlmoco'].request() as req_almoco:

        yield req_almoco
        entidade['filaAlmoco'] = env.now - inicio

        yield env.timeout(645 + 1650 * random.betavariate(1.86, 1.66))

        if entidade['pagamento'] <= 0.3556:
            env.process(pagamentoDinheiro(env, entidade, recursos, dados))
        elif entidade['pagamento'] >= 0.3556:
            env.process(pagamentoCartao(env, entidade, recursos, dados))


def pagamentoDinheiro(env, entidade, recursos, dados):
    inicio = env.now
    with recursos['atendenteDinheiro'].request() as req_dinheiro:

        yield req_dinheiro
        tempo = env.now - inicio
        dados["filaDinheiro"].append(tempo)
        if entidade['intervalo'] == 'manha':
            dados["tempoFilaDinheiroIntervaloManha"].append(tempo)
        elif entidade['intervalo'] == 'tarde':
            dados["tempoFilaDinheiroIntervaloTarde"].append(tempo)
        elif entidade['intervalo'] == 'restante':
            dados["tempoFilaDinheiroDuranteAulas"].append(tempo)
        elif entidade['intervalo'] == 'almoco':
            dados["tempoFilaDinheiroAlmoco"].append(tempo)

        yield env.timeout(5 + random.weibullvariate(28.2, 1.84))

        if entidade['horario'] == 'lanche':
            env.process(lanche(env, entidade, recursos, dados))


def pagamentoCartao(env, entidade, recursos, dados):
    inicio = env.now
    with recursos['atendenteCartao'].request() as req_cartao:

        yield req_cartao
        tempo = env.now - inicio
        dados["filaCartao"].append(tempo)
        if entidade['intervalo'] == 'manha':
            dados["tempoFilaCartaoIntervaloManha"].append(tempo)
        elif entidade['intervalo'] == 'tarde':
            dados["tempoFilaCartaoIntervaloTarde"].append(tempo)
        elif entidade['intervalo'] == 'restante':
            dados["tempoFilaCartaoDuranteAulas"].append(tempo)
        elif entidade['intervalo'] == 'almoco':
            dados["tempoFilaCartaoAlmoco"].append(tempo)

        yield env.timeout((13 + random.gammavariate(7.81, 4.22)))

        if entidade['horario'] == 'lanche':
            env.process(lanche(env, entidade, recursos, dados))


def main():
    iniciaCenarios(1, 1, 1)
    iniciaCenarios(1, 2, 1)
    iniciaCenarios(1, 3, 1)
    iniciaCenarios(1, 2, 2)
    iniciaCenarios(1, 3, 2)


if __name__ == "__main__":
    main()
