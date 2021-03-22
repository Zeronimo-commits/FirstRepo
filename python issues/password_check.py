#при первом включении задаем пароль с подтверждением и записываем в файлик для хранения(если он отсутсвтвует)
#подтверждение (в случае не совпадения ошибка)
#
#ввод пароля с проверка пароля  на 8 символов
def pass_init():
    i = False
    while not i:
        paswd = input("Задайте пароль: ")
        paswd2 = input("Подтвердите пароль: ")
        if len(paswd) < 8:
            print("Пароль слишком короткий, нужно 8 символов. \n Попробуйте ещё раз. ") 
            continue
        elif paswd != paswd2:
            print("Пароли не совпадают, задайте одинаковые пароли")
            continue
        elif paswd == paswd2:
            i = True
            print("Пароль сохранен")
            pass_write(paswd)
            welcome()

def pass_check():
    my_file = open("password.txt", "r")
    stored_passwd = my_file.read()
    my_file.close()
    if stored_passwd == "":
        pass_not_exist = input("Пароль не задан! \n Вы хотите задать пароль? y/n:")
        if pass_not_exist == "y":
            pass_init()
        else: 
            print("До свидания!")
    
    else:
        tries = False
        while not tries:
            inp_paswd = input("ВВедите ваш пароль:")
            if inp_paswd != stored_passwd:
                print("Пароль не верен, попробуйте ещё раз:")
                continue
            else:
                print("Доступ открыт")
                tries = True

def pass_write(paswd):
    my_file = open("password.txt", "w")
    my_file.write(paswd)
    my_file.close()
def welcome():
    print("Вы хотите зайти в систему?")
    answer = input("y/n?")
    if answer == "y":
        pass_check()
    else:
        print("До свидания!")


welcome()