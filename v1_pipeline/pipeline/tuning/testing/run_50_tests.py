import urllib.request
import json
import time

url = "http://localhost:11434/api/generate"
model_name = "mohamedelawakey/sql_coder:latest"

questions = [
    # ----------------- LEVEL 1: VERY EASY (Simple SELECT & WHERE) -----------------
    "What is the nationality of the player messi?",
    "Show me all the books written in 2020.",
    "Get the names of employees who work in the IT department.",
    "What is the price of the item with the name 'MacBook Pro'?",
    "Find all the customers living in 'New York'.",
    "List the emails of users whose status is active.",
    "What is the population of the city named 'Tokyo'?",
    "Show the phone number for the hospital named 'Mercy'.",
    "Get the details of the car with the license plate 'XYZ-123'.",
    "What is the release date of the movie 'Inception'?",

    # ----------------- LEVEL 2: EASY (Aggregations, ORDER BY, LIMIT) -----------------
    "How many students are enrolled in the school?",
    "What is the average salary of the employees?",
    "Get the maximum score achieved in the exam.",
    "Show the top 5 most expensive products.",
    "List the 3 youngest players in the team.",
    "What is the total revenue for the year 2023?",
    "Show the names of the movies ordered by their rating from highest to lowest.",
    "Find the minimum age of a patient in the clinic.",
    "Count the number of cars that are red.",
    "List 10 cities ordered alphabetically.",

    # ----------------- LEVEL 3: MEDIUM (GROUP BY, HAVING, LIKE, Simple JOINs) -----------------
    "How many employees are there in each department?",
    "Show the average age of students grouped by their major.",
    "List the departments that have more than 50 employees.",
    "Find all users whose email ends with '@gmail.com'.",
    "What is the name of the department the employee 'John Doe' works in?",
    "Show the total sales for each product category.",
    "Get the names of the authors who have written more than 3 books.",
    "Find the products whose name contains the word 'Phone'.",
    "Count how many orders were made by each customer.",
    "List the artists and the count of their albums.",

    # ----------------- LEVEL 4: COMPLEX (Subqueries, Multiple JOINs) -----------------
    "What is the name of the manager of the IT department?",
    "Show the names of students who have scored higher than the average score of all students.",
    "Get the list of products that have never been ordered.",
    "Which customer has spent the most money in total?",
    "Find the employees who earn more than their department's average salary.",
    "Show the names of the actors who acted in a movie directed by 'Christopher Nolan'.",
    "List the top 3 cities with the highest number of total orders.",
    "Get the names of the courses taken by the student named 'Alice'.",
    "Which department has the highest average salary?",
    "Find the names of the customers who ordered a 'Laptop'.",

    # ----------------- LEVEL 5: VERY COMPLEX (Nested Subqueries, Advanced Logic, Multiple Tables) -----------------
    "Show the names of the employees who work in the same department as 'Sarah'.",
    "Find the names of the artists who have no albums released after 2010.",
    "Get the names of the customers who have ordered all the products available in the store.",
    "What is the name of the student who got the highest grade in the 'Math' course?",
    "List the names of the departments where the total salary is greater than 100000 and the number of employees is less than 10.",
    "Show the names of the movies that have been reviewed by more than 100 people and have an average rating above 4.5.",
    "Find the names of the players who have scored more goals than the average goals scored by players in their own team.",
    "Get the second highest salary from the employee table.",
    "List the names of the suppliers who supply at least one part that is used in the project named 'Apollo'.",
    "Show the names of the authors who have written books in both the 'Fiction' and 'Non-Fiction' genres."
]

markdown_output = "# 50 SQL Tests Evaluation Report\n\n"

for i, q in enumerate(questions):
    payload = {
        "model": model_name,
        "prompt": q,
        "stream": False
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        start_time = time.time()
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            sql_response = result.get("response", "").strip()
            duration = round(time.time() - start_time, 2)
            
            level = "Level 1: Very Easy" if i < 10 else \
                    "Level 2: Easy" if i < 20 else \
                    "Level 3: Medium" if i < 30 else \
                    "Level 4: Complex" if i < 40 else \
                    "Level 5: Very Complex"
            
            markdown_output += f"### Test {i+1} ({level})\n"
            markdown_output += f"**Question:** {q}\n\n"
            markdown_output += f"**Generated SQL ({duration}s):**\n```sql\n{sql_response}\n```\n\n---\n"
            print(f"Tested {i+1}/50: {q}")
    except Exception as e:
        print(f"Error on question {i+1}: {e}")

with open("50_tests_report.md", "w") as f:
    f.write(markdown_output)

print("\nFinished! Wrote results to 50_tests_report.md")
