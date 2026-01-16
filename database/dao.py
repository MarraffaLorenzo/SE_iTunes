from database.DB_connect import DBConnect
from model.album import Album

class DAO:
    @staticmethod
    def get_nodes(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.id as id, a.artist_id as artist_id,a.title as title,sum(t.milliseconds) as durata
                    FROM album a, track t
                    WHERE a.id=t.album_id 
                    GROUP BY a.id 
                    HAVING sum(t.milliseconds)> %s """

        cursor.execute(query,(durata,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni(dict_album):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT distinct t1.album_id as id1 ,t2.album_id as id2
                    FROM playlist_track pt1,playlist_track pt2, track t1, track t2
                    WHERE pt1.track_id=t1.id and pt2.track_id=t2.id
                    and pt1.playlist_id =pt2.playlist_id and t1.id < t2.id and t1.album_id <t2.album_id  """

        cursor.execute(query)

        for row in cursor:
            album1=dict_album.get(row['id1'])
            album2=dict_album.get(row['id2'])
            if album1 and album2:
                result.append((album1,album2))


        cursor.close()
        conn.close()
        return result

