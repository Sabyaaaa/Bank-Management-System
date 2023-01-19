from prettytable import PrettyTable

import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", passwd="1234", autocommit=True)
my_cursor = conn.cursor()
my_cursor.execute("create database if not exists bank1")
my_cursor.execute("use bank1")
my_cursor.execute(
    "create table if not exists customer(name varchar(45),phone_no varchar(45),aadhar_no varchar(45),acc_no int not null primary key auto_increment,acc_type varchar(45));")
my_cursor.execute(
    "create table if not exists transaction(trans_id int(12) not null primary key auto_increment,acc_no int(12) not null,to_acc_no int(12),amount int(10) not null,balance int(10) not null,trans_type varchar(20), trans_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,foreign key(acc_no) references customer(acc_no));")
print("***********************")
print("Welcome to HCL Bank")
print("***********************")


# Function to check available balance of customer
def availableBal():
    ac = input("Enter Account No :")
    s = ac
    b = "SELECT acc_type,balance FROM customer,transaction WHERE customer.acc_no=%s and transaction.acc_no=%s order by trans_id desc"
    data = (ac, s)
    c = conn.cursor(buffered=True)
    c.execute(b, data)
    try:
        result = c.fetchone()
        print("Balance for Account : ", ac, " is ", result[1])
        print("Type of Acc : ", result[0])
        print("\n")
        print("**************Available Balance Printed Successfully**************")
    except:
        print("No Records Found. Please Check Your Account Number.")


# function to check previous transaction of customer
def previousTrans():
    ac = input("Enter Account No :")
    b = "select * from transaction where acc_no=%s order by trans_id desc"
    data = (ac,)
    c = conn.cursor(buffered=True)
    c.execute(b, data)
    try:
        result = c.fetchone()
        t = PrettyTable(['Trans_id', 'AccNo', 'to_AccNo', 'Amount', 'Balance', 'Trans_type', 'Date'])
        t.add_row(result)
        print(t)
        print("\n")
        print("***************Previous Transaction Printed Successfully***************")
    except:
        print("No Records Found. Please Check Your Account Number.")


# Function to check transaction between given dates
def BalEnquiryDates():
    ac = input("Enter Account No :")
    frm = input("Enter the from date (YYYY-MM-DD) : ")
    t = input("Enter the to date (YYYY-MM-DD) : ")
    b = "select * from transaction where acc_no = %s and trans_date between %s and %s"
    data = (ac, frm, t)
    c = conn.cursor(buffered=True)
    c.execute(b, data)
    try:
        result = c.fetchall()
        t = PrettyTable(['Trans_id', 'AccNo', 'to_AccNo', 'Amount', 'Balance', 'Trans_type', 'Date'])
        t.add_rows(result)
        print("\n")
        print(t)
        print("\n")
        print("***************Transactions Between Given Dates are Printed Successfully***************")
    except:
        print("No Data Found. Please Check Your Account Number or Dates Given.")


