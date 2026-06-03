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
        {"usuarios": 100, "req_s": 5350, "mediana": 130, "p95": 200, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 200, "req_s": 4494, "mediana": 220, "p95": 1300, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 600, "req_s": 6844, "mediana": 240, "p95": 3300, "falhas": 8, "taxa_falha": 0.0},
    ],
}

cenario_python_soap = {
    "nome": "Python + SOAP",
    "tipo": "Python SOAP",
    "dados": [
        {"usuarios": 100, "req_s": 4890, "mediana": 140, "p95": 250, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 200, "req_s": 4120, "mediana": 240, "p95": 1400, "falhas": 2, "taxa_falha": 0.0},
        {"usuarios": 600, "req_s": 5980, "mediana": 280, "p95": 3800, "falhas": 15, "taxa_falha": 0.01},
    ],
}

cenario_python_grpc = {
    "nome": "Python + gRPC",
    "tipo": "Python gRPC",
    "dados": [
        {"usuarios": 100, "req_s": 8920, "mediana": 80, "p95": 150, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 200, "req_s": 9340, "mediana": 140, "p95": 800, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 600, "req_s": 9880, "mediana": 180, "p95": 2500, "falhas": 5, "taxa_falha": 0.0},
    ],
}

cenario_python_graphql = {
    "nome": "Python + GraphQL",
    "tipo": "Python GraphQL",
    "dados": [
        {"usuarios": 100, "req_s": 5120, "mediana": 150, "p95": 280, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 200, "req_s": 4780, "mediana": 260, "p95": 1500, "falhas": 1, "taxa_falha": 0.0},
        {"usuarios": 600, "req_s": 6340, "mediana": 300, "p95": 4000, "falhas": 12, "taxa_falha": 0.01},
    ],
}

# ==================== TYPESCRIPT ====================
cenario_typescript_rest = {
    "nome": "TypeScript + REST",
    "tipo": "TypeScript REST",
    "dados": [
        {"usuarios": 100, "req_s": 12450, "mediana": 90, "p95": 180, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 200, "req_s": 11890, "mediana": 180, "p95": 950, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 600, "req_s": 13240, "mediana": 210, "p95": 2800, "falhas": 3, "taxa_falha": 0.0},
    ],
}

cenario_typescript_soap = {
    "nome": "TypeScript + SOAP",
    "tipo": "TypeScript SOAP",
    "dados": [
        {"usuarios": 100, "req_s": 11200, "mediana": 110, "p95": 220, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 200, "req_s": 10450, "mediana": 200, "p95": 1100, "falhas": 1, "taxa_falha": 0.0},
        {"usuarios": 600, "req_s": 11680, "mediana": 260, "p95": 3200, "falhas": 8, "taxa_falha": 0.01},
    ],
}

cenario_typescript_grpc = {
    "nome": "TypeScript + gRPC",
    "tipo": "TypeScript gRPC",
    "dados": [
        {"usuarios": 100, "req_s": 15340, "mediana": 60, "p95": 120, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 200, "req_s": 16120, "mediana": 110, "p95": 650, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 600, "req_s": 16890, "mediana": 150, "p95": 2100, "falhas": 2, "taxa_falha": 0.0},
    ],
}

