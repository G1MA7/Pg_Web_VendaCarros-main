from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime

# Configurar o Selenium para usar o Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- DADOS DE LOGIN E CADASTRO ---

# Usuário Administrador
ADMIN_USER = {
    "email": "admin@vendacarros.com",
    "password": "admin123"
}

# Novo Usuário Comum para ser cadastrado
COMMON_USER = {
    "nome_completo": "Ana Silva",
    "data_nascimento": "15-08-1995", # Formato DD-MM-AAAA
    "email": "ana.silva@emailteste.com",
    "password": "senha123"
}

# Dados dos veículos para teste
veiculos = [
    {"modelo": "Civic", "marca": "Honda", "ano": "2020", "placa": "ABC1D23", "cor": "Preto"},
    {"modelo": "Corolla", "marca": "Toyota", "ano": "2019", "placa": "XYZ9F87", "cor": "Branco"},
    {"modelo": "Gol", "marca": "Volkswagen", "ano": "2018", "placa": "QWE4R56", "cor": "Prata"},
    {"modelo": "Onix", "marca": "Chevrolet", "ano": "2021", "placa": "RTY7U89", "cor": "Azul"},
    {"modelo": "Fiesta", "marca": "Ford", "ano": "2017", "placa": "ASD2F34", "cor": "Vermelho"},
]

# URL da aplicação rodando localmente
URL = "http://127.0.0.1:5000/"

# Inicializar o navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    # =============================================================================
    # ETAPA 1: LOGIN DO ADMIN E CADASTRO DE VEÍCULOS
    # =============================================================================
    print("--- INICIANDO ETAPA 1: TAREFAS DO ADMINISTRADOR ---")
    
    # 1.1) Acessar o sistema e fazer login como administrador
    print("Acessando a página de login...")
    driver.get(URL)
    
    print("Realizando login do administrador...")
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(ADMIN_USER["email"])
    driver.find_element(By.ID, "password").send_keys(ADMIN_USER["password"])
    driver.find_element(By.XPATH, "//button[text()='Entrar']").click()
    wait.until(EC.url_contains('/listagem'))
    print("Login do admin realizado com sucesso!")

    # 1.2) Cadastrar os 5 veículos
    print("\nIniciando cadastro de veículos...")
    for i, veiculo in enumerate(veiculos):
        print(f"Cadastrando veículo {i+1}: {veiculo['marca']} {veiculo['modelo']}")
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cadastrar Veículo"))).click()
        wait.until(EC.presence_of_element_located((By.ID, "modelo")))
        
        driver.find_element(By.ID, "modelo").send_keys(veiculo["modelo"])
        driver.find_element(By.ID, "marca").send_keys(veiculo["marca"])
        driver.find_element(By.ID, "ano").send_keys(veiculo["ano"])
        driver.find_element(By.ID, "placa").send_keys(veiculo["placa"])
        driver.find_element(By.ID, "cor").send_keys(veiculo["cor"])
        driver.find_element(By.XPATH, "//button[contains(., 'Salvar Veículo')]").click()
        
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
        print("Veículo cadastrado.")

    # 1.3) Fazer logout do administrador
    print("\nRealizando logout do administrador...")
    # Clica no dropdown do usuário e depois no botão "Sair"
    wait.until(EC.element_to_be_clickable((By.ID, "navbarDropdownUser"))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sair"))).click()
    wait.until(EC.url_contains('/login'))
    print("Logout do admin realizado com sucesso!")
    print("--- ETAPA 1 CONCLUÍDA ---")


    # =============================================================================
    # ETAPA 2: CADASTRO E LOGIN DO USUÁRIO COMUM
    # =============================================================================
    print("\n--- INICIANDO ETAPA 2: TAREFAS DO USUÁRIO COMUM ---")
    
    # 2.1) Cadastrar um novo usuário comum
    print("Navegando para a página de cadastro de usuário...")
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Cadastre-se aqui"))).click()
    wait.until(EC.url_contains('/cadastro_usuario'))
    
    print(f"Cadastrando novo usuário: {COMMON_USER['email']}")
    wait.until(EC.presence_of_element_located((By.ID, "nome_completo"))).send_keys(COMMON_USER["nome_completo"])
    driver.find_element(By.ID, "data_nascimento").send_keys(COMMON_USER["data_nascimento"])
    driver.find_element(By.ID, "email").send_keys(COMMON_USER["email"])
    driver.find_element(By.ID, "password").send_keys(COMMON_USER["password"])
    driver.find_element(By.XPATH, "//button[text()='Cadastrar']").click()
    
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-success")))
    print("Usuário comum cadastrado com sucesso!")
    
    # 2.2) Fazer login como usuário comum
    print(f"Realizando login como usuário comum: {COMMON_USER['email']}")
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(COMMON_USER["email"])
    driver.find_element(By.ID, "password").send_keys(COMMON_USER["password"])
    driver.find_element(By.XPATH, "//button[text()='Entrar']").click()
    wait.until(EC.url_contains('/listagem'))
    print("Login do usuário comum realizado com sucesso!")
    

    # =============================================================================
    # ETAPA 3: VERIFICAÇÃO DO CONTROLE DE ACESSO
    # =============================================================================
    print("\n--- INICIANDO ETAPA 3: VERIFICAÇÃO DE PERMISSÕES ---")

    # 3.1) Verificar se o botão "Cadastrar Veículo" NÃO está visível
    print("Verificando se o botão 'Cadastrar Veículo' NÃO está visível...")
    botoes_cadastrar = driver.find_elements(By.LINK_TEXT, "Cadastrar Veículo")
    assert len(botoes_cadastrar) == 0, "ERRO: Botão 'Cadastrar Veículo' está visível para usuário comum!"
    print("OK: Botão 'Cadastrar Veículo' não encontrado.")

    # 3.2) Verificar se a coluna "Ações" NÃO está na tabela
    print("Verificando se a coluna 'Ações' NÃO está visível na tabela...")
    coluna_acoes = driver.find_elements(By.XPATH, "//th[text()='Ações']")
    assert len(coluna_acoes) == 0, "ERRO: Coluna 'Ações' está visível para usuário comum!"
    print("OK: Coluna 'Ações' não encontrada.")

    # 3.3) Verificar se os botões "Editar" e "Excluir" NÃO estão na página
    print("Verificando se os botões de 'Editar' e 'Excluir' NÃO estão visíveis...")
    botoes_editar = driver.find_elements(By.XPATH, "//a[contains(@class, 'btn-warning')]") # Botão Editar
    botoes_excluir = driver.find_elements(By.XPATH, "//button[contains(@class, 'btn-danger')]") # Botão Excluir
    
    assert len(botoes_editar) == 0, "ERRO: Botões de 'Editar' estão visíveis para usuário comum!"
    assert len(botoes_excluir) == 0, "ERRO: Botões de 'Excluir' estão visíveis para usuário comum!"
    print("OK: Nenhum botão de ação de administrador foi encontrado.")
    print("--- ETAPA 3 CONCLUÍDA ---")


    print("\n>>> TESTE DE CONTROLE DE ACESSO CONCLUÍDO COM SUCESSO! <<<")

finally:
    time.sleep(5)
    driver.quit()