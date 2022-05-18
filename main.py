from website import create_app    # website is a python package (which runs the __init__.py file)

app = create_app()                # function from __init__.py file in 'website' folder

if __name__ == '__main__':
    app.run(debug=True)           # run the flask application (we now have a running web server)
                                  # debug=True means that every time we make a change to our code, it'll rerun the web server with the changes (live update)
