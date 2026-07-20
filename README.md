# Smart SMT Setup Manager 

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

🔗 Acesse a aplicação em produção: smt-setup-optimizer.streamlit.app

### 🛠️ Como Testar a Aplicação (Passo a Passo)

Para validar o funcionamento completo da ferramenta, preparamos um cenário de teste interativo utilizando um arquivo PDF de exemplo disponível neste repositório.

1. Cadastre os Códigos de Teste no Sistema

Antes de processar o PDF, a aplicação precisa conhecer os códigos de componentes. Acesse o painel do sistema no Streamlit e cadastre os seguintes códigos (com seus respectivos endereços/localizações de sua escolha):

010010111

020020222

030030333

040040444

050050555

060060666

070070777

080080888

090090999

2. Baixe o PDF de Teste

Baixe o arquivo de simulação localizado na raiz deste repositório:

📥 setup.pdf (Clique no arquivo aqui no GitHub e faça o download).

3. Upload e Processamento

No menu lateral ou tela principal da aplicação Streamlit, faça o upload do arquivo setup.pdf baixado.

O sistema fará a leitura automática (OCR/Parsing) dos códigos contidos no documento.

Ele cruzará os dados do PDF com os endereços que você cadastrou no Passo 1.

4. Download do Setup Otimizado

Após o processamento, clique em Download para baixar o novo arquivo de setup gerado pelo sistema. Você verá que os códigos do PDF agora estão acompanhados de suas devidas localizações físicas de armazenamento de forma dinâmica!
