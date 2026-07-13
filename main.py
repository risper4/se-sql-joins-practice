import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')


boston_employees = pd.read_sql("""
    SELECT employees.firstName, employees.lastName
                               FROM employees
                               JOIN offices
                               ON employees.officeCode = offices.officeCode
                               WHERE city = 'Boston';
""", conn)
# print(boston_employees)


zero_employees = pd.read_sql("""
    SELECT offices.officeCode, offices.city, COUNT(employees.employeeNumber) AS num_employees
                             FROM offices
                             LEFT JOIN employees
                             USING(officeCode)
                             GROUP BY officeCode
                             HAVING num_employees = 0 ;
""", conn)
# print(zero_employees)


office_customers = pd.read_sql("""
    SELECT offices.officeCode, officeS.city, COUNT(customers.customerNumber) AS customer_num
                               FROM offices
                               JOIN employees
                               USING(officeCode)
                               JOIN customers
                               ON customers.salesRepEmployeeNumber = employees.employeeNumber
                               GROUP BY offices.officeCode;                              
""", conn)
# print(office_customers)


product_names = pd.read_sql("""
    SELECT employees.firstName AS employee_name, products.productName AS product_name
                            FROM employees
                            JOIN customers
                            ON customers.salesRepEmployeeNumber = employees.employeeNumber
                            JOIN orders
                            USING(customerNumber)
                            JOIN orderdetails
                            USING(orderNumber)
                            JOIN products
                            USING(productCode);
""", conn)
# print(product_names)


product_number = pd.read_sql("""
    SELECT employees.firstName AS employee_name, SUM(orderDetails.quantityOrdered) AS product_num
                            FROM employees
                            JOIN customers
                            ON customers.salesRepEmployeeNumber = employees.employeeNumber
                            JOIN orders
                            USING(customerNumber)
                            JOIN orderdetails
                            USING(orderNumber)
                            JOIN products
                            USING(productCode)
                            GROUP BY employees.employeeNumber
                            ORDER BY employees.lastName;
""", conn)
# print(product_number)


product_numbers_above_200 = pd.read_sql("""
    SELECT employees.firstName AS employee_name, COUNT(products.productCode) AS dif_products_sold
                            FROM employees
                            JOIN customers
                            ON customers.salesRepEmployeeNumber = employees.employeeNumber
                            JOIN orders
                            USING(customerNumber)
                            JOIN orderdetails
                            USING(orderNumber)
                            JOIN products
                            USING(productCode)
                            GROUP BY employees.employeeNumber
                            HAVING dif_products_sold > 200
                            ORDER BY employees.lastName;
""", conn)
# print(product_numbers_above_200)


conn.close()
