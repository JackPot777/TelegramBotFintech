from abc import ABC, abstractmethod
import database.DataBase as DB
import configuration.public as publ


class Table(ABC):

    # Variables to be implemented in each subclass

    name = NotImplemented
    creationQuery = NotImplemented

    instance = DB.instance

    # Most used sql statements format
    TypicalWhereSelect = "select {} from {} where {} = '{}'"
    TypicalUpdate = "update {} set {} = '{}' where {} = '{}'"
    TypicalDelete = "delete from {} where {} = '{}'"

    @classmethod
    def genFullName(cls, name) -> str:
        return publ.schema + "." + name


    @abstractmethod
    def insert(cls, **kwargs) -> None:
        """Insert data into table"""


    @classmethod
    def sql(cls, query: str) -> None:
        """Execute query received as parameter"""
        cls.instance.query(query)


    @classmethod
    def createQuery(cls, name: str, query: str) -> None:
        """Create table"""
        cls.sql("create table if not exists " + name + query)


    @classmethod
    def dropQuery(cls, name) -> None:
        """Drop table"""
        cls.sql("drop table if exists " + name)

    @classmethod
    def getAbyB(cls, Acol: str, Bcol: str, Bval: str, substr:bool = False) -> str:
        """ Return value from column Acol
            where value in column Bcol equals to Bval"""
        cls.sql(cls.TypicalWhereSelect.format(Acol, cls.genFullName(cls.name), Bcol, Bval))
        tempRes = cls.instance.use_result()
        if substr:
            res = str(tempRes.fetch_row()[0][0])[2:-1]
        else:
            res = str(tempRes.fetch_row()[0][0])
        return res
