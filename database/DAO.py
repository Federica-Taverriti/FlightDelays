from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO():

    @staticmethod
    def getAllAirports(): #legge tutte le righe
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
        query = """SELECT t.ID, t.IATA_CODE , count(*) as N
                    FROM (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*)
                    from airports a, flights f 
                    where a.ID = f.ORIGIN_AIRPORT_ID  
                    or a.ID = f.DESTINATION_AIRPORT_ID
                    group by a.ID, a.IATA_CODE, f.AIRLINE_ID) t
                    GROUP BY t.ID, t.IATA_CODE
                    HAVING N >= %s
                    ORDER BY N asc"""

        cursor.execute(query,(n,))

        for row in cursor:
            result.append(idMapA[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID , count(*) as peso
                    FROM flights f 
                    GROUP BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    ORDER BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID"""

        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(
                idMapA[row["ORIGIN_AIRPORT_ID"]],
                idMapA[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]))
            #result.append((idMapA[row["ORIGIN_AIRPORT_ID"]],
                          #idMapA[row["DESTINATION_AIRPORT_ID"]],
                          #row["peso"]))


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, COALESCE(t1.n,0) + COALESCE(t2.n,0) as peso
                    FROM (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID , count(*) as n
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID )t1
                    LEFT JOIN (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID , count(*) as n
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID )t2
                    ON t1.ORIGIN_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID 
                    AND t1.DESTINATION_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID 
                    WHERE t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID
                    OR t2.ORIGIN_AIRPORT_ID is Null"""

        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(
                idMapA[row["ORIGIN_AIRPORT_ID"]],
                idMapA[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]))
            # result.append((idMapA[row["ORIGIN_AIRPORT_ID"]],
            # idMapA[row["DESTINATION_AIRPORT_ID"]],
            # row["peso"]))

        cursor.close()
        conn.close()
        return result