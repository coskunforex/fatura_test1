import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_consumption_data(csv_path, output_dir):
    data = pd.read_csv(csv_path)
    
    # Zaman sütununu indeks olarak ayarla
    data.set_index('Zaman', inplace=True)
    
    # Her sütun için grafik oluştur
    for column in data.columns:
        plt.figure()
        plt.plot(data.index, data[column], marker='o')
        plt.title(f'{column} Grafiği')
        plt.xlabel('Zaman')
        plt.ylabel(column)
        plt.xticks(rotation=45)
        plt.grid(True)
        
        # Grafik dosyasını kaydet
        output_path = os.path.join(output_dir, f'{column}_grafik.png')
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(output_path)
        plt.close()
        print(f'Grafik oluşturuldu: {output_path}')

if __name__ == "__main__":
    csv_path = 'C:/Users/cosku/fatura_test1/data/output/consumption_data.csv'
    output_dir = 'C:/Users/cosku/fatura_test1/data/output/graphs/'
    
    plot_consumption_data(csv_path, output_dir)
