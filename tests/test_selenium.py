import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class TestCadastroVeiculos(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Executa sem abrir o navegador
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("http://localhost:5000")

    def test_login_e_cadastro(self):
        # Login
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("admin123")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Verifica se está na página de listagem
        self.assertIn("Veículos Cadastrados", self.driver.page_source)
        
        # Vai para a página de cadastro
        self.driver.find_element(By.LINK_TEXT, "Novo Veículo").click()
        
        # Preenche o formulário
        self.driver.find_element(By.ID, "modelo").send_keys("Gol")
        self.driver.find_element(By.ID, "marca").send_keys("Volkswagen")
        self.driver.find_element(By.ID, "ano").send_keys("2020")
        self.driver.find_element(By.ID, "placa").send_keys("ABC1234")
        self.driver.find_element(By.ID, "cor").send_keys("Prata")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # Verifica se voltou para a listagem e se o veículo foi cadastrado
        self.assertIn("Veículos Cadastrados", self.driver.page_source)
        self.assertIn("Gol", self.driver.page_source)
        self.assertIn("ABC1234", self.driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()