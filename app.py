"""this the starting point of our flask server, that will run our website"""


from online_examination import app


if __name__ == '__main__':
    app.run(debug=True)
