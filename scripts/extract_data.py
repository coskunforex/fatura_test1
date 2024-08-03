import camelot
import pandas as pd
import os
from glob import glob

def extract_consumption_data(pdf_path):
    # PDF'den tabloları ayıklama
    tables = camelot.read_pdf(pdf_path, pages='1', flavor='stream')

    if len(tables) > 3:
        # İlgili tabloyu seçme ve temizleme
        df = tables[3].df
        print(f"Extracted table from {pdf_path}:\n", df)  # Tabloyu yazdırarak kontrol et

        # Verileri temizleme ve doğru satır/sütunları seçme
        df = df.iloc[10:15, 1:]  # İlgili satır ve sütunları seçme
        df.columns = ['Tüm Zaman (T0)', 'Gündüz (T1)', 'Puant (T2)', 'Gece (T3)', 'Endüktif', 'Kapasitif']
        df = df.reset_index(drop=True)

        # Verileri dönüştürme
        son_endeks = pd.to_numeric(df.iloc[0].str.replace('.', '').str.replace(',', '.'), errors='coerce')
        ilk_endeks = pd.to_numeric(df.iloc[1].str.replace('.', '').str.replace(',', '.'), errors='coerce')
        tuketim = pd.to_numeric(df.iloc[2].str.replace('.', '').str.replace(',', '.'), errors='coerce')
        trafo_kaybi = pd.to_numeric(df.iloc[3].str.replace('.', '').str.replace(',', '.'), errors='coerce')
        toplam_tuketim = pd.to_numeric(df.iloc[4].str.replace('.', '').str.replace(',', '.'), errors='coerce')

        # DataFrame oluşturma
        data = {
            'Zaman': ['Son Endeks', 'İlk Endeks', '(+,-) Tüketim', 'Trafo Kaybı', 'Toplam Tüketim'],
            'Tüm Zaman (T0)': [son_endeks[0], ilk_endeks[0], tuketim[0], trafo_kaybi[0], toplam_tuketim[0]],
            'Gündüz (T1)': [son_endeks[1], ilk_endeks[1], tuketim[1], trafo_kaybi[1], toplam_tuketim[1]],
            'Puant (T2)': [son_endeks[2], ilk_endeks[2], tuketim[2], trafo_kaybi[2], toplam_tuketim[2]],
            'Gece (T3)': [son_endeks[3], ilk_endeks[3], tuketim[3], trafo_kaybi[3], toplam_tuketim[3]],
            'Endüktif': [son_endeks[4], ilk_endeks[4], tuketim[4], trafo_kaybi[4], toplam_tuketim[4]],
            'Kapasitif': [son_endeks[5], ilk_endeks[5], tuketim[5], trafo_kaybi[5], toplam_tuketim[5]]
        }

        result_df = pd.DataFrame(data)
        return result_df
    else:
        print(f"Table 3 not found in {pdf_path}")
        return pd.DataFrame(columns=['Zaman', 'Tüm Zaman (T0)', 'Gündüz (T1)', 'Puant (T2)', 'Gece (T3)', 'Endüktif', 'Kapasitif'])

def write_to_csv(data, output_csv):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    data.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Data extracted to {output_csv}")

if __name__ == "__main__":
    input_dir = 'C:/Users/cosku/fatura_test1/data/input/'
    output_csv = 'C:/Users/cosku/fatura_test1/data/output/consumption_data.csv'
    
    all_data = pd.DataFrame(columns=['Zaman', 'Tüm Zaman (T0)', 'Gündüz (T1)', 'Puant (T2)', 'Gece (T3)', 'Endüktif', 'Kapasitif'])
    for pdf_path in glob(os.path.join(input_dir, '*.pdf')):
        df = extract_consumption_data(pdf_path)
        all_data = pd.concat([all_data, df], ignore_index=True)
    
    write_to_csv(all_data, output_csv)
