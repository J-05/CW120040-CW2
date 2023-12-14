import sqlite3

model_table = {
    "name" : "model", 
    "attributes" : [("model_code", "char(4)"), 
                    ("name", "varchar(50)"), 
                    ("capacity", "INT")],
    "fkeys" : [],
    "pkeys" : ["model_code"]
}

aircraft_table = {
    "name" : "aircraft", 
    "attributes" : [("aircraft_id", "INT"), 
                    ("model_code", "char(4)"), 
                    ("flight_id", "INT")],
    "fkeys" : [("model_code", "model"), ("flight_id", "flight")],
    "pkeys" : ["aircraft_id"]    
}

flight_table = {
    "name" : "flight", 
    "attributes" : [("flight_id", "INT"), 
                    ("departure_time", "DATETIME"),
                    ("arrival_time","DATETIME"),
                    ("departure_airport","char(3)"),
                    ("arrival_airport","char(3)"),
                    ("status","varchar(9)"),
                    ("aircraft_id","INT")],
    "fkeys" : [("aircraft_id", "aircraft")],
    "pkeys" : ["flight_id"]   
}

instance_table = {
    "name" : "instance", 
    "attributes" : [("flight_id", "INT"), 
                    ("pilot_id","INT")],
    "fkeys" : [("flight_id","flight"), ("pilot_id","pilot")],
    "pkeys" : ["flight_id", "pilot_id"]    
}

pilot_table = {
    "name" : "pilot", 
    "attributes" : [("pilot_id", "INT"), 
                    ("first_name","varchar(30)"), 
                    ("last_name","varchar(30)"), 
                    ("dob","DATE"), 
                    ("title","varchar(30)")],
    "fkeys" : [],
    "pkeys" : ["pilot_id"]
}

airline_db = [model_table, aircraft_table, flight_table, instance_table, pilot_table]

def get_table_from_name(name):
    for table in airline_db:
        if table["name"] == name:
            return table
        
def generate_create_table(name, attributes, f_keys, p_keys):
    parameters = [] # all parameters of create table

    # format for attributes
    for attribute, type in attributes:
        parameters.append(f"{attribute} {type}")
    
    # format for foreign keys
    for key, ref in f_keys:
        parameters.append(f"FOREIGN KEY ({key}) REFERENCES {ref} ({key})") 

    # format for primary keys
    parameters.append(f"PRIMARY KEY({", ".join(p_keys)})")

    return f"CREATE TABLE {name} (" + ", ".join(parameters) + ");"

def generate_insert(name, fields, rows, dupe_action):  # dupe action: REPLACE or IGNORE
    if fields == []:
        fields_specifier = ""
    else: 
        fields_specifier = f"({", ".join(fields)}) "
    return f"INSERT or {dupe_action} INTO {name} {fields_specifier}VALUES {", ".join(rows)};"

def generate_fetch(columns, table):
    return f"SELECT {", ".join(columns)} FROM {table};"

def generate_update(table_name, attributes, new_values, constraint):
    update_values = [f"{x} = {y}" for x, y in zip(attributes, new_values)]
    return f"UPDATE {table_name} SET {", ".join(update_values)} WHERE {constraint};"

if __name__ == "__main__":
    conn = sqlite3.connect("airline.db")
    curs = conn.cursor()
    # creates tables
    # for table in airline_db:
    #     curs.execute(f"DROP TABLE IF EXISTS {table["name"]};")
    #     curs.execute(generate_create_table(table["name"], table["attributes"], table["fkeys"], table["pkeys"]))
    
    curs.execute(generate_update("model", ["name", "capacity"], ["\"hisdkfjs\"", 123123], "name = \"silly\""))

    conn.commit()
    conn.close()