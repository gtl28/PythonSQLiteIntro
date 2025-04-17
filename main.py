import sqlite3

tableNames = ["Airport", "Pilot", "Plane", "Schedule", "Flight"]

def print2dArray(array, name):
    print("\n" + name + " Table:")

    maxColumnLengths = []

    for i in range(0, len(array[0])):
        lengths = []
        for j in range(0, len(array)):
            lengths.append(len(str(array[j][i])))
        maxColumnLengths.append(max(lengths))
    
    tableString = ""
    for j in range(0, len(array)):
        for i in range(0, len(array[0])):
            tableString += " " * (maxColumnLengths[i] - len(str(array[j][i]))) + str(array[j][i]) + " | "
        tableString += "\n"
        if j == 0:
            tableString += "-" * (len(tableString) - 2) + "\n"

    print(tableString)

# Connect to the database
conn = sqlite3.connect('store')
print("Database has been created")

# Delete any exisiting tables
for tableName in tableNames:
    conn.execute("DROP TABLE IF EXISTS " +  tableName)

# Create the Airport table
conn.execute("""
CREATE TABLE Airport (
    Airport_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Airport_Name TEXT,
    Latitude FLOAT,
    Longitude FLOAT,
    Time_Difference INTEGER
);
""")

# Create the Pilot table
conn.execute("""
CREATE TABLE Pilot (
    Pilot_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Pilot_Name TEXT,
    Pilot_Age INTEGER,
    Flight_Experience INTEGER
);
""")

# Create the Plane table
conn.execute("""
CREATE TABLE Plane (
    Plane_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Plane_Name TEXT,
    Cargo_Capacity INTEGER,
    People_Capacity INTEGER
);
""")

# Create the Schedule table
conn.execute("""
CREATE TABLE Schedule (
    Schedule_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Planned_Datetime TEXT,
    Actual_Datetime TEXT,
    Status TEXT
);
""")

# Create the Flight table
conn.execute("""
CREATE TABLE Flight (
    Flight_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Origin_Airport_ID INTEGER,
    Destination_Airport_ID INTEGER,
    Departure_Schedule_ID INTEGER,
    Arrival_Schedule_ID INTEGER,
    Pilot_ID INTEGER,
    Plane_ID INTEGER,
    FOREIGN KEY (Origin_Airport_ID) REFERENCES Airport(Airport_ID),
    FOREIGN KEY (Destination_Airport_ID) REFERENCES Airport(Airport_ID),
    FOREIGN KEY (Departure_Schedule_ID) REFERENCES Schedule(Schedule_ID),
    FOREIGN KEY (Arrival_Schedule_ID) REFERENCES Schedule(Schedule_ID),
    FOREIGN KEY (Pilot_ID) REFERENCES Pilot(Pilot_ID),
    FOREIGN KEY (Plane_ID) REFERENCES Plane(Plane_ID)
);
""")

# Populate the Airport table
conn.execute("""
INSERT INTO Airport (Airport_Name, Latitude, Longitude, Time_Difference) VALUES
('Los Angeles International', 33.9416, -118.4085, -8),
('John F. Kennedy International', 40.6413, -73.7781, -5),
('Heathrow', 51.4700, -0.4543, 0),
('Haneda', 35.5494, 139.7798, 9),
('Changi', 1.3644, 103.9915, 8),
('Dubai International', 25.2532, 55.3657, 4),
('Hong Kong International', 22.3080, 113.9185, 8),
('Sydney Kingsford Smith', -33.9399, 151.1753, 11),
('Charles de Gaulle', 49.0097, 2.5479, 1),
('Frankfurt am Main', 50.0379, 8.5622, 1);
""")

# Populate the Pilot table
conn.execute("""
INSERT INTO Pilot (Pilot_Name, Pilot_Age, Flight_Experience)
VALUES 
    ('John Smith', 45, 2000),
    ('Alice Johnson', 38, 1500),
    ('Michael Brown', 55, 3000),
    ('Tom Davis', 40, 1800),
    ('Emily Clark', 33, 5500),
    ('Sophia Lewis', 47, 2200),
    ('James Wilson', 52, 6600),
    ('Daniel White', 35, 8800),
    ('Liam Martin', 29, 7200),
    ('Emma Thompson', 42, 4100);
""")

