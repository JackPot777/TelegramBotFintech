import _mysql
import configuration.private as priv

instance = _mysql.connect( host=priv.DB_HOSTNAME, user=priv.DB_USERNAME, passwd=priv.DB_PASSWORD, db=priv.DB_DATABASE )


# Most used sql statements format
TypicalWhereSelect = "select {} from {} where {} = '{}'"
TypicalUpdate = "update {} set {} = '{}' where {} = '{}'"
TypicalDelete = "delete from {} where {} = '{}'"


def sql(query: str):
    """Executes query received as parameter """
    instance.query(query)