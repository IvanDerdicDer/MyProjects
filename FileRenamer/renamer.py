import nt
import os
import typing

#Returns index as negative
#Returns False if char is not in a string
def getLastIndexOfChar(c:str, s:str) -> int:
    index = 0
    if c not in s:
        return False
    for i in reversed(s):
        index -= 1
        if i == c:
            return index

if __name__ == '__main__':
    i = typing.NewType('DirEntry', nt.DirEntry)
    dirPath = input("Unesite putanju direktorija s datotekama za preimenovanje: ")
    dirPath.replace('\\', '/')
    fileType = input("Unesite tip datoteke za preimenovanje: ")
    tmp = input("Unesite znak do kojeg želite maknuti znakove ili broj znakova za maknuti: ")
    whatToRemove = None
    try:
        whatToRemove = int(tmp)
    except Exception:
        whatToRemove = tmp
    dirIter = os.scandir(dirPath)
    for file in dirIter:
        if file.is_file() and file.name[-len(fileType):] == fileType:
            oldName = file.name
            oldName = oldName[:-len(fileType)-1]
            newName = ''
            if type(whatToRemove) == type(int()):
                newName = oldName[:-whatToRemove]
            else:
                howMuchToRemove = getLastIndexOfChar(whatToRemove, oldName)
                newName = oldName[:howMuchToRemove]
            newName += ('.' + fileType)
            os.chdir(dirPath)
            os.renames(file.name, newName)
    print("Preimenovane datoteke: ")
    for i in os.listdir(os.getcwd()):
        print(f"\t-{i}")

    """a = os.scandir('C:/Users/ivand/Music/Fitz And The Tantrums')
    i = typing.NewType('DirEntry', nt.DirEntry)
    for i in a:
        for j in os.scandir(i.path):
            print(j.name)"""