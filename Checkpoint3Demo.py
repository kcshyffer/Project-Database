import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
    except Error as e:
        print(e)
    return conn

def closeConnection(_conn, _dbFile):
    try:
        _conn.close()
    except Error as e:
        return
    
def clearScreen():
    print("\033c")
    
def enterContinue():
    placehold = input("Press enter when you are done viewing. ")
    
def intInput():
    return int(input("Enter a number: "))
    
# Returns 0 if transaction is possible, otherwise returns amount that can be withdrawn if not possible
def validAmount(_conn, serviceKey, materialAmount):
    curr = _conn.cursor()
    table = """
            SELECT l_materialamountkg
            FROM locations
            WHERE l_servicekey = ?
            """
    curr.execute(table, (serviceKey,))
    results = curr.fetchall()
    if(int(results[0][0]) >= materialAmount):
        return 0
    else:
        return int(results[0][0])
    
# Print menu with options: create account, view services, view accounts, add new services, remove old services, view sales, modify locations, purchase services
# Menu will have a few options, 1. Accounts 2. Services 3. Locations 4. Equipment 5. View Sales 6. View Materials
def displayMenu():
    print("--------------")
    print("1. Accounts")
    print("2. Services")
    print("3. Locations")
    print("4. Equipment")
    print("5. View Sales")
    print("6. View Materials")
    print("7. Exit Menu")

def addSale(totalPrice, orderDate, receiptDate, materialName, materialAmount, serviceKey, customerKey):
    return

