import pandas as pd

def client_db():
    client_db = pd.DataFrame(columns=['login', 'email', 'senha'], data=[["ppnery", "ppnery95@gmail.com", "12345"]])
    #client_db = client_db.append([["ppnery", "ppnery95@gmail.com", "12345"]])
    print(client_db)
    client_db.to_csv("client_db.csv",  sep=";")

client_db()