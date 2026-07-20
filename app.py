import streamlit as st
import pandas as pd
import base64
from database import inicializar_banco, SessionLocal, Componente
from pdf_engine import processar_setup_maquina, gerar_pdf_com_enderecos

# Garante a criação do banco de dados ao iniciar
inicializar_banco()

st.set_page_config(page_title="SMT | Gerenciador de Setup 4.0", page_icon="favicon.ico", layout="centered")

# ================= FUNDO PERSONALIZADO (IMAGEM JPG) =================
def get_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as f:
        dados = f.read()
    return base64.b64encode(dados).decode()

#CAMINHO_FUNDO = r""
#img_base64 = get_base64(CAMINHO_FUNDO)

# ================= LOGO DA EMPRESA NA SIDEBAR =================
#CAMINHO_LOGO = r""
#logo_base64 = get_base64(CAMINHO_LOGO)

#st.sidebar.markdown(f"""
#    <div style="display: flex; justify-content: flex-start; align-items: left; margin: -40px 0px 15px 0; padding: 0;">
#        <img src="data:image/png;base64,{logo_base64}" style="max-width: 170px; width: 100%; height: auto;">
#    </div>
#    <hr style="margin-top: 0; margin-bottom: 20px;">
#""", unsafe_allow_html=True)


# ================= RESTYLING TOTAL =================
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">

    <style>
        /* 1. TIPOGRAFIA GLOBAL */
        html, body, [class*="css"], [data-testid="stAppViewContainer"] {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
            color: #212529 !important;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }

        [data-testid="stSidebarCollapseButton"] button, 
        [data-testid="stSidebarExpandButton"] button {
            color: #FFFFFF !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 6px !important;
        }
        [data-testid="stSidebarCollapseButton"] button:hover, 
        [data-testid="stSidebarExpandButton"] button:hover {
            background-color: rgba(255, 255, 255, 0.25) !important;
        }

        /* 2. CABEÇALHO DA PÁGINA */
        .empresa-header {
            background: linear-gradient(90deg, #002B36 0%, #0056B3 100%) !important;
            color: #FFFFFF !important;
            padding: 20px 25px !important;
            border-radius: 8px !important;
            margin-bottom: 25px !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        }
        .empresa-header h2 {
            margin: 0 !important;
            font-weight: 700 !important;
            font-size: 1.6rem !important;
            letter-spacing: 0.5px !important;
            color: #FFFFFF !important;
        }
        .empresa-header p {
            margin: 6px 0 0 0 !important;
            font-size: 0.88rem !important;
            opacity: 0.9 !important;
            color: #E2E8F0 !important;
        }

        /* 3. SIDEBAR */
        [data-testid="stSidebar"] {
            background-color: #002B36 !important;
            border-right: 1px solid #001F28 !important;
        }
        
        [data-testid="stSidebar"] *, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
            color: #FFFFFF !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] > div {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-radius: 6px !important;
            padding: 8px 12px !important;
            margin-bottom: 6px !important;
            transition: all 0.2s !important;
        }
        [data-testid="stSidebar"] [role="radiogroup"] > div:hover {
            background-color: rgba(255, 255, 255, 0.15) !important;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.2) !important;
        }

        /* 4. BOTÕES PRIMÁRIOS */
        .stButton>button {
            background-color: #0056B3 !important;
            color: #FFFFFF !important;
            border-radius: 6px !important;
            border: 1px solid #004494 !important;
            font-weight: 600 !important;
            padding: 9px 20px !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08) !important;
        }
        .stButton>button:hover {
            background-color: #004085 !important;
            border-color: #003366 !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.18) !important;
            color: #FFFFFF !important;
        }

        /* BOTÃO VERMELHO DE EXCLUIR */
        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button,
        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:hover,
        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:focus,
        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:active,
        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:disabled {
            background-color: #DC3545 !important;
            border: 1px solid #BD2130 !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }

        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button * {
            color: #FFFFFF !important;
            opacity: 1 !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:hover {
            background-color: #B21F2D !important;
            border-color: #8f1a24 !important;
        }

        [data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:hover * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        /* 5. INPUTS, SELECTS E FORMULÁRIOS (GERAL) */
        .stTextInput input, .stSelectbox select, [data-baseweb="input"] {
            border-radius: 6px !important;
            border: 1px solid #CED4DA !important;
            background-color: #FFFFFF !important;
            color: #212529 !important;
            font-size: 0.95rem !important;
        }

        [data-testid="stSidebar"] [data-testid="stForm"],
        [data-testid="stSidebar"] [data-testid="stForm"] > div,
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"],
        [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
            overflow: visible !important;
        }

        [data-testid="stSidebar"] [data-baseweb="input"] {
            border: none !important;
            box-shadow: none !important;
            outline: 1px solid #CED4DA !important;
            outline-offset: 0px !important;
            border-radius: 6px !important;
            background-color: #FFFFFF !important;
        }

        [data-testid="stSidebar"] [data-baseweb="base-input"] {
            border: none !important;
            box-shadow: none !important;
            background-color: transparent !important;
        }

        [data-testid="stSidebar"] input {
            color: #212529 !important;
            background-color: #FFFFFF !important;
        }

        [data-testid="stSidebar"] [data-baseweb="input"]:focus-within {
            outline: 2px solid #0056B3 !important;
        }

        [data-testid="stSidebar"] [data-testid="stForm"] {
            padding-top: 6px !important;
        }

        /* 6. TABELAS E FORMULÁRIOS (ÁREA PRINCIPAL) — sem contorno/caixa */
        [data-testid="stMain"] [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.85) !important;
            border: none !important;
            box-shadow: none !important;
            border-radius: 8px !important;
            padding: 1.2rem !important;
        }

        [data-testid="stMain"] [data-testid="stDataFrame"] {
            border: none !important;
            box-shadow: none !important;
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ================= APLICA A IMAGEM DE FUNDO =================
#st.markdown(f"""
#    <style>
#        [data-testid="stAppViewContainer"] {{
#            background-image: url("data:image/jpg;base64,{img_base64}") !important;
#            background-size: cover !important;
#            background-position: center !important;
#            background-repeat: no-repeat !important;
#            background-attachment: fixed !important;
#        }}

#        /* Remove qualquer fundo/contorno do container principal */
#        [data-testid="stMain"] .block-container {{
#            background-color: transparent !important;
#            border: none !important;
#            box-shadow: none !important;
#            padding: 2rem !important;
#        }}
#    </style>
#""", unsafe_allow_html=True)

# Barra Lateral de Navegação
st.sidebar.title("📌 Navegação")
aba_selecionada = st.sidebar.radio(
    "Selecione a tela:", 
    ["Processar Setup (PDF)", "Cadastrar Componentes", "Consultar Componentes"]
)

st.sidebar.markdown("---")
st.sidebar.title("🗑️ Excluir Componentes")
with st.sidebar.form("form_deletar", clear_on_submit=True):
    codigo_deletar = st.text_input("Código para DELETAR", placeholder="Ex: 070070777").strip()
    botao_deletar = st.form_submit_button("🚨 Excluir Componente")

if botao_deletar:
    if not codigo_deletar:
        st.sidebar.error("Digite um código para deletar!")
    else:
        db = SessionLocal()
        try:
            comp_para_deletar = db.query(Componente).filter(Componente.codigo == codigo_deletar).first()
            if comp_para_deletar:
                db.delete(comp_para_deletar)
                db.commit()
                st.session_state["msg_delete"] = ("success", f"✔️ Componente '{codigo_deletar}' excluído!")
                st.rerun()
            else:
                st.session_state["msg_delete"] = ("error", f"❌ Código '{codigo_deletar}' não encontrado.")
        except Exception as e:
            st.session_state["msg_delete"] = ("error", f"Erro: {e}")
        finally:
            db.close()
            
# Exibe a mensagem salva (após o rerun ou no fluxo normal)
if "msg_delete" in st.session_state:
    tipo, texto = st.session_state.pop("msg_delete")
    if tipo == "success":
        st.sidebar.success(texto)
    else:
        st.sidebar.error(texto)

# Lista de Endereços Oficiais
lista_enderecos = [
    "Prateleira A", "Prateleira B", "Prateleira C", "Prateleira D"
]

# ================= TELA 1: PROCESSAR SETUP =================
if aba_selecionada == "Processar Setup (PDF)":
    st.markdown("""
        <div class="empresa-header">
            <h2><i class="bi bi-cpu-fill me-2"></i>SMT | Processador de Setup</h2>
            <p>Módulo de Mapeamento Automático de Endereços (Máquinas SMT)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("Arraste o PDF gerado pela máquina para mapear os endereços dos componentes.")

    arquivo_carregado = st.file_uploader("Escolha o arquivo PDF do Setup", type=["pdf"])

    if arquivo_carregado is not None:
        st.success("PDF carregado com sucesso! Cruzando informações com o Banco de Dados...")
        
        df_resultado = processar_setup_maquina(arquivo_carregado)
        
        if df_resultado is not None and not df_resultado.empty:
            st.subheader("📋 Lista Mapeada para o Operador")
            st.dataframe(df_resultado, use_container_width=True)
            
            st.markdown("---")
            st.write("### 💾 Exportar Resultado")
            
            try:
                pdf_bytes = gerar_pdf_com_enderecos(arquivo_carregado)
                st.download_button(
                    label="📄 Baixar PDF com Endereços",
                    data=pdf_bytes,
                    file_name="Setup_SMT_Original_Com_Enderecos.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erro ao gerar o PDF: {e}")
        else:
            st.warning("⚠️ Nenhum código de 9 dígitos foi encontrado dentro deste PDF.")

# ================= TELA 2: CADASTRO =================
elif aba_selecionada == "Cadastrar Componentes":
    st.markdown("""
        <div class="empresa-header">
            <h2><i class="bi bi-plus-circle-fill me-2"></i>SMT | Cadastro de Componentes</h2>
            <p>Módulo de Endereçamento de Componentes Kanban e não Kanban</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("Insira o código e selecione o endereço correspondente.")

    with st.form("form_cadastro", clear_on_submit=True):
        codigo = st.text_input("Código do Componente", placeholder="Digite os 9 números do código...").strip()
        endereco_selecionado = st.selectbox("Selecione o Endereço / Posição", options=lista_enderecos)
        botao_salvar = st.form_submit_button("Cadastrar Componente")

    if botao_salvar:
        if not codigo:
            st.error("⚠️ Por favor, digite o código do componente antes de salvar!")
        elif not codigo.isdigit():
            st.error("❌ Erro: O código deve conter APENAS números.")
        elif len(codigo) != 9:
            st.error(f"❌ Erro: O código precisa ter exatamente 9 dígitos. Você digitou {len(codigo)}.")
        else:
            if endereco_selecionado == "Kanban":
                tipo_fluxo = "Kanban"
            else:
                tipo_fluxo = "Não-Kanban"
                
            db = SessionLocal()
            try:
                componente_existente = db.query(Componente).filter(Componente.codigo == codigo).first()
                if componente_existente:
                    st.warning(f"⚠️ O componente '{codigo}' já está cadastrado no sistema!")
                else:
                    novo_item = Componente(codigo=codigo, tipo=tipo_fluxo, endereco=endereco_selecionado)
                    db.add(novo_item)
                    db.commit()
                    st.success(f"✔️ Componente '{codigo}' salvo com sucesso em '{endereco_selecionado}'!")
            except Exception as e:
                st.error(f"Erro ao salvar no banco: {e}")
            finally:
                db.close()

# ================= TELA 3: CONSULTA =================
elif aba_selecionada == "Consultar Componentes":
    st.markdown("""
        <div class="empresa-header">
            <h2><i class="bi bi-search me-2"></i>SMT | Consulta de Componentes</h2>
            <p>Visualização Geral e Busca de Componentes</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("Veja todos os itens ou busque por um código específico.")

    db = SessionLocal()
    try:
        componentes = db.query(Componente).all()
        if not componentes:
            st.info("Nenhum componente cadastrado ainda.")
        else:
            dados_tabela = []
            for c in componentes:
                dados_tabela.append({
                    "Código": c.codigo,
                    "Tipo": c.tipo,
                    "Endereço / Posição": c.endereco,
                    "Data de Cadastro": c.data_cadastro.strftime("%d/%m/%Y %H:%M")
                })
            
            df = pd.DataFrame(dados_tabela)
            busca = st.text_input("🔍 Buscar por Código", placeholder="Digite o código para filtrar...").strip()
            
            if busca:
                df_filtrado = df[df['Código'].str.contains(busca, case=False, na=False)]
                st.write(f"Resultados encontrados: {len(df_filtrado)}")
                st.dataframe(df_filtrado, use_container_width=True)
            else:
                st.write(f"Total de componentes cadastrados: {len(df)}")
                st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao consultar o banco: {e}")
    finally:
        db.close()
