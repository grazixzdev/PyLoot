# PyLoot - Web Scraper de Ofertas (Nuuvem)



O **PyLoot** é uma ferramenta de automação desenvolvida em Python para minerar dados de ofertas de jogos no site Nuuvem. O script navega pelo catálogo, extrai informações de preços e organiza tudo em um arquivo estruturado para análise.



Este projeto foi construído para consolidar conhecimentos da matéria de **Programação de Computadores**, focando em requisições HTTP, manipulação de HTML e persistência de dados.



---

<div class="languages-svg" align="center">
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="PYTHON" width="50px">
</div>


## 🛠️ Tecnologias e Bibliotecas



*   **Python 3.x**: Linguagem principal.

*   **Requests**: Para comunicação com o servidor e download das páginas.

*   **BeautifulSoup4**: Para o parsing (análise) do HTML e navegação na árvore de elementos.

*   **CSV**: Para a geração de relatórios estruturados.

*   **Time**: Para controle de fluxo e respeito aos limites do servidor.



---



## Funcionalidades Técnicas



### 1. Paginação Dinâmica

Diferente de scripts básicos, o PyLoot utiliza um laço `while True` que identifica automaticamente o fim do catálogo, permitindo extrair centenas de jogos sem intervenção manual.



### 2. Extração Inteligente (Scraping)

O script localiza os seletores CSS específicos dos cards de jogos e realiza um tratamento de dados:

- **Limpeza de texto:** Remove quebras de linha e espaços excedentes.

- **Isolamento de Preços:** Utiliza o método `.decompose()` do BeautifulSoup para separar o preço original do preço promocional, evitando sujeira nos dados.



### 3. Ética e Resiliência

- **User-Agent:** O script envia headers que identificam a requisição de forma amigável ao site.

- **Request Throttling:** Implementação de `time.sleep(1.5)` para evitar sobrecarga no servidor alvo (previne banimentos de IP).

- **Tratamento de Erros:** Blocos `try/except` e `raise_for_status()` garantem que o programa informe erros de conexão sem travar.



---



## Como Instalar e Rodar



1. **Clone este repositório:**

   ```bash

   git clone https://github.com/grazixzdev/PyLoot

   ```


2. **Acesse a pasta:**

   ```bash

   cd PyLoot

   ```


3. **Instale as dependências necessárias:**

   ```bash

   pip install requests beautifulsoup4

   ```


4. **Execute o minerador:**

   ```bash

   python main.py

   ```


---

## 📊 Exemplo de Saída (CSV)


Após a execução, o arquivo `ofertas_nuuvem.csv` será gerado com o seguinte formato:



| Título | Preço Antigo | Preço com Oferta |
| :--- | :---: | :---: |
| **Elden Ring** | R$ 229,90 | R$ 149,43 |
| **Resident Evil 4** | R$ 199,00 | R$ 99,50 |
| **Monster Hunter Rise** | R$ 139,90 | R$ 34,97 |
| **Street Fighter 6** | R$ 249,00 | R$ 124,50 |



---



## 💡 Aprendizados Adquiridos



*   **Manipulação de DOM (Document Object Model):** Localização de elementos específicos através de tags e classes HTML.

*   **Requisições HTTP:** Entendimento de métodos `GET` e tratamento de *status codes* para garantir a integridade da conexão.

*   **Encoding (utf-8-sig):** Implementação de codificação específica para garantir a compatibilidade de caracteres especiais e símbolos de moeda no **Microsoft Excel**.

*   **Modularização:** Estruturação do código em funções independentes, facilitando a manutenção e leitura.



---



## 👤 Autor



Desenvolvido por **Graziela Lucena**.  

Sinta-se à vontade para entrar em contato ou dar um *fork* no projeto!



> *Este projeto tem fins puramente educacionais.*
