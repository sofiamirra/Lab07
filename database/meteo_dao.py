from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    """Visualizzare l'umidità media per ogni città in un determinato mese"""
    @staticmethod
    def get_umidita_media(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, AVG(Umidita) as Media 
                        FROM situazione s 
                        WHERE MONTH(Data) = %s
                        GROUP BY s.Localita"""
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(row)
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_tutti_meteo_mese(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx:
            cursor = cnx.cursor(dictionary=True)
            # Prendiamo Torino, Milano, Genova per i primi 15 giorni del mese
            query = """SELECT Localita, Data, Umidita 
                           FROM situazione 
                           WHERE MONTH(Data) = %s AND DAY(Data) <= 15
                           ORDER BY Data ASC, Localita ASC"""
            cursor.execute(query, (mese,))
            for row in cursor:
                result.append(Situazione(row["Localita"], row["Data"], row["Umidita"]))
            cursor.close()
            cnx.close()
        return result
