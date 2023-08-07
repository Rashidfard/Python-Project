import pyodbc
from prettytable import PrettyTable
from tkinter import *
from persiantools.jdatetime import JalaliDateTime


class Db:
    def create_database(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=.;'
                              'Trusted_Connection=yes;'
                              )
        cursor = conn.cursor()
        cursor.commit()

        cursor.execute('CREATE DATABASE TestScore')
        cursor.commit()

    def connect_to_database(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=.;'
                              'Database=TestScore;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        return cursor

    def create_tables(self):
        cursor = self.connect_to_database()
        cursor.execute(''' CREATE TABLE STORAGE (
                            barcode integer primary key,
                            name text,
                            price integer,
                            off_price integer,
                            mojoodi integer)''')
        cursor.commit()

    def insert(self):
        newbarcode = new_barcode.get()
        newname = new_name.get()
        newprice = new_price.get()
        newoffprice = new_off_price.get()
        newmojoodi = new_mojoodi.get()
        cursor = self.connect_to_database()
        cursor.execute('''INSERT INTO STORAGE(barcode, name, price, off_price, mojoodi)
                            VALUES (?, ?, ?, ?, ?)''', (newbarcode, newname, newprice, newoffprice, newmojoodi))
        cursor.commit()
        new_barcode.delete(0, END)
        new_name.delete(0, END)
        new_price.delete(0, END)
        new_off_price.delete(0, END)
        new_mojoodi.delete(0, END)
        new_barcode.focus()

    def show_table(self):
        cursor = self.connect_to_database()
        cursor.execute('SELECT * FROM STORAGE')
        mytable = PrettyTable(['barcode', 'name', 'price', 'off_price', 'mojoodi'])
        data = cursor.fetchall()
        for row in data:
            mytable.add_row(row)
        print(mytable)

    def select_product(self):
        cursor = self.connect_to_database()
        cursor.execute('SELECT * FROM STORAGE')

    def delete_product(self):
        cursor = self.connect_to_database()
        self.select_product()
        deletebarcode = delete_barcode.get()
        cursor.execute(f'DELETE FROM STORAGE WHERE barcode = ?', [deletebarcode])
        cursor.commit()
        delete_barcode.delete(0, END)
        delete_barcode.focus()

    def search_product_barcode(self):
        cursor = self.connect_to_database()
        self.select_product()
        searchbarcode = search_barcode.get()
        cursor.execute(f'SELECT barcode, name, price, off_price, mojoodi FROM STORAGE WHERE barcode = ?'
                       , [searchbarcode])
        mytable_search = PrettyTable(['barcode', 'name', 'price', 'off_price', 'mojoodi'])
        data_search = cursor.fetchone()
        mytable_search.add_row(data_search)
        print(mytable_search)
        search_barcode.delete(0, END)
        search_barcode.focus()

    def update_product(self):
        cursor = self.connect_to_database()
        self.select_product()
        updatebarcode = update_barcode.get()
        updatename = update_name.get()
        updateprice = update_price.get()
        updateoffprice = update_off_price.get()
        updatemojoodi = update_mojoodi.get()
        cursor.execute(f'UPDATE STORAGE SET name = ?, price = ?, off_price = ?, mojoodi = ? WHERE barcode = ?',
                       [updatename, updateprice, updateoffprice, updatemojoodi, updatebarcode])
        cursor.commit()
        update_barcode.delete(0, END)
        update_name.delete(0, END)
        update_price.delete(0, END)
        update_off_price.delete(0, END)
        update_mojoodi.delete(0, END)
        update_barcode.focus()

    def sell_product_mojoodi(self):
        cursor = self.connect_to_database()
        records1 = []
        for row in mylist:
            sellupdatebarcode = row[0]
            sellupdatetedad = int(row[1])
            cursor.execute('SELECT name, price, off_price, mojoodi FROM STORAGE WHERE barcode = ?', sellupdatebarcode)
            record = cursor.fetchone()
            record_name = record[0]
            record_price = record[1]
            record_off_price = record[2]
            record_mojoodi = record[3]
            records = [sellupdatebarcode, record_name, sellupdatetedad, record_price, record_off_price]
            records1.append(records)
            self.select_product()
            cursor.execute(f'UPDATE STORAGE SET mojoodi = ? WHERE barcode = ?',
                           [record_mojoodi - sellupdatetedad, sellupdatebarcode])
            cursor.commit()
        return records1


db = Db()
# db.create_database()
# db.connect_to_database()
# db.create_tables()


# print('######################################add#######################################')
def add_product():
    global new_barcode
    global new_name
    global new_price
    global new_off_price
    global new_mojoodi
    window = Tk()
    window.title('Add Product')
    window.geometry('450x300')

    label1 = Label(text='Enter barcode : ')
    label1.place(x=30, y=35)
    new_barcode = Entry()
    new_barcode.place(x=150, y=35, width=200, height=25)
    label2 = Label(text='Enter name : ')
    label2.place(x=30, y=70)
    new_name = Entry()
    new_name.place(x=150, y=70, width=200, height=25)
    label3 = Label(text='Enter price : ')
    label3.place(x=30, y=105)
    new_price = Entry()
    new_price.place(x=150, y=105, width=200, height=25)
    label4 = Label(text='Enter off_price : ')
    label4.place(x=30, y=140)
    new_off_price = Entry()
    new_off_price.place(x=150, y=140, width=200, height=25)
    label5 = Label(text='Enter mojoodi : ')
    label5.place(x=30, y=175)
    new_mojoodi = Entry()
    new_mojoodi.place(x=150, y=175, width=200, height=25)
    addbtn = Button(text='ADD', command=db.insert)
    addbtn.place(x=150, y=210, width=200, height=25)

    window.mainloop()
# print('####################################add########################################')

# print('####################################delete######################################')
def delete_product():
    global delete_barcode
    window = Tk()
    window.title('Delete Product')
    window.geometry('450x200')

    label1 = Label(text='Enter barcode : ')
    label1.place(x=30, y=35)
    delete_barcode = Entry()
    delete_barcode.place(x=150, y=35, width=200, height=25)
    addbtn = Button(text='DELETE', command=db.delete_product)
    addbtn.place(x=150, y=100, width=200, height=25)

    window.mainloop()
# print('####################################delete########################################')

# print('####################################search_barcode######################################')
def search_product_by_barcode():
    global search_barcode
    window = Tk()
    window.title('Search Product')
    window.geometry('450x200')

    label1 = Label(text='Enter barcode : ')
    label1.place(x=30, y=35)
    search_barcode = Entry()
    search_barcode.place(x=150, y=35, width=200, height=25)
    addbtn = Button(text='SEARCH', command=db.search_product_barcode)
    addbtn.place(x=150, y=100, width=200, height=25)

    window.mainloop()
# print('####################################search_barcode########################################')

# print('####################################update########################################')
def update_product():
    global update_barcode
    global update_name
    global update_price
    global update_off_price
    global update_mojoodi
    window = Tk()
    window.title('Update Product')
    window.geometry('450x300')

    label1 = Label(text='Enter barcode : ')
    label1.place(x=30, y=35)
    update_barcode = Entry()
    update_barcode.place(x=150, y=35, width=200, height=25)
    label2 = Label(text='Enter name : ')
    label2.place(x=30, y=70)
    update_name = Entry()
    update_name.place(x=150, y=70, width=200, height=25)
    label3 = Label(text='Enter price : ')
    label3.place(x=30, y=105)
    update_price = Entry()
    update_price.place(x=150, y=105, width=200, height=25)
    label4 = Label(text='Enter off_price : ')
    label4.place(x=30, y=140)
    update_off_price = Entry()
    update_off_price.place(x=150, y=140, width=200, height=25)
    label5 = Label(text='Enter mojoodi : ')
    label5.place(x=30, y=175)
    update_mojoodi = Entry()
    update_mojoodi.place(x=150, y=175, width=200, height=25)
    addbtn = Button(text='UPDATE', command=db.update_product)
    addbtn.place(x=150, y=210, width=200, height=25)

    window.mainloop()
# print('####################################update########################################')

# print('####################################delete######################################')
def mojoodi_product():
    window = Tk()
    window.title('Mojoodi Product')
    window.geometry('400x200')

    addbtn = Button(text='MOJOODI TABLE', command=db.show_table)
    addbtn.place(x=110, y=80, width=200, height=25)

    window.mainloop()
# print('####################################delete########################################')

# # print('#####################################menu######################################')
def sell_product():
    global mylist1
    global mylist2
    global sell_update_barcode
    global sell_update_tedad
    window = Tk()
    window.title('Sell Product')
    window.geometry('450x300')
    mylist1 = []
    mylist2 = []
    lst1 = []
    lst2 = []

    def run(lst1, lst2):
        lst1.append(sell_update_barcode.get())
        lst2.append(sell_update_tedad.get())
        sell_update_barcode.delete(0, END)
        sell_update_tedad.delete(0, END)
        sell_update_barcode.focus()

    label1 = Label(text='Enter barcode : ')
    label1.place(x=30, y=35)
    sell_update_barcode = Entry()
    sell_update_barcode.place(x=150, y=35, width=200, height=25)
    label2 = Label(text='Enter tedad : ')
    label2.place(x=30, y=70)
    sell_update_tedad = Entry()
    sell_update_tedad.place(x=150, y=70, width=200, height=25)

    addbtn = Button(text='Sell', command=lambda: run(mylist1, mylist2))
    addbtn.place(x=150, y=105, width=200, height=25)

    window.mainloop()


flag = True
while flag:
    print('', '1. add product', '\n', '2. delete product', '\n', '3. search product', '\n', '4. update product',
          '\n', '5. table product', '\n', '6. sell product', '\n', '7. exit')
    choice = input('enter your choice : ')
    if choice == '1':
        add_product()
    elif choice == '2':
        delete_product()
    elif choice == '3':
        search_product_by_barcode()
    elif choice == '4':
        update_product()
    elif choice == '5':
        mojoodi_product()
    elif choice == '6':
        sell_product()
        mylist = zip(mylist1, mylist2)
        mylist = list(mylist)
        save = db.sell_product_mojoodi()

        class DateTime:
            def __init__(self):
                self.dt_now = JalaliDateTime.now()
                self.year = self.dt_now.strftime('%Y')
                self.month = self.dt_now.strftime('%B')
                self.day = self.dt_now.strftime('%d')
                self.time = self.dt_now.strftime('%H:%M:%S')

        class Product:
            def product_char(self):
                self.d = {}
                self.d['barcode'] = save[j][0]
                self.d['name'] = save[j][1]
                self.d['tedad'] = save[j][2]
                self.d['price'] = save[j][3]
                self.d['darsad_takhfif'] = save[j][4]

            def off(self):
                self.off_percentage = self.d['darsad_takhfif'] / 100
                return self.off_percentage

            def factor(self):
                self.off_price = round((self.d['price'] * (1 - self.off_percentage)), 2)
                self.mablagh = round((self.off_price * self.d['tedad']), 2)
                return [self.d['barcode'], self.d['name'], self.d['tedad'], self.d['price'], self.off_price,
                        self.mablagh]

        sum_factor = []
        for j in range(len(save)):
            x = lambda y: y[j]
            x(save)
            obj2 = Product()
            obj2.product_char()
            obj2.off()
            obj2.factor()
            sum_factor.append(obj2.factor())
        obj1 = DateTime()
        table1 = PrettyTable(['Year', 'Month', 'Day', 'time'])
        date_time = ([obj1.year, obj1.month, obj1.day, obj1.time])
        table1.add_row(date_time)
        print(table1.get_string(title='Date_Time'))
        table2 = PrettyTable(['barcode', 'Name', 'tedad', 'price', 'off_price', 'jam_factor'])
        for i in range(len(sum_factor)):
            x1 = lambda y1: y1[i]
            table2.add_row(x1(sum_factor))
        sum1 = 0
        for i in range(len(sum_factor)):
            sum1 += sum_factor[i][5]
        table2.add_row(['Total', '', '', '', '', "%.1f" % sum1])
        print(table2.get_string(title='factor_kharid'))
    elif choice == '7':
        flag = False
    else:
        print('incorrect selection')
# # print('####################################################################################')






