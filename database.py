from sqlalchemy import create_engine

def store_data(data):
    engine = create_engine("sqlite:///retail.db")
    data.to_sql("sales", engine, if_exists='replace', index=False)