# Creating a menu
while True:
    print('''
    1.Create account 
    2.Deposit amount
    3.Withdraw money 
    4.Transfer money 
    5.Balance Enquiry 
    6.Customer Details 
    7.Exit
    ''')

    ch = int(input("Enter your choice:"))
    if ch == 1:
        # Validating name field
        while True:
            try:
                a = '.'
                a1 = '#'
                a2 = '$'
                a3 = '*'
                a4 = '&'
                a5 = '='
                a6 = ','
                a7 = '@'
                a8 = '?'
                a9 = '/'
                name = input("Enter Your Name Here : ")
                if (a in name) or (a1 in name) or (a2 in name) or (a3 in name) or (a4 in name) or (a5 in name) or (
                        a6 in name) or (a7 in name) or (
                        a8 in name) or (a9 in name) \
                        or (name.isdigit()):
                    raise TypeError
                break
            except TypeError:
                print("Special Characters like . , @ # < > ? / ; and numbers are not allowed")

        # Validating phone number field
        while True:
            try:
                phone_no = input("Enter Your Phone Number : ")  # change
                if len(phone_no) != 10:
                    raise ValueError("Pls enter a valid 10 digit Number")
                break
            except ValueError as m:
                print(m)
        # Validating aadhar number field
        while True:
            try:
                aadhar_no = input("Enter Your 12 Digit Aadhar Number : ")
                if (len(aadhar_no) != 12) or (aadhar_no.isalpha()):
                    raise ValueError("Please Enter a valid 12 digit aadhar Number")
                break
            except ValueError as m:
                print(m)
        acc_type = input("Enter the Type of Account You Want (Savings/Current) : ")
        balance = input("Enter Deposit Amount: ")
        sql = "insert into customer(name,phone_no,aadhar_no,acc_type) values (%s ,%s , %s, %s )"
        val = (name, phone_no, aadhar_no, acc_type)
        my_cursor.execute(sql, val)
        select_Query = "select acc_no from customer where name = '" + name + "'"
        my_cursor.execute(select_Query)
        number = my_cursor.fetchone()[0]
        trans_type = "Deposit"
        my_cursor.execute(
            "insert into transaction(acc_no,amount,balance,trans_type) values('" + str(number) + "','" + str(
                balance) + "','" + str(balance) + "','" + trans_type + "')")
        my_cursor.execute("select * from customer where phone_no='" + phone_no + "'")
        print("Account is successfully created with account number: ", number)
        # for i in my_cursor:
        #     print(i)

    # Deposit amount
    elif ch == 2:
        number = input("Enter your Account number: ")
        deposit = int(input("Enter Amount to be deposited:"))
        select_Query = "select balance from transaction where acc_no = '" + str(
            number) + "' order by trans_id desc limit 1;"
        my_cursor.execute(select_Query)
        balance = 0
        try:
            balance = my_cursor.fetchone()[0]
        except:
            print("-------------------------------------------")
            print("         User Doesn't exist")
            print("-------------------------------------------")
            continue
        trans_type = "Deposit"
        my_cursor.execute(
            "insert into transaction(acc_no,amount,balance,trans_type) values('" + str(number) + "','" + str(
                deposit) + "','" + str(balance + deposit) + "','" + trans_type + "')")
        print("Rs.", deposit, "has been deposited successfully to Acc no", number)

    # Withdraw amount
    elif ch == 3:
        number = int(input("Enter your Account number: "))
        wd = int(input("Enter Amount to be withdrawn:"))
        select_Query = "select balance from transaction where acc_no = '" + str(
            number) + "' order by trans_id desc limit 1;"
        my_cursor.execute(select_Query)
        balance = 0
        try:
            balance = my_cursor.fetchone()[0]
        except:
            print("-------------------------------------------")
            print("         User Doesn't exist")
            print("-------------------------------------------")
            continue
        if wd <= balance:
            trans_type = "Withdraw"
            my_cursor.execute(
                "insert into transaction(acc_no,amount,balance,trans_type) values('" + str(number) + "','" + str(
                    wd) + "','" + str(balance - wd) + "','" + trans_type + "')")
            print("Rs.", wd, "has been withdrawn successfully from acc no", number)
        else:
            print("Sorry, Insufficient Balance")

    # Transfer Money from one account to another.
    elif ch == 4:
        number1 = int(input("Enter your Account number: "))
        transfer = int(input("Enter Amount to be transfered:"))
        number2 = int(input("Enter Account number to be transfered: "))
        select_Query = "select balance from transaction where acc_no = '" + str(
            number1) + "' order by trans_id desc limit 1;"
        my_cursor.execute(select_Query)
        balance = 0
        try:
            balance = my_cursor.fetchone()[0]
        except:
            print("-------------------------------------------")
            print("         User Doesn't exist")
            print("-------------------------------------------")
            continue
        select_Query1 = "select balance from transaction where acc_no = '" + str(
            number2) + "' order by trans_id desc limit 1;"
        my_cursor.execute(select_Query1)
        balance1 = 0
        try:
            balance1 = my_cursor.fetchone()[0]
        except:
            print("-------------------------------------------")
            print("         User Doesn't exist")
            print("-------------------------------------------")
            continue
        if transfer <= balance:
            trans_type = "Transfer"
            my_cursor.execute("insert into transaction(acc_no,to_acc_no,amount,balance,trans_type) values('" + str(
                number1) + "','" + str(number2) + "','" + str(transfer) + "','" + str(
                balance - transfer) + "','" + trans_type + "')")
            trans_type = "Deposit"
            my_cursor.execute(
                "insert into transaction(acc_no,amount,balance,trans_type) values('" + str(number2) + "','" + str(
                    transfer) + "','" + str(balance1 + transfer) + "','" + trans_type + "')")
            print("Rs.", transfer, "has been transfered successfully from account number : ", number1,
                  " to account number :", number2)
        else:
            print("Sorry, Insufficient Balance")

    # Balance Enquiry
    elif ch == 5:
        Task = input(''' 
        Please Enter Your Choice:
        1. Available Balance 
        2. Previous Transaction Details 
        3. Balance Enquiry Between Dates
        ''')
        if Task == '1':
            availableBal()  # for checking the available balance in account
        elif Task == '2':
            previousTrans() # checking the previous transaction
        elif Task == '3':
            BalEnquiryDates() # Transaction between dates
        else:
            print("Wrong input")

    # Customer Details
    elif ch == 6:
        ac = input("Enter Your Account Number : ")
        b = "select * from customer where acc_no=%s"
        data = (ac,)
        c = conn.cursor(buffered=True)
        c.execute(b, data)
        try:
            result = c.fetchone()
            print("Name : ", result[0])
            print("Phone Number : ", result[1])
            print("Aadhar Number : ", result[2])
            print("Account Number : ", result[3])
            print("Account Type : ", result[4])
            print("**********Customer Details Printed Successfully**********")
        except:
            print("No Records Found. Please Check Your Account Number.")
    else:
        break
