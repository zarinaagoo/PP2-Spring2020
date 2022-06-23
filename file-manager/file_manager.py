import os
import os.path

print("Hello! \nPlease introduce yourself, what's your name?")
name = input()
curpath = os.getcwd()

def firstStep():
    print(name, """, to work with Directory, press 1
    or if you want to work with File press 2""")

def Dir():
    print("There you have 6 options:")
    print("1 - Rename directory\n2 - Number of files in directory\n3 - Number of directories in your computer\n4 - List directories\n5 - Create File in Directory\n6 - Create Directory")
    choise = int(input("What's your choice: "))

    if choise == 1:
        nameDir = input("Write the name of Directory, that you want to rename: ")
        if os.path.exists(nameDir):
            newName = input("Write the new name for Directory: ")
            os.rename(nameDir, newName)
            print("Directory %s was renamed successfully!", nameDir)
        else:
            print("Error, directory doesn't exist")
    elif choise == 2:
        num = 0
        for f in os.listdir():
            numOfFiles = os.path.join(f)
            if os.path.isfile(numOfFiles):
                num+=1
        print("Number of files: ", num)
    elif choise == 3:
        num = 0
        for f in os.listdir():
            numOfDir = os.path.join(f)
            if os.path.isdir(numOfDir):
                num+=1
        print("Number of directories: ", num)
    elif choise == 4:
        print(os.listdir())
    elif choise == 5:
        nameForNewFile = input("Name of the file: ")
        addFile = open(nameForNewFile+'.txt', 'w')
        print("File was created!")
    elif choise == 6:
        nameForNewDir = input("Name of the directory: ")
        os.mkdir(nameForNewDir)
        print("Directory was created!")

def File():
    print("There you have 5 options:")
    print("1 - Delete File\n2 - Rename File\n3 - Write in File\n4 - Rewrite the File\n5 - Get your current path")
    choise = int(input("What's your choice: "))
    if choise == 1:
        namef = input("The name of the file, that you want to delete: ")
        if os.path.exists(namef):
            os.remove(namef)
            print("File was deleted!")
        else:
            print("Error, file doesn't exist")
    elif choise == 2:
        namef = input("The name of the file, that you want to rename: ")
        if os.path.exists(namef):
            name = input("Enter new name for the file: ")
            os.rename(namef, name)
            print("File was renamed!")
        else:
            print("Error, file doesn't exist")
    elif choise == 3:
        fileToCon = input("The name of the file, in which you want to make changes: ")
        if os.path.exists(fileToCon):
            b = open(fileToCon, 'a')
            content = input("Write out your changes: ")
            b.write(content)
            b.close()
            print("New information was added to the file.")
        else:
            print("Error, file doesn't exist")
    elif choise == 4:
        fileToCon = input("The name of the file, which you want to rewrite: ")
        if os.path.exists(fileToCon):
            b = open(fileToCon, 'w')
            content = input("Write out your changes: ")
            b.write(content)
            b.close()
            print("You rewrite the content successfully.")
        else:
            print("Error, file doesn't exist")
    elif choise == 5:
        curPath = os.getcwd()
        print("Your path is: ", curPath)

bool = True
while bool:
    firstStep()
    pnt = int(input())
    if pnt == 1:
        print("Directory manager mode")
        Dir()
    elif pnt == 2:
        print("File manager mode")
        File()
    else:
        bool = False