cenario_typescript_graphql = {
    "nome": "TypeScript + GraphQL",
    "tipo": "TypeScript GraphQL",
    "dados": [
        {"usuarios": 100, "req_s": 11890, "mediana": 100, "p95": 200, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 200, "req_s": 11340, "mediana": 190, "p95": 1050, "falhas": 0, "taxa_falha": 0.0},
        {"usuarios": 600, "req_s": 12540, "mediana": 240, "p95": 2950, "falhas": 5, "taxa_falha": 0.0},
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


def _gerar_readme(graficos_gerados: list[dict]) -> None:
    """Gera o arquivo README.md com as imagens renderizadas organizadas por categorias."""
    caminho_readme = os.path.join(OUTPUT_DIR, "README.md")
    
    with open(caminho_readme, "w", encoding="utf-8") as f:
        f.write("# Resultados dos Testes de Carga (Streaming API)\n\n")
        f.write("Abaixo estão os gráficos comparativos considerando a **Quantidade de Usuários**.\n\n")
        
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
    # 1. Gráficos PYTHON (todos os protocolos)
    # ==========================================
    _plot_metrica_vs_usuarios(CENARIOS_PYTHON, "taxa_falha", "Taxa de Falha (%)", "Taxa de Falha vs Usuários (Python)", "python_falha", converter_pct=True)
    _plot_metrica_vs_usuarios(CENARIOS_PYTHON, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (Python)", "python_p95")
    _plot_metrica_vs_usuarios(CENARIOS_PYTHON, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (Python)", "python_rps")
    _plot_metrica_vs_usuarios(CENARIOS_PYTHON, "mediana", "Mediana (ms)", "Mediana vs Usuários (Python)", "python_mediana")
    
    configuracoes_graficos.append({
        "grupo": "1. Python (REST vs SOAP vs gRPC vs GraphQL)",
        "graficos": [
            ("Taxa de Falha", "python_falha"),
            ("Tempo de Resposta (P95)", "python_p95"),
            ("Requisições por Segundo (RPS)", "python_rps"),
            ("Mediana de Tempo de Resposta", "python_mediana")
        ]
    })

    # ==========================================
    # 2. Gráficos TYPESCRIPT (todos os protocolos)
    # ==========================================
    _plot_metrica_vs_usuarios(CENARIOS_TYPESCRIPT, "taxa_falha", "Taxa de Falha (%)", "Taxa de Falha vs Usuários (TypeScript)", "typescript_falha", converter_pct=True)
    _plot_metrica_vs_usuarios(CENARIOS_TYPESCRIPT, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (TypeScript)", "typescript_p95")
    _plot_metrica_vs_usuarios(CENARIOS_TYPESCRIPT, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (TypeScript)", "typescript_rps")
    _plot_metrica_vs_usuarios(CENARIOS_TYPESCRIPT, "mediana", "Mediana (ms)", "Mediana vs Usuários (TypeScript)", "typescript_mediana")

    configuracoes_graficos.append({
        "grupo": "2. TypeScript (REST vs SOAP vs gRPC vs GraphQL)",
        "graficos": [
            ("Taxa de Falha", "typescript_falha"),
            ("Tempo de Resposta (P95)", "typescript_p95"),
            ("Requisições por Segundo (RPS)", "typescript_rps"),
            ("Mediana de Tempo de Resposta", "typescript_mediana")
        ]
    })

    # ==========================================
    # 3. Gráficos por PROTOCOLO (Python vs TypeScript)
    # ==========================================
    _plot_metrica_vs_usuarios(CENARIOS_REST, "taxa_falha", "Taxa de Falha (%)", "Taxa de Falha vs Usuários (REST)", "rest_falha", converter_pct=True)
    _plot_metrica_vs_usuarios(CENARIOS_REST, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (REST)", "rest_p95")
    _plot_metrica_vs_usuarios(CENARIOS_REST, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (REST)", "rest_rps")

    configuracoes_graficos.append({
        "grupo": "3. REST (Python vs TypeScript)",
        "graficos": [
            ("Taxa de Falha", "rest_falha"),
            ("Tempo de Resposta (P95)", "rest_p95"),
            ("Requisições por Segundo (RPS)", "rest_rps")
        ]
    })

    _plot_metrica_vs_usuarios(CENARIOS_SOAP, "taxa_falha", "Taxa de Falha (%)", "Taxa de Falha vs Usuários (SOAP)", "soap_falha", converter_pct=True)
    _plot_metrica_vs_usuarios(CENARIOS_SOAP, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (SOAP)", "soap_p95")
    _plot_metrica_vs_usuarios(CENARIOS_SOAP, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (SOAP)", "soap_rps")

    configuracoes_graficos.append({
        "grupo": "4. SOAP (Python vs TypeScript)",
        "graficos": [
            ("Taxa de Falha", "soap_falha"),
            ("Tempo de Resposta (P95)", "soap_p95"),
            ("Requisições por Segundo (RPS)", "soap_rps")
        ]
    })

    _plot_metrica_vs_usuarios(CENARIOS_GRPC, "taxa_falha", "Taxa de Falha (%)", "Taxa de Falha vs Usuários (gRPC)", "grpc_falha", converter_pct=True)
    _plot_metrica_vs_usuarios(CENARIOS_GRPC, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (gRPC)", "grpc_p95")
    _plot_metrica_vs_usuarios(CENARIOS_GRPC, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (gRPC)", "grpc_rps")

    configuracoes_graficos.append({
        "grupo": "5. gRPC (Python vs TypeScript)",
        "graficos": [
            ("Taxa de Falha", "grpc_falha"),
            ("Tempo de Resposta (P95)", "grpc_p95"),
            ("Requisições por Segundo (RPS)", "grpc_rps")
        ]
    })

    _plot_metrica_vs_usuarios(CENARIOS_GRAPHQL, "taxa_falha", "Taxa de Falha (%)", "Taxa de Falha vs Usuários (GraphQL)", "graphql_falha", converter_pct=True)
    _plot_metrica_vs_usuarios(CENARIOS_GRAPHQL, "p95", "Tempo de Resposta P95 (ms)", "P95 vs Usuários (GraphQL)", "graphql_p95")
    _plot_metrica_vs_usuarios(CENARIOS_GRAPHQL, "req_s", "Requisições por Segundo (RPS)", "RPS vs Usuários (GraphQL)", "graphql_rps")

    configuracoes_graficos.append({
        "grupo": "6. GraphQL (Python vs TypeScript)",
        "graficos": [
            ("Taxa de Falha", "graphql_falha"),
            ("Tempo de Resposta (P95)", "graphql_p95"),
            ("Requisições por Segundo (RPS)", "graphql_rps")
        ]
    })

    # ==========================================
    # 4. Gráficos GERAIS (Todos Juntos)
    # ==========================================
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "taxa_falha", "Taxa de Falha (%)", "Visão Geral: Taxa de Falha vs Usuários", "geral_falha", converter_pct=True)
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "p95", "Tempo de Resposta P95 (ms)", "Visão Geral: P95 vs Usuários", "geral_p95")
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "req_s", "Requisições por Segundo (RPS)", "Visão Geral: RPS vs Usuários", "geral_rps")
    _plot_metrica_vs_usuarios(TODOS_CENARIOS, "mediana", "Mediana (ms)", "Visão Geral: Mediana vs Usuários", "geral_mediana")

    configuracoes_graficos.append({
        "grupo": "7. Visão Geral (Todos os Protocolos e Linguagens)",
        "graficos": [
            ("Taxa de Falha", "geral_falha"),
            ("Tempo de Resposta (P95)", "geral_p95"),
            ("Requisições por Segundo (RPS)", "geral_rps"),
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
