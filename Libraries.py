import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
import logging
import pymysql
from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy import text
from sqlalchemy import insert
import configparser
from tqdm import tqdm
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
import os
from sqlalchemy.sql import text
import re
print('hello')