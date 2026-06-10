from __future__ import annotations

import csv
import os
from pathlib import Path

import matplotlib.pyplot as plt

# Marcadores por linha (círculo, quadrado, losango, etc.)
MARKERS_LINE = ["o", "s", "D", "p", "P", "*", "X", "h", "8", "H", "d", "+", "x", "1", "2", "3", "4"]

# ============================================================================
# PASTA DE SAÍDA
# ============================================================================
OUTPUT_DIR = "output_graphs"
Path(OUTPUT_DIR).mkdir(exist_ok=True)


# ============================================================================
# CARREGAMENTO DINÂMICO DOS DADOS DOS ARQUIVOS CSV
# ============================================================================

def load_scenario_from_csv(lang: str, tech: str) -> dict:
    """Carrega dados de teste de carga de arquivos CSV para uma linguagem e tecnologia específicas."""
    tech_folder = "graphQL" if tech.lower() == "graphql" else tech
    tech_name = "GraphQL" if tech.lower() == "graphql" else tech
    
    csv_dir = Path("csv") / lang.lower() / tech_folder
    
    dados = []
    if csv_dir.exists():
        csv_files = list(csv_dir.glob("req_*.csv"))
        def get_users_count(path: Path) -> int:
            try:
                return int(path.stem.split("_")[1])
            except (IndexError, ValueError):
                return 0
                
        csv_files.sort(key=get_users_count)
        
        for file_path in csv_files:
            users = get_users_count(file_path)
            if users == 0:
                continue
                
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    
                    req_idx = headers.index("Request Count")
                    fail_idx = headers.index("Failure Count")
                    med_idx = headers.index("Median Response Time")
                    req_s_idx = headers.index("Requests/s")
                    p90_idx = headers.index("90%")
                    
                    for row in reader:
                        if len(row) > 1 and row[1] == "Aggregated":
                            req_cnt = int(row[req_idx])
                            fail_cnt = int(row[fail_idx])
                            mediana = int(float(row[med_idx]))
                            req_s = float(row[req_s_idx])
                            p90 = int(float(row[p90_idx]))
                            taxa_falha = fail_cnt / req_cnt if req_cnt > 0 else 0.0
                            
                            dados.append({
                                "usuarios": users,
                                "req_s": round(req_s, 2),
                                "mediana": mediana,
                                "p90": p90,
                                "falhas": fail_cnt,
                                "taxa_falha": round(taxa_falha, 4)
                            })
                            break
            except Exception as e:
                print(f"Erro ao ler/processar {file_path}: {e}")
                
    lang_display = "Python" if lang.lower() == "python" else "TypeScript"
    
    return {
        "nome": f"{lang_display} + {tech_name}",
        "tipo": f"{lang_display} {tech_name}",
        "dados": dados
    }


# ==================== PYTHON ====================
cenario_python_rest = load_scenario_from_csv("python", "REST")
cenario_python_soap = load_scenario_from_csv("python", "SOAP")
cenario_python_grpc = load_scenario_from_csv("python", "gRPC")
cenario_python_graphql = load_scenario_from_csv("python", "GraphQL")

# ==================== TYPESCRIPT ====================
cenario_typescript_rest = load_scenario_from_csv("typescript", "REST")
cenario_typescript_soap = load_scenario_from_csv("typescript", "SOAP")
cenario_typescript_grpc = load_scenario_from_csv("typescript", "gRPC")
cenario_typescript_graphql = load_scenario_from_csv("typescript", "GraphQL")

# Agrupamentos solicitados
CENARIOS_PYTHON = [cenario_python_rest, cenario_python_soap, cenario_python_grpc, cenario_python_graphql]
CENARIOS_TYPESCRIPT = [cenario_typescript_rest, cenario_typescript_soap, cenario_typescript_grpc, cenario_typescript_graphql]

CENARIOS_REST = [cenario_python_rest, cenario_typescript_rest]
CENARIOS_SOAP = [cenario_python_soap, cenario_typescript_soap]
CENARIOS_GRPC = [cenario_python_grpc, cenario_typescript_grpc]
CENARIOS_GRAPHQL = [cenario_python_graphql, cenario_typescript_graphql]

TODOS_CENARIOS = [
    cenario_python_rest, cenario_python_soap, cenario_python_grpc, cenario_python_graphql,
    cenario_typescript_rest, cenario_typescript_soap, cenario_typescript_grpc, cenario_typescript_graphql
]


