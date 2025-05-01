from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configurar o Selenium para usar o Chrome (pode ser Firefox se quiser)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Dados de login
USERNAME = 'admin'
PASSWORD = 'admin123'

# Dados dos veículos
veiculos = [
    {"modelo": "Civic", "marca": "Honda", "ano": "2020", "placa": "ABC1D23", "cor": "Preto"},
    {"modelo": "Corolla", "marca": "Toyota", "ano": "2019", "placa": "XYZ9F87", "cor": "Branco"},
    {"modelo": "Gol", "marca": "Volkswagen", "ano": "2018", "placa": "QWE4R56", "cor": "Prata"},
    {"modelo": "Onix", "marca": "Chevrolet", "ano": "2021", "placa": "RTY7U89", "cor": "Azul"},
    {"modelo": "Fiesta", "marca": "Ford", "ano": "2017", "placa": "ASD2F34", "cor": "Vermelho"},
]

# URL da aplicação rodando localmente
URL = "http://127.0.0.1:5000/login"  # Ajuste a porta se necessário

# Inicializar o navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

try:
    # 1) Acessar o sistema e fazer login
    driver.get(URL)
    time.sleep(1)

    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[text()='Entrar']").click()

    time.sleep(2)

    # 2) Cadastrar 5 veículos
    for veiculo in veiculos:
        # Ir para a página de cadastro
        driver.find_element(By.LINK_TEXT, "Cadastrar").click()
        time.sleep(1)

        # Preencher o formulário
        driver.find_element(By.ID, "modelo").send_keys(veiculo["modelo"])
        driver.find_element(By.ID, "marca").send_keys(veiculo["marca"])
        driver.find_element(By.ID, "ano").send_keys(veiculo["ano"])
        driver.find_element(By.ID, "placa").send_keys(veiculo["placa"])
        driver.find_element(By.ID, "cor").send_keys(veiculo["cor"])

        # Submeter o formulário
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Cadastrar')]")))
        driver.find_element(By.XPATH, "//button[contains(., 'Cadastrar')]").click()
        time.sleep(2)

    # 3) Acessar a página de listagem
    driver.find_element(By.LINK_TEXT, "Listar").click()
    time.sleep(2)

    # 4) Exibir os dados dos veículos
    linhas = driver.find_elements(By.XPATH, "//tbody/tr")
    print("\nVeículos Cadastrados:")
    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        dados = [coluna.text for coluna in colunas[:6]]  # Pega as 6 primeiras colunas (sem Ações)
        print(dados)

finally:
    time.sleep(5)  # Dá tempo de ver o resultado no navegador
    driver.quit()