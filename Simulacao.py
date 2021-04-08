import sys
print(sys.version)

import simpy
import random
import numpy


def distribuicoesChegadas(env):
    dist = 0
    valores = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5,
               12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5, 29.5,
               30.5, 31.5, 32.5, 33.5, 34.5, 35.5, 36.5, 37.5, 38.5, 39.5, 40.5, 61, 87.5]
    probabilidades = [0.085, 0.211, 0.106, 0, 0.010, 0, 0, 0, 0, 0.010, 0.031, 0.010, 0.053, 0.010, 0, 0.031, 0.031,
                      0.021, 0.031, 0.010, 0.021, 0.021, 0.021, 0.031, 0, 0.010, 0.010, 0, 0.010, 0.010, 0.031, 0.021, 0, 0,
                      0.031, 0, 0.031, 0.010, 0, 0.010, 0, 0.021, 0, 0.010, 0, 0.010, 0, 0, 0.010, 0.021, 0.010]

    if (env.now >= 14400) and (env.now < 23400):
        x = random.gammavariate(0.315, 1)
        y = random.gammavariate(2.08, 1)
        dist = 108 * x / (x + y)

    elif (env.now >= 7200) and (env.now < 9000):
        dist = random.lognormvariate(1.5287, -1.528)

    elif ((env.now >= 27600) and (env.now < 28800)) or ((env.now >= 34200) and (env.now < 35400)) or \
            ((env.now >= 39600) and (env.now < 43200)):
        dist = numpy.random.choice(valores, 1, p=probabilidades)

    elif ((env.now >= 0) and (env.now < 7200)) or ((env.now >= 9000) and (env.now < 14400)) or ((env.now >= 23400) and (env.now < 27600)) \
            or ((env.now >= 28800) and (env.now < 34200)) or ((env.now >= 35400) and (env.now < 39600)) or ((env.now >= 43200) and (env.now < 50400)):
        dist = random.weibullvariate(22.8, 0.755)
    return dist



def chegadas(env, entidade, recursos, filaCartao, filaDinheiro, filaLanche, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
             tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
             tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
             tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas):
    contadorChegadas = 0
    while True:
        yield env.timeout(distribuicoesChegadas(env))
        contadorChegadas += 1
        cliente = dict(
            nome = entidade + str(int(contadorChegadas)),
            servico = random.random(),
            pagamento = random.random(),
            entrada = env.now,
            horario = " ",
            intervalo = " "
        )

        if (cliente['entrada'] >= 14400) and (cliente['entrada'] < 23400):
            cliente['horario'] = 'almoco'
        else:
            cliente['horario'] = 'lanche'

        if (cliente['entrada'] >= 14400) and (cliente['entrada'] < 23400):
            cliente['intervalo'] = 'almoco'
        elif (cliente['entrada'] >= 7200) and (cliente['entrada'] < 9000):
            cliente['intervalo'] = 'manha'
        elif ((env.now >= 27600) and (env.now < 28800)) or ((env.now >= 34200) and (env.now < 35400)):
            cliente['intervalo'] = 'tarde'
        elif ((env.now >= 0) and (env.now < 7200)) or ((env.now >= 9000) and (env.now < 14400)) or ((env.now >= 23400) and (env.now < 27600)) \
            or ((env.now >= 28800) and (env.now < 34200)) or ((env.now >= 35400) and (env.now < 50400)):
            cliente['intervalo'] = 'restante'

        if cliente['horario'] == 'almoco':
            if cliente['servico'] >= 0.16666:
                env.process(almoco(env, cliente, recursos,filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                                   tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
                                   tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                                   tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))
            else:
                env.process(lanche(env, cliente, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                                   tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
                                   tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                                   tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))
        elif cliente['pagamento'] <= 0.3556:
            env.process(pagamentoDinheiro(env, cliente, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                                          tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
                                          tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                                          tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))
        elif cliente['pagamento'] >= 0.3556:
            env.process(pagamentoCartao(env, cliente, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                                        tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
                                        tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                                        tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))



