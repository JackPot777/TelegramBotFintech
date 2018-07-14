"""
File with public configuration
"""



# DataBase.py configuration
schema = "telegramDB"
picturesTable = "Picture"
userTable = "Users"

# Picture Table Column names
ID_COL = "ID"
USER_ID_COL = "UserID"
USER_NAME_COL = "UserName"
PICTURE_NAME_COL = "Name"
COMMENTS_COL = "Comments"
KEY_IN_S3_COL = "S3KEY"
DATE_TIME_COL = "Date"
PRIVATE_POLICY_VOL = "Private"

# S3 Configuration
s3_picturesbucket = "telegrampictures"

# Folder with photos
photoFolderPath = "data/downloadedPhotos/"

