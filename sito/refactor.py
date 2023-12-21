import pandas as pd
from pathlib import Path
from os import path
from . import db
from .modelli import User, Classi
def refactor_file():

    name_file=path.join(Path.cwd(),'instance','foglio.xlsx')

    file=pd.read_excel(name_file)
    file['Data'] = pd.to_datetime(file['Data']) 
    for x in file.values.tolist():
        print(x)

  

