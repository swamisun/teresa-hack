from app import create_app

config_name = 'development'  # os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(port=8080)
