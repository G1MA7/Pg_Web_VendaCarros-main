from app import create_app, db
from app.models import Usuario, Veiculo

app = create_app()

@app.before_request
def create_tables():
    db.create_all()
    
    # Criar um usuário administrador se não existir
    if not Usuario.query.filter_by(username='admin').first():
        admin = Usuario(username='admin', admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)