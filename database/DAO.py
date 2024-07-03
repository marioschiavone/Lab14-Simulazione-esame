from database.DB_connect import DBConnect
from model.genes import Gene


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from genes"""

        cursor.execute(query)

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllChromosomes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = '''select distinct Chromosome from genes where Chromosome!=0'''
        cursor.execute(query)

        for row in cursor:
            result.append(row["Chromosome"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnectedGenes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = '''select g1.GeneID as Gene1, g2.GeneID as Gene2, g1.Chromosome, g2.Chromosome, i.Expression_Corr 
                    from interactions i, genes g1, genes g2
                    where g1.GeneID=i.GeneID1 and g2.GeneID=i.GeneID2 
                    and g1.Chromosome!=g2.Chromosome 
                    and g1.Chromosome>0
                    and g2.Chromosome>0
                    group by g1.GeneID, g2.GeneID'''
        cursor.execute(query)

        for row in cursor:
            result.append((row["Gene1"], row["Gene2"], row["Expression_Corr"]))

        cursor.close()
        conn.close()
        return result

