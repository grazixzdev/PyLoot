import requests
from bs4 import BeautifulSoup
import csv
import time

def clean_text(text):
    return " ".join(text.split())

def scrape_all_pages(base_url):
    all_games = []
    page = 1
    
    while True:
        url = f"{base_url}{page}"
        print(f"Buscando página {page}...")
        
        html_content = fetch_game_page(url)
        
        if not html_content:
            break
        
        games_from_page = parse_games(html_content)
        
        if len(games_from_page) == 0:
            print(f"\nFim de linha! Nenhuma oferta encontrada na página {page}.")
            break
        
        print(f"Página {page}: {len(games_from_page)} jogos extraídos.")
        
        all_games.extend(games_from_page)
        page += 1
        time.sleep(1.5)
        
    return all_games
        

def fetch_game_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Ocorreu um erro ao acessar o site: {e}")
        return None
        

def parse_games(soup):
    save_game_list = []

    cards = soup.find_all('div', class_='grid-col-6 grid-col-sm-4 grid-col-md-4 grid-col-lg-3')
    
    for jogo in cards:
        title_element = jogo.find('h3', class_='game-card__product-name') 
        if (title_element):
            title_game = clean_text(title_element.text)
            price_game = jogo.find('span', class_='product-price--val')
            old_price_element = price_game.find('span', class_='product-price--old')
            old_price = old_price_element.text.strip() if old_price_element else "N/A"
            
            if old_price_element:
                old_price_element.decompose()
                
            save_game_list.append({
                'Título': title_game,
                'Preço Antigo': old_price,
                'Preço com Oferta': price_game.text.strip()
            })
            
            print(f"Processando {len(save_game_list)}/{len(cards)}: {title_game}...")
        else:
            print("Não foi possível carregar o título do jogo.")
            
        print("-" * 30) 
        
    return save_game_list
                
def save_csv(games_list):
    if not games_list:
        print("Nenhum jogo para salvar.")
        return
    
    columns = ["Título", "Preço Antigo", "Preço com Oferta"]
    try:
        with open('ofertas_nuuvem.csv', 'w', newline='', encoding='utf-8-sig') as archive:
            writer = csv.DictWriter(archive, fieldnames=columns)
            writer.writeheader()
            writer.writerows(games_list)
        print(f"\nRelatório com {len(games_list)} jogos salvos com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")
        
if __name__ == "__main__":
    my_url = "https://www.nuuvem.com/br-pt/catalog/price/promo/sort/bestselling/sort-mode/desc/page/"
    print("Iniciando o PyLoot - Raspagem de Ofertas...")
    
    games = scrape_all_pages(my_url)
    if games:
        save_csv(games)
        print("Processo concluído! Verifique o arquivo ofertas_nuuvem.csv para os detalhes.")
    
    
    