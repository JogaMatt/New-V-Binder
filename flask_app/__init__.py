from flask_bcrypt import Bcrypt
from flask import Flask, flash
import re, requests

app = Flask(__name__)

app.secret_key = "WagnerLovesCo**"