import ticket.CloudDB2 as DB
import pandas as pd


class User:
    def __init__(self):
        self.Id = ""
        self.Name = ""
        self.User_Type = ""
        self.Mobile = ""
        self.Email = ""
        self.Password = ""

        # query = "drop table users"
        # nos = DB.check(query)

        query = "select count(ID) from users"
        nos = DB.check(query)
        print(nos)
        if nos == 0:
            query = "create table users(ID INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 1 " \
                    "INCREMENT BY 1), Name VARCHAR(75) NOT NULL, " \
                    "User_Type VARCHAR(75) NOT NULL, " \
                    "Mobile VARCHAR(15) NOT NULL, Email VARCHAR(50), Password VARCHAR(50) )"
            DB.run(query)

    def save(self):
        print(self.Name)

        if self.Id != "":
            query = "update users set Name='{self.Name}'" \
                    ",User_Type='{self.User_Type}'" \
                    ",Mobile='{self.Mobile}'" \
                    ",Email='{self.Email}'" \
                    ",Password='{self.Password}'" \
                    " WHERE ID = '{self.Id}'"
        else:
            query = "insert into users(Name, User_Type,  Mobile, Email, Password) " \
                    "VALUES('{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}')" \
                .format(self.Name, self.User_Type, self.Mobile, self.Email, self.Password)

        DB.run(query)

    def login(self):
        query = "select * from users WHERE User_Type='{}' and Email='{}' and Password='{}'".format(self.User_Type,
                                                                                                   self.Email,
                                                                                                   self.Password)
        return DB.view(query)

    def get(self):
        query = "select * from users WHERE ID='{}'".format(self.Id)
        return DB.view(query)

    def agents(self):
        query = "select * from users WHERE User_Type='{}'".format("agent")
        return DB.view(query)

    def display(self):
        return DB.view("select * from users")
