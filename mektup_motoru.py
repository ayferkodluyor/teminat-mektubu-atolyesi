from datetime import date

KURUMLAR = {
    "Örnek Kent Belediyesi": {
        "Geçici": (
            "Örnek Kent Belediyesi tarafından yürütülen {is_konusu} "
            "kapsamında, {lehtar} adına {tutar} {para_birimi} "
            "tutarında geçici teminat taslağı hazırlanmıştır."
        ),
        "Kesin": (
            "{lehtar} tarafından üstlenilen {is_konusu} işinin "
            "yerine getirilmesine ilişkin {tutar} {para_birimi} "
            "tutarındaki kesin teminat için örnek metindir."
        ),
        "Avans": (
            "{is_konusu} kapsamında {lehtar} firmasına yapılması "
            "öngörülen avans ödemesine ilişkin {tutar} {para_birimi} "
            "tutarındaki örnek avans teminatı metnidir."
        ),
    },
    "Örnek Altyapı İdaresi": {
        "Geçici": (
            "{is_konusu} ihalesine katılan {lehtar} için "
            "{tutar} {para_birimi} tutarında geçici teminat "
            "örneği düzenlenmiştir."
        ),
        "Kesin": (
            "Örnek Altyapı İdaresi ile ilgili {is_konusu} "
            "çalışması kapsamında {lehtar} adına "
            "{tutar} {para_birimi} tutarında kesin teminat "
            "taslağı oluşturulmuştur."
        ),
        "Avans": (
            "{lehtar} tarafından yürütülecek {is_konusu} "
            "çalışmasına yönelik avans için {tutar} {para_birimi} "
            "tutarında örnek teminat metnidir."
        ),
    },
    "Örnek Teknoloji A.Ş.": {
        "Geçici": (
            "Örnek Teknoloji A.Ş. tarafından açılan {is_konusu} "
            "ihalesi için {lehtar} adına {tutar} {para_birimi} "
            "tutarında geçici teminat taslağı hazırlanmıştır."
        ),
        "Kesin": (
            "{lehtar} firmasının {is_konusu} kapsamındaki "
            "yükümlülükleri için {tutar} {para_birimi} "
            "tutarında örnek kesin teminat metnidir."
        ),
        "Avans": (
            "Örnek Teknoloji A.Ş. tarafından {lehtar} firmasına "
            "{is_konusu} kapsamında yapılacak avans ödemesine "
            "ilişkin {tutar} {para_birimi} tutarında örnek "
            "avans teminatı taslağıdır."
        ),
    },
}


def mektup_olustur(
    kurum: str,
    mektup_turu: str,
    lehtar: str,
    tutar: float,
    para_birimi: str,
    is_konusu: str,
    vade: date,
) -> str:
    """Seçilen kurum ve türe ait şablonu bilgilerle doldurur."""

    if kurum not in KURUMLAR:
        raise ValueError("Seçilen kurum için şablon bulunamadı.")

    if mektup_turu not in KURUMLAR[kurum]:
        raise ValueError("Seçilen mektup türü için şablon bulunamadı.")

    if not lehtar.strip() or not is_konusu.strip():
        raise ValueError("Lehtar ve işin konusu boş bırakılamaz.")

    if tutar <= 0:
        raise ValueError("Teminat tutarı sıfırdan büyük olmalıdır.")

    sablon = KURUMLAR[kurum][mektup_turu]

    metin = sablon.format(
        lehtar=lehtar.strip(),
        tutar=f"{tutar:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
        para_birimi=para_birimi,
        is_konusu=is_konusu.strip(),
    )

    return (
        f"{mektup_turu.upper()} TEMİNAT MEKTUBU — ÖRNEK TASLAK\n\n"
        f"Muhatap: {kurum}\n"
        f"Düzenleme tarihi: {date.today():%d.%m.%Y}\n"
        f"Vade tarihi: {vade:%d.%m.%Y}\n\n"
        f"{metin}\n\n"
        "EĞİTİM AMAÇLI TASLAKTIR. "
        "GEÇERLİ BİR BANKA TEMİNAT MEKTUBU DEĞİLDİR."
    )