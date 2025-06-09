from app import create_app, db
from app.models import Usuario, Veiculo
from datetime import date # Importe date

app = create_app()

@app.before_first_request
def create_tables():
    db.create_all()
    
    # Criar um usuário administrador se não existir (agora com email)
    if not Usuario.query.filter_by(email='admin@vendacarros.com').first():
        admin = Usuario(
            email='admin@vendacarros.com', 
            admin=True,
            nome_completo='Administrador',
            data_nascimento=date(2000, 1, 1) # Data de exemplo
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)