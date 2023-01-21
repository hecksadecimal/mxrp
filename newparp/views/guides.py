import requests
from flask import render_template


def user_guide():
    return render_template("guides/user_guide.html")

def bbcode_guide():
    return render_template("guides/bbcode_guide.html")

def privacy():
    return render_template("guides/privacy.html")

def site_rules():
    return render_template("guides/rules.html")

def tos():
    return render_template("guides/tos.html")
