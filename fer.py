import streamlit as st
import pandas as pd

st.title("Tratamento de Planilha - Proposta Comercial")

# Upload do arquivo
file = st.file_uploader("Envie o arquivo Excel", type=["xlsx"])

if file:
    # Ler arquivo
    df_dict = pd.read_excel(file, sheet_name=None)
    df = list(df_dict.values())[0]

    # ✅ Corrigir nomes das colunas (remove espaços invisíveis)
    df.columns = df.columns.str.strip()

    st.subheader("Prévia dos dados")
    st.dataframe(df.head())

    # =========================
    # ✅ TRATAMENTO
    # =========================

    # ✅ Tratar vazios em Segmentos
    df["Segmentos"] = df["Segmentos"].replace("", pd.NA)

    # ✅ 1. Preencher Segmento pelo Usuário 

    # ✅ padronizar usuário primeiro (CORRETO)
    df["Usuário Cadastro"] = df["Usuário Cadastro"].astype(str).str.strip().str.upper()

    # ✅ MAPA FIXO (mesmo que você já fez)
    mapa = {
        "ALICE ALVES ARAUJO": "COMERCIAL",
        "ALEXSANDRO DINIZ": "COMERCIAL",
        "HIGOR CERIMAC OLIVEIRA": "COMERCIAL",
        "DANIELY FARIA DOS SANTOS": "COMERCIAL",
        "FERNANDA SILVA DE CARVALHO": "COMERCIAL",
        "GIOVANA MACEDO DE ARRUDA": "COMERCIAL",

        "ALEKSANDER RUIZ BATISTA": "ENERGIA E AUTOMAÇÃO",
        "AMANDA CAROLYNE REGO FREITAS": "ENERGIA E AUTOMAÇÃO",
        "BEATRIZ RODRIGUES DOMINGUES": "ENERGIA E AUTOMAÇÃO",
        "REBECKA MARIANE SACHARO DO PRADO": "ENERGIA E AUTOMAÇÃO",
        "VANESSA DANIELLE SALVADOR MARTINS": "ENERGIA E AUTOMAÇÃO",

        "RENATO APARECIDO CAETANO FILHO": "OUTRAS ESPECIALIDADES",
        "RAFAEL LOPES REIS": "OUTRAS ESPECIALIDADES",

        "MATHEUS JESUS": "ÓLHO E GAS",
        "REBECA EDUARDA MATA DE BARROS": "ÓLHO E GAS",

        "ERICA KYNSKOWO ALCAZAR": "AVIAÇÃO",
        "CLAUDIA APARECIDA SALINA MURTA": "AVIAÇÃO",
        "JULIANA MIGUEL DA SILVA": "AVIAÇÃO",
        "LETICIA SERRA DE ARAUJO": "AVIAÇÃO",

        "CAIO VINICIUS": "QUIMICO E PETROQUIMICO",
        "CAMILA ARRAIS MACEDO DA SILVA": "QUIMICO E PETROQUIMICO",
        "MARIA TATIANA CARNEIRO DE LIMA": "QUIMICO E PETROQUIMICO",
        "THAMIRES CARNEIRO DE SOUZA": "QUIMICO E PETROQUIMICO"
    }

    # ✅ aplicar mapeamento
    df["Segmentos"] = df["Usuário Cadastro"].map(mapa)

    # ✅ 🔥 NOVO AJUSTE (resolve None visual)
    df["Segmentos"] = df["Segmentos"].fillna("NÃO DEFINIDO")

    # ✅ validar (agora mostra só os problemáticos)
    usuarios_sem_segmento = df[df["Segmentos"] == "NÃO DEFINIDO"]["Usuário Cadastro"].unique()

    if len(usuarios_sem_segmento) > 0:
        st.warning(f"⚠️ Usuários não mapeados: {usuarios_sem_segmento}")


    # ✅ 2. Remover duplicados (mantendo o primeiro)
    df = df.drop_duplicates(subset=["Número Cotação"], keep="first")

    # ✅ 3. Tratativa Motivo rejeição (forma segura)
    col_motivo = next((c for c in df.columns if "Motivo" in c), None)

    if col_motivo:
        # ✅ padronizar texto (RESOLVE seu problema)
        df[col_motivo] = df[col_motivo].astype(str).str.strip().str.upper()

        # ✅ substituir corretamente
        df[col_motivo] = df[col_motivo].replace({
            "OUTROS": "SEM RETORNO DO CLIENTE",
            "PRAZO DE ENTREGA": "INDISPONIBILIDADE DE ATENDIMENTO",
            "VALOR DO FRETE": "PREÇO SUPERIOR AO DO CONCORRENTE"
        })

        # ✅ corrigir NAN que virou string
        df[col_motivo] = df[col_motivo].replace("NAN", pd.NA)
        
        # ✅ tratar células vazias
        df[col_motivo] = df[col_motivo].replace("", pd.NA)
        
        # ✅ padronizar status
        df["Status"] = df["Status"].astype(str).str.strip().str.upper()
        
        # ✅ preencher SOMENTE para REPROVADO sem motivo
        df.loc[
            (df["Status"] == "REPROVADO") &
            (df[col_motivo].isna()),
            col_motivo
        ] = "NÃO INCLUIU O MOTIVO DA REPROVAÇÃO"

    else:
        st.warning("⚠️ Coluna 'Motivo rejeição' não encontrada")

    # =========================
    # ✅ RESULTADO
    # =========================

    st.subheader("Planilha tratada")
    st.dataframe(df)

    # Download do arquivo tratado
    arquivo_saida = "arquivo_tratado.xlsx"
    df.to_excel(arquivo_saida, index=False)

    with open(arquivo_saida, "rb") as f:
        st.download_button(
            label="📥 Baixar Excel tratado",
            data=f,
            file_name="arquivo_tratado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
