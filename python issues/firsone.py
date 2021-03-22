#lst = ['ZDARATUTI', 1, 'YA', 2, 'VASH', 3, 'REBENOK', 4]
#print(lst)
#lib = {'ZDARATUTI':1, 'YA':2, 'VASH':3, 'REBENOK':4}

#def to_dict(lst):
#    for i in range(len(lst)):
#        voc.update({lst[i]:lst[i]})
#    return voc

#def to_dicti(lst):
#    return {element:element for element in lst}
#
#voc = to_dicti(lst)
#print(voc)

#voc={}
#to_dict(lst)    
#print(voc)


#def fnc(stroka):
#    a = stroka.split(' ')
#    b = a[::-1]
#    c = ' '.join(b)
#    return c
#
#print(fnc('Здравствуйте я ваша боль'))


#Задачка 
#при первом включении задаем пароль с подтверждением и записываем в файлик для хранения(если он отсутсвтвует)
#подтверждение (в случае не совпадения ошибка)
#
#ввод пароля с проверка пароля  на 8 символов
#дважды запрос пароля



def PasswordCreate():
    repeat=1
    print('Введите пароль :')
    firstInput = input()
    print('Подтвердите пароль :')
    secondInput = input()
    
    #проверка на совпадение
    while repeat == 1:
        if (firstInput!=secondInput):
            print('Пароли не совпадают')
            print('Введите пароль заново:')
            firstInput = input()
            print('Подтвердите пароль :')
            secondInput = input()
        elif (len(str(secondInput))<3):
            print('Пароль должен быть более 3 символов')
            print('Введите пароль заново:')
            firstInput = input()
            print('Подтвердите пароль :')
            secondInput = input()
        else:
            repeat=0
            print('попытка сохраненения')
    WritePasswrd(firstInput)
                
def WritePasswrd(passwrd):
    file = open("E:/Learning/GitHubRepo/FirstRepo/test.txt", 'w')  # указание полного пути
    file.write(passwrd)
    file.close

def CheckPasswrd():
    file = open("E:/Learning/GitHubRepo/FirstRepo/test.txt", 'r')  # указание полного пути
    chkPasInFile = file.read()
    file.close()
    print('Введите ваш пароль')
    inPasswrd = input()
    while chkPasInFile != inPasswrd:
        print('Неверный пароль, попробуйте еще раз')
        print('Введите ваш пароль ЕЩЕ РАЗ')
        inPasswrd = input()
    else:
        print('Да вы МОЛОДЕЦ!!!')
    
    
CheckPasswrd()


