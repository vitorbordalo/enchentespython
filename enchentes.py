# ----------------------------------------------------------------------------
# Tech Water - Sistema de Monitoramento de Enchentes
# Disciplina: Computational Thinking Using Python
# Aluno: Vitor Bordalo | RM: 561592
# Aluno: Lucas Flekner | RM: 562262
# ----------------------------------------------------------------------------

import matplotlib.pyplot as plt  # Biblioteca para gráficos
import random                    # Biblioteca para simulação de dados
import csv                       # Biblioteca para exportar alertas em CSV

# -------------------------------
# FUNÇÕES DO SISTEMA
# -------------------------------

# Valida a entrada do usuário, garantindo que seja um número real positivo e plausível
def validar_entrada(valor):
    try:
        nivel = float(valor)
        if nivel < 0:
            print("[ERRO] Nível não pode ser negativo.")
            return None
        if nivel > 20:
            print("[ERRO] Valor muito alto. Verifique se está correto (em metros).")
            return None
        return nivel
    except ValueError:
        print("[ERRO] Entrada inválida. Digite um número.")
        return None

# Simula valores de nível do rio para um sensor durante 'dias' dias
def simular_dados_sensor(dias, media=2.0, variacao=0.5):
    return [round(random.uniform(media - variacao, media + variacao), 2) for _ in range(dias)]

# Coleta dados manualmente ou por simulação
def coletar_dados_sensor(nome_sensor, dias, modo_simulacao=False):
    niveis = []
    if modo_simulacao:
        niveis = simular_dados_sensor(dias)
        print(f"\n[SENSOR SIMULADO] Dados para '{nome_sensor}': {niveis}")
    else:
        print(f"\nDigite os níveis do rio para o local '{nome_sensor}':")
        for dia in range(1, dias+1):
            while True:
                entrada = input(f"  Dia {dia}: ")
                nivel = validar_entrada(entrada)
                if nivel is not None:
                    niveis.append(nivel)
                    break
    return niveis

# Retorna uma lista com os dias que ultrapassaram o limite seguro
def analisar_alertas(niveis, limite):
    return [(i+1, nivel) for i, nivel in enumerate(niveis) if nivel > limite]

# Calcula a previsão de nível com base na média dos últimos dias
def calcular_previsao(niveis, periodo=3):
    if len(niveis) < periodo:
        return None
    return round(sum(niveis[-periodo:]) / periodo, 2)

# Exibe relatório com dados, alertas e previsão
def exibir_relatorio(nome_sensor, niveis, limite, alertas, previsao):
    print(f"\n=== Relatório do local: {nome_sensor} ===")
    print("Níveis registrados:", ", ".join([f"{n:.2f}" for n in niveis]))
    print(f"Limite seguro: {limite:.2f} m")
    if alertas:
        print("[ALERTA] Dias com risco de enchente:", ", ".join([f"Dia {d} ({v:.2f} m)" for d, v in alertas]))
    else:
        print("[OK] Nenhum risco de enchente no período.")
    if previsao is not None:
        print(f"Previsão para amanhã: {previsao:.2f} m")
        if previsao > limite:
            print("[ALERTA] Risco previsto para o próximo dia!")
        else:
            print("[OK] Previsão dentro do nível seguro.")
    else:
        print("[INFO] Não há dados suficientes para previsão.")

# Gera gráfico com os níveis, limite e pontos de alerta
def mostrar_grafico(nome_sensor, niveis, limite, alertas):
    dias = list(range(1, len(niveis)+1))
    plt.figure(figsize=(7,4))
    plt.plot(dias, niveis, marker='o', label="Nível do Rio")
    plt.axhline(limite, color='red', linestyle='--', label=f"Limite Seguro ({limite} m)")
    if alertas:
        dias_alerta, valores_alerta = zip(*alertas)
        plt.scatter(dias_alerta, valores_alerta, color='orange', label="Alerta de Risco", zorder=5)
    plt.title(f"Monitoramento - {nome_sensor}", fontsize=14, fontweight='bold')
    plt.xlabel("Dia")
    plt.ylabel("Nível do Rio (m)")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Exporta relatório completo em formato texto (.txt)
def exportar_relatorio(sensores, dados, alertas, previsoes):
    with open("relatorio_techwater.txt", "w") as f:
        f.write("Relatório de Monitoramento de Enchentes - Tech Water\n")
        f.write("# Aluno: Vitor Bordalo | RM: 561592\n")
        f.write("# Aluno: Lucas Flekner | RM: 562262\n")
        for i, sensor in enumerate(sensores):
            f.write(f"\nLocal: {sensor['nome']}\n")
            f.write("Níveis registrados: " + ", ".join([f"{v:.2f}" for v in dados[i]]) + "\n")
            f.write(f"Limite seguro: {sensor['limite']:.2f} m\n")
            if alertas[i]:
                f.write("ALERTAS: " + ", ".join([f"Dia {d} ({v:.2f} m)" for d, v in alertas[i]]) + "\n")
            else:
                f.write("Nenhum risco de enchente.\n")
            if previsoes[i] is not None:
                f.write(f"Previsão para amanhã: {previsoes[i]:.2f} m\n")
            else:
                f.write("Previsão não calculada (dados insuficientes).\n")
        f.write("\nRelatório gerado pelo sistema Tech Water.\n")

# Exporta apenas os alertas em arquivo CSV
def exportar_csv_alertas(sensores, alertas):
    with open("alertas.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Local", "Dia", "Nível"])
        for sensor, alerta in zip(sensores, alertas):
            for dia, nivel in alerta:
                writer.writerow([sensor["nome"], dia, nivel])

# -------------------------------
# CONFIGURAÇÃO DOS SENSORES
# -------------------------------

sensores = [
    {"nome": "Centro", "limite": 2.0},
    {"nome": "Zona Norte", "limite": 2.5},
    {"nome": "Zona Sul", "limite": 2.2},
    {"nome": "Bairro Industrial", "limite": 2.3}
]
dias_monitorados = 10  # Número de dias analisados

# -------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------

if __name__ == "__main__":
    print("\n💧 Tech Water – Monitoramento de Enchentes 💧")
    print("-" * 55)
    
    # Usuário escolhe se deseja simular ou inserir dados manualmente
    while True:
        escolha = input("Deseja simular os dados dos sensores? (s/n): ").strip().lower()
        if escolha in ('s', 'n'):
            break
        print("[ERRO] Opção inválida. Digite apenas 's' para sim ou 'n' para não.")

    modo_simulacao = escolha == 's'

    dados_sensores = []
    alertas_sensores = []
    previsoes_sensores = []

    # Loop que percorre todos os sensores
    for sensor in sensores:
        niveis = coletar_dados_sensor(sensor["nome"], dias_monitorados, modo_simulacao)
        alertas = analisar_alertas(niveis, sensor["limite"])
        previsao = calcular_previsao(niveis)
        dados_sensores.append(niveis)
        alertas_sensores.append(alertas)
        previsoes_sensores.append(previsao)
        exibir_relatorio(sensor["nome"], niveis, sensor["limite"], alertas, previsao)
        mostrar_grafico(sensor["nome"], niveis, sensor["limite"], alertas)

    # Geração de arquivos de saída
    exportar_relatorio(sensores, dados_sensores, alertas_sensores, previsoes_sensores)
    exportar_csv_alertas(sensores, alertas_sensores)
    print("\n[SUCESSO] Relatórios exportados: 'relatorio_techwater.txt' e 'alertas.csv'. Sistema finalizado.")