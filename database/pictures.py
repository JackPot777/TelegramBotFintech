import configuration.public as publ


# Table Name
from database.DataBase import sql, TypicalWhereSelect, instance, TypicalUpdate, TypicalDelete

picturesTable = publ.schema + "." + publ.picturesTable

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
PictureTableCreationQuery = "create table if not exists " + picturesTable + \
    """(
        {} Int NOT NULL AUTO_INCREMENT, 
        {} BIGINT NOT NULL, 
        {} VARCHAR(20), 
        {} VARCHAR(50),
        {} TEXT,
        {} VARCHAR(50),
        {} BOOLEAN, 
        {} DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
        PRIMARY KEY ({})
    )"""\
        .format(ID_COL,
                USER_ID_COL,
                USER_NAME_COL,
                PICTURE_NAME_COL,
                COMMENTS_COL,
                KEY_IN_S3_COL,
                PRIVATE_POLICY_VOL,
                DATE_TIME_COL,
                ID_COL)


def createPicturesTable():
    """Create table containing picture info"""
    sql(PictureTableCreationQuery)


def getPictureInfo(column: str, value: str) -> bool :
    sql(TypicalWhereSelect.format("*", picturesTable, column, value))
    tempRes = instance.use_result()
    if tempRes.fetch_row():
        return True
    else:
        return False


def getLastPictureS3KeybyUserID(userID: int) -> str:
    """Find last picture belonging to user"""
    sql("select {} from {} where {} = '{}' order by {} desc" \
        .format(KEY_IN_S3_COL, picturesTable, USER_ID_COL, str(userID), ID_COL))
    tempRes = instance.use_result()
    res = str(tempRes.fetch_row()[0][0])[2:-1]  # substring to make b'PartYouNeed' returned by query PartYouNeed
    return res


def getS3KeybyID(ID: str) -> str:
    """ Return picture by ID"""
    sql(TypicalWhereSelect.format(KEY_IN_S3_COL, picturesTable, ID_COL, ID))
    tempRes = instance.use_result()
    res = str(tempRes.fetch_row()[0][0])[2:-1]
    return res


def getIDbyS3Key(Key: str) -> str:
    """ Finds ID corresponding to S3_key """
    sql(TypicalWhereSelect.format(ID_COL, picturesTable, KEY_IN_S3_COL, Key))
    tempRes = instance.use_result()
    res = str(tempRes.fetch_row()[0][0])
    return res


def getIDbyUserID(UserID: str) -> str:
    """ Finds picture's ID corresponding to user """
    sql(TypicalWhereSelect.format(ID_COL, picturesTable, USER_ID_COL, UserID))
    tempRes = instance.use_result()
    res = str(tempRes.fetch_row()[0][0])
    return res


def getOwnerIDbyPictureID(ID: str) -> str:
    """ Finds picture's owner ID"""
    sql(TypicalWhereSelect.format(USER_ID_COL, picturesTable, ID_COL, ID))
    tempRes = instance.use_result()
    res = str(tempRes.fetch_row()[0][0])
    return res


def getOwnerNamebyPictureID(ID: str) -> str:
    """ Finds picture's owner Name"""
    sql(TypicalWhereSelect.format(USER_NAME_COL, picturesTable, ID_COL, ID))
    tempRes = instance.use_result()
    res = str(tempRes.fetch_row()[0][0])[2:-1]
    return res


def insertIntoPictures(userID: str, UserName: str, S3_Key: str, Private = 1, Name: str = "NULL", Comment: str = "NULL"):
    """Inserts into database information about picture"""
    sql("insert into {}({}, {}, {}, {}, {}, {}) values('{}', '{}', '{}', '{}', '{}', '{}')"
        .format(picturesTable, USER_ID_COL, USER_NAME_COL, PICTURE_NAME_COL, COMMENTS_COL, KEY_IN_S3_COL,
                PRIVATE_POLICY_VOL,
                userID, UserName, Name, Comment, S3_Key, Private))


def definePictureName(ID: str, name: str):
    """ Updates picture's name  with ID in the database """
    sql(TypicalUpdate.format(picturesTable, PICTURE_NAME_COL, name, ID_COL, ID))


def deletePictureByID(ID: str):
    """ Deletes picture from database """
    sql(TypicalDelete.format(picturesTable, ID_COL, ID))


def deletePictureByName(name: str):
    """ Deletes picture from database """
    sql(TypicalDelete.format(picturesTable, USER_NAME_COL, name))


def countUserPicturesByName(Name:str, UserID: str) -> int:
    """Deletes picture from database by Name"""
    sql("select count(*) from {} where {} = '{}' group by {} having {} '{}'" \
        .format(picturesTable, USER_ID_COL, UserID, PICTURE_NAME_COL, PICTURE_NAME_COL, Name))
    tempRes = instance.use_result()
    res = int(tempRes.fetch_row()[0][0])
    return res


def setPublic(ID: str):
    """Set privacy policy of picture to public, so anyone can access it"""
    sql(TypicalUpdate.format(picturesTable, PRIVATE_POLICY_VOL, 0, ID_COL, ID))


def getPubic(ID: str) -> str:
    """Check if picture is public """
    sql(TypicalWhereSelect.format(PRIVATE_POLICY_VOL, picturesTable, ID_COL, ID))
    tempRes = instance.use_result()
    res = str(tempRes.fetch_row()[0][0])
    return res


def getStringOfUserPictures(userID: str) -> str:
    """Return picture IDs separated by comma"""
    sql(TypicalWhereSelect.format(ID_COL, picturesTable, USER_ID_COL, userID))
    tempRes = instance.use_result()
    output = ", ".join([str(x[0]) for x in tempRes.fetch_row(0)])
    return output


def getListOfUserS3Keys(userID: str):
    """Return list of picture S3 keys"""
    sql(TypicalWhereSelect.format(KEY_IN_S3_COL, picturesTable, USER_ID_COL, userID))
    tempRes = instance.use_result()
    output = []
    for x in tempRes.fetch_row(0): output.append(str(x[0])[2:-1])
    return output