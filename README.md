The DBMS used in this program is MySQL or PostgreSQL, make sure your computer installed with MySQL/PostgreSQL

1. Modify the database username and password in config.py

For mysql: 'mysql+pymysql://root:password@127.0.0.1:3306/database_name'
For postgresql: 'postgresql://postgres:password@localhost:5433/database_name'

2. Reset elements in database by:

'''
    from app import create_app, db 
    app = create_app() 
    app.app_context().push() 
    db.create_all()

3. pip install all dependencies in the requirements.txt

4. pip install password-validator

5. pip install pymysql or pip install pygresql

6. run python wsgi.py 
