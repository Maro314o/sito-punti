from sito import crea_app

app = crea_app()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
