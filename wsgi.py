from app import create_app, db


app = create_app()
app.app_context().push() 
db.create_all()

# 初始化数据库
"""from app import create_app, db 

app = create_app() 
app.app_context().push() 
db.create_all()"""



if __name__ == "__main__":
    app.run(host='localhost', port=8000, threaded=False)