def displaySales(_conn):
    clearScreen()
    curr = _conn.cursor()
    table = """
            SELECT * FROM sales
            """
    curr.execute(table)
    results = curr.fetchall()
    
    header = "{:<10} {:<20} {:<15} {:<15} {:<30} {:<20} {:<10} {:<10}"
    print((header.format("ID", "Total Price", "Order Date", "Receipt Date", "Material Name", "Material Amount", "Service Key", "Customer Key")))
    for row in results:
        print(header.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    enterContinue()

def displayServiceMenu():
    print("--------------")
    print("1. Display Services")
    print("2. Purchase Services")
    print("3. Add Services")
    print("4. Remove Services")
    print("5. Modify Services")
    print("6. Return")

def displayServices(_conn):
    return

def purchaseService(_conn, serviceKey, materialAmount):
    return

def addService(_conn, serviceFee, servicePrice, optionalDescription="No description", equipmentKey=1):
    return

def removeService(_conn, serviceKey):
    return

def modifyService(_conn, serviceKey):
    return
    
def displayLocationMenu():
    print("--------------")
    print("1. Display Locations")
    print("2. Add Locations")
    print("3. Remove Locations")
    print("4. Modify Locations")
    print("5. Return")

def displayLocations(_conn):
    curr = _conn.cursor()
    table = """
            SELECT * FROM locations
            """
    curr.execute(table)
    results = curr.fetchall()
    
    header = "{:<15} {:<35} {:<30} {:<20} {:<10}"
    print((header.format("Fee", "Name", "Material Name", "Material Amount", "Service Key")))
    for row in results:
        print(header.format(row[0], row[1], row[2], row[3], row[4]))
    enterContinue()

def addLocation(_conn, locationFee, locationName, materialName, materialAmountKG, serviceKey):
    modifyMaterial(_conn, materialName, materialAmountKG)
    curr = _conn.cursor()
    table = """
            INSERT INTO locations (l_locationfee, l_locationname, l_materialname, l_materialamountkg, l_servicekey)
            VALUES (?, ?, ?, ?, ?)
            """
    curr.execute(table, (locationFee, locationName, materialName, materialAmountKG, serviceKey))

def fetchMaterialAndAmountLocation(_conn, locationName):
    curr = _conn.cursor()
    table = """
            SELECT l_materialname, l_materialamountkg
            FROM locations
            WHERE l_locationname = ?
            """
    return curr.execute(table, (locationName,))

def removeLocation(_conn, locationName):
    materialRemove = fetchMaterialAndAmountLocation(_conn, locationName)
    modifyMaterial(_conn, materialRemove[0][0], -(materialRemove[0][1]))
    curr = _conn.cursor()
    table = """
            DELETE FROM locations
            WHERE l_locationname = ?
            """
    curr.execute(table, (locationName,))

def modifyLocation(_conn, locationName, materialChange, newFee=0):
    curr = _conn.cursor()
    if(newFee != 0):
        table = """
                UPDATE locations
                SET l_locationfee = ?,
                    l_materialamountkg = l_materialamountkg + ?
                WHERE locationName = ?
                """
        curr.execute(table, (newFee, materialChange, locationName))
    else:
        table = """
                UPDATE locations
                SET l_materialamountkg = l_materialamountkg + ?
                WHERE locationName = ?
                """
        curr.execute(table, (materialChange, locationName))

def handleLocations(_conn):
    while(True):
        clearScreen()
        displayLocationMenu()
        choice = intInput()
        clearScreen()
        if(choice == 1):
            displayLocations(_conn)
        elif(choice == 2):
            print("Starting creation process...")
            locationFee = int(input("Enter location fee: "))
            locationName = input("Enter location name: ")
            materialName = input("Enter material name: ")
            materialAmountKG = input("Enter material amount in KG: ")
            serviceKey = int(input("Enter service key: "))
            addLocation(_conn, locationFee, locationName, materialName, materialAmountKG, serviceKey)
            print("Added successfully!")
            enterContinue()
        elif(choice == 3):
            while(True):
                decision = input("Which location do you want removed? Type 0 to cancel or return. ")
                if(decision == '0'):
                    break
                else:
                    confirmation = input(f"Are you sure you want to delete location {decision}? Type Y to confirm, N to cancel. ")
                    if(confirmation == 'Y'):
                        removeLocation(_conn, decision)
                        print(f"Deleted location {decision}.")
                        enterContinue()
                        break
        elif(choice == 4):
            locationName = int(input("Which location do you want to modify? "))
            materialChange = input("By how much has the material changed?: ")
            feeChange = int(input("Has the fee changed to a new number? (0 if not): "))
            modifyLocation(_conn, materialChange, feeChange)
            print("Location changed successfully. ")
            enterContinue()
        elif(choice == 5):
            break

def displayEquipmentMenu():
    print("--------------")
    print("1. Display Equipment")
    print("2. View Equipment Record")
    print("3. Add Equipment")
    print("4. Remove Equipment")
    print("5. Modify Equipment Condition")
    print("6. Return")

def displayEquipment(_conn):
    curr = _conn.cursor()
    table = """
            SELECT * FROM equipment
            """
    curr.execute(table)
    results = curr.fetchall()
    
    header = "{:<10} {:<35} {:<15} {:<15} {:<10}"
    print((header.format("ID", "Name", "Condition", "Purchase Date", "Purchase Price")))
    for row in results:
        print(header.format(row[0], row[1], row[2], row[3], row[4]))
    enterContinue()

def displayEquipmentRecord(_conn):
    curr = _conn.cursor()
    table = """
            SELECT * FROM equipmentrecord
            """
    curr.execute(table)
    results = curr.fetchall()
    
    header = "{:<15} {:<15} {:<10} {:<10}"
    print((header.format("Use Date", "Condition", "ID", "Service ID")))
    for row in results:
        print(header.format(row[0], row[1], row[2], row[3]))
    enterContinue()

# Gets next available equipment ID
def fetchNextAvailableEquipmentID(_conn):
    curr = _conn.cursor()
    table = """
            SELECT MIN(e_equipmentkey + 1)
            FROM equipment e1
            WHERE NOT EXISTS (SELECT 1 FROM equipment e2 WHERE e2.e_equipmentkey = e1.e_equipmentkey + 1)
            """
    curr.execute(table)
    return curr.fetchall()[0][0]

def addEquipment(_conn, equipmentName, equipmentCondition, purchaseDate, purchasePrice):
    curr = _conn.cursor()
    table = """
            INSERT INTO equipment(e_equipmentkey, e_equipmentname, e_equipmentcondition, e_purchasedate, e_purchaseprice)
            VALUES (?, ?, ?, ?, ?)
            """
    curr.execute(table, (fetchNextAvailableEquipmentID(), equipmentName, equipmentCondition, purchaseDate, purchasePrice))

def removeEquipment(_conn, equipmentKey):
    curr = _conn.cursor()
    table = """
            DELETE FROM equipment
            WHERE e_equipmentkey = ?
            """
    curr.execute(table, (equipmentKey,))

def modifyEquipmentCondition(_conn, equipmentKey, newEquipmentCondition):
    curr = _conn.cursor()
    table = """
            UPDATE equipment
            SET e_equipmentcondition = ?
            WHERE e_equipmentkey = ?
            """
    curr.execute(table, (newEquipmentCondition, equipmentKey))

def handleEquipment(_conn):
    while(True):
        clearScreen()
        displayEquipmentMenu()
        choice = intInput()
        clearScreen()
        if(choice == 1):
            displayEquipment(_conn)
        elif(choice == 2):
            displayEquipmentRecord(_conn)
        elif(choice == 3):
            print("Starting creation process...")
            equipmentName = int(input("Enter equipment name: "))
            equipmentCondition = input("Enter equipment condition: ")
            purchaseDate = input("Enter purchase date: ")
            purchasePrice = input("Enter purchase price: ")
            addEquipment(_conn, equipmentName, equipmentCondition, purchaseDate, purchasePrice)
            print("Added successfully!")
            enterContinue()
        elif(choice == 4):
            while(True):
                decision = int(input("Which equipment ID do you want removed? Type 0 to cancel or return. "))
                if(decision == 0):
                    break
                else:
                    confirmation = input(f"Are you sure you want to delete equipment {decision}? Type Y to confirm, N to cancel. ")
                    if(confirmation == 'Y'):
                        removeEquipment(_conn, decision)
                        print(f"Deleted equipment {decision}.")
                        enterContinue()
                        break
        elif(choice == 5):
            equipmentKey = int(input("Which equipment do you want to modify? "))
            newCondition = input("What is the new condition (A, B, or C): ")
            modifyEquipmentCondition(_conn, equipmentKey, newCondition)
            print("Condition changed successfully. ")
            enterContinue()
        elif(choice == 6):
            break

# Displays all materials
def displayMaterials(_conn):
    clearScreen()
    curr = _conn.cursor()
    table = """
            SELECT * FROM materials
            """
    curr.execute(table)
    results = curr.fetchall()
    
    header = "{:<30} {:<10} {:<15} {:<15}"
    print((header.format("Material Name", "Density", "Amount (KG)", "Price per KG")))
    for row in results:
        print(header.format(row[0], row[1], row[2], row[3]))
    enterContinue()

# Command to modify materials, typically for amount change. 
def modifyMaterial(_conn, materialName, materialAmountChange, newMaterialPrice=0):
    curr = _conn.cursor()
    if(newMaterialPrice != 0):
        table = """    
                UPDATE materials
                SET m_materialpriceperkg = ?,
                    m_materialamountkg = m_materialamountkg + ?
                WHERE m_materialname = ?;
                """
        curr.execute(table, (newMaterialPrice, materialAmountChange, materialName))
    else:
        table = """    
                UPDATE materials
                SET m_materialamountkg = m_materialamountkg + ?
                WHERE m_materialname = ?;
                """
        curr.execute(table, (materialAmountChange, materialName))

# Displays account menu
def displayAccountMenu():
    print("--------------")
    print("1. Display Accounts")
    print("2. Register New Account")
    print("3. Return")
    return

# Gets next available customer ID (not just one after max, but say ID 3 if customer 3 has been deleted even if customer 4, 5, etc. exist)
def fetchNextAvailableCustomerID(_conn):
    curr = _conn.cursor()
    table = """
            SELECT MIN(c_customerkey + 1)
            FROM customers c1
            WHERE NOT EXISTS (SELECT 1 FROM customers c2 WHERE c2.c_customerkey = c1.c_customerkey + 1)
            """
    curr.execute(table)
    return curr.fetchall()[0][0]
   
# Creates customer name based off of ID 
def formatCustomerName(customerID):
    lenID = len(str(customerID))
    return "Customer#" + ('0' * (9 - lenID)) + str(customerID)

# Creates accounts with entered parameters
def createAccount(_conn, customerBalance="0", customerAddress="No address", customerPhoneNumber="No phone", customerEmail="No email"):
    curr = _conn.cursor()
    table = """
            INSERT INTO customers(c_customerkey, c_customername, c_customerbalance, c_address, c_phonenumber, c_email)
            VALUES (?, ?, ?, ?, ?, ?)
            """
    customerID = fetchNextAvailableCustomerID(_conn)
    curr.execute(table, (customerID, formatCustomerName(customerID), customerBalance, customerAddress, customerPhoneNumber, customerEmail))

# Displays all accounts
def displayAccounts(_conn):
    curr = _conn.cursor()
    table = """
            SELECT * FROM customers
            """
    curr.execute(table)
    results = curr.fetchall()
    
    header = "{:<10} {:<25} {:<10} {:<30} {:<15} {:<40}"
    print((header.format("ID", "Name", "Balance", "Address", "Number", "Email")))
    for row in results:
        print(header.format(row[0], row[1], row[2], row[3], row[4], row[5]))
    enterContinue()
        
# Account handling function
def handleAccounts(_conn):
    while(True):
        clearScreen()
        displayAccountMenu()
        choice = intInput()
        clearScreen()
        if(choice == 1):
            displayAccounts(_conn)
        elif(choice == 2):
            print("Starting creation process...")
            customerBalance = int(input("Enter customer balance: "))
            customerAddress = input("Enter customer address: ")
            customerNumber = input("Enter customer phone number: ")
            customerEmail = input("Enter customer email: ")
            createAccount(_conn, customerBalance, customerAddress, customerNumber, customerEmail)
            print("Added successfully!")
            enterContinue()
        elif(choice == 3):
            break
    

def main():
    database = r"Checkpoint2-dbase.sqlite3"

    # create a database connection
    conn = openConnection(database)
    
    while(True):
        clearScreen()
        displayMenu()
        choice = intInput()
        if(choice == 1):
            handleAccounts(conn)
        elif (choice == 2):
            displayServiceMenu()
        elif (choice == 3):
            handleLocations(conn)
        elif (choice == 4):
            handleEquipment(conn)
        elif (choice == 5):
            displaySales(conn)
        elif (choice == 6):
            displayMaterials(conn)
        elif (choice == 7):
            break
        
    clearScreen()

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