# Populate the Schedule table
conn.execute("""
INSERT INTO Schedule (Planned_Datetime, Actual_Datetime, Status) VALUES 
('2025-04-16 08:00:00', '2025-04-16 08:00:00', 'On Time'),
('2025-04-16 15:00:00', '2025-04-16 23:00:00', 'Cancelled'),
('2025-04-17 10:00:00', '2025-04-17 11:00:00', 'Delayed'),
('2025-04-17 22:00:00', '2025-04-17 22:00:00', 'On Time'),
('2025-04-18 06:00:00', '2025-04-18 06:20:00', 'Delayed'),
('2025-04-18 14:00:00', '2025-04-18 14:00:00', 'On Time'),
('2025-04-18 20:00:00', '2025-04-18 20:55:00', 'Delayed'),
('2025-04-19 09:00:00', '2025-04-19 09:00:00', 'On Time'),
('2025-04-19 17:00:00', '2025-04-19 22:55:00', 'Delayed'),
('2025-04-20 12:00:00', '2025-04-20 23:15:00', 'Cancelled');
""")

# Populate the Plane table
conn.execute("""
INSERT INTO Plane (Plane_Name, Cargo_Capacity, People_Capacity)
VALUES 
    ('Boeing 747', 15000, 416),
    ('Airbus A380', 13000, 555),
    ('Boeing 777', 16000, 396),
    ('Airbus A350', 12000, 366),
    ('Boeing 787', 135000, 242),
    ('Embraer 190', 3000, 114),
    ('Boeing 767', 14500, 290),
    ('Airbus A320', 6800, 180),
    ('Airbus A321', 6700, 236),
    ('Boeing 737', 6700, 189);
""")

# Populate the Flight table
conn.execute("""
INSERT INTO Flight (Origin_Airport_ID, Destination_Airport_ID, Departure_Schedule_ID, Arrival_Schedule_ID, Pilot_ID, Plane_ID)
VALUES 
    (1, 2, 1, 2, 1, 3),
    (3, 4, 3, 4, 8, 3),
    (5, 6, 5, 6, 6, 3),
    (7, 1, 7, 8, 2, 8),
    (2, 8, 9, 10, 7, 9),
    (9, 3, 2, 3, 3, 1),
    (4, 5, 8, 1, 2, 2),
    (8, 10, 3, 5, 5, 7),
    (6, 9, 4, 7, 8, 8),
    (10, 7, 7, 2, 4, 9);
""")

cursor = conn.cursor()

def printTable(name):
    query = "SELECT * FROM " + name
    cursor.execute(query)
    rows = [list(row) for row in cursor.fetchall()]
    headings = [descriptions[0] for descriptions in cursor.description]
    table = [headings] + rows
    print2dArray(table, name)
    


runApplication = True

def select_option(option_type, options, return_type):
    print("Please select a " + option_type + " Option Number")
    print("Your options are: ")
    options = [str(option) for option in options]
    for i in range(1, len(options)+1):
        print("Option " + str(i) + " : " + options[i-1])
    option_selected = False
    while not option_selected:
        option_index = input("\nSelect " + option_type + " Option Number : ")
        if option_index in [str(x) for x in range(1, len(options)+1)]:
            print("Option " + option_index + " : " + options[int(option_index) - 1] + " Selected\n")
            if return_type == "index":
                return int(option_index)
            if return_type == "element":
                return options[int(option_index) - 1]
        else:
            print("Option selection is not valid. Please try again.\n")


# Creation
def get_fields(table_name):
    fields = []
    query = "PRAGMA table_info(" + tableName + ")"
    cursor.execute(query)
    fields = [x[1] for x in cursor.fetchall()]
    print("The " + table_name + " Table has the following fields: ")
    for field in fields:
        print(field)
    print("\n")
    return fields
    #keep it simple as and just select row from each fields

# Creation
def add_item_to_table(tableName):
    fields = get_fields(tableName)[1:]
    item = []

    for field in fields:
        query = "SELECT DISTINCT " + field + " FROM " + tableName
        cursor.execute(query)
        options = [row[0] for row in cursor.fetchall()]
        choice = select_option(field, options, "element")
        item.append(choice)

    print("Item to Add: " + str(item))
    fields_string = ", ".join(fields)
    item_values = ", ".join(item)
    query = "INSERT INTO " + tableName + " (" + fields_string + ") VALUES (" + item_values + ")"
    cursor.execute(query)
    print("Item added to " + tableName)

