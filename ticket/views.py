import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import CreateTicketForm, UpdateTicketForm
from .models import Ticket

#view ticket details
def ticket_details(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    context = {'ticket':ticket}
    return render(request, 'ticket/ticket_details.html', context)

# Create a ticket.
""" For Customers """ 

def create_ticket(request):
    if request.method == "POST":
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = 'Pending'
            var.save()
            messages.info(request, 'Your ticket has been succesfully submitted. An engineer will be assigned to it')
            return redirect('dashboard')
        else:
            messages.warning(request, 'something went wrong.Please check form input')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form':form}
        return render(request, 'ticket/create_ticket.html', context)
    

#Updating the tickett
def update_ticket(request, pk):
    ticket = Ticket.object.get(pk=pk)
    if request.method == "POST":
        form = CreateTicketForm(request.POST,instance=ticket)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your ticket has been succesfully updated and all changes are saved in the Database')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
    else:
        form = UpdateTicketForm(instance=ticket)
        context = {'form':form}
        return render(request, 'ticket/create_ticket.html', context)
    

# viewing all created tickers

def all_tickers(request):
    ticket = Ticket.objects.filter(created_by = request.user)
    context = {'tickets': ticket}
    return render(request, 'ticket/all_tickets.html', context)


""" For Engineers"""
# view ticket queue
def ticket_queue(request):
    tickets = Ticket.objects.filter(ticket_status= 'Pending')
    context = {'tickets': tickets}
    return render(request, 'ticket/ticket_queue.html', context)

#close a ticket
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticker_status = 'Active'
    ticket.accepted_date = datetime.datetime.now()
    ticket.save()
    messages.info(request,'Ticket has been accepted. Please resolve as soon as possible!')
    return redirect('ticket-queue')


#accept a ticket
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticker_status = 'Completed'
    ticket.is_resolved = True
    ticket.closed_date = datetime.datetime.now()
    ticket.save()
    messages.info(request,'Ticket has been resolved. Thank you brilliant Support Engineer!')
    return redirect('ticket-queue')

#ticket engineer is working on
def workspace(request):
    tickets = Ticket.objects.filter(assigned_to = request.user, is_resolved = False)
    context = {'tickets': tickets}
    return render(request, 'ticket/workspace.html', context)

#all closed/resolved tickets
def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_tO= request.user, is_resolved=True)
    context = {'tickets':tickets}
    return render(request, 'ticket/all_closed_tickets.html', context)


