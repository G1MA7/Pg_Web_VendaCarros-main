import pytest
from app import create_app, db
from app.models import Usuario, Veiculo
from datetime import date

# Importa a classe Config do seu config.py
from config import Config 

@pytest.fixture(scope='module')
def test_app():
    """
    Fixture para configurar o contexto da aplicação Flask para os testes.
    Assume que o banco de dados e os dados iniciais já foram populados
    pelo script locadora.sql.
    """
    app = create_app(Config)
    with app.app_context():
        # Apenas garante que as tabelas existem.
        # A população de dados é esperada via locadora.sql antes dos testes.
        db.create_all()  
    yield app
    # Teardown: Não é necessário um teardown complexo aqui,
    # pois os dados de teste serão excluídos dentro do próprio teste.
    pass

def test_database_integration_with_existing_data(test_app):
    """
    Testa a integração do banco de dados verificando dados existentes e
    executando operações CRUD básicas com um registro temporário.
    """
    with test_app.app_context():
        print("\n--- INICIANDO TESTE DE INTEGRAÇÃO COM O BANCO DE DADOS (DADOS EXISTENTES) ---")

        # 1. Verificar a existência do usuário administrador (populado via locadora.sql)
        print("Verificando a existência do usuário administrador...")
        admin_user = Usuario.query.filter_by(email='admin@vendacarros.com').first()
        assert admin_user is not None, "ERRO: Usuário administrador 'admin@vendacarros.com' não encontrado no banco de dados."
        assert admin_user.nome_completo == 'Administrador', "ERRO: Nome completo do admin não corresponde."
        assert admin_user.admin is True, "ERRO: Usuário admin não está marcado como administrador."
        print("OK: Usuário administrador encontrado e dados corretos.")

        # 2. Verificar a existência de veículos iniciais (populados via locadora.sql)
        print("Verificando a existência de veículos iniciais...")
        initial_vehicle_count = Veiculo.query.count()
        # O locadora.sql insere 5 veículos. Assumimos que eles estão lá.
        assert initial_vehicle_count >= 5, f"ERRO: Esperado pelo menos 5 veículos iniciais, mas encontrado {initial_vehicle_count}."
        print(f"OK: Encontrados {initial_vehicle_count} veículos iniciais (esperado >= 5).")
        
        # Verifica por um veículo específico dos dados iniciais
        civic = Veiculo.query.filter_by(placa='ABC1D23').first()
        assert civic is not None, "ERRO: Veículo 'Civic' com placa 'ABC1D23' não encontrado."
        assert civic.modelo == 'Civic', "ERRO: Modelo do Civic não corresponde."
        assert civic.marca == 'Honda', "ERRO: Marca do Civic não corresponde."
        print("OK: Veículo 'Civic' encontrado com dados corretos.")

        # --- Testes de CRUD com um registro temporário ---

        # 3. Inserir um novo veículo de teste
        print("Inserindo um novo veículo de teste...")
        new_veiculo_data = {
            "modelo": "Kombi",
            "marca": "Volkswagen",
            "ano": 1985,
            "placa": "TESTE01", # Placa única para este teste
            "cor": "Branca"
        }
        test_veiculo = Veiculo(**new_veiculo_data)
        db.session.add(test_veiculo)
        db.session.commit()
        print("OK: Novo veículo de teste adicionado ao banco de dados.")

        # 4. Recuperar o veículo recém-inserido (Teste de Leitura)
        print("Recuperando o veículo recém-inserido...")
        retrieved_veiculo = Veiculo.query.filter_by(placa="TESTE01").first()
        assert retrieved_veiculo is not None, "ERRO: Não foi possível recuperar o veículo de teste após a inserção."
        assert retrieved_veiculo.modelo == "Kombi", "ERRO: Modelo do veículo recuperado não corresponde."
        assert retrieved_veiculo.placa == "TESTE01", "ERRO: Placa do veículo recuperado não corresponde."
        print("OK: Veículo recuperado com sucesso e dados consistentes.")

        # 5. Excluir o veículo de teste
        print("Excluindo o veículo de teste...")
        db.session.delete(retrieved_veiculo)
        db.session.commit()
        
        # 6. Verificar se o veículo foi realmente excluído
        print("Verificando se o veículo de teste foi excluído...")
        deleted_veiculo = Veiculo.query.filter_by(placa="TESTE01").first()
        assert deleted_veiculo is None, "ERRO: Veículo de teste ainda presente no banco de dados após a exclusão."
        print("OK: Veículo de teste excluído com sucesso.")

        print("\n>>> TESTE DE INTEGRAÇÃO COM O BANCO DE DADOS CONCLUÍDO COM SUCESSO! <<<")