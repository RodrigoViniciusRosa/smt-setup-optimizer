# Smart SMT Setup Manager 🚀

Um sistema inteligente para otimização de setup físico em linhas de montagem de placas eletrônicas (SMT - Surface Mount Technology).

Este projeto automatiza o cruzamento de relatórios de programação de máquinas (gerados em PDF) com o banco de dados físico de posições de estoque (Kanban e Não-Kanban), reduzindo o tempo de máquina parada e mitigando erros humanos de separação.

## 📊 Resultados e Impacto de Negócio (ROI)
* **-20%** de tempo de setup na Fase 1 (validação da hipótese com protótipo em planilhas/VBA).
* **-35%** de redução consolidada de tempo na Fase 2 (aplicação Web Python integrada e automatizada).
* Eliminação completa de anotações manuais e transcrições físicas por parte dos operadores.

## 🛠️ Tecnologias Utilizadas
* **Frontend/Interface:** Python & Streamlit (UI interativa e ágil).
* **Engine de Processamento de PDF:** `pdfplumber` (extração lógica de dados do PDF original) e `PyMuPDF` / `fitz` (injeção direta de coordenadas e reescrita de endereços no PDF de saída).
* **Banco de Dados:** SQLite integrado via ORM SQLAlchemy.
* **Segurança e Arquitetura:** Revisão lógica auxiliada por Inteligência Artificial para prevenção de vazamento de conexões (session leaks), resolução de loops redundantes de consultas SQL (problema N+1) e otimização de performance.