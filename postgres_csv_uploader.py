import psycopg2
import csv

def execute_sql(connection, cursor, sql_statements):
    for statement in sql_statements:
        #print(statement)
        cursor.execute(statement)
    connection.commit()

def create_tables_and_foreign_keys(connection, cursor):
    # SQL statements to create tables
    create_table_statements = [
        """
        CREATE TABLE IF NOT EXISTS "property_listing" (
          "id" serial PRIMARY KEY,
          "listing_description" varchar,
          "price" bigint,
          "LT" bigint,
          "LB" int,
          "bedroom_count" int,
          "bathroom_count" int,
          "garage_count" int,
          "property_url" varchar(55),
          "agent_corporate_id" int,
          "user_id" int,
          "property_type_id" int,
          "location_id" int
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS "user" (
          "id" serial PRIMARY KEY,
          "name" varchar UNIQUE,
          "phone_number" varchar(20),
          "agent_id" int
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS "agent_corporate" (
          "id" serial PRIMARY KEY,
          "name" varchar UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS "listing_type" (
          "id" serial PRIMARY KEY,
          "name" char(8) UNIQUE
        );
        """,
         """
        CREATE TABLE IF NOT EXISTS "property_type" (
          "id" serial PRIMARY KEY,
          "name" char(11) UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS "location" (
          "id" serial PRIMARY KEY,
          "name" varchar UNIQUE
        );
        """
    ]
    
    # SQL statements to add foreign key constraints
    foreign_key_statements = [
        """
        ALTER TABLE "property_listing"
        ADD COLUMN IF NOT EXISTS "user_id" int;
        """,
        """
        ALTER TABLE "property_listing"
        ADD COLUMN IF NOT EXISTS "agent_id" int;
        """,
        """
        ALTER TABLE "property_listing"
        ADD COLUMN IF NOT EXISTS "property_type_id" int;
        """,
        """
        ALTER TABLE "property_listing"
        ADD COLUMN IF NOT EXISTS "listing_type_id" int;
        """,
        """
        ALTER TABLE "property_listing"
        ADD COLUMN IF NOT EXISTS "location_id" int;
        """,
        """
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY' AND table_name = 'property_listing' AND constraint_name = 'property_listing_agent_id_fkey') THEN
                ALTER TABLE "property_listing" ADD CONSTRAINT "property_listing_agent_id_fkey" FOREIGN KEY ("agent_id") REFERENCES "agent_corporate" ("id");
            END IF;
        END $$;
        """,
        """
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY' AND table_name = 'property_listing' AND constraint_name = 'property_listing_user_id_fkey') THEN
                ALTER TABLE "property_listing" ADD CONSTRAINT "property_listing_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "user" ("id");
            END IF;
        END $$;
        """,
        """
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY' AND table_name = 'property_listing' AND constraint_name = 'property_listing_type_fkey') THEN
                ALTER TABLE "property_listing" ADD CONSTRAINT "property_listing_type_fkey" FOREIGN KEY ("listing_type_id") REFERENCES "listing_type" ("id");
            END IF;
        END $$;
        """,
        """
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY' AND table_name = 'property_listing' AND constraint_name = 'property_listing_property_type_id_fkey') THEN
                ALTER TABLE "property_listing" ADD CONSTRAINT "property_listing_property_type_id_fkey" FOREIGN KEY ("property_type_id") REFERENCES "property_type" ("id");
            END IF;
        END $$;
        """,
        """
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY' AND table_name = 'property_listing' AND constraint_name = 'property_listing_location_id_fkey') THEN
                ALTER TABLE "property_listing" ADD CONSTRAINT "property_listing_location_id_fkey" FOREIGN KEY ("location_id") REFERENCES "location" ("id");
            END IF;
        END $$;
        """,
        """
        ALTER TABLE "user"
        ADD COLUMN IF NOT EXISTS "agent_id" int;
        """,
        """
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY' AND table_name = 'user' AND constraint_name = 'user_agent_id_fkey') THEN
                ALTER TABLE "user" ADD CONSTRAINT "user_agent_id_fkey" FOREIGN KEY ("agent_id") REFERENCES "agent_corporate" ("id");
            END IF;
        END $$;
        """
    ]

    # Execute table creation statements
    execute_sql(connection, cursor, create_table_statements)

    # Execute foreign key constraint statements
    execute_sql(connection, cursor, foreign_key_statements)

    print("Tables and Foreign Keys Established")


