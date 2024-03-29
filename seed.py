from models import db,User,Feedback
from app import app

# drop and recreate tables
db.drop_all()
db.create_all()

gene = User.register(username='GeneBean',password='I<3Treats!')
augie = User.register(username='AugieChknNug',password='UnderCover$pls!')
# create a couple users
u1 = User(username=gene.username,password=gene.password,first_name='Gene',last_name='Bean',email='GeneBean@gmail.com')
u2 = User(username=augie.username,password=augie.password,first_name='Augie',last_name='Nugget',email='AugieNugget@gmail.com')

db.session.add_all([u1,u2])
db.session.commit()