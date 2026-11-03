from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta



class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(n, idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        # io qui mi devo selezionare gli aeroporti dove operano più di n compagnie
        query = """SELECT t.ID, t.IATA_CODE, count(*) as N
                    FROM (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*)
                           from airports a, flights f
                           where a.ID = f.ORIGIN_AIRPORT_ID 
                           or a.ID = f.DESTINATION_AIRPORT_ID 
                           GROUP BY a.ID, a.IATA_CODE, f.AIRLINE_ID ) t
                    GROUP BY t.ID, t.IATA_CODE
                    having N >= %s
                    order by N asc"""
        #spiegazione:
        # abbiamo un select da una from di un'altra from
        # partiamo dalla select interna:
        # select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*)
        # from airports a, flights f
        # where a.ID = f.ORIGIN_AIRPORT_ID
        # or a.ID = f.DESTINATION_AIRPORT_ID
        # mi faccio il join tra queste tabelle, join fatto per id aeroporto
        #siccome un volo ha un aeroporto partenza e destinazione metto or
        # quindi come risultato avrò una tabella con id aeroporto e id airline
        # che rappresenta TUTTI i voli
        # questi voli sono rappresentatati come aeroporto-compagnia
        # (quindi avrò righe ripetute, perchè ho più voli che partono da un determinato aeroporto con una determinata compagnia
        # magari in orari diversi)
        # e allora raggruppo per id aeroporto e id airline, e faccio il count per ognuno
        # che quindi mi dira per aeroporto id x, con la compagnia id 1, sono partiti count voli
        # poi riga sotto: per aeroporto id x, con la compagnia id 2, sono partiti count voli
        # e poi sotto magari un altro aeroporto y, e tutte le compagnie che partono da lui

        # da questa tabella faccio un group by per aeroporto e conto le righe distinte di compagnie
        # per id aeroporto
        # quindi il risultato è che per aeroporto id, ci sono tot compagnie che partono
        # di queste mi seleziono solo quelle con count maggiore di N



        cursor.execute(query, (n,))

        for row in cursor:
            result.append(idMapA[row["ID"]]) # oggetto aeroporto data la sua chiave (preso da idMap)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as peso
                       from flights f
                       group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                       order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID """

        cursor.execute(query)

        for row in cursor:
            # result.append((idMapA[row["ORIGIN_AIRPORT_ID"]],
            #                idMapA[row["DESTINATION_AIRPORT_ID"]],
            #                row["peso"]
            #                ))

            result.append(Tratta(  #oppure creo oggetto apposta (e quindi sopra accedo al risultato dalla posizione, qui con l'attributo)
                idMapA[row["ORIGIN_AIRPORT_ID"]],
                idMapA[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.ORIGIN_AIRPORT_ID , t1.DESTINATION_AIRPORT_ID , coalesce(t1.n,0) + coalesce(t1.n,0) as peso
                       FROM (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                            from flights f
                            group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                            order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t1
                       left Join (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                                  from flights f
                                  group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                                  order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t2
                       on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID 
                       and t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID 
                       where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is Null
                       """

        # ovvero:
        # dalla tabella scritta nel metodo sopra (t1)
        # faccio la join con (left join) sè stessa (t2)
        # faccio la join su (on) gli id aeroporto partenza e destinazione
        # ovvero dove t1 ha id partenza, e t2 destinazione e viceversa (perchè tratte in andata e in ritorno, e il peso dell'arco le conta tutte)
        # e poi nella selezione faccio la somma dei loro pesi (coalesce(t1.n,0) + coalesce(t1.n,0))
        # coalesce perchè se sommo un numero e un null, la somma è null,
        # quindi così gli dico se il numero è null, restituisci zero, altrimenti mi dai il numero
        # il where è per evitare i duplicati
        # e se non sono riuscito a fare la join tra i due aeroporti (magari non sono connessi) e quindi uno dei due è null


        cursor.execute(query)

        for row in cursor:
            # result.append((idMapA[row["ORIGIN_AIRPORT_ID"]],
            #                idMapA[row["DESTINATION_AIRPORT_ID"]],
            #                row["peso"]
            #                ))

            result.append(Tratta(
                idMapA[row["ORIGIN_AIRPORT_ID"]],
                idMapA[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]))

        cursor.close()
        conn.close()
        return result