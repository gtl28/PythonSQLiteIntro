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
    'Airport ID' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Airport Name' TEXT,
    Latitude FLOAT,
    Longitude FLOAT,
    'Time Difference' INTEGER
);
""")

# Create the Pilot table
conn.execute("""
CREATE TABLE Pilot (
    'Pilot ID' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Pilot Name' TEXT,
    'Pilot Age' INTEGER,
    'Flight Experience' INTEGER
);
""")

# Create the Plane table
conn.execute("""
CREATE TABLE Plane (
    'Plane ID' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Plane Name' TEXT,
    'Cargo Capacity' INTEGER,
    'People Capacity' INTEGER
);
""")

# Create the Schedule table
conn.execute("""
CREATE TABLE Schedule (
    'Schedule ID' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Planned Datetime' TEXT,
    'Actual Datetime' TEXT,
    Status TEXT
);
""")

# Create the Flight table
conn.execute("""
CREATE TABLE Flight (
    'Flight ID' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Origin Airport ID' INTEGER,
    'Destination Airport ID' INTEGER,
    'Departure Schedule ID' INTEGER,
    'Arrival Schedule ID' INTEGER,
    'Pilot ID' INTEGER,
    'Plane ID' INTEGER,
    FOREIGN KEY ('Origin Airport ID') REFERENCES Airport('Airport ID'),
    FOREIGN KEY ('Destination Airport ID') REFERENCES Airport('Airport ID'),
    FOREIGN KEY ('Departure Schedule ID') REFERENCES Schedule('Schedule ID'),
    FOREIGN KEY ('Arrival Schedule ID') REFERENCES Schedule('Schedule ID'),
    FOREIGN KEY ('Pilot ID') REFERENCES Pilot('Pilot ID'),
    FOREIGN KEY ('Plane ID') REFERENCES Plane('Plane ID')
);
""")

# Populate the Airport table
conn.execute("""
INSERT INTO Airport ('Airport Name', Latitude, Longitude, 'Time Difference') VALUES
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
INSERT INTO Pilot ('Pilot Name', 'Pilot Age', 'Flight Experience')
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
INSERT INTO Schedule ('Planned Datetime', 'Actual Datetime', 'Status') VALUES 
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
INSERT INTO Plane ('Plane Name', 'Cargo Capacity', 'People Capacity')
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
INSERT INTO Flight ('Origin Airport ID', 'Destination Airport ID', 'Departure Schedule ID', 'Arrival Schedule ID', 'Pilot ID', 'Plane ID')
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
    print("Please select a " + option_type)
    print("Your options are: ")
    for i in range(1, len(options)+1):
        print("Option " + str(i) + " : " + options[i-1])
    option_selected = False
    while not option_selected:
        option_index = input("\nSelect " + option_type + " : ")
        if option_index in [str(x) for x in range(1, len(options)+1)]:
            print("Option " + option_index + " : " + options[int(option_index) - 1] + " Selected\n")
            if return_type == "index":
                return int(option_index)
            if return_type == "element":
                return options[int(option_index) - 1]
        else:
            print("Option selection is not valid. Please try again.\n")


# Creation
def add_item(table_name):
    fields = []
    query = "PRAGMA table_info(" + tableName + ")"
    cursor.execute(query)
    fields = [x[1] for x in cursor.fetchall()]
    print("The " + table_name + " Table has the following fields: ")
    for field in fields:
        print(field)
    print("\n")

    select_option()
    #keep it simple as and just select row from each fields
# Creation
def add_pilot():
    print("Pilot Added")

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
    print("Pilot Removed")

# Deletion
def remove_flight():
    print("Flight")

print("Welcome to the Flight Management Database Application.")
print("The database has been reset and filled with example data.")
print("You many perform various CRUD operation on this data using the actions available in the Actions Menu")

actions = ["(Create) Add a new flight", "(Create) Add a new pilot", "(Read) View flight information", "(Read) View pilot schedule", "(Read) View table", "(Update) Update flight information", "(Update) Update destination information", "(Delete) Remove pilot", "(Delete) Remove flight"]
tables = []

while runApplication:
    print("\n-----------------------------------------")
    menuChoice = select_option("Action", actions, "index")
    
    match menuChoice:
        case 1:
            add_item("Flight")
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

cursor.close()
conn.close()
