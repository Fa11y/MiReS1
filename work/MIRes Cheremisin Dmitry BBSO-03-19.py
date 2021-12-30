import os
import time
import shutil
import random

class io:
    
    def createFile(path):
        file = open(path, "w")
        file.close()

    def createDir(path):
        if not io.exists(path):
            os.mkdir(path)

    def delete(path):
        if io.isDir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
            
    def isDir(path):
        return os.path.isdir(path)
    
    def isFile(path):
        return os.path.isfile(path)

    def exists(path):
        return os.path.exists(path)
    
    def size(path):
        if io.isFile(path):
            return os.path.getsize(path)
        else:
            size = 0
            for subdir, dirs, files in os.walk(path):
                for f in files:
                    fp = os.path.join(subdir, f)
                    size += os.path.getsize(fp)
            return size
        
    def getAbsolutePath(path):
        return os.path.abspath(path)

    def rename(path1, path2):
        os.rename(path1, path2)

    def countfiles(path):
        counter = 0;
        for subdir, dirs, files in os.walk(path):
                for f in files:
                    counter+=1
        return counter

    def getFileByID(path, fileid):
        if fileid>io.countfiles(path)-1 or fileid<0:
            fileid = fileid%io.countfiles(path)
        counter = 0;
        for subdir, dirs, files in os.walk(path):
                for f in files:
                    if counter == fileid:
                        return subdir+"\\"+f
                    counter+=1
        return ""
        

class security:

    def mirror(path):
        f = open(path, "r+b")
        filesize = io.size(path)
        pos = 0
        if filesize%2==1:
            pos = filesize/2 + 1
        else:
            pos = filesize/2
        pos = int(pos)
        i = 0
        while pos+i < filesize-i:
            f.seek(pos+i)
            tempbyte1 = f.read(1)

            f.seek(filesize-i-1)
            tempbyte2 = f.read(1)

            f.seek(filesize-i-1)
            f.write(tempbyte1)

            f.seek(pos+i)
            f.write(tempbyte2)

            i += 1
        f.close()
    
    def inverse(path):
        f = open(path, "r+b")
        filesize = io.size(path)
        pos = 0
        while pos < filesize:
            f.seek(pos)
            tempbyte = f.read(1)
            arr = bytearray(tempbyte)
            arr[0] = (arr[0]-128)%256
            f.seek(pos)
            f.write(arr)
            pos += 1
        f.close()
    
    def reverse(path):
        f = open(path, "r+b")
        filesize = io.size(path)
        pos = 0
        while pos < filesize/2:
            f.seek(pos)
            tempbyte1 = f.read(1)

            f.seek(filesize-pos-1)
            tempbyte2 = f.read(1)

            f.seek(filesize-pos-1)
            f.write(tempbyte1)

            f.seek(pos)
            f.write(tempbyte2)

            pos+=1
        f.close()

    def plus(path, b):
        f = open(path, "r+b")
        filesize = io.size(path)
        pos = 0
        while pos < filesize:
            f.seek(pos)
            tempbyte = f.read(1)
            arr1 = bytearray(tempbyte)
            arr2 = bytearray(b)
            arr1[0] = (arr1[0]+arr2[0])%256
            f.seek(pos)
            f.write(arr1)
            pos += 1
        f.close()
        return b

    def minus(path, b):
        f = open(path, "r+b")
        filesize = io.size(path)
        pos = 0
        while pos < filesize:
            f.seek(pos)
            tempbyte = f.read(1)
            arr1 = bytearray(tempbyte)
            arr2 = bytearray(b)
            arr1[0] = (arr1[0]-arr2[0])%256
            f.seek(pos)
            f.write(arr1)
            pos += 1
        f.close()
        return b

    def deltaEncode(path):
        f = open(path, "r+b")
        filesize = io.size(path)
        last = bytearray(f.read(1))
        temp = bytearray(1)
        pos = 1
        while pos < filesize:
            arr = bytearray(f.read(1))
            f.seek(pos)
            temp[0] = (arr[0]-last[0])%256
            f.write(temp)
            last[0] = arr[0]
            pos += 1
        f.close()

    def deltaDecode(path):
        f = open(path, "r+b")
        filesize = io.size(path)
        last = bytearray(f.read(1))
        temp = bytearray(1)
        pos = 1
        while pos < filesize:
            temp[0] = (f.read(1)[0]+last[0])%256
            f.seek(pos)
            f.write(temp)
            last[0] = temp[0]
            pos += 1
        f.close()

    def encryption(path):
        f = open(path+"\\mires.mires", "w")
        i = 0
        count = io.countfiles(path)
        while i < count:
            if count-i-1 > 0:
                print("Осталось зашифровать " + str(count-i-1) + " файлов!")
            fp = io.getFileByID(path, i)
            print(fp + " " + str(i))
            if fp!=path+"\\mires.mires":
                sec = random.randint(0, 255)
                b = bytearray(1)
                b[0] = sec
                f.write(str(sec)+"\n")
                f.write(str(security.plus(fp, random.randint(1, 256)))+"\n")
                f.write(str(security.minus(fp, random.randint(1, 256)))+"\n")
                if sec%2==0:
                    security.inverse(fp)
                if sec%3==0:
                    security.reverse(fp)
                if sec%5==0:
                    security.mirror(fp)
                if sec%7==0:
                    security.deltaEncode(fp)
                if sec%11==0:
                    security.deltaDecode(fp)
            i += 1
        f.close()
    
    def decryption(path):
        f = open(path+"\\mires.mires", "r")
        i = 0
        count = io.countfiles(path)
        while i < count:
            if count-i-1>0:
                print("Осталось расшифровать " + str(count-i-1) + " файлов!")
            fp = io.getFileByID(path, i)
            if fp!=path+"\\mires.mires":
                sec = int(f.readline())
                b = bytearray(1)
                b[0] = sec
                security.minus(fp, int(f.readline()))
                security.plus(fp, int(f.readline()))
                if sec%11==0:
                    security.deltaEncode(fp)
                if sec%7==0:
                    security.deltaDecode(fp)
                if sec%5==0:
                    security.mirror(fp)
                if sec%3==0:
                    security.reverse(fp)
                if sec%2==0:
                    security.inverse(fp)
            i += 1
        f.close()
        io.delete(path+"\\mires.mires")