def _plot_metrica_vs_usuarios(cenarios: list[dict], metrica_chave: str, eixo_y_label: str, titulo: str, nome_arquivo: str, converter_pct: bool = False) -> None:
    """Gera um gráfico de linha comparando uma métrica específica pela quantidade de usuários."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    todos_usuarios = set()
    
    for idx, cenario in enumerate(cenarios):
        dados = cenario["dados"]
        usuarios = sorted({d["usuarios"] for d in dados})
        todos_usuarios.update(usuarios)
        
        valores = []
        for u in usuarios:
            val = next((d[metrica_chave] for d in dados if d["usuarios"] == u), 0)
            if converter_pct:
                val *= 100
            valores.append(val)
            
        mk = MARKERS_LINE[idx % len(MARKERS_LINE)]
        ax.plot(
            usuarios,
            valores,
            marker=mk,
            linewidth=2.5,
            markersize=9,
            label=cenario['tipo']
        )
        
    ax.set_xlabel("Quantidade de Usuários", fontsize=12, fontweight="bold")
    ax.set_ylabel(eixo_y_label, fontsize=12, fontweight="bold")
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.set_xticks(sorted(list(todos_usuarios)))
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.4, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{nome_arquivo}.png", dpi=150)
    plt.close()

def _plot_bar_chart_comparativo(cenarios: list[dict], metrica_chave: str, eixo_y_label: str, titulo: str, nome_arquivo: str) -> None:
    """Gera um gráfico de barras agrupadas comparando linguagens x tecnologias (Média da métrica)."""
    tecnologias = ["REST", "SOAP", "gRPC", "GraphQL"]
    
    python_medias = []
    ts_medias = []

    for tech in tecnologias:
        # Busca cenário Python correspondente
        cen_py = next((c for c in cenarios if c["tipo"] == f"Python {tech}"), None)
        if cen_py and len(cen_py["dados"]) > 0:
            media_py = sum(d[metrica_chave] for d in cen_py["dados"]) / len(cen_py["dados"])
            python_medias.append(media_py)
        else:
            python_medias.append(0)

        # Busca cenário TypeScript correspondente
        cen_ts = next((c for c in cenarios if c["tipo"] == f"TypeScript {tech}"), None)
        if cen_ts and len(cen_ts["dados"]) > 0:
            media_ts = sum(d[metrica_chave] for d in cen_ts["dados"]) / len(cen_ts["dados"])
            ts_medias.append(media_ts)
        else:
            ts_medias.append(0)

    x = range(len(tecnologias))
    width = 0.35

    x_py = [pos - width/2 for pos in x]
    x_ts = [pos + width/2 for pos in x]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Cores contrastantes para destacar a diferença entre as linguagens
    barras_py = ax.bar(x_py, python_medias, width, label='Python', color='#1f77b4', edgecolor='black')
    barras_ts = ax.bar(x_ts, ts_medias, width, label='TypeScript', color='#ff7f0e', edgecolor='black')

    ax.set_ylabel(eixo_y_label, fontsize=12, fontweight="bold")
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(tecnologias, fontsize=11, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.4, linestyle='--')

    # Adiciona os valores no topo das barras
    ax.bar_label(barras_py, padding=3, fmt='%.0f')
    ax.bar_label(barras_ts, padding=3, fmt='%.0f')

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{nome_arquivo}.png", dpi=150)
    plt.close()


def _gerar_readme(graficos_gerados: list[dict]) -> None:
    """Gera o arquivo README.md com as imagens renderizadas organizadas por categorias."""
    caminho_readme = os.path.join(OUTPUT_DIR, "README.md")
    
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write("# Resultados dos Testes de Carga (Streaming API)\n\n")
        f.write("Abaixo estão os gráficos comparativos considerando a **Quantidade de Usuários** e resumos gerais de **Linguagem vs Tecnologia**.\n\n")
        
        for secao in graficos_gerados:
            f.write(f"## {secao['grupo']}\n\n")
            for titulo, arquivo in secao['graficos']:
                f.write(f"### {titulo}\n")
                f.write(f"![{titulo}]({arquivo}.png)\n\n")
            f.write("---\n\n")


def main() -> None:
    print("Gerando gráficos de testes de carga...")
    
    configuracoes_graficos = []

    # ==========================================
    # 0. Gráficos de Barras (Resumo Média Geral Python vs TS)
    # ==========================================
    _plot_bar_chart_comparativo(TODOS_CENARIOS, "req_s", "Média de RPS", "Comparação Direta: Média de RPS (Python vs TypeScript)", "barras_rps")
    _plot_bar_chart_comparativo(TODOS_CENARIOS, "p90", "Média de P90 (ms)", "Comparação Direta: Média de Latência P90 (Python vs TypeScript)", "barras_p90")

    configuracoes_graficos.append({
        "grupo": "🏆 Resumo Executivo (Médias Gerais Lado a Lado)",
        "graficos": [
            ("Comparação de Throughput (Média de RPS)", "barras_rps"),
            ("Comparação de Latência (Média P90)", "barras_p90")
        ]
    })

    # ==========================================
    # 1. Gráficos PYTHON (todos os protocolos)
    # ==========================================
    _plot_metrica_vs_usuarios(CENARIOS_PYTHON, "p90", "Tempo de Resposta P90 (ms)", "P90 vs Usuários (Python)", "python_p90")
    _plot_metrica_vs_usuarios(CENARIOS_PYTHON, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (Python)", "python_rps")
    _plot_metrica_vs_usuarios(CENARIOS_PYTHON, "mediana", "Mediana (ms)", "Mediana vs Usuários (Python)", "python_mediana")
    
    configuracoes_graficos.append({
        "grupo": "1. Python (REST vs SOAP vs gRPC vs GraphQL)",
        "graficos": [
            ("Tempo de Resposta (P90)", "python_p90"),
            ("Requisições por Segundo (RPS)", "python_rps"),
            ("Mediana de Tempo de Resposta", "python_mediana")
        ]
    })

    # ==========================================
    # 2. Gráficos TYPESCRIPT (todos os protocolos)
    # ==========================================
    _plot_metrica_vs_usuarios(CENARIOS_TYPESCRIPT, "p90", "Tempo de Resposta P90 (ms)", "P90 vs Usuários (TypeScript)", "typescript_p90")
    _plot_metrica_vs_usuarios(CENARIOS_TYPESCRIPT, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (TypeScript)", "typescript_rps")
    _plot_metrica_vs_usuarios(CENARIOS_TYPESCRIPT, "mediana", "Mediana (ms)", "Mediana vs Usuários (TypeScript)", "typescript_mediana")

    configuracoes_graficos.append({
        "grupo": "2. TypeScript (REST vs SOAP vs gRPC vs GraphQL)",
        "graficos": [
            ("Tempo de Resposta (P90)", "typescript_p90"),
            ("Requisições por Segundo (RPS)", "typescript_rps"),
            ("Mediana de Tempo de Resposta", "typescript_mediana")
        ]
    })

    # ==========================================
    # 3. Gráficos por PROTOCOLO (Python vs TypeScript)
    # ==========================================
    _plot_metrica_vs_usuarios(CENARIOS_REST, "p90", "Tempo de Resposta P90 (ms)", "P90 vs Usuários (REST)", "rest_p90")
    _plot_metrica_vs_usuarios(CENARIOS_REST, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (REST)", "rest_rps")

    configuracoes_graficos.append({
        "grupo": "3. REST (Python vs TypeScript)",
        "graficos": [
            ("Tempo de Resposta (P90)", "rest_p90"),
            ("Requisições por Segundo (RPS)", "rest_rps")
        ]
    })

    _plot_metrica_vs_usuarios(CENARIOS_SOAP, "p90", "Tempo de Resposta P90 (ms)", "P90 vs Usuários (SOAP)", "soap_p90")
    _plot_metrica_vs_usuarios(CENARIOS_SOAP, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (SOAP)", "soap_rps")

    configuracoes_graficos.append({
        "grupo": "4. SOAP (Python vs TypeScript)",
        "graficos": [
            ("Tempo de Resposta (P90)", "soap_p90"),
            ("Requisições por Segundo (RPS)", "soap_rps")
        ]
    })

    _plot_metrica_vs_usuarios(CENARIOS_GRPC, "p90", "Tempo de Resposta P90 (ms)", "P90 vs Usuários (gRPC)", "grpc_p90")
    _plot_metrica_vs_usuarios(CENARIOS_GRPC, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (gRPC)", "grpc_rps")

    configuracoes_graficos.append({
        "grupo": "5. gRPC (Python vs TypeScript)",
        "graficos": [
            ("Tempo de Resposta (P90)", "grpc_p90"),
            ("Requisições por Segundo (RPS)", "grpc_rps")
        ]
    })

    _plot_metrica_vs_usuarios(CENARIOS_GRAPHQL, "p90", "Tempo de Resposta P90 (ms)", "P90 vs Usuários (GraphQL)", "graphql_p90")
    _plot_metrica_vs_usuarios(CENARIOS_GRAPHQL, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (GraphQL)", "graphql_rps")

    configuracoes_graficos.append({
        "grupo": "6. GraphQL (Python vs TypeScript)",
        "graficos": [
            ("Tempo de Resposta (P90)", "graphql_p90"),
            ("Requisições por Segundo (RPS)", "graphql_rps")
        ]
    })

    # ==========================================
    # 7. Gráficos GERAIS (Todos Juntos)
    # ==========================================
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "p90", "Tempo de Resposta P90 (ms)", "Visão Geral: P90 vs Usuários", "geral_p90")
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "req_s", "Requisições por Segundo (RPS)", "Visão Geral: RPS vs Usuários (Todos os Protocolos)", "geral_rps")
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "mediana", "Mediana (ms)", "Visão Geral: Mediana vs Usuários", "geral_mediana")

    configuracoes_graficos.append({
        "grupo": "7. Visão Geral em Linha (Todos os Protocolos e Linguagens)",
        "graficos": [
            ("Tempo de Resposta (P90)", "geral_p90"),
            ("Requisições por Segundo (RPS) - Comparação Geral", "geral_rps"),
            ("Mediana de Tempo de Resposta", "geral_mediana")
        ]
    })

    # Gerar o README
    _gerar_readme(configuracoes_graficos)

    total_graficos = sum(len(secao['graficos']) for secao in configuracoes_graficos)
    print(f"Concluído! Foram gerados {total_graficos} gráficos na pasta '{OUTPUT_DIR}'.")
    print(f"O arquivo README.md foi criado e organizado com todas as imagens.")


if __name__ == "__main__":
    main()