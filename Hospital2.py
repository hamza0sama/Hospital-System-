from Hospital_database import Database

db = Database()
db.connection()

class Person:
    def __init__(self, name="", age=0, address=None, phone_number=None):
        self.name = name
        self.age = age
        self.address = address
        self.phone_number = phone_number

    def Add(self, table, cols, data):
        db.insert(table, cols, data)

    def Delete(self, table, ID):
        db.delete(table, ID)

    def Update(self, table, cols, updated_data, ID):
        db.update(table, cols, updated_data, ID)

    def Display(self, table):
        rows = db.display(table)
        for row in rows:
            print(row)

    def Search_id(self, table, ID):
        row = db.search_id(table, ID)
        if row:
            print(row)

    def Search_name(self, table, name):
        row = db.search_name(table, name)
        if row:
            print(row)

#***********************************************************************************************************************

class Doctor(Person):
    def Add(self, data): return super().Add("Doctor", ("Doctor_name","Doctor_Age","Doctor_Address","Doctor_number","Doctor_experience_years","Room_id"), data)
    def Delete(self, ID): return super().Delete("Doctor", ID)
    def Update(self, cols, data, ID): return super().Update("Doctor", cols, data, ID)
    def Search_id(self, ID): return super().Search_id("Doctor", ID)
    def Search_name(self, name): return super().Search_name("Doctor", name)
    def Display(self): return super().Display("Doctor")

#***********************************************************************************************************************

class Nurse(Person):
    def Add(self, data): return super().Add("Nurse", ("Nurse_name","Nurse_Age","Nurse_Address","Nurse_number","Doctor_id"), data)
    def Delete(self, ID): return super().Delete("Nurse", ID)
    def Update(self, cols, data, ID): return super().Update("Nurse", cols, data, ID)
    def Search_id(self, ID): return super().Search_id("Nurse", ID)
    def Search_name(self, name): return super().Search_name("Nurse", name)
    def Display(self): return super().Display("Nurse")

#***********************************************************************************************************************

class Patient(Person):
    def Add(self, data):super().Add("Patient", ("Patient_name","Patient_Age","Patient_Address","Patient_number","Room_id"), data)
    def Delete(self, ID):return super().Delete("Patient", ID)
    def Update(self, cols, data, ID): return super().Update("Patient", cols, data, ID)
    def Search_id(self, ID): return super().Search_id("Patient", ID)
    def Search_name(self, name): return super().Search_name("Patient", name)
    def Display(self): return super().Display("Patient")

#***********************************************************************************************************************

def handle_entity(entity_class, cols):
    entity = entity_class()
    operation = input("Operation (add/search/delete/update/display): ").strip().lower()

    if operation == "add":
        data = []
        for col in cols:
            val = input(f"Enter {col}: ").strip()
            try:
                if "Age" in col or "years" in col:
                    val = int(val)
            except ValueError:
                print(f"Invalid number for {col}, skipping...")
                return
            data.append(val)
        entity.Add(data)

    elif operation == "search":
        mode = input("Search by (id/name): ").strip().lower()
        if mode == "id":
            try:
                ID = int(input("Enter ID: ").strip())
                entity.Search_id(ID)
            except ValueError:
                print("Invalid ID!")
        elif mode == "name":
            name = input("Enter Name: ").strip()
            entity.Search_name(name)
        else:
            print("Invalid search mode!")

    elif operation == "delete":
        try:
            ID = int(input("Enter ID: ").strip())
            entity.Delete(ID)
        except ValueError:
            print("Invalid ID!")

    elif operation == "update":
        try:
            ID = int(input("Enter ID: ").strip())
        except ValueError:
            print("Invalid ID!")
            return

        updated_cols, updated_data = [], []
        for col in cols:
            if input(f"Update {col}? (y/n): ").lower() == "y":
                val = input(f"Enter new {col}: ").strip()
                try:
                    if "Age" in col or "id" in col.lower() or "years" in col:
                        val = int(val)
                except ValueError:
                    print(f"Invalid number for {col}, skipping...")
                    continue
                updated_cols.append(col)
                updated_data.append(val)
        entity.Update(updated_cols, updated_data, ID)

    elif operation == "display":
        entity.Display()

    else:
        print("Invalid operation!")

#***********************************************************************************************************************

def hospital_menu():
    while True:
        choice = input("\n1. Patient\n2. Doctor\n3. Nurse\n4. Exit\nChoose: ").strip()
        if choice == '1':
            handle_entity(Patient, ["Patient_name","Patient_Age","Patient_Address","Patient_number","Room_id",])
        elif choice == '2':
            handle_entity(Doctor, ["Doctor_name","Doctor_Age","Doctor_Address","Doctor_number","Doctor_experience_years","Room_id"])
        elif choice == '3':
            handle_entity(Nurse, ["Nurse_name","Nurse_Age","Nurse_Address","Nurse_number","Doctor_id"])
        elif choice == '4':
            db.close_Connection()
            print("Thank you!")
            break
        else:
            print("Wrong input, try again!")

hospital_menu()
