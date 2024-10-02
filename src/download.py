import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_goes16(year,month,dom_unique):
    
    #GOES 16
    base_url = f"http://ftp.cptec.inpe.br/goes/goes16/retangular/ch13/{year:04d}/{month:02d}/"
    # #GOES 13
    # base_url = f"http://ftp.cptec.inpe.br/goes/goes13/retangular_4km/ch4_bin/{year:04d}/{month:02d}/"
    
    unique_date = f"{year}{month:02d}{dom_unique:02d}"  # Modify this with your desired maximum date
    folder_save = f"/media/hisashi/D/Banco_Dados/CPTEC/{year:04d}/{month:02d}/{dom_unique}/"
    
    if not os.path.exists(folder_save):
        os.makedirs(folder_save)
    
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    for link in soup.find_all('a'):
        file_name = link.get('href')
        if file_name == "../" or not file_name.endswith('.nc'):
            continue
        file_date = file_name.split('_')[1].split('.')[0][:8]
        

        if unique_date == file_date:
 
            local_file_path = os.path.join(folder_save, file_name)
            if not os.path.exists(local_file_path):
                file_url = urljoin(base_url, file_name)
                print("Downloading:", file_name)
                with open(os.path.join(folder_save, file_name), 'wb') as file:
                    file_response = requests.get(file_url)
                    file.write(file_response.content)
            if os.path.exists(local_file_path):
                print("File in the disk:", file_name)
                
    
    print(f"Download completed for [{year}{month:02d}{dom_unique:02d}]")