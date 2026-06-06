from __future__ import annotations

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
# DADOS — SUBSTITUA APÓS CADA BATERIA DE TESTES
# ============================================================================

# ==================== PYTHON ====================
cenario_python_rest = {
    "nome": "Python + REST",
    "tipo": "Python REST",
    "dados": [
        {"usuarios": 900, "req_s": 5062, "mediana": 410, "p95": 850, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 1800, "req_s": 5188, "mediana": 380, "p95": 800, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 3600, "req_s": 5148, "mediana": 390, "p95": 810, "falhas": 0, "taxa_falha": 0.0},
    ],
}

cenario_python_soap = {
    "nome": "Python + SOAP",
    "tipo": "Python SOAP",
    "dados": [
        {"usuarios": 900, "req_s": 1599, "mediana": 2000, "p95": 3500, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 1800, "req_s": 1655, "mediana": 1900, "p95": 3300, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 3600, "req_s": 1654, "mediana": 1800, "p95": 3600, "falhas": 0, "taxa_falha": 0.0},
    ],
}

cenario_python_grpc = {
    "nome": "Python + gRPC",
    "tipo": "Python gRPC",
    "dados": [
        {"usuarios": 900, "req_s": 7052, "mediana": 12, "p95": 19, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 1800, "req_s": 7095, "mediana": 12, "p95": 18, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 3600, "req_s": 7206, "mediana": 12, "p95": 16, "falhas": 0, "taxa_falha": 0.0},
    ],
}

cenario_python_graphql = {
    "nome": "Python + GraphQL",
    "tipo": "Python GraphQL",
    "dados": [
        {"usuarios": 900, "req_s": 3282, "mediana": 730, "p95": 1600, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 1800, "req_s": 3539, "mediana": 630, "p95": 1500, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 3600, "req_s": 3572, "mediana": 650, "p95": 1400, "falhas": 0, "taxa_falha": 0.0},
    ],
}

# ==================== TYPESCRIPT ====================
cenario_typescript_rest = {
    "nome": "TypeScript + REST",
    "tipo": "TypeScript REST",
    "dados": [
        {"usuarios": 900, "req_s": 11790, "mediana": 10, "p95": 18, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 1800, "req_s": 11738, "mediana": 10, "p95": 18, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 3600, "req_s": 11780, "mediana": 9, "p95": 17, "falhas": 0, "taxa_falha": 0.0},
    ],
}

cenario_typescript_soap = {
    "nome": "TypeScript + SOAP",
    "tipo": "TypeScript SOAP",
    "dados": [
        {"usuarios": 900, "req_s": 11565, "mediana": 13, "p95": 33, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 1800, "req_s": 10672, "mediana": 23, "p95": 140, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 3600, "req_s": 11659, "mediana": 12, "p95": 28, "falhas": 0, "taxa_falha": 0.0},
    ],
}

cenario_typescript_grpc = {
    "nome": "TypeScript + gRPC",
    "tipo": "TypeScript gRPC",
    "dados": [
        {"usuarios": 900, "req_s": 8190, "mediana": 10, "p95": 13, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 1800, "req_s": 8203, "mediana": 10, "p95": 15, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 3600, "req_s": 8253, "mediana": 10, "p95": 13, "falhas": 0, "taxa_falha": 0.0},
    ],
}

