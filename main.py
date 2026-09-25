from datetime import date, timedelta
from html import escape
import json

import streamlit as st

from mektup_motoru import KURUMLAR, mektup_olustur


st.set_page_config(
    page_title="Teminat Mektubu Atölyesi",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------
# TASARIM
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 90% 0%, #1d3851 0%, transparent 36%),
            #101827;
        color: #eef4fb;
    }

    .block-container {
        max-width: 1750px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .ust-etiket {
        color: #85dbea;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 3px;
    }

    .ust-baslik {
        color: #ffffff;
        font-size: clamp(28px, 3vw, 43px);
        font-weight: 800;
        margin: 5px 0;
    }

    .ust-aciklama {
        color: #a9bdd3;
        font-size: 14px;
        margin-bottom: 20px;
    }

    .bolum-baslik {
        color: #8bddec;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
    }

    .belge-ust {
        background: #26364c;
        border: 1px solid #425772;
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 15px;
    }

    .belge-ust strong {
        color: #ffffff;
        font-size: 15px;
    }

    .belge-ust span {
        color: #b6c9dd;
        font-size: 12px;
    }

    div[data-testid="stTextArea"] textarea {
        background: #ffffff !important;
        color: #182438 !important;
        font-family: Georgia, "Times New Roman", serif !important;
        font-size: 15px !important;
        line-height: 1.9 !important;
        border: 1px solid #d7dfe8 !important;
        border-radius: 4px !important;
        padding: 34px 38px !important;
        box-shadow: 0 16px 30px rgba(0, 0, 0, 0.22);
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: #58c9dc !important;
        box-shadow: 0 0 0 2px rgba(88, 201, 220, 0.2) !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #087e96, #2563eb);
        color: #ffffff;
        border: 0;
        border-radius: 10px;
        min-height: 46px;
        font-weight: 700;
    }

    .uyari {
        background: #3b2b22;
        color: #ffd6b0;
        border: 1px solid #77513b;
        border-radius: 10px;
        padding: 11px 14px;
        font-size: 12px;
        margin-top: 12px;
    }

    .teknik-bilgi {
        background: #1b2b3f;
        border: 1px solid #354b65;
        border-radius: 10px;
        padding: 12px;
        color: #d9e6f4;
        font-size: 13px;
    }

    @media (max-width: 850px) {
        div[data-testid="stTextArea"] textarea {
            padding: 20px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# YARDIMCI FONKSİYONLAR
# --------------------------------------------------

UYARI = (
    "EĞİTİM AMAÇLI TASLAKTIR. "
    "GEÇERLİ BİR BANKA TEMİNAT MEKTUBU DEĞİLDİR."
)


def belge_bilgileri():
    """Mevcut formdaki bilgilerin anlık kopyasını döndürür."""
    return (
        st.session_state["kurum"],
        st.session_state["mektup_turu"],
        st.session_state["lehtar"],
        st.session_state["tutar"],
        st.session_state["para_birimi"],
        st.session_state["is_konusu"],
        st.session_state["vade"],
    )


def yeni_mektup_olustur():
    """Mektup motorunu çalıştırır ve metni düzenleme alanına aktarır."""
    try:
        metin = mektup_olustur(
            kurum=st.session_state["kurum"],
            mektup_turu=st.session_state["mektup_turu"],
            lehtar=st.session_state["lehtar"],
            tutar=st.session_state["tutar"],
            para_birimi=st.session_state["para_birimi"],
            is_konusu=st.session_state["is_konusu"],
            vade=st.session_state["vade"],
        )

        st.session_state["duzenlenebilir_mektup"] = metin
        st.session_state["olusturulan_bilgiler"] = belge_bilgileri()
        st.session_state["mektup_hatasi"] = ""

    except ValueError as hata:
        st.session_state["mektup_hatasi"] = str(hata)


def yazdirma_html(metin):
    """
    Düzenlenmiş mektubu ayrı bir baskı sayfasına yerleştirir.
    Metin HTML içine güvenli biçimde aktarılır.
    """
    guvenli_metin = escape(metin)

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Teminat Mektubu - Örnek Taslak</title>

<style>
@page {{
    size: A4;
    margin: 20mm;
}}

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    background: #e6eaf0;
    color: #172033;
    font-family: Georgia, "Times New Roman", serif;
}}

.toolbar {{
    background: #15243a;
    color: white;
    padding: 15px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: Arial, sans-serif;
}}

.toolbar button {{
    background: #0d92aa;
    color: white;
    border: 0;
    border-radius: 8px;
    padding: 11px 20px;
    font-weight: bold;
    cursor: pointer;
}}

.paper {{
    width: 210mm;
    min-height: 297mm;
    margin: 24px auto;
    padding: 20mm;
    background: white;
    box-shadow: 0 10px 30px rgba(0, 0, 0, .15);
}}

.document {{
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    font-size: 12pt;
    line-height: 1.65;
}}

.watermark {{
    color: #a04732;
    border-top: 1px solid #d4dce5;
    margin-top: 35px;
    padding-top: 12px;
    text-align: center;
    font: bold 9pt Arial, sans-serif;
}}

@media print {{
    body {{
        background: white;
    }}

    .toolbar {{
        display: none;
    }}

    .paper {{
        width: auto;
        min-height: auto;
        margin: 0;
        padding: 0;
        box-shadow: none;
    }}
}}
</style>
</head>

<body>

<div class="toolbar">
    <span>Örnek mektup · Baskı önizlemesi</span>
    <button onclick="window.print()">Yazdır</button>
</div>

<main class="paper">
    <div class="document">{guvenli_metin}</div>

    <div class="watermark">
        EĞİTİM AMAÇLI ÖRNEK TASLAKTIR.<br>
        GEÇERLİ BİR BANKA TEMİNAT MEKTUBU DEĞİLDİR.
    </div>
</main>

</body>
</html>"""


# --------------------------------------------------
# BAŞLANGIÇ DEĞERLERİ
# --------------------------------------------------

if "duzenlenebilir_mektup" not in st.session_state:
    st.session_state["duzenlenebilir_mektup"] = ""

if "olusturulan_bilgiler" not in st.session_state:
    st.session_state["olusturulan_bilgiler"] = None

if "mektup_hatasi" not in st.session_state:
    st.session_state["mektup_hatasi"] = ""


# --------------------------------------------------
# ÜST ALAN
# --------------------------------------------------

st.markdown(
    """
    <div class="ust-etiket">
        DOCUMENT WORKSPACE / BANKACILIK SENARYOSU
    </div>

    <div class="ust-baslik">
        Teminat Mektubu Atölyesi
    </div>

    <div class="ust-aciklama">
        Kuruma özel şablon seçimi · Düzenlenebilir belge ·
        Baskı önizlemesi · Yazdırma
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# ANA EKRAN
# --------------------------------------------------

sol, sag = st.columns([1, 1.75], gap="large")


# --------------------------------------------------
# SOL — BİLGİ GİRİŞİ
# --------------------------------------------------

with sol:
    with st.container(border=True):

        st.markdown(
            '<div class="bolum-baslik">01 / BELGE HAZIRLIĞI</div>',
            unsafe_allow_html=True,
        )

        st.selectbox(
            "Muhatap kurum",
            list(KURUMLAR.keys()),
            key="kurum",
        )

        st.radio(
            "Teminat mektubu türü",
            ["Geçici", "Kesin", "Avans"],
            horizontal=True,
            key="mektup_turu",
        )

        st.divider()

        st.text_input(
            "Lehtar firma",
            value="Örnek Yapı A.Ş.",
            key="lehtar",
        )

        st.number_input(
            "Teminat tutarı",
            min_value=0.0,
            value=250000.0,
            step=1000.0,
            key="tutar",
        )

        st.selectbox(
            "Para birimi",
            ["TL", "USD", "EUR"],
            key="para_birimi",
        )

        st.text_area(
            "İşin konusu",
            value="Örnek hizmet alımı",
            height=90,
            key="is_konusu",
        )

        st.date_input(
            "Vade tarihi",
            value=date.today() + timedelta(days=180),
            min_value=date.today(),
            format="DD.MM.YYYY",
            key="vade",
        )

        st.caption(f"Düzenleme tarihi: {date.today():%d.%m.%Y}")

        st.button(
            "✦ Mektubu oluştur",
            type="primary",
            use_container_width=True,
            on_click=yeni_mektup_olustur,
        )

        if st.session_state["mektup_hatasi"]:
            st.error(st.session_state["mektup_hatasi"])


# --------------------------------------------------
# SAĞ — DÜZENLENEBİLİR MEKTUP
# --------------------------------------------------

with sag:

    st.markdown(
        '<div class="bolum-baslik">02 / MEKTUP ÇALIŞMA SAYFASI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="belge-ust">
            <strong>📄 Düzenlenebilir örnek mektup</strong><br>
            <span>
                Soldaki bilgileri doldurup Mektubu oluştur'a basın.
                Oluşan metin üzerinde doğrudan değişiklik yapabilirsiniz.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.text_area(
        "Mektup metni",
        key="duzenlenebilir_mektup",
        height=610,
        label_visibility="collapsed",
        placeholder="Mektup metni burada oluşturulacak...",
    )

    mevcut_metin = st.session_state["duzenlenebilir_mektup"]

    bilgiler_degisti = (
        st.session_state["olusturulan_bilgiler"] is not None
        and st.session_state["olusturulan_bilgiler"] != belge_bilgileri()
    )

    if bilgiler_degisti:
        st.warning(
            "Soldaki bilgiler, son oluşturulan mektuptan farklı. "
            "Yeni bilgilerin metne yansıması için tekrar "
            "'Mektubu oluştur'a basın."
        )

    if mevcut_metin.strip():

        # Streamlit'in yerleşik indirme düğmesiyle, kullanıcının
        # düzenlediği SON METİN bir HTML dosyası olarak indirilir.
        # Dosya tarayıcıda açılınca baskı önizlemesi ve Yazdır düğmesi görünür.

        baski_sayfasi = yazdirma_html(mevcut_metin)

        st.download_button(
            "🖨 Baskı önizlemesini aç / Yazdır",
            data=baski_sayfasi.encode("utf-8"),
            file_name="teminat_mektubu_yazdir.html",
            mime="text/html",
            use_container_width=True,
            type="primary",
        )

        st.caption(
            "İndirilen HTML dosyasını tarayıcıda açın. "
            "Açılan sayfadaki Yazdır düğmesiyle çıktı alın "
            "veya PDF olarak kaydedin."
        )

    else:
        st.button(
            "🖨 Baskı önizlemesini aç / Yazdır",
            disabled=True,
            use_container_width=True,
        )

    st.markdown(
        '<div class="uyari">'
        'Bu belge eğitim amaçlı bir taslaktır. '
        'Geçerli banka teminat mektubu yerine kullanılamaz.'
        '</div>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# TEKNİK BÖLÜM
# --------------------------------------------------

st.divider()

with st.expander("⌘ Bu belge nasıl oluşturuldu?"):

    st.markdown(
        "Bu uygulamada mektup metni, seçilen kuruma ve "
        "mektup türüne ait şablondan oluşturulur."
    )

    kurum = st.session_state["kurum"]
    tur = st.session_state["mektup_turu"]

    st.markdown("**1. Şablon seçimi**")

    st.code(
        "sablon = KURUMLAR[kurum][mektup_turu]",
        language="python",
    )

    st.markdown("**2. Seçilen gerçek şablon metni**")

    st.code(
        KURUMLAR[kurum][tur],
        language="text",
    )

    st.markdown("**3. Bilgilerin şablona yerleştirilmesi**")

    st.code(
        """metin = sablon.format(
    lehtar=lehtar.strip(),
    tutar=biçimlendirilmiş_tutar,
    para_birimi=para_birimi,
    is_konusu=is_konusu.strip(),
)""",
        language="python",
    )

    st.markdown("**4. Düzenleme ve yazdırma**")

    st.write(
        "Oluşturulan metin düzenlenebilir alana aktarılır. "
        "Kullanıcının yaptığı son değişiklikler baskı sayfasına "
        "aynı metin olarak gönderilir."
    )

    st.caption(
        "Şablonların ve mektup oluşturma fonksiyonunun gerçek kodu "
        "mektup_motoru.py dosyasındadır."
    )


st.divider()

st.caption(
    "Python + Streamlit · Hayalî kurumlar ve örnek mektup metinleri · "
    "Eğitim amaçlı portföy projesi"
)