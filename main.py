import requests
from bs4 import BeautifulSoup
import csv
import time

# Remove espaços desnecessários e organiza o texto extraído do HTML
def clean_text(text):
    return " ".join(text.split())

# Gerencia a navegação entre as páginas até que não existam mais jogos para coletar
def scrape_all_pages(base_url):
    all_games = []
    page = 1
    
    while True:
        url = f"{base_url}{page}"
        print(f"Buscando página {page}...")
        
        # Faz o download do HTML da página atual
        html_content = fetch_game_page(url)
        
        if not html_content:
            break
        
        # Extrai os dados dos jogos da página processada
        games_from_page = parse_games(html_content)
        
        # Para o loop se a página vier vazia (fim do catálogo)
        if len(games_from_page) == 0:
            print(f"\nFim de linha! Nenhuma oferta encontrada na página {page}.")
            break
        
        print(f"Página {page}: {len(games_from_page)} jogos extraídos.")
        
        # Junta os jogos desta página na lista principal
        all_games.extend(games_from_page)
        page += 1
        
        # Pausa para evitar bloqueio do servidor (Request Throttle)
        time.sleep(1.5)
        
    return all_games
        
# Configura e executa a requisição HTTP para obter o conteúdo do site
def fetch_game_page(url):
    # Simula um navegador real para evitar ser barrado pelo site
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Trava o erro caso o status code não seja 200
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Ocorreu um erro ao acessar o site: {e}")
        return None
        
# Varre o HTML buscando as tags específicas de nome e preço dos jogos
def parse_games(soup):
    save_game_list = []

    # Localiza todos os containers de produtos na grade da página
    cards = soup.find_all('div', class_='grid-col-6 grid-col-sm-4 grid-col-md-4 grid-col-lg-3')
    
    for jogo in cards:
        title_element = jogo.find('h3', class_='game-card__product-name') 
        if (title_element):
            title_game = clean_text(title_element.text)
            price_game = jogo.find('span', class_='product-price--val')
            
            # Tenta pegar o preço original (antes do desconto)
            old_price_element = price_game.find('span', class_='product-price--old')
            old_price = old_price_element.text.strip() if old_price_element else "N/A"
            
            # Remove o preço antigo do HTML para isolar o preço atual/promocional
            if old_price_element:
                old_price_element.decompose()
                
            # Organiza os dados em um dicionário para facilitar o salvamento
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

# Cria o arquivo CSV e salva as informações coletadas com encoding para Excel
def save_csv(games_list):
    if not games_list:
        print("Nenhum jogo com oferta para salvar.")
        return
    
    columns = ["Título", "Preço Antigo", "Preço com Oferta"]
    try:
        # utf-8-sig garante que acentos e símbolos de moeda apareçam certo no Excel
        with open('ofertas_nuuvem.csv', 'w', newline='', encoding='utf-8-sig') as archive:
            writer = csv.DictWriter(archive, fieldnames=columns)
            writer.writeheader()
            writer.writerows(games_list)
        print(f"\nRelatório com {len(games_list)} jogos salvos com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")

# Ponto de entrada que inicia o fluxo do programa
if __name__ == "__main__":
    my_url = "https://www.nuuvem.com/br-pt/catalog/price/promo/sort/bestselling/sort-mode/desc/page/"
    print("Iniciando o PyLoot - Raspagem de Ofertas...")
    
    # Chama a função de varredura e armazena o resultado total
    games = scrape_all_pages(my_url)
    if games:
        save_csv(games)
        print("Processo concluído! Verifique o arquivo ofertas_nuuvem.csv para os detalhes.")