def insert_data(connection, cursor, username, phone_number, agent_corporate, property_location,
                description, property_type, bed, bath, garage, LT, LB, listing_type,
                property_url, price):
    
    # Handle escaped string
    for i, text in enumerate([username, agent_corporate, description]):
        if "'" in text:
            escaped_text = text.replace("'", "''")
            if i == 0:
                print(i)
                username = escaped_text
            elif i == 1:
                print(i)
                agent_corporate = escaped_text
            elif i == 2:
                print(i)
                description = escaped_text
               
    # Insert data into the "agent_corporate" table
    agent_corporate_insert = f"""
    INSERT INTO "agent_corporate" (name)
    VALUES ('{agent_corporate}')
    ON CONFLICT DO NOTHING;
    """
    
    # Insert data into the "property_type" table
    property_type_insert = f"""
    INSERT INTO "property_type" (name)
    VALUES ('{property_type}')
    ON CONFLICT DO NOTHING;
    """
    
    # Insert data into the "location" table
    location_insert = f"""
    INSERT INTO "location" (name)
    VALUES ('{property_location}')
    ON CONFLICT DO NOTHING;
    """
    
    # Insert data into the "listing_type" table
    listing_type_insert = f"""
    INSERT INTO "listing_type" (name)
    VALUES ('{listing_type}')
    ON CONFLICT DO NOTHING;
    """

    # Insert data into the "user" table
    user_insert = f"""
    INSERT INTO "user" ("name", "phone_number", "agent_id")
    VALUES ('{username}', '{phone_number}', (SELECT "id" FROM "agent_corporate" WHERE "name" = '{agent_corporate}' LIMIT 1))
    ON CONFLICT DO NOTHING;
    """

    # Insert data into the "property_listing" table
    property_listing_insert = f"""
    INSERT INTO "property_listing" (
        "listing_description", "price", "LT", "LB",
        "bedroom_count", "bathroom_count", "garage_count", "property_url", "user_id", "agent_id", "listing_type_id", "property_type_id", "location_id"
    )
    VALUES (
        '{description}', {price}, {LT}, {LB},
        {bed}, {bath}, {garage}, '{property_url}',
        (SELECT "id" FROM "user" WHERE "name" = '{username}' AND "phone_number" = '{phone_number}' LIMIT 1),
        (SELECT "id" FROM "agent_corporate" WHERE "name" = '{agent_corporate}' LIMIT 1),
        (SELECT "id" FROM "listing_type" WHERE "name" = '{listing_type}' LIMIT 1),
        (SELECT "id" FROM "property_type" WHERE name = '{property_type}' LIMIT 1),
        (SELECT "id" FROM "location" WHERE "name" = '{property_location}' LIMIT 1)
    );
    """
    # Execute SQL statements
    execute_sql(connection, cursor, [agent_corporate_insert, property_type_insert, location_insert, user_insert, listing_type_insert, property_listing_insert])
    #print("Data Inserted")

def insert_data_from_csv(connection, cursor, filepath):
    with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        total_rows = sum(1 for row in reader)
        print(f'Detected a total of {total_rows} rows in the dataset')
        csvfile.seek(0)  # Reset the file pointer to the beginning
        next(reader) # Skip header
        
        # Skip rows until the desired starting row
        start_row = 55065
        for _ in range(start_row - 1):
            next(reader)

        for i, row in enumerate(reader):
            try:
                insert_data(connection, cursor, row['user'], row['phone_number'], row['agent_corporate'],
                                row['property_location'], row['description'], row['property_type'],
                                float(row['bed']), float(row['bath']), float(row['garage']),
                                float(row['LT']), float(row['LB']), row['listing_type'],
                                row['property_url'], float(row['price (IDR. Million Rupiah)']))
                print(f"Inserted {start_row + i + 1} out of {total_rows} rows")
            except ValueError as e:
                print(row)
                print(f"Error inserting row {start_row + i + 1}: {e}")
                continue
    

def main():
    # Database Info
    hostname = "YOUR HOST HERE"
    username = "YOUR USERNAME HERE"
    password = "YOUR DATABASE PASSWORD HERE"
    port_id = "5432" # Default Port for PostgreSQL
    
    file_path = 'rumah123_bekasiv2_cleaned.csv'
    
    # Init connection and cursor
    connection = None
    cursor = None
    
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(
        host=hostname,
        user=username,
        password=password,
        port=port_id
    )

        # Create a cursor object to interact with the database
        cursor = connection.cursor()
        print(f'Connection Established')

        # Call the function to create tables and foreign keys
        create_tables_and_foreign_keys(connection, cursor)
        
        insert_data_from_csv(connection, cursor, file_path)

    except Exception as e:
        print("Error:", e)

    finally:
        # Remember to close the cursor and connection when done
        if connection is not None:
            connection.close()
        if cursor is not None:
            cursor.close()

if __name__ == "__main__":
    main()