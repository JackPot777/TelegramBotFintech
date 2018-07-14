"""
File with miscellaneous code used multiple times
"""
import subprocess

import database.pictures
from time import gmtime, strftime
from actions.adminfunctions import loginedAdmins

TIME = strftime("%Y_%m_%d_%H_%M_%S", gmtime()) # Time in format yyyy_MM_dd_hh_mm_ss

def rm(path: str):
    """Delete directory on server"""
    subprocess.call("rm " + path, shell=True)


def hasAccess(UserID, PictureID) -> bool:
    """Check if user has access to picture"""
    if (database.pictures.getOwnerIDbyPictureID(PictureID) == str(UserID)) or isAdmin(UserID):
        return True
    else:
        return False


def isPublic(pictureID) -> bool:
    """Check if picture with PictureID is public"""
    if database.pictures.getPubic(pictureID) == '0':
        return True
    else:
        return False # if picture does not exists result is false


def pictureExists(pictureID) -> bool:
    """Check if picture exists"""
    if database.pictures.getPictureInfo(database.pictures.ID_COL, pictureID):
        return True
    else:
        return False


def isAdmin(user: str) -> bool:
    """Check if user is admin"""
    if user in loginedAdmins:
        return True
    else:
        return False