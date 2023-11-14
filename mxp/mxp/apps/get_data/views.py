from django.shortcuts import render

from .models import data
from django.shortcuts import render
from .forms import UserForm
import paramiko
from django.shortcuts import redirect
import psycopg2
def index(request):
    submitbutton = request.POST.get("submit")
    address=''
    username=''
    password=''
    port=''
    form = UserForm(request.POST or None)
    if form.is_valid():
        address = form.cleaned_data.get("address")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        port = form.cleaned_data.get("port")

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=address, username=username, password=password, port=port)
        stdin, stdout, stderr = client.exec_command('cat /etc/issue')
        os_type_data = stdout.read() + stderr.read()
        stdin, stdout, stderr = client.exec_command('date')
        os_type_date = stdout.read() + stderr.read()

        stdin, stdout, stderr = client.exec_command('uname -r')
        version_data1 =  stdout.read() + stderr.read()
        stdin, stdout, stderr = client.exec_command('date')
        version_date1 = stdout.read() + stderr.read()

        stdin, stdout, stderr = client.exec_command('arch')
        architecture_data =  stdout.read() + stderr.read()
        stdin, stdout, stderr = client.exec_command('date')
        architecture_date = stdout.read() + stderr.read()
        client.close()

        log1 = os_type_date.decode('utf-8')[:len(os_type_date)-1] + " cat /etc/issue"
        log2 = version_date1.decode('utf-8')[:len( version_date1)-1] + " uname -r"
        log3 = architecture_date.decode('utf-8')[:len(architecture_date)-1] + " arch"
        String_log = log1 + "\n" + log2 + "\n" + log3 + "\n"
        connection = psycopg2.connect(user="postgres",password="user",host="127.0.0.1",port="5432",database="postgres")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO get_data_data (operation_system, version, architecture, log_history)
                                                      VALUES (%s,%s,%s,%s)"""
        record_to_insert = (os_type_data.decode('utf-8')[:len(os_type_data)-8], version_data1.decode('utf-8'),  architecture_data.decode('utf-8'),String_log)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        return(redirect(index1))
    context = {'form':form,'address':address,'username':username,'password':password,'port':port, 'submitbutton': submitbutton}

    return render(request,'get_data/list.html', context)
def index1(request):
    found_info = data.objects.all()
    return render(request,'get_data/list1.html',{'found_info' : found_info})