from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def get_album():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        try:
            query = """ SELECT a.id, a.title, a.artist_id, SUM(t.milliseconds) as durata
                        FROM album a, track t
                        WHERE a.id = t.album_id 
                        GROUP BY a.id, a.title, a.artist_id """

            cursor.execute(query)

            for row in cursor:
                result.append(Album(id=row["id"], title=row["title"], artist_id=row["artist_id"],durata=row["durata"]))

        except Exception as e:
            print(f"Errore in get_album: {e}")

        finally:
            cursor.close()
            conn.close()

        return result

    @staticmethod
    def get_connessioni(dict_album):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        try:
            query = """ SELECT DISTINCT t1.album_id as id1, t2.album_id as id2
                        FROM playlist_track pt1, playlist_track pt2, track t1, track t2
                        WHERE t1.id=pt1.track_id 
                          AND t2.id=pt2.track_id 
                          AND pt1.playlist_id=pt2.playlist_id 
                          AND pt1.track_id<pt2.track_id 
                          AND t1.album_id<t2.album_id
                    """
            cursor.execute(query)

            for row in cursor:
                album1 = dict_album.get(row["id1"])
                album2 = dict_album.get(row["id2"])
                if album1 is not None and album2 is not None:
                    result.append((album1, album2))

        except Exception as e:
            print(f"Errore in get_connessioni: {e}")

        finally:
                cursor.close()
                conn.close()

        return result