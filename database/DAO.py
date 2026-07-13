from database.DB_connect import DBConnect
from model.arco import Arco
from model.cliente import Cliente


class DAO():
    @staticmethod
    def getAllAlbums():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select * from album
                """

        cursor.execute(query)

        for row in cursor:
            results.append(**row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.Country as country
                from customer c 
                order by c.Country asc 
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(country):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
               select c.CustomerId, c.FirstName , c.LastName, c.Company , c.Address , c.City , c.State , c.Country , c.PostalCode, c.Phone , c.Fax , c.Email ,c.SupportRepId, sum(i.Total) as fatturatoTot
from customer c ,invoice i 
where c.CustomerId = i.CustomerId and c.Country = %s
group by c.CustomerId, c.FirstName , c.LastName, c.Company , c.Address , c.City , c.State , c.Country , c.PostalCode, c.Phone , c.Fax , c.Email, c.SupportRepId 
                """

        cursor.execute(query,(country,))

        for row in cursor:
            results.append(Cliente(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(country, idMapClienti):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct i.CustomerId id1, i2.CustomerId id2
from invoice i, invoice i2, invoiceline il , invoiceline il2 , track t , track t2, album al, album al2 , artist a, artist a2, customer c , customer c2 
where i.InvoiceId = il.InvoiceId and il.TrackId = t.TrackId and t.AlbumId = al.AlbumId and al.ArtistId = a.ArtistId
and i2.InvoiceId = il2.InvoiceId and il2.TrackId = t2.TrackId and t2.AlbumId = al2.AlbumId and al2.ArtistId = a2.ArtistId
and c.CustomerId = i.CustomerId and c.Country = %s  and c2.CustomerId = i2.CustomerId and c2.Country  = %s
and a.ArtistId = a2.ArtistId and i.CustomerId < i2.CustomerId
                """

        cursor.execute(query, (country,country))

        for row in cursor:
            results.append(Arco(idMapClienti[row["id1"]], idMapClienti[row["id2"]]))

        cursor.close()
        conn.close()
        return results