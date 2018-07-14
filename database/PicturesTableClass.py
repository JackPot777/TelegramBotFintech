import configuration.public as publ
from database.TableClass import Table
from functools import partial

class PicturesTable(Table):

    # Table Name
    name = publ.picturesTable
    fullName = Table.genFullName(name)

    # Column Names
    ID_COL = publ.ID_COL
    USER_ID_COL = publ.USER_ID_COL
    USER_NAME_COL = publ.USER_NAME_COL
    PICTURE_NAME_COL = publ.PICTURE_NAME_COL
    COMMENTS_COL = publ.COMMENTS_COL
    KEY_IN_S3_COL = publ.KEY_IN_S3_COL
    DATE_TIME_COL = publ.DATE_TIME_COL
    PRIVATE_POLICY_VOL = publ.PRIVATE_POLICY_VOL

    # Picture data table creation query
    creationQuery = """({} Int NOT NULL AUTO_INCREMENT,
                        {} BIGINT NOT NULL,
                        {} VARCHAR(20),
                        {} VARCHAR(50),
                        {} TEXT,
                        {} VARCHAR(50),
                        {} BOOLEAN,
                        {} DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        PRIMARY KEY ({})
                       )""" \
                       .format(ID_COL,
                               USER_ID_COL,
                               USER_NAME_COL,
                               PICTURE_NAME_COL,
                               COMMENTS_COL,
                               KEY_IN_S3_COL,
                               PRIVATE_POLICY_VOL,
                               DATE_TIME_COL,
                               ID_COL)

    def create(self) -> None: Table.createQuery(self.fullName, self.creationQuery)
    def drop(self): Table.dropQuery(self.fullName)

    @classmethod
    def insert(cls, **kwargs) -> None:
        Table.sql("insert into {}({}, {}, {}, {}, {}, {}) values('{}', '{}', '{}', '{}', '{}', '{}')" \
                  .format(cls.name,
                          cls.USER_ID_COL,
                          cls.USER_NAME_COL,
                          cls.PICTURE_NAME_COL,
                          cls.COMMENTS_COL,
                          cls.KEY_IN_S3_COL,
                          cls.PRIVATE_POLICY_VOL,
                          kwargs['userID'],
                          kwargs['UserName'],
                          kwargs['Name'],
                          kwargs['Comment'],
                          kwargs['S3_Key'],
                          kwargs['Private']))

    @classmethod
    def get_id_by_s3key(cls, key: str) -> str:
        return Table.getAbyB(cls.ID_COL, cls.KEY_IN_S3_COL, key)

    @classmethod
    def get_s3key_by_id(cls, id: str) -> str:
        return Table.getAbyB(cls.KEY_IN_S3_COL, cls.ID_COL, id, substr=True)

    @classmethod
    def get_id_by_userid(cls, userid: str) -> str:
        return Table.getAbyB(cls.ID_COL, cls.USER_ID_COL, userid)

    @classmethod
    def get_userid_by_id(cls, id: str) -> str:
        return Table.getAbyB(cls.USER_ID_COL, cls.ID_COL, id)

    @classmethod
    def ger_username_by_id(cls, id: str) -> str:
        return Table.getAbyB(cls.USER_NAME_COL, cls.ID_COL, id, substr=True)