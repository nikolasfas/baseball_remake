from database.DB_connect import DBConnect
from model.team import Team


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct `year` 
                    from teams t 
                    where `year` >= '1980' """

        cursor.execute(query)

        for row in cursor:
            result.append(row['year'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID, t.`year` , t.teamCode , t.name , sum(s.salary) as salaries
                    from teams t, salaries s 
                    where t.`year` = %s
                    and s.`year` = %s
                    and t.ID = s.teamID 
                    group by t.ID, t.teamCode , t.name """

        cursor.execute(query, (year, year,))

        for row in cursor:
            result.append((Team(**row)))

        cursor.close()
        conn.close()
        return result