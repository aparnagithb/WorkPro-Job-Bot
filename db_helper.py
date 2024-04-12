import mysql.connector
import re


mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="chatbot_schema"
    )
def store_details(query_text):


    # Create a cursor object to execute SQL queries
    cursor = mydb.cursor()

    user_details = {}
    pattern = r"Name: (\w+), Age: (\d+), Educational Qualifications: ([\w\s']+), Skills: ([\w\s,']+)"
    match = re.match(pattern, query_text)
    if match:
        user_details["name"] = match.group(1)
        user_details["age"] = match.group(2)
        user_details["education"] = match.group(3)
        user_details["skills"] = match.group(4)

        # SQL query to insert user details into the users table
        sql = "INSERT INTO users (Name, Age, Educational_Qualifications, Skills) VALUES (%s, %s, %s, %s)"
        values = (user_details["name"], user_details["age"], user_details["education"], user_details["skills"])

        # Execute the SQL query
        cursor.execute(sql, values)

        # Get the ID of the inserted user
        user_id = cursor.lastrowid

        # Commit changes to the database
        mydb.commit()

        # Close the cursor
        cursor.close()

        return f"Thank you !Now type in 'job search ' or 'trends' according to what you would like to see! . Your ID is {user_id}"
    else:
        return "Error: Unable to extract user details from the query text."


#store_details()
def fetch_user_data_from_database(user_id):
    # Create a cursor object to execute SQL queries
    cursor = mydb.cursor(dictionary=True)

    # SQL query to fetch user data based on the provided user ID
    sql = "SELECT * FROM users WHERE ID = %s"
    values = (user_id,)

    # Execute the SQL query
    cursor.execute(sql, values)

    # Fetch the user data
    user_data = cursor.fetchone()

    # Close the cursor
    cursor.close()

    return user_data

# Example usage
'''user_id =4 # Replace with the actual user ID
user_data = fetch_user_data_from_database(user_id)
print(user_data)'''
