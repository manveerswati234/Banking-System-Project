import mysql.connector
from datetime import date
dt=date.today()
print("Today is   ",dt)
con= mysql.connector.connect(host='localhost', user= 'root', password= '', database='uinfo')
cur=con.cursor()
while True:
    print("----------WELCOME TO BANKING PROGRAM----------")
    print("Press-1 to create account.")
    print("Press-2 to Fund Withdrawl.")
    print("Press-3 to Fund Transfer.")
    print("Press-4 to Fund Deposite")
    print("Press-5 to Account Balance.")
    print("Press-6 to Pin Change.")
    print("Press-7 to Account Summary.")
    print("--------------------------------------")
    operation= int(input("Enter your choice-->"))
    if operation==1:
        print("Create account----")
        ac_no = input("Enter Your Account Number :")
        pin = int(input("Set your PIN: "))
        name = input("Enter your name: ")
        f_name = input("Enter your father's name: ")
        phone_no = input("Enter your phone number: ")
        gender = input("Enter your gender: ")
        country = input("Enter your country: ")
        state = input("Enter your state: ")
        city = input("Enter your city: ")
        balance= int(input("Enter your amount:"))
        cur.execute(f"insert into users(ac_no,pin,name,f_name,phone_no,gender,country,state,city,balance) values('{ac_no}',{pin},'{name}','{f_name}','{phone_no}','{gender}','{country}','{state}','{city}',{balance})")
        con.commit()
        print("Account Created Is Sucessfully_______")
    elif operation == 2:
        ac_no_withdrawl = input("Enter your account number :")
        pin_withdrawl = int(input("Enter your Pin no. :"))
        amount = int(input("Enter your amount :"))
        cur.execute(f"select pin, balance from users where ac_no = '{ac_no_withdrawl}'")
        result= cur.fetchone()

        if result is None:
            print("Account not found---")
        else:
            stored_pin, balance = result
            if stored_pin != pin_withdrawl:
                print("Incorrect Pin----")
            elif balance < amount:
                print("Insuficient Balance !")
            else:
                new_balance= balance-amount
                cur.execute(f"update users set balance = {new_balance} where ac_no = '{ac_no_withdrawl}'")
                con.commit()
                cur.execute(f"insert into mytrans(ac_no,balance,dt,ds) values ('{ac_no_withdrawl}',{amount},'{dt}','Withdrawl')")
                con.commit()
                print(f"Withdrawl Sucessfully. New Balance :{new_balance}")
    elif operation == 3:
        ac_no_from = input("Enter Sender Account Number :")
        pin_from = int(input("Enter Sender Pin_No. :"))
        ac_no_to = input("Enter Reciver Account Number :")
        transfer_amount= int(input("Enter The Amount To Transfer :"))
        cur.execute(f"select pin, balance from users where ac_no = '{ac_no_from}'")
        result_from = cur.fetchone()
        if result_from is None:
            print("Account Not Found----")
        else:
            stored_pin_from, balance_from = result_from
            if stored_pin_from != pin_from:
                print("Incorrect Pin----")
            elif balance_from < transfer_amount:
                print("Insuficient Balance !")
            else:
                cur.execute(f"select balance from users where ac_no = '{ac_no_to}'")
                result_to = cur.fetchone()
            if result_to is None:
                print("Reciever Account Not Found!!!")
            else:
                balance_to = result_to[0]
                new_balance_from = balance_from - transfer_amount
                new_balance_to = balance_to + transfer_amount
                cur.execute(f"update users set balance = {new_balance_from} where ac_no = '{ac_no_from}'")
                cur.execute(f"update users set balance = {new_balance_to} where ac_no = '{ac_no_to}'")
                con.commit()
                cur.execute(f"insert into mytrans(ac_no,balance,dt,ds) values('{ac_no_from}',{transfer_amount},'{dt}','Transfer')")
                con.commit()
                print(f"Transfer of {transfer_amount} sucessful from account '{ac_no_from}' to '{ac_no_to}'.")
    elif operation == 4:
        ac_no_deposite = input("Enter Your Account Number :")
        pin_deposite = int(input("Enter Your Pin :"))
        amount_deposite = int(input("Enter Your Amount To Deposite :"))
        cur.execute(f"select pin, balance from users where ac_no = '{ac_no_deposite}'")
        result_deposite = cur.fetchone()
        if result_deposite is None:
            print("Account Not Found----")
        else:
            stored_pin, balance= result_deposite
            if stored_pin != pin_deposite:
                print("Incorrect Pin----")
            else:
                new_balance_deposite = balance + amount_deposite
                cur.execute(f"update users set balance = {new_balance_deposite} where ac_no = '{ac_no_deposite}'")
                con.commit()
                cur.execute(f"insert into mytrans(ac_no, balance, dt, ds) values ('{ac_no_deposite}',{amount_deposite},'{dt}', 'Deposite')")
                con.commit()
                print(f"Your Amount Deposite{amount_deposite}. New Balance{new_balance_deposite}")

    elif operation == 5:
        ac_no_balance = input("Enter Your Account Number To Check Balance :")
        pin_balance = int(input("Enter Your Pin :"))
        cur.execute(f"select pin, balance from users where ac_no = '{ac_no_balance}'")
        result_balance = cur.fetchone()
        if result_balance is None:
            print("Account Not Found----")
        else:
            stored_pin, balance = result_balance
            if stored_pin != pin_balance:
             print("Incorrect Pin----") 
            else:
                print(f"Your Account Balance : {balance}")
    elif operation == 6:
        ac_no_pin = input("Enter Your Account Number To Change Pin---> ")
        old_pin = int(input("Enter Your Old Pin :"))
        new_pin = int(input("Enter Your New Pin :"))
        cur.execute(f"select pin from users where ac_no = '{ac_no_pin}'")
        result_pin = cur.fetchone()
        if result_pin is None:
            print("Account not found.")
        else:
            stored_pin, balance = result_pin[0]
            if stored_pin != old_pin:
                print("Incorrect old PIN.")
            else:
                cur.execute(f"update users set pin = {new_pin} where ac_no = '{ac_no_pin}'")
                con.commit()
                print("Pin Change Sucessfully------")
    elif operation == 7:
        ac_no_summary = input("Enter your account number for summary: ")
        pin_summary = int(input("Enter Your Pin."))
        cur.execute(f"select *  from users where ac_no = '{ac_no_summary}' and pin={pin_summary}")
        x=0
        for row in cur:
            x=x+1
        if x>0:
            cur.execute(f"select * from mytrans where ac_no = '{ac_no_summary}'")
            for row in cur:
                print(row)
        else:
           print("Invalid Pin.")
    cur.close()
    con.close() 

 