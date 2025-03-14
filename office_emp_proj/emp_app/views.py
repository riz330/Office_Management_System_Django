from django.shortcuts import render,HttpResponse
from . models import Employee, Role, Department
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, 'index.html')



def all_emp(request):
    emp=Employee.objects.all()
    context={
        'emps':emp
    }
    print(context)
    
    return render(request, 'view_all_emp.html',context=context)
def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone_no = int(request.POST['phone_no'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])

        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone_no=phone_no,
            dept_id=dept,
            role_id=role,
            hire_date=datetime.now()
        )
        new_emp.save()
        return HttpResponse('Employee added successfully')

    elif request.method == 'GET':
        departments = Department.objects.all()  # Fetch all departments
        roles = Role.objects.all()  # Fetch all roles
        return render(request, 'add_emp.html', {'departments': departments, 'roles': roles})  # No pre-filled data

    else:
        return HttpResponse('An exception occurred! Employee has not been added')

    # return render(request, 'add_emp.html')

def remove_emp(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        try:
            emp = Employee.objects.get(id=emp_id)
            emp.delete()
            return HttpResponse('Employee removed successfully')
        except Employee.DoesNotExist:
            return HttpResponse('Employee not found')

    employees = Employee.objects.all()
    return render(request, 'remove_emp.html', {'employees': employees})


import re

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip().lower()
        dept = request.POST.get('dept', '').strip().lower()
        role = request.POST.get('role', '').strip().lower()

        emps = Employee.objects.all()

        # Normalize spaces (replace multiple spaces with a single space)
        name = re.sub(r'\s+', ' ', name)
        dept = re.sub(r'\s+', ' ', dept)
        role = re.sub(r'\s+', ' ', role)

        if name:
            name_parts = name.split()  # Split full name into parts
            for part in name_parts:
                emps = emps.filter(first_name__icontains=part) | emps.filter(last_name__icontains=part)

        if dept:
            emps = emps.filter(dept__name__icontains=dept)

        if role:
            emps = emps.filter(role__name__icontains=role)

        context = {'emps': emps}
        return render(request, 'view_all_emp.html', context)

    return render(request, 'filter_emp.html')
