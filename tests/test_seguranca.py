from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Configurar o Selenium para usar o Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- DADOS E CONSTANTES PARA O TESTE ---

# URL da aplicação
BASE_URL = "http://127.0.0.1:5000"

# Credenciais de um usuário válido (usaremos para testar senha errada)
VALID_USER_EMAIL = "ana.silva@emailteste.com"
VALID_USER_PASSWORD = "senha123"

# Lista de tentativas de login inválidas
INVALID_LOGIN_ATTEMPTS = [
    {
        "description": "Email correto, senha incorreta",
        "email": VALID_USER_EMAIL,
        "password": "senhaerrada"
    },
    {
        "description": "Email incorreto, senha qualquer",
        "email": "ninguem@site.com",
        "password": "123"
    },
    {
        "description": "Ambos os campos em branco (se o HTML permitir)",
        "email": "",
        "password": ""
    },
    {
        "description": "Tentativa de SQL Injection simples no email",
        "email": "'OR'1'='1'--@exemplo.com",
        "password": "qualquercoisa"
    },
    {
        "description": "Tentativa de SQL Injection simples na senha",
        "email": VALID_USER_EMAIL,
        "password": "' OR '1'='1"
    }
]


# Inicializar o navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    # =============================================================================
    # TESTE 1: TENTATIVA DE ACESSO DIRETO A UMA PÁGINA PROTEGIDA
    # =============================================================================
    print("--- INICIANDO TESTE 1: Acesso direto a /listagem sem login ---")
    
    # Tenta acessar a URL /listagem diretamente
    driver.get(f"{BASE_URL}/listagem")
    print("Tentando acessar a URL /listagem...")
    
    # VERIFICAÇÃO: A aplicação deve redirecionar para a página de cadastro
    wait.until(EC.url_contains('/cadastro_usuario'))
    print(f"OK: Redirecionado para a URL: {driver.current_url}")
    
    # VERIFICAÇÃO: A URL atual NÃO deve ser /listagem
    assert "/listagem" not in driver.current_url, "ERRO: Acesso a /listagem foi permitido sem login!"
    print("OK: Acesso a /listagem foi bloqueado.")
    
    # VERIFICAÇÃO: Deve aparecer uma mensagem flash informando o motivo
    try:
        flash_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-info"))).text
        expected_message = "Você precisa se cadastrar ou fazer login para acessar esta página."
        assert expected_message in flash_message, f"ERRO: Mensagem flash incorreta! Recebido: '{flash_message}'"
        print(f"OK: Mensagem de aviso exibida corretamente: '{flash_message}'")
    except Exception as e:
        print(f"AVISO: Não foi possível verificar a mensagem flash. {e}")

    print("--- TESTE 1 CONCLUÍDO COM SUCESSO ---\n")
    time.sleep(2)


    # =============================================================================
    # TESTE 2: TENTATIVAS DE LOGIN INVÁLIDAS
    # =============================================================================
    print("--- INICIANDO TESTE 2: Múltiplas tentativas de login inválidas ---")
    
    for attempt in INVALID_LOGIN_ATTEMPTS:
        print(f"\nTestando: {attempt['description']}")
        
        # Vai para a página de login
        driver.get(f"{BASE_URL}/login")
        wait.until(EC.presence_of_element_located((By.ID, "email")))
        
        # Preenche os campos e tenta logar
        driver.find_element(By.ID, "email").send_keys(attempt["email"])
        driver.find_element(By.ID, "password").send_keys(attempt["password"])
        driver.find_element(By.XPATH, "//button[text()='Entrar']").click()
        time.sleep(5)

        # VERIFICAÇÃO: Deve aparecer uma mensagem de erro
        try:
            error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))).text
            expected_error = "Email ou senha inválidos"
            assert expected_error in error_message, f"ERRO: Mensagem de falha no login não apareceu! Recebido: '{error_message}'"
            print(f"OK: Mensagem de erro exibida: '{error_message}'")
        except Exception as e:
            # Se a validação do HTML (required) bloquear o envio, o teste passa aqui
            if attempt["email"] == "" or attempt["password"] == "":
                 print("OK: Formulário não foi enviado com campos em branco, como esperado pela validação do HTML.")
            else:
                raise e # Se não for o caso de campos em branco, o erro é inesperado

        # VERIFICAÇÃO: O usuário NÃO deve ser redirecionado para /listagem
        assert "/listagem" not in driver.current_url, f"ERRO GRAVE: Login bem-sucedido com credenciais inválidas! ({attempt['description']})"
        print("OK: Permaneceu na página de login.")

    print("\n--- TESTE 2 CONCLUÍDO COM SUCESSO ---")


    print("\n>>> TODOS OS TESTES DE SEGURANÇA E ROBUSTEZ FORAM CONCLUÍDOS COM SUCESSO! <<<")

finally:
    time.sleep(5)
    driver.quit()