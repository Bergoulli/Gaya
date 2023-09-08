import scribd_dl

with scribd_dl.ScribdDL() as session:
    session.download('https://www.scribd.com/document/352366744/', pages='1-3')
    session.download('https://www.scribd.com/document/351688288/', pages='3-5')
    for title in session.doc_titles:
        print(title)