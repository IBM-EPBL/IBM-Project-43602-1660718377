from flask import session

import ticket.CloudDB2 as DB
import pandas as pd


class Ticket:
    def __init__(self):
        self.Id = ""
        self.UserId = 0
        self.AgentId = 0
        self.Title = ""
        self.Description = ""
        self.Priority = ""
        self.Note = ""
        self.Status = 0

        # query = "drop table tickets"
        # nos = DB.check(query)

        query = "select count(ID) from tickets"
        nos = DB.check(query)
        print(nos)
        if nos == 0:
            query = "create table tickets(ID INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 1 " \
                    "INCREMENT BY 1), UserId INT NULL,AgentId INT NULL," \
                    "Title VARCHAR(75) NOT NULL, Description VARCHAR(255) NOT NULL, " \
                    "Priority VARCHAR(75) NOT NULL, Note VARCHAR(50), Status INT NOT NULL )"
            DB.run(query)

    def save(self):
        if session['user_type'] == 'agent':
            self.AgentId = session['user_id']
        elif session['user_type'] == 'user':
            self.UserId = session['user_id']

        if self.Id != "":
            query = "update tickets set AgentId='{}', Title='{}', Description='{}'" \
                    ",Priority='{}'" \
                    ",Note='{}'" \
                    ",Status='{}'" \
                    " WHERE ID = '{}'".format(self.AgentId, self.Title, self.Description, self.Priority, self.Note,
                                              self.Status, self.Id)
        else:
            query = "insert into tickets(UserId, AgentId, Title, Description, Priority,Status, Note) VALUES('{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}'" \
                    ",'{}')" \
                .format(self.UserId, self.AgentId, self.Title, self.Description, self.Priority, self.Status, self.Note)
        DB.run(query)

    def close(self, id):
        return DB.view("update tickets set Status='1' where ID=" + str(id))

    def get(self, id):
        return DB.view("select * from tickets where ID=" + str(id))

    def display(self):
        query = "select tickets.*, user.Name as USER_NAME, agent.Name as AGENT_NAME from tickets " \
                "left outer join users as user on user.ID = tickets.UserId " \
                "left outer join users as agent on agent.ID = tickets.AgentId " \
                "where Status = '" + str(self.Status) + "' "

        if session['user_type'] == 'agent':
            query = query + " and AgentId='" + str(session['user_id']) + "'"
        elif session['user_type'] == 'admin':
            query = query + " "
        else:
            query = query + " and UserId='" + str(session['user_id']) + "'"

        return DB.view(query)
