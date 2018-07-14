import configuration.public as publ
from database.TableClass import Table

class UserTable(Table):

    # Table Name
    name = publ.userTable
    fullName = Table.genFullName(name)

    # Column Names
    ID_COL = publ.ID_COL
    USER_ID_COL = publ.USER_ID_COL
    USER_NAME_COL = publ.USER_NAME_COL
    DATE_TIME_COL = publ.DATE_TIME_COL

    # User table creation query
    creationQuery = """({} Int NOT NULL AUTO_INCREMENT,
                        {} BIGINT NOT NULL, 
                        {} VARCHAR(50),
                        {} DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  
                        PRIMARY KEY ({})
                       )"""\
                       .format(ID_COL,
                               USER_ID_COL,
                               USER_NAME_COL,
                               DATE_TIME_COL,
                               ID_COL)

    def create(self) -> None: Table.createQuery(self.fullName, self.creationQuery)
    def drop(self): Table.dropQuery(self.fullName)

    #create = partial(super(UserTable, self)., name = fullName, query = creationQuery)

    #drop = partial(Table.drop, name = fullName)

    @classmethod
    def insert(cls, **kwargs) -> None:
        Table.sql("insert into {}({}, {}, {}) values('{}', '{}', '{}')" \
                  .format(cls.name,
                          cls.ID_COL,
                          cls.USER_ID_COL,
                          cls.USER_NAME_COL,
                          kwargs['ID'],
                          kwargs['UserID'],
                          kwargs['UserName']
                          ))
