from app import *
from models.user import User
from models.recipe import Recipe

app=create_app()
app.app_context().push()
user = User(username='Marion', email='marion@gmail.com', password='WkQa')
db.session.add(user)
db.session.commit()
user = User.query.filter_by(username='johanna').first()
print(user.recipes)