cenario_typescript_graphql = {
    "nome": "TypeScript + GraphQL",
    "tipo": "TypeScript GraphQL",
    "dados": [
        {"usuarios": 900, "req_s": 9515, "mediana": 50, "p95": 200, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 1800, "req_s": 9612, "mediana": 50, "p95": 180, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 3600, "req_s": 9389, "mediana": 54, "p95": 210, "falhas": 0, "taxa_falha": 0.0},
    ],
}

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
        if cen_py:
            media_py = sum(d[metrica_chave] for d in cen_py["dados"]) / len(cen_py["dados"])
            python_medias.append(media_py)
        else:
            python_medias.append(0)

        # Busca cenário TypeScript correspondente
        cen_ts = next((c for c in cenarios if c["tipo"] == f"TypeScript {tech}"), None)
        if cen_ts:
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
    _plot_bar_chart_comparativo(TODOS_CENARIOS, "p95", "Média de P95 (ms)", "Comparação Direta: Média de Latência P95 (Python vs TypeScript)", "barras_p95")

    configuracoes_graficos.append({
        "grupo": "🏆 Resumo Executivo (Médias Gerais Lado a Lado)",
        "graficos": [
            ("Comparação de Throughput (Média de RPS)", "barras_rps"),
            ("Comparação de Latência (Média P95)", "barras_p95")
        ]
    })

    # ==========================================
    # 1. Gráficos PYTHON (todos os protocolos)
    # ==========================================
    _plot_metrica_vs_usuarios(CENARIOS_PYTHON, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (Python)", "python_p95")
    _plot_metrica_vs_usuarios(CENARIOS_PYTHON, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (Python)", "python_rps")
    _plot_metrica_vs_usuarios(CENARIOS_PYTHON, "mediana", "Mediana (ms)", "Mediana vs Usuários (Python)", "python_mediana")
    
    configuracoes_graficos.append({
        "grupo": "1. Python (REST vs SOAP vs gRPC vs GraphQL)",
        "graficos": [
            ("Tempo de Resposta (P95)", "python_p95"),
            ("Requisições por Segundo (RPS)", "python_rps"),
            ("Mediana de Tempo de Resposta", "python_mediana")
        ]
    })

    # ==========================================
    # 2. Gráficos TYPESCRIPT (todos os protocolos)
    # ==========================================
    _plot_metrica_vs_usuarios(CENARIOS_TYPESCRIPT, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (TypeScript)", "typescript_p95")
    _plot_metrica_vs_usuarios(CENARIOS_TYPESCRIPT, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (TypeScript)", "typescript_rps")
    _plot_metrica_vs_usuarios(CENARIOS_TYPESCRIPT, "mediana", "Mediana (ms)", "Mediana vs Usuários (TypeScript)", "typescript_mediana")

    configuracoes_graficos.append({
        "grupo": "2. TypeScript (REST vs SOAP vs gRPC vs GraphQL)",
        "graficos": [
            ("Tempo de Resposta (P95)", "typescript_p95"),
            ("Requisições por Segundo (RPS)", "typescript_rps"),
            ("Mediana de Tempo de Resposta", "typescript_mediana")
        ]
    })

    # ==========================================
    # 3. Gráficos por PROTOCOLO (Python vs TypeScript)
    # ==========================================
    _plot_metrica_vs_usuarios(CENARIOS_REST, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (REST)", "rest_p95")
    _plot_metrica_vs_usuarios(CENARIOS_REST, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (REST)", "rest_rps")

    configuracoes_graficos.append({
        "grupo": "3. REST (Python vs TypeScript)",
        "graficos": [
            ("Tempo de Resposta (P95)", "rest_p95"),
            ("Requisições por Segundo (RPS)", "rest_rps")
        ]
    })

    _plot_metrica_vs_usuarios(CENARIOS_SOAP, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (SOAP)", "soap_p95")
    _plot_metrica_vs_usuarios(CENARIOS_SOAP, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (SOAP)", "soap_rps")

    configuracoes_graficos.append({
        "grupo": "4. SOAP (Python vs TypeScript)",
        "graficos": [
            ("Tempo de Resposta (P95)", "soap_p95"),
            ("Requisições por Segundo (RPS)", "soap_rps")
        ]
    })

    _plot_metrica_vs_usuarios(CENARIOS_GRPC, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (gRPC)", "grpc_p95")
    _plot_metrica_vs_usuarios(CENARIOS_GRPC, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (gRPC)", "grpc_rps")

    configuracoes_graficos.append({
        "grupo": "5. gRPC (Python vs TypeScript)",
        "graficos": [
            ("Tempo de Resposta (P95)", "grpc_p95"),
            ("Requisições por Segundo (RPS)", "grpc_rps")
        ]
    })

    _plot_metrica_vs_usuarios(CENARIOS_GRAPHQL, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (GraphQL)", "graphql_p95")
    _plot_metrica_vs_usuarios(CENARIOS_GRAPHQL, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (GraphQL)", "graphql_rps")

    configuracoes_graficos.append({
        "grupo": "6. GraphQL (Python vs TypeScript)",
        "graficos": [
            ("Tempo de Resposta (P95)", "graphql_p95"),
            ("Requisições por Segundo (RPS)", "graphql_rps")
        ]
    })

    # ==========================================
    # 7. Gráficos GERAIS (Todos Juntos)
    # ==========================================
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "p95", "Tempo de Resposta P95 (ms)", "Visão Geral: P95 vs Usuários", "geral_p95")
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "req_s", "Requisições por Segundo (RPS)", "Visão Geral: RPS vs Usuários (Todos os Protocolos)", "geral_rps")
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "mediana", "Mediana (ms)", "Visão Geral: Mediana vs Usuários", "geral_mediana")

    configuracoes_graficos.append({
        "grupo": "7. Visão Geral em Linha (Todos os Protocolos e Linguagens)",
        "graficos": [
            ("Tempo de Resposta (P95)", "geral_p95"),
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