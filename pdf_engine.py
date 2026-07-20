import io
import re
import pdfplumber
import fitz  # PyMuPDF
import pandas as pd
from database import SessionLocal, Componente

PADRAO_CODIGO = re.compile(r'\b\d{9}\b')


def _obter_bytes(arquivo_pdf_input):
    """
    Extrai os bytes de forma segura, seja de um UploadedFile do Streamlit
    (que tem ponteiro de stream) ou de um caminho de arquivo em disco.
    Reposiciona o ponteiro no início ao final, para permitir reutilização
    do mesmo objeto de upload em chamadas subsequentes.
    """
    if hasattr(arquivo_pdf_input, 'read'):
        arquivo_pdf_input.seek(0)
        bytes_data = arquivo_pdf_input.read()
        arquivo_pdf_input.seek(0)
    else:
        with open(arquivo_pdf_input, 'rb') as f:
            bytes_data = f.read()

    if not bytes_data:
        raise ValueError("O arquivo recebido está vazio (0 bytes).")

    if not bytes_data.startswith(b"%PDF-"):
        raise ValueError(
            f"O conteúdo recebido não é um PDF válido "
            f"(assinatura encontrada: {bytes_data[:10]!r})."
        )

    return bytes_data


def mapear_enderecos_pdf(bytes_data):
    """
    Recebe BYTES (já extraídos por _obter_bytes) e relaciona cada
    código de 9 dígitos ao seu Endereço/Tipo cadastrado no banco.
    """
    db = SessionLocal()
    mapa_enderecos = {}

    try:
        with pdfplumber.open(io.BytesIO(bytes_data)) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text() or ""
                for cod in PADRAO_CODIGO.findall(texto):
                    if cod not in mapa_enderecos:
                        comp = db.query(Componente).filter(Componente.codigo == cod).first()
                        mapa_enderecos[cod] = (
                            f"{comp.endereco} ({comp.tipo})" if comp else "NÃO CADASTRADO"
                        )
    finally:
        db.close()

    return mapa_enderecos


def processar_setup_maquina(arquivo_pdf_input):
    """
    Recebe o objeto de upload do Streamlit (ou caminho de arquivo),
    e retorna um DataFrame para exibição na tela.
    """
    bytes_data = _obter_bytes(arquivo_pdf_input)
    mapa = mapear_enderecos_pdf(bytes_data)

    if not mapa:
        return None

    dados = [{"Código": k, "Endereço / Posição": v} for k, v in mapa.items()]
    return pd.DataFrame(dados)


def gerar_pdf_com_enderecos(arquivo_pdf_input):
    """
    Insere os endereços ao lado de cada código encontrado no PDF original
    e retorna os BYTES do novo PDF (para uso com st.download_button).
    Mantém o layout original do documento.
    """
    bytes_data = _obter_bytes(arquivo_pdf_input)
    mapa_enderecos = mapear_enderecos_pdf(bytes_data)

    doc = fitz.open(stream=bytes_data, filetype="pdf")

    for pagina in doc:
        palavras = pagina.get_text("words")

        for w in palavras:
            x0, y0, x1, y1, texto = w[0], w[1], w[2], w[3], w[4]
            texto = texto.strip()

            if PADRAO_CODIGO.fullmatch(texto):
                endereco = mapa_enderecos.get(texto, "NÃO CADASTRADO")
                cor = (0.86, 0.15, 0.15) if endereco == "NÃO CADASTRADO" else (0.02, 0.52, 0.83)

                pagina.insert_text(
                    (x1 + 3, y1 - 1),
                    f"-> {endereco}",
                    fontsize=6,
                    fontname="helv",
                    color=cor,
                    render_mode=0,
                )

    pdf_bytes = doc.tobytes(garbage=4, deflate=True)
    doc.close()

    return pdf_bytes