def lanche(env, entidade, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
           tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
           tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
           tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas):
    inicio = env.now
    with recursos['atendenteLanche'].request() as req_lanche:

        yield req_lanche
        tempo = env.now - inicio
        filaLanche.append(tempo)
        if entidade['intervalo'] == 'manha':
            tempoFilaLancheIntervaloManha.append(tempo)
        elif entidade['intervalo'] == 'tarde':
            tempoFilaLancheIntervaloTarde.append(tempo)
        elif entidade['intervalo'] == 'restante':
            tempoFilaLancheDuranteAulas.append(tempo)
        elif entidade['intervalo'] == 'almoco':
            tempoFilaLancheAlmoco.append(tempo)

        yield env.timeout(random.weibullvariate(15.4, 1.45))

        if entidade['horario'] == 'almoco':
            if entidade['pagamento'] <= 0.3556:
                env.process(pagamentoDinheiro(env, entidade, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                                              tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
                                              tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                                              tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))
            elif entidade['pagamento'] >= 0.3556:
                env.process(pagamentoCartao(env, entidade, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                                            tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
                                            tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                                            tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))







def almoco(env, entidade, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
           tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
           tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
           tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas):
    inicio = env.now
    with recursos['atendenteAlmoco'].request() as req_almoco:

        yield req_almoco
        entidade['filaAlmoco'] = env.now - inicio

        yield env.timeout(645 + 1650 * random.betavariate(1.86, 1.66))

        if entidade['pagamento'] <= 0.3556:
            env.process(pagamentoDinheiro(env, entidade, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco,
                                          tempoFilaCartaoIntervaloManha, tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas,
                                          tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha, tempoFilaDinheiroIntervaloTarde,
                                          tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                                          tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))
        elif entidade['pagamento'] >= 0.3556:
            env.process(pagamentoCartao(env, entidade, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco,
                                        tempoFilaCartaoIntervaloManha, tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas,
                                        tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha, tempoFilaDinheiroIntervaloTarde,
                                        tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                                        tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))













def pagamentoDinheiro(env, entidade, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                      tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
                      tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                      tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas):
    inicio = env.now
    with recursos['atendenteDinheiro'].request() as req_dinheiro:

        yield req_dinheiro
        tempo = env.now - inicio
        filaDinheiro.append(tempo)
        if entidade['intervalo'] == 'manha':
            tempoFilaDinheiroIntervaloManha.append(tempo)
        elif entidade['intervalo'] == 'tarde':
            tempoFilaDinheiroIntervaloTarde.append(tempo)
        elif entidade['intervalo'] == 'restante':
            tempoFilaDinheiroDuranteAulas.append(tempo)
        elif entidade['intervalo'] == 'almoco':
            tempoFilaDinheiroAlmoco.append(tempo)

        yield env.timeout(5 + random.weibullvariate(28.2, 1.84))

        if entidade['horario'] == 'lanche':
            env.process(lanche(env, entidade, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                               tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
                               tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                               tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))






def pagamentoCartao(env, entidade, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                    tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
                    tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                    tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas):
    inicio = env.now
    with recursos['atendenteCartao'].request() as req_cartao:

        yield req_cartao
        tempo = env.now - inicio
        filaCartao.append(tempo)
        if entidade['intervalo'] == 'manha':
            tempoFilaCartaoIntervaloManha.append(tempo)
        elif entidade['intervalo'] == 'tarde':
            tempoFilaCartaoIntervaloTarde.append(tempo)
        elif entidade['intervalo'] == 'restante':
            tempoFilaCartaoDuranteAulas.append(tempo)
        elif entidade['intervalo'] == 'almoco':
            tempoFilaCartaoAlmoco.append(tempo)

        yield env.timeout( (13 + random.gammavariate(7.81, 4.22)))

        if entidade['horario'] == 'lanche':
            env.process(lanche(env, entidade, recursos, filaLanche, filaDinheiro, filaCartao, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                               tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
                               tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                               tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))






