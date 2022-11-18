# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import ibm_db
from flask import Flask, render_template, request, redirect, url_for, flash, session
from ticket.User import User
from ticket.Ticket import Ticket
import sendgrid
import os
from sendgrid.helpers.mail import *

app = Flask(__name__)
app.secret_key = b'_4#z2G"F5Q9z\n\xec]/'


@app.route("/")
def show_login():
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("hi")
        if request.form['username'] != "" and request.form['password'] != "":
            user = User()
            user.User_Type = request.form['user_type']
            user.Email = request.form['username']
            user.Password = request.form['password']
            result = user.login()

            print("login result", result)
            if len(result) > 0:
                session['name'] = result[0]['NAME']
                session['user_id'] = result[0]['ID']
                session['user_type'] = result[0]['USER_TYPE']

            return redirect(url_for('dashboard'))

        else:
            flash(u'username or password is incorrect.', 'danger')
            return redirect(url_for('login'))

    else:
        return render_template('login.html')


@app.route("/user/signup", methods=['GET', 'POST'])
def vendor_signup():
    if request.method == 'POST':
        user = User()
        user.Id = ""
        user.Name = request.form['name']
        user.User_Type = request.form['user_type']
        user.Mobile = request.form['mobile']
        user.Email = request.form['email']
        user.Password = request.form['password']
        user.save()

        flash(u'User Sign up done, you login now with your username and password.', 'success')

        return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route("/dashboard", methods=['GET'])
def dashboard():
    if session['name'] is None:
        return redirect(url_for('login'))

    # inventory = Inventory()
    # inventory = inventory.display()
    return render_template('dashboard.html')


@app.route("/ticket/create", methods=['GET', 'POST'])
def create_ticket():
    if session['name'] is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        ticket = Ticket()
        ticket.Title = request.form['title']
        ticket.Description = request.form['description']
        ticket.Priority = request.form['priority']
        id = request.form.get('id')

        old_ticket = Ticket()

        if id is not None:
            ticket.Id = id
            tickets = old_ticket.get(id)
            old_ticket = tickets[0]
        agent_id = request.form.get('agent_id')
        if agent_id is not None:
            ticket.AgentId = agent_id
        status = request.form.get('status')
        if status is not None:
            ticket.Status = status
        ticket.Status = 0
        ticket.save()

        if ticket.AgentId != 0 and ticket.AgentId != old_ticket["AGENTID"]:
            return redirect(url_for('ticketagentassigned', ticket_id=id))

        flash(u'Ticket has been saved successfully.', 'success')

        return redirect(url_for('active_tickets'))
    else:
        ticket = Ticket()
        agents = []
        return render_template('createcomplaint.html', ticket=ticket, agents=agents)


@app.route("/ticket/edit/<id1>", methods=['GET'])
def edit_ticket(id1):
    if session['name'] is None:
        return redirect(url_for('login'))

    ticket = Ticket()
    tickets = ticket.get(id1)
    ticket = tickets[0]

    user = User()
    agents = user.agents()
    return render_template('createcomplaint.html', ticket=ticket, agents=agents)


@app.route("/tickets/active", methods=['GET'])
def active_tickets():
    if session['name'] is None:
        return redirect(url_for('login'))

    ticket = Ticket()
    ticket.Status = 0
    tickets = ticket.display()

    print(tickets)
    return render_template('tickets.html', title='Active Tickets', tickets=tickets)


@app.route("/tickets/closed", methods=['GET'])
def closed_tickets():
    if session['name'] is None:
        return redirect(url_for('login'))

    ticket = Ticket()
    ticket.Status = 1
    tickets = ticket.display()
    return render_template('tickets.html', title='Closed Tickets', tickets=tickets)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/ticket/agent-assigned/<ticket_id>', methods=['GET'])
def ticketagentassigned(ticket_id):
    if session['name'] is None:
        return redirect(url_for('login'))

    id1 = ticket_id

    ticket = Ticket()
    ticket.close(id1)

    ticket = Ticket()
    tickets = ticket.get(id1)
    ticket = tickets[0]

    user = User()
    user.Id = ticket["USERID"]
    users = user.get()
    user = users[0]

    agent = User()
    agent.Id = ticket["AGENTID"]
    users = agent.get()
    agent = users[0]

    sg = sendgrid.SendGridAPIClient(api_key="")
    from_email = Email("rajesh@malaris.com")
    to_email = To(user.Email)
    subject = "Customer Care Agent Assigned Notification"
    html_content = str(render_template('email_agent_assigned.html', ticket=ticket, user=user, agent=agent))
    content = Content("text/html", html_content)
    print(html_content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    return redirect(url_for('active_tickets'))


@app.route('/ticket/close/<ticket_id>', methods=['GET'])
def ticketclose(ticket_id):
    if session['name'] is None:
        return redirect(url_for('login'))

    id1 = ticket_id

    ticket = Ticket()
    ticket.close(id1)

    ticket = Ticket()
    tickets = ticket.get(id1)
    ticket = tickets[0]

    user = User()
    user.Id = ticket["USERID"]
    users = user.get()
    user = users[0]
    sg = sendgrid.SendGridAPIClient(api_key="")
    from_email = Email("rajesh@malaris.com")
    to_email = To(user["EMAIL"])
    subject = "Customer Care Ticket Closed Notification"
    content = Content("text/html", render_template('email_ticket_closed.html', ticket=ticket, user=user))
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    return redirect(url_for('active_tickets'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