# Creation
def add_flight():
    tableName = "Flight"

    fields = get_fields(tableName)[1:]
    item = []

    for field in fields:
        print(field)
        query = "SELECT DISTINCT " + field + " FROM " + tableName
        cursor.execute(query)
        options = [row[0] for row in cursor.fetchall()]
        match field:
            case "Origin_Airport_ID":
                printTable("Airport")
            case "Destination_Airport_ID":
                printTable("Airport")
            case "Departure_Schedule_ID":
                printTable("Schedule") 
            case "Arrival_Schedule_ID":
                printTable("Schedule")
            case "Pilot_ID": 
                printTable("Pilot")
            case "Plane_ID":
                printTable("Plane")
        choice = select_option(field, options, "element")
        item.append(choice)

    print("Item to Add: " + str(item))
    fields_string = ", ".join(fields)
    item_values = ", ".join(item)
    query = "INSERT INTO " + tableName + " (" + fields_string + ") VALUES (" + item_values + ")"
    cursor.execute(query)
    print("New item added to " + tableName + " table.")
    print("The updated Flight table is below.")
    printTable("Flight")

# Creation
def add_pilot():
    print("Pilot added")

# Read
def view_flight():

    print("Flight Viewed")

# Read
def view_pilot_schedule():
    print("Pilot Schedule Viewed")

# Read
def view_table():
    tableSelected = select_option("Table", tableNames, "element")
    printTable(tableSelected)

# Update
def update_flight():
    print("Flight Updated")

# Update
def update_destination():
    print("Destination Information Updated")

# Deletion
def remove_pilot():
    print("This is the current Pilot table")
    printTable("Pilot")
    print("Please select the Pilot ID of the Pilot you wish to remove")
    query = "SELECT DISTINCT Pilot_ID FROM Pilot"
    cursor.execute(query)
    options = [row[0] for row in cursor.fetchall()]
    id_to_delete = select_option("Pilot ID", options, "element")
    query = "DELETE FROM Pilot WHERE Pilot_ID = " + id_to_delete
    cursor.execute(query)
    query = "DELETE FROM Flight WHERE Pilot_ID = " + id_to_delete
    cursor.execute(query)
    print("This is the updated Pilot table after a row was deleted")
    printTable("Pilot")

# Deletion
def remove_flight():
    print("This is the current Flight table")
    printTable("Flight")
    print("Please select the Flight ID of the Flight you wish to remove")
    query = "SELECT DISTINCT Flight_ID FROM Flight"
    cursor.execute(query)
    options = [row[0] for row in cursor.fetchall()]
    id_to_delete = select_option("Flight ID", options, "element")
    query = "DELETE FROM Flight WHERE Flight_ID = " + id_to_delete
    cursor.execute(query)
    print("This is the updated Flight table after a row was deleted")
    printTable("Flight")
    
def view_all_tables():
    for table in tableNames:
        printTable(table)

print("Welcome to the Flight Management Database Application.")
print("The database has been reset and filled with example data.")

print("All the tables in this database are shown below.")
view_all_tables()

print("You many perform various CRUD operation on this data using the actions available in the Actions Menu")



actions = ["(Create) Add a new flight", "(Create) Add a new pilot", "(Read) View flight information", "(Read) View pilot schedule", "(Read) View table", "(Update) Update flight information", "(Update) Update destination information", "(Delete) Remove pilot", "(Delete) Remove flight", "(View) View all tables"]
tables = []

while runApplication:
    print("\n-----------------------------------------")
    menuChoice = select_option("Action", actions, "index")
    
    match menuChoice:
        case 1:
            add_flight()
        case 2:
            add_pilot()
        case 3:
            view_flight()
        case 4:
            view_pilot_schedule
        case 5:
            view_table()
        case 6:
            update_flight()
        case 7:
            update_destination()
        case 8:
            remove_pilot()
        case 9:
            remove_flight()
        case 10:
            view_all_tables()

cursor.close()
conn.close()
