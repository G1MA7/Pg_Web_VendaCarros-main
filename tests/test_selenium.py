from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configurar o Selenium para usar o Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- DADOS DE LOGIN ATUALIZADOS ---
# O login agora é feito com o email do administrador
USERNAME_ADMIN = 'admin@vendacarros.com'
PASSWORD_ADMIN = 'admin123'

# Dados dos veículos para teste
veiculos = [
    {"modelo": "Civic", "marca": "Honda", "ano": "2020", "placa": "ABC1D23", "cor": "Preto"},
    {"modelo": "Corolla", "marca": "Toyota", "ano": "2019", "placa": "XYZ9F87", "cor": "Branco"},
    {"modelo": "Gol", "marca": "Volkswagen", "ano": "2018", "placa": "QWE4R56", "cor": "Prata"},
    {"modelo": "Onix", "marca": "Chevrolet", "ano": "2021", "placa": "RTY7U89", "cor": "Azul"},
    {"modelo": "Fiesta", "marca": "Ford", "ano": "2017", "placa": "ASD2F34", "cor": "Vermelho"},
]

# URL da aplicação rodando localmente (pode ser / ou /login)
URL = "http://127.0.0.1:5000/"

# Inicializar o navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    # 1) Acessar o sistema e fazer login como administrador
    print("Acessando a página de login...")
    driver.get(URL)
    
    # --- MUDANÇA: O campo de usuário agora é 'email' ---
    print("Realizando login do administrador...")
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(USERNAME_ADMIN)
    driver.find_element(By.ID, "password").send_keys(PASSWORD_ADMIN)
    driver.find_element(By.XPATH, "//button[text()='Entrar']").click()

    # Espera a página de listagem carregar
    wait.until(EC.url_contains('/listagem'))
    print("Login realizado com sucesso!")

    # 2) Cadastrar 5 veículos
    print("\nIniciando cadastro de veículos...")
    for i, veiculo in enumerate(veiculos):
        print(f"Cadastrando veículo {i+1}: {veiculo['marca']} {veiculo['modelo']}")
        
        # --- MUDANÇA: O texto do link mudou ---
        # Ir para a página de cadastro de veículo
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cadastrar Veículo"))).click()
        
        # Espera o formulário carregar
        wait.until(EC.presence_of_element_located((By.ID, "modelo")))

        # Preencher o formulário
        driver.find_element(By.ID, "modelo").send_keys(veiculo["modelo"])
        driver.find_element(By.ID, "marca").send_keys(veiculo["marca"])
        driver.find_element(By.ID, "ano").send_keys(veiculo["ano"])
        driver.find_element(By.ID, "placa").send_keys(veiculo["placa"])
        driver.find_element(By.ID, "cor").send_keys(veiculo["cor"])

        # --- MUDANÇA: O texto do botão de submissão mudou ---
        # Submeter o formulário
        driver.find_element(By.XPATH, "//button[contains(., 'Salvar Veículo')]").click()
        
        # Espera a mensagem de sucesso e o redirecionamento para a listagem
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
        print("Veículo cadastrado.")

    # 3) Acessar a página de listagem (já estamos nela, mas podemos clicar para garantir)
    print("\nAcessando a página de listagem de veículos...")
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Listar Veículos"))).click()
    
    # 4) Exibir os dados dos veículos cadastrados
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    linhas = driver.find_elements(By.XPATH, "//tbody/tr")
    print("\n--- Veículos Cadastrados na Página ---")
    
    # Verifica se a quantidade de linhas corresponde à de veículos cadastrados
    assert len(linhas) >= len(veiculos), f"Esperado pelo menos {len(veiculos)} veículos, mas {len(linhas)} foram encontrados."
    print(f"Total de {len(linhas)} veículos encontrados na tabela.")

    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        # Pega as 6 primeiras colunas (ID, Modelo, Marca, Ano, Placa, Cor)
        dados = [coluna.text for coluna in colunas[:6]]
        print(dados)

    print("\nTeste concluído com sucesso!")

finally:
    time.sleep(5)  # Dá tempo de ver o resultado final no navegador
    driver.quit()