def main():

    print('Resultados com 1 atendente no dinheiro, 1 no cartão e 1 no lanche:')

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

    replicacoes = 30
    i = 0
    while i < replicacoes:

        env = simpy.Environment()

        # Tempos do dia inteiro
        filaCartao = []
        filaDinheiro = []
        filaLanche = []

        # Tempos do fila do cartão para cada intervalo
        tempoFilaCartaoAlmoco = []
        tempoFilaCartaoIntervaloManha = []
        tempoFilaCartaoIntervaloTarde = []
        tempoFilaCartaoDuranteAulas = []

        # Tempos da fila do dinheiro para cada intervalo
        tempoFilaDinheiroAlmoco = []
        tempoFilaDinheiroIntervaloManha = []
        tempoFilaDinheiroIntervaloTarde = []
        tempoFilaDinheiroDuranteAulas = []

        # Tempos da fila do lanche para cada intervalo
        tempoFilaLancheAlmoco = []
        tempoFilaLancheIntervaloManha = []
        tempoFilaLancheIntervaloTarde = []
        tempoFilaLancheDuranteAulas = []

        recursos = dict(
            atendenteDinheiro = simpy.Resource(env, capacity=1),
            atendenteCartao = simpy.Resource(env, capacity=1),
            atendenteLanche = simpy.Resource(env, capacity=1),
            atendenteAlmoco = simpy.Resource(env, capacity = float('inf'))  # Capacidade infinita, pois não é o objetivo da simulação
        )
        env.process(chegadas(env, 'cliente', recursos, filaCartao, filaDinheiro, filaLanche, tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                             tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco, tempoFilaDinheiroIntervaloManha,
                             tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco, tempoFilaLancheIntervaloManha,
                             tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))
        env.run(until = 50400)      # Considerado que eles trabalham de 7h as 21h, totalizando 50400 segundos

        todasfilaCartao.append(numpy.mean(filaCartao))
        todasfilaDinheiro.append(numpy.mean(filaDinheiro))
        todasfilaLanche.append(numpy.mean(filaLanche))

        todastempoFilaCartaoAlmoco.append(numpy.mean(tempoFilaCartaoAlmoco))
        todastempoFilaCartaoIntervaloManha.append(numpy.mean(tempoFilaCartaoIntervaloManha))
        todastempoFilaCartaoIntervaloTarde.append(numpy.mean(tempoFilaCartaoIntervaloTarde))
        todastempoFilaCartaoDuranteAulas.append(numpy.mean(tempoFilaCartaoDuranteAulas))

        todastempoFilaDinheiroAlmoco.append(numpy.mean(tempoFilaDinheiroAlmoco))
        todastempoFilaDinheiroIntervaloManha.append(numpy.mean(tempoFilaDinheiroIntervaloManha))
        todastempoFilaDinheiroIntervaloTarde.append(numpy.mean(tempoFilaDinheiroIntervaloTarde))
        todastempoFilaDinheiroDuranteAulas.append(numpy.mean(tempoFilaDinheiroDuranteAulas))

        todastempoFilaLancheAlmoco.append(numpy.mean(tempoFilaLancheAlmoco))
        todastempoFilaLancheIntervaloManha.append(numpy.mean(tempoFilaLancheIntervaloManha))
        todastempoFilaLancheIntervaloTarde.append(numpy.mean(tempoFilaLancheIntervaloTarde))
        todastempoFilaLancheDuranteAulas.append(numpy.mean(tempoFilaLancheDuranteAulas))

        i += 1

    print('\nTempos médios durante todo o expediente:')
    print('Fila do dinheiro: {}' .format(numpy.mean(todasfilaDinheiro)))
    print('Fila do cartao: {}' .format(numpy.mean(todasfilaCartao)))
    print('Fila do lanche: {}' .format(numpy.mean(todasfilaLanche)))

    print('\nTempos médios durante o almoço:')
    print('Fila do dinheiro: {}' .format(numpy.mean(todastempoFilaDinheiroAlmoco)))
    print('Fila do cartao: {}' .format(numpy.mean(todastempoFilaCartaoAlmoco)))
    print('Fila do lanche: {}' .format(numpy.mean(todastempoFilaLancheAlmoco)))

    print('\nTempos médios durante o intervalo da manhã:')
    print('Fila do dinheiro: {}' .format(numpy.mean(todastempoFilaDinheiroIntervaloManha)))
    print('Fila do cartao: {}' .format(numpy.mean(todastempoFilaCartaoIntervaloManha)))
    print('Fila do lanche: {}' .format(numpy.mean(todastempoFilaLancheIntervaloManha)))

    print('\nTempos médios durante os intervalos da tarde:')
    print('Fila do dinheiro: {}' .format(numpy.mean(todastempoFilaDinheiroIntervaloTarde)))
    print('Fila do cartao: {}' .format(numpy.mean(todastempoFilaCartaoIntervaloTarde)))
    print('Fila do lanche: {}' .format(numpy.mean(todastempoFilaLancheIntervaloTarde)))

    print('\nTempos médios durante o restante do dia:')
    print('Fila do dinheiro: {}' .format(numpy.mean(todastempoFilaDinheiroDuranteAulas)))
    print('Fila do cartao: {}' .format(numpy.mean(todastempoFilaCartaoDuranteAulas)))
    print('Fila do lanche: {}' .format(numpy.mean(todastempoFilaLancheDuranteAulas)))




    print('\n \nResultados com 1 atendente no dinheiro, 2 no cartão e 1 no lanche:')

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

    replicacoes = 30
    i = 0
    while i < replicacoes:
        env = simpy.Environment()

        # Tempos do dia inteiro
        filaCartao = []
        filaDinheiro = []
        filaLanche = []

        # Tempos do fila do cartão para cada intervalo
        tempoFilaCartaoAlmoco = []
        tempoFilaCartaoIntervaloManha = []
        tempoFilaCartaoIntervaloTarde = []
        tempoFilaCartaoDuranteAulas = []

        # Tempos da fila do dinheiro para cada intervalo
        tempoFilaDinheiroAlmoco = []
        tempoFilaDinheiroIntervaloManha = []
        tempoFilaDinheiroIntervaloTarde = []
        tempoFilaDinheiroDuranteAulas = []

        # Tempos da fila do lanche para cada intervalo
        tempoFilaLancheAlmoco = []
        tempoFilaLancheIntervaloManha = []
        tempoFilaLancheIntervaloTarde = []
        tempoFilaLancheDuranteAulas = []

        recursos = dict(
            atendenteDinheiro=simpy.Resource(env, capacity=1),
            atendenteCartao=simpy.Resource(env, capacity=2),
            atendenteLanche=simpy.Resource(env, capacity=1),
            atendenteAlmoco=simpy.Resource(env, capacity=float('inf'))      # Capacidade infinita, pois não é o objetivo da simulação
        )
        env.process(chegadas(env, 'cliente', recursos, filaCartao, filaDinheiro, filaLanche,
                             tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                             tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco,
                             tempoFilaDinheiroIntervaloManha,
                             tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco,
                             tempoFilaLancheIntervaloManha,
                             tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))
        env.run(until=50400)  # Considerado que eles trabalham de 7h as 21h, totalizando 50400 segundos

        todasfilaCartao.append(numpy.mean(filaCartao))
        todasfilaDinheiro.append(numpy.mean(filaDinheiro))
        todasfilaLanche.append(numpy.mean(filaLanche))

        todastempoFilaCartaoAlmoco.append(numpy.mean(tempoFilaCartaoAlmoco))
        todastempoFilaCartaoIntervaloManha.append(numpy.mean(tempoFilaCartaoIntervaloManha))
        todastempoFilaCartaoIntervaloTarde.append(numpy.mean(tempoFilaCartaoIntervaloTarde))
        todastempoFilaCartaoDuranteAulas.append(numpy.mean(tempoFilaCartaoDuranteAulas))

        todastempoFilaDinheiroAlmoco.append(numpy.mean(tempoFilaDinheiroAlmoco))
        todastempoFilaDinheiroIntervaloManha.append(numpy.mean(tempoFilaDinheiroIntervaloManha))
        todastempoFilaDinheiroIntervaloTarde.append(numpy.mean(tempoFilaDinheiroIntervaloTarde))
        todastempoFilaDinheiroDuranteAulas.append(numpy.mean(tempoFilaDinheiroDuranteAulas))

        todastempoFilaLancheAlmoco.append(numpy.mean(tempoFilaLancheAlmoco))
        todastempoFilaLancheIntervaloManha.append(numpy.mean(tempoFilaLancheIntervaloManha))
        todastempoFilaLancheIntervaloTarde.append(numpy.mean(tempoFilaLancheIntervaloTarde))
        todastempoFilaLancheDuranteAulas.append(numpy.mean(tempoFilaLancheDuranteAulas))

        i += 1

    print('\nTempos médios durante todo o expediente:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todasfilaDinheiro)))
    print('Fila do cartao: {}'.format(numpy.mean(todasfilaCartao)))
    print('Fila do lanche: {}'.format(numpy.mean(todasfilaLanche)))

    print('\nTempos médios durante o almoço:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroAlmoco)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoAlmoco)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheAlmoco)))

    print('\nTempos médios durante o intervalo da manhã:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroIntervaloManha)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoIntervaloManha)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheIntervaloManha)))

    print('\nTempos médios durante os intervalos da tarde:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroIntervaloTarde)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoIntervaloTarde)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheIntervaloTarde)))

    print('\nTempos médios durante o restante do dia:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroDuranteAulas)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoDuranteAulas)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheDuranteAulas)))




    print('\n \nResultados com 1 atendente no dinheiro, 2 no cartão e 2 no lanche:')

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

    replicacoes = 30
    i = 0
    while i < replicacoes:
        env = simpy.Environment()

        # Tempos do dia inteiro
        filaCartao = []
        filaDinheiro = []
        filaLanche = []

        # Tempos do fila do cartão para cada intervalo
        tempoFilaCartaoAlmoco = []
        tempoFilaCartaoIntervaloManha = []
        tempoFilaCartaoIntervaloTarde = []
        tempoFilaCartaoDuranteAulas = []

        # Tempos da fila do dinheiro para cada intervalo
        tempoFilaDinheiroAlmoco = []
        tempoFilaDinheiroIntervaloManha = []
        tempoFilaDinheiroIntervaloTarde = []
        tempoFilaDinheiroDuranteAulas = []

        # Tempos da fila do lanche para cada intervalo
        tempoFilaLancheAlmoco = []
        tempoFilaLancheIntervaloManha = []
        tempoFilaLancheIntervaloTarde = []
        tempoFilaLancheDuranteAulas = []

        recursos = dict(
            atendenteDinheiro=simpy.Resource(env, capacity=1),
            atendenteCartao=simpy.Resource(env, capacity=2),
            atendenteLanche=simpy.Resource(env, capacity=2),
            atendenteAlmoco=simpy.Resource(env, capacity=float('inf'))      # Capacidade infinita, pois não é o objetivo da simulação
        )
        env.process(chegadas(env, 'cliente', recursos, filaCartao, filaDinheiro, filaLanche,
                             tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                             tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco,
                             tempoFilaDinheiroIntervaloManha,
                             tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco,
                             tempoFilaLancheIntervaloManha,
                             tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))
        env.run(until=50400)  # Considerado que eles trabalham de 7h as 21h, totalizando 50400 segundos

        todasfilaCartao.append(numpy.mean(filaCartao))
        todasfilaDinheiro.append(numpy.mean(filaDinheiro))
        todasfilaLanche.append(numpy.mean(filaLanche))

        todastempoFilaCartaoAlmoco.append(numpy.mean(tempoFilaCartaoAlmoco))
        todastempoFilaCartaoIntervaloManha.append(numpy.mean(tempoFilaCartaoIntervaloManha))
        todastempoFilaCartaoIntervaloTarde.append(numpy.mean(tempoFilaCartaoIntervaloTarde))
        todastempoFilaCartaoDuranteAulas.append(numpy.mean(tempoFilaCartaoDuranteAulas))

        todastempoFilaDinheiroAlmoco.append(numpy.mean(tempoFilaDinheiroAlmoco))
        todastempoFilaDinheiroIntervaloManha.append(numpy.mean(tempoFilaDinheiroIntervaloManha))
        todastempoFilaDinheiroIntervaloTarde.append(numpy.mean(tempoFilaDinheiroIntervaloTarde))
        todastempoFilaDinheiroDuranteAulas.append(numpy.mean(tempoFilaDinheiroDuranteAulas))

        todastempoFilaLancheAlmoco.append(numpy.mean(tempoFilaLancheAlmoco))
        todastempoFilaLancheIntervaloManha.append(numpy.mean(tempoFilaLancheIntervaloManha))
        todastempoFilaLancheIntervaloTarde.append(numpy.mean(tempoFilaLancheIntervaloTarde))
        todastempoFilaLancheDuranteAulas.append(numpy.mean(tempoFilaLancheDuranteAulas))

        i += 1

    print('\nTempos médios durante todo o expediente:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todasfilaDinheiro)))
    print('Fila do cartao: {}'.format(numpy.mean(todasfilaCartao)))
    print('Fila do lanche: {}'.format(numpy.mean(todasfilaLanche)))

    print('\nTempos médios durante o almoço:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroAlmoco)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoAlmoco)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheAlmoco)))

    print('\nTempos médios durante o intervalo da manhã:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroIntervaloManha)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoIntervaloManha)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheIntervaloManha)))

    print('\nTempos médios durante os intervalos da tarde:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroIntervaloTarde)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoIntervaloTarde)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheIntervaloTarde)))

    print('\nTempos médios durante o restante do dia:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroDuranteAulas)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoDuranteAulas)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheDuranteAulas)))




    print('\n \nResultados com 1 atendente no dinheiro, 3 no cartão e 1 no lanche:')

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

    replicacoes = 30
    i = 0
    while i < replicacoes:
        env = simpy.Environment()

        # Tempos do dia inteiro
        filaCartao = []
        filaDinheiro = []
        filaLanche = []

        # Tempos do fila do cartão para cada intervalo
        tempoFilaCartaoAlmoco = []
        tempoFilaCartaoIntervaloManha = []
        tempoFilaCartaoIntervaloTarde = []
        tempoFilaCartaoDuranteAulas = []

        # Tempos da fila do dinheiro para cada intervalo
        tempoFilaDinheiroAlmoco = []
        tempoFilaDinheiroIntervaloManha = []
        tempoFilaDinheiroIntervaloTarde = []
        tempoFilaDinheiroDuranteAulas = []

        # Tempos da fila do lanche para cada intervalo
        tempoFilaLancheAlmoco = []
        tempoFilaLancheIntervaloManha = []
        tempoFilaLancheIntervaloTarde = []
        tempoFilaLancheDuranteAulas = []

        recursos = dict(
            atendenteDinheiro=simpy.Resource(env, capacity=1),
            atendenteCartao=simpy.Resource(env, capacity=3),
            atendenteLanche=simpy.Resource(env, capacity=1),
            atendenteAlmoco=simpy.Resource(env, capacity=float('inf'))      # Capacidade infinita, pois não é o objetivo da simulação
        )
        env.process(chegadas(env, 'cliente', recursos, filaCartao, filaDinheiro, filaLanche,
                             tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                             tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco,
                             tempoFilaDinheiroIntervaloManha,
                             tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco,
                             tempoFilaLancheIntervaloManha,
                             tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))
        env.run(until=50400)  # Considerado que eles trabalham de 7h as 21h, totalizando 50400 segundos

        todasfilaCartao.append(numpy.mean(filaCartao))
        todasfilaDinheiro.append(numpy.mean(filaDinheiro))
        todasfilaLanche.append(numpy.mean(filaLanche))

        todastempoFilaCartaoAlmoco.append(numpy.mean(tempoFilaCartaoAlmoco))
        todastempoFilaCartaoIntervaloManha.append(numpy.mean(tempoFilaCartaoIntervaloManha))
        todastempoFilaCartaoIntervaloTarde.append(numpy.mean(tempoFilaCartaoIntervaloTarde))
        todastempoFilaCartaoDuranteAulas.append(numpy.mean(tempoFilaCartaoDuranteAulas))

        todastempoFilaDinheiroAlmoco.append(numpy.mean(tempoFilaDinheiroAlmoco))
        todastempoFilaDinheiroIntervaloManha.append(numpy.mean(tempoFilaDinheiroIntervaloManha))
        todastempoFilaDinheiroIntervaloTarde.append(numpy.mean(tempoFilaDinheiroIntervaloTarde))
        todastempoFilaDinheiroDuranteAulas.append(numpy.mean(tempoFilaDinheiroDuranteAulas))

        todastempoFilaLancheAlmoco.append(numpy.mean(tempoFilaLancheAlmoco))
        todastempoFilaLancheIntervaloManha.append(numpy.mean(tempoFilaLancheIntervaloManha))
        todastempoFilaLancheIntervaloTarde.append(numpy.mean(tempoFilaLancheIntervaloTarde))
        todastempoFilaLancheDuranteAulas.append(numpy.mean(tempoFilaLancheDuranteAulas))

        i += 1

    print('\nTempos médios durante todo o expediente:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todasfilaDinheiro)))
    print('Fila do cartao: {}'.format(numpy.mean(todasfilaCartao)))
    print('Fila do lanche: {}'.format(numpy.mean(todasfilaLanche)))

    print('\nTempos médios durante o almoço:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroAlmoco)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoAlmoco)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheAlmoco)))

    print('\nTempos médios durante o intervalo da manhã:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroIntervaloManha)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoIntervaloManha)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheIntervaloManha)))

    print('\nTempos médios durante os intervalos da tarde:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroIntervaloTarde)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoIntervaloTarde)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheIntervaloTarde)))

    print('\nTempos médios durante o restante do dia:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroDuranteAulas)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoDuranteAulas)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheDuranteAulas)))




    print('\n \nResultados com 1 atendente no dinheiro, 3 no cartão e 2 no lanche:')

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

    replicacoes = 30
    i = 0
    while i < replicacoes:
        env = simpy.Environment()

        # Tempos do dia inteiro
        filaCartao = []
        filaDinheiro = []
        filaLanche = []

        # Tempos do fila do cartão para cada intervalo
        tempoFilaCartaoAlmoco = []
        tempoFilaCartaoIntervaloManha = []
        tempoFilaCartaoIntervaloTarde = []
        tempoFilaCartaoDuranteAulas = []

        # Tempos da fila do dinheiro para cada intervalo
        tempoFilaDinheiroAlmoco = []
        tempoFilaDinheiroIntervaloManha = []
        tempoFilaDinheiroIntervaloTarde = []
        tempoFilaDinheiroDuranteAulas = []

        # Tempos da fila do lanche para cada intervalo
        tempoFilaLancheAlmoco = []
        tempoFilaLancheIntervaloManha = []
        tempoFilaLancheIntervaloTarde = []
        tempoFilaLancheDuranteAulas = []

        recursos = dict(
            atendenteDinheiro=simpy.Resource(env, capacity=1),
            atendenteCartao=simpy.Resource(env, capacity=3),
            atendenteLanche=simpy.Resource(env, capacity=2),
            atendenteAlmoco=simpy.Resource(env, capacity=float('inf'))  # Capacidade infinita, pois não é o objetivo da simulação
        )
        env.process(chegadas(env, 'cliente', recursos, filaCartao, filaDinheiro, filaLanche,
                             tempoFilaCartaoAlmoco, tempoFilaCartaoIntervaloManha,
                             tempoFilaCartaoIntervaloTarde, tempoFilaCartaoDuranteAulas, tempoFilaDinheiroAlmoco,
                             tempoFilaDinheiroIntervaloManha,
                             tempoFilaDinheiroIntervaloTarde, tempoFilaDinheiroDuranteAulas, tempoFilaLancheAlmoco,
                             tempoFilaLancheIntervaloManha,
                             tempoFilaLancheIntervaloTarde, tempoFilaLancheDuranteAulas))
        env.run(until=50400)  # Considerado que eles trabalham de 7h as 21h, totalizando 50400 segundos

        todasfilaCartao.append(numpy.mean(filaCartao))
        todasfilaDinheiro.append(numpy.mean(filaDinheiro))
        todasfilaLanche.append(numpy.mean(filaLanche))

        todastempoFilaCartaoAlmoco.append(numpy.mean(tempoFilaCartaoAlmoco))
        todastempoFilaCartaoIntervaloManha.append(numpy.mean(tempoFilaCartaoIntervaloManha))
        todastempoFilaCartaoIntervaloTarde.append(numpy.mean(tempoFilaCartaoIntervaloTarde))
        todastempoFilaCartaoDuranteAulas.append(numpy.mean(tempoFilaCartaoDuranteAulas))

        todastempoFilaDinheiroAlmoco.append(numpy.mean(tempoFilaDinheiroAlmoco))
        todastempoFilaDinheiroIntervaloManha.append(numpy.mean(tempoFilaDinheiroIntervaloManha))
        todastempoFilaDinheiroIntervaloTarde.append(numpy.mean(tempoFilaDinheiroIntervaloTarde))
        todastempoFilaDinheiroDuranteAulas.append(numpy.mean(tempoFilaDinheiroDuranteAulas))

        todastempoFilaLancheAlmoco.append(numpy.mean(tempoFilaLancheAlmoco))
        todastempoFilaLancheIntervaloManha.append(numpy.mean(tempoFilaLancheIntervaloManha))
        todastempoFilaLancheIntervaloTarde.append(numpy.mean(tempoFilaLancheIntervaloTarde))
        todastempoFilaLancheDuranteAulas.append(numpy.mean(tempoFilaLancheDuranteAulas))

        i += 1

    print('\nTempos médios durante todo o expediente:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todasfilaDinheiro)))
    print('Fila do cartao: {}'.format(numpy.mean(todasfilaCartao)))
    print('Fila do lanche: {}'.format(numpy.mean(todasfilaLanche)))

    print('\nTempos médios durante o almoço:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroAlmoco)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoAlmoco)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheAlmoco)))

    print('\nTempos médios durante o intervalo da manhã:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroIntervaloManha)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoIntervaloManha)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheIntervaloManha)))

    print('\nTempos médios durante os intervalos da tarde:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroIntervaloTarde)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoIntervaloTarde)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheIntervaloTarde)))

    print('\nTempos médios durante o restante do dia:')
    print('Fila do dinheiro: {}'.format(numpy.mean(todastempoFilaDinheiroDuranteAulas)))
    print('Fila do cartao: {}'.format(numpy.mean(todastempoFilaCartaoDuranteAulas)))
    print('Fila do lanche: {}'.format(numpy.mean(todastempoFilaLancheDuranteAulas)))

if __name__ == "__main__":
    main()