from flask import render_template


class HomeController:
    @classmethod
    def index(self):
        return render_template('index.html')
