import mysql.connector
import numpy as np
import matplotlib.pyplot as plt

# Get user input for database connection
host = input("Enter MySQL host (default: localhost): ") or "localhost"
user = input("Enter MySQL username (default: root): ") or "root"
password = input("Enter MySQL password: ")
database = input("Enter database name: ")

# Connect to MySQL database with error handling
try:
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor()
    if conn.is_connected():
        print("Connected to MySQL successfully")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

# Fetch data from SQL table with error handling
try:
    table_name = input("Enter table name: ")
    query = f"SELECT x_value, y_value FROM {table_name}"
    cursor.execute(query)
    data = cursor.fetchall()

    if not data:
        print("Error: No data found in the specified table.")
        exit()
except mysql.connector.Error as err:
    print(f"Error executing query: {err}")
    exit()

# Convert data to NumPy arrays
x, y = zip(*data)
x = np.array(x)
y = np.array(y)

# Calculate Pearson's correlation coefficient
correlation_matrix = np.corrcoef(x, y)
pearson_corr = correlation_matrix[0, 1]
if pearson_corr==1:
    print("It is perfect positive linear correlation.")
elif pearson_corr<1 and pearson_corr>0:
    print("It is positive linear correlation.")
elif pearson_corr<0 and pearson_corr>-1:
    print("It is negative linear correlation.")
elif pearson_corr==0:
    print("No linear correlation.")
elif pearson_corr==-1:
    print("It is perfect negative linear correlation.")

print(f"Karl Pearson’s coefficient of correlation: {pearson_corr:.4f}")

# Visualize the data with a scatter plot
plt.scatter(x, y, color='red', label='Data points')
plt.title("Scatter Plot of X vs Y")
plt.xlabel("X Values")
plt.ylabel("Y Values")
plt.legend()
plt.grid(True)
plt.show()

# Save result to a text file
with open("correlation_result.txt", "w") as f:
    f.write(f"Karl Pearson’s coefficient of correlation: {pearson_corr:.4f}\n")

print("Result saved to correlation_result.txt")

# Close connection
cursor.close()
conn.close()