def RunInterface():
    print("Добро пожаловать в программу шифрования данных MIRes!")
    print("Чтобы посмотреть список команд, введите \"help\"")
    stop = False
    command = ""
    while not stop:
        command = input("\n>---> ")
        print()
        if command=="help":
            print("******* Список команд MIRes *******")
            print("help - пулучить список команд")
            print("information - получить информацию о программе")
            print("instruction - получить инструкцию к программе")
            print("encryption - зашифровать все файлы в указанной папке")
            print("decryption - расшифровать все файлы в указанной папке")
            print("evaluate - выполненить однострочную команду в интерпретаторе Python")
            print("system - выполненить однострочную команду в системной консоли")
            print("isdir - проверка принадлежности указанного пути к папке")
            print("isfile - проверка принадлежности указанного пути к файлу")
            print("createfile - создать новый файл")
            print("createdir - создать новую папку")
            print("exists - проверка папки или файла на существование")
            print("countfiles - посчитать, сколько файлов в указанной папке")
            print("delete - удалить папку или файл")
            print("size - определить размер папки или файла")
            print("getabsolutepath - получить абсолютный путь к папке или файлу")
            print("rename - переименовать папку или файл")
            print("copy - скопировать папку или файл")
            print("move - переместить папку или файл")
            print("... - игнорировать следующее сообщение")
            print("exit - выйти из программы")
            print("stop - выйти из программы")
            print("*********************************")
        elif command=="information":
            print("******* Информация *******")
            print("  Версия программы: 1.0 стабильная")
            print("  Техническая поддержка: cheremis1290@gmail.com")
            print("  Задача:")
            print("        Основной задачей данного проекта является перекрёстное шифрование и дешифрование файлов в указанной папке.")
            print("***************************")
        elif command=="instruction":
            print("******* Инструкция *******")
            print("    Введите команду \"help\" и ознакомьтесь со списком команд. Основными командами данной программы являются \"encryption\" - шифрование и \"decryption\" - дешифрование")
            print("***************************")
        elif command=="encryption":
            path = input("Введите путь к папке >---> ")
            print()
            if io.exists(path):
                if io.isDir(path):
                    security.encryption(path)
                    print("Файлы успешно зашифрованы!")
                else:
                    print("Нужно указать папку, а не файл!")
            else:
                print("Указанной папки не существует!")
        elif command=="decryption":
            path = input("Введите путь к папке >---> ")
            print()
            if io.exists(path):
                if io.isDir(path):
                    security.decryption(path)
                    print("Файлы успешно дешифрованы!")
                else:
                    print("Нужно указать папку, а не файл!")
            else:
                print("Указанной папки не существует!")
        elif command=="evaluate":
            eval(input("eval >---> "))
        elif command=="system":
            print(os.system(input("system >---> ")))
        elif command=="isfile":
            path = input("Введите путь >---> ")
            if io.exists(path):
                if io.isFile(path):
                    print("По указанному пути находится файл!")
                else:
                    print("По указанному пути находится не файл!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="isdir":
            path = input("Введите путь >---> ")
            if io.exists(path):
                if io.isDir(path):
                    print("По указанному пути находится папка!")
                else:
                    print("По указанному пути находится не папка!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="createfile":
            io.createFile(input("Введите путь к файлу >---> "))
            print("Файл создан!")
        elif command=="createdir":
            io.createDir(input("Введите путь к папке >---> "))
            print("Папка создана!")
        elif command=="exists":
            path = input("Введите путь >---> ")
            if io.exists(path):
                if io.isFile(path):
                    print("Файл найден!")
                else:
                    print("Папка найдена!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="countfiles":
            path = input("Введите путь >---> ")
            if io.exists(path):
                if io.isDir(path):
                    print("Всего в указанной папке " + str(io.countfiles(path)) + " файлов!")
                else:
                    print("Требуется указать папку, а не файл!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="delete":
            path = input("Введите путь >---> ")
            if io.exists(path):
                if io.isFile(path):
                    io.delete(path)
                    print("Файл по указанному пути успешно удалён!")
                else:
                    io.delete(path)
                    print("Папка по указанному пути успешно удалена со всем содержимым!")
            else:
                print("По указанному пути ничего не найдено")
        elif command=="size":
            path = input("Введите путь к файлу >---> ")
            if io.exists(path):
                if io.isFile(path):
                    print("Размер файла в байтах: " + str(io.size(path)))
                else:
                    print("Размер папки в байтах: " + str(io.size(path)))
            else:
                print("Путь указан не верно")
        elif command=="getabsolutepath":
            path = input("Введите путь >---> ")
            if io.exists(path):
                if io.isFile(path):
                    print("Абсолютный путь к указанному файлу: " + io.getAbsolutePath(path))
                else:
                    print("Абсолютный путь к указанной папке: " + io.getAbsolutePath(path))
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="rename":
            path = input("Введите путь >---> ")
            if io.exists(path):
                if io.isFile(path):
                    io.rename(path, input("Введите путь к файлу вместе с новым именем >---> "))
                    print("Файл успешно переименован!")
                else:
                    io.rename(path, input("Введите путь к папке с новым наименованием >---> "))
                    print("Папка успешно переименована!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command=="":
            print()
        elif command=="...":
            input("\n>---> ")
            print()
        elif command=="exit" or command=="stop":
            stop=True
            print("Выход из программы MIRes!\n")
            time.sleep(5)
        else:
            print ("Неизвестная команда!")

def Main():
    RunInterface()

Main()
