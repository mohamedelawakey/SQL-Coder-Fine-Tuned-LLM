import os
import json

base_questions = [
    # Schema 1: employees
    ("Tables: CREATE TABLE employees (id INT, name VARCHAR, department VARCHAR, salary INT, hire_date DATE)", [
        ("Level 1: Very Easy", "What is the name of the employee with id 5?"),
        ("Level 2: Easy", "How many employees are in the IT department?"),
        ("Level 4: Complex", "Which department has the highest average salary?"),
        ("Level 5: Very Complex", "Find the names of employees who earn more than the average salary of their own department.")
    ]),
    # Schema 2: students
    ("Tables: CREATE TABLE students (student_id INT, name VARCHAR, major VARCHAR, gpa FLOAT, age INT)", [
        ("Level 1: Very Easy", "Show all students named 'John'."),
        ("Level 2: Easy", "What is the average GPA of students in the 'Computer Science' major?"),
        ("Level 4: Complex", "List the majors that have more than 100 students."),
        ("Level 5: Very Complex", "What is the name of the youngest student who has the highest GPA in the 'Physics' major?")
    ]),
    # Schema 3: products
    ("Tables: CREATE TABLE products (product_id INT, name VARCHAR, category VARCHAR, price FLOAT, stock INT)", [
        ("Level 1: Very Easy", "What is the price of the product named 'iPhone'?"),
        ("Level 2: Easy", "Show the top 5 most expensive products."),
        ("Level 4: Complex", "List all categories that have less than 50 items in total stock."),
        ("Level 5: Very Complex", "Find the products whose price is higher than the average price of products in their respective category.")
    ]),
    # Schema 4: orders
    ("Tables: CREATE TABLE orders (order_id INT, customer_id INT, product_id INT, order_date DATE, amount FLOAT)", [
        ("Level 1: Very Easy", "Show the order details for order_id 101."),
        ("Level 2: Easy", "What is the total amount of orders placed on '2023-01-01'?"),
        ("Level 4: Complex", "Which customer has the highest total order amount?"),
        ("Level 5: Very Complex", "Find the customer_id of the customer who ordered the most distinct products.")
    ]),
    # Schema 5: movies
    ("Tables: CREATE TABLE movies (movie_id INT, title VARCHAR, director VARCHAR, release_year INT, rating FLOAT)", [
        ("Level 1: Very Easy", "What is the rating of the movie 'The Dark Knight'?"),
        ("Level 2: Easy", "Count how many movies were released in 2015."),
        ("Level 4: Complex", "Show the names of directors who have directed more than 5 movies."),
        ("Level 5: Very Complex", "Find the director who has the highest average rating for their movies released after 2000.")
    ]),
    # Schema 6: cars
    ("Tables: CREATE TABLE cars (car_id INT, make VARCHAR, model VARCHAR, year INT, color VARCHAR)", [
        ("Level 1: Very Easy", "Show the color of the car model 'Civic'."),
        ("Level 2: Easy", "How many 'Toyota' cars are there?"),
        ("Level 4: Complex", "List the makes of cars that have red color available in year 2020."),
        ("Level 5: Very Complex", "Find the make that has the widest variety of colors across all models.")
    ]),
    # Schema 7: patients
    ("Tables: CREATE TABLE patients (patient_id INT, name VARCHAR, age INT, disease VARCHAR, doctor_id INT)", [
        ("Level 1: Very Easy", "What disease does the patient named 'Alice' have?"),
        ("Level 2: Easy", "What is the average age of patients with 'Flu'?"),
        ("Level 4: Complex", "Count the number of patients for each doctor_id."),
        ("Level 5: Very Complex", "Find the doctor_id who treats patients with the highest average age.")
    ]),
    # Schema 8: hospitals
    ("Tables: CREATE TABLE hospitals (hospital_id INT, name VARCHAR, city VARCHAR, capacity INT)", [
        ("Level 1: Very Easy", "What is the capacity of the hospital named 'City Hospital'?"),
        ("Level 2: Easy", "List the hospitals in 'Boston' ordered by capacity."),
        ("Level 4: Complex", "Show the cities that have a total hospital capacity of more than 1000."),
        ("Level 5: Very Complex", "Find the city with the largest difference in capacity between its largest and smallest hospital.")
    ]),
    # Schema 9: countries
    ("Tables: CREATE TABLE countries (country_id INT, name VARCHAR, continent VARCHAR, population INT)", [
        ("Level 1: Very Easy", "What is the population of 'France'?"),
        ("Level 2: Easy", "Show the total population of countries in 'Europe'."),
        ("Level 4: Complex", "List the continents that have more than 10 countries."),
        ("Level 5: Very Complex", "Find the continent with the highest average country population, excluding countries with less than 1 million people.")
    ]),
    # Schema 10: cities
    ("Tables: CREATE TABLE cities (city_id INT, name VARCHAR, country_id INT, population INT)", [
        ("Level 1: Very Easy", "Show the country_id for the city 'Tokyo'."),
        ("Level 2: Easy", "What is the total population of all cities in country_id 5?"),
        ("Level 4: Complex", "Find the country_id that has the most cities listed."),
        ("Level 5: Very Complex", "List the city names that have a population greater than the average population of all cities in their same country_id.")
    ]),
    # Schema 11: authors
    ("Tables: CREATE TABLE authors (author_id INT, name VARCHAR, country VARCHAR)", [
        ("Level 1: Very Easy", "What country is the author 'J.K. Rowling' from?"),
        ("Level 2: Easy", "Count how many authors are from the 'USA'."),
        ("Level 4: Complex", "List the countries that have more than 5 authors."),
        ("Level 5: Very Complex", "Find the country that has exactly 3 authors whose names start with the letter 'A'.")
    ]),
    # Schema 12: books
    ("Tables: CREATE TABLE books (book_id INT, title VARCHAR, author_id INT, genre VARCHAR, publish_year INT)", [
        ("Level 1: Very Easy", "What is the genre of the book titled '1984'?"),
        ("Level 2: Easy", "Show all books published after 2010."),
        ("Level 4: Complex", "Find the author_id who has written the most books in the 'Fantasy' genre."),
        ("Level 5: Very Complex", "Find the author_id who has written books in both 'Sci-Fi' and 'Fantasy' genres.")
    ]),
    # Schema 13: users
    ("Tables: CREATE TABLE users (user_id INT, username VARCHAR, email VARCHAR, is_active BOOLEAN)", [
        ("Level 1: Very Easy", "Is the user with username 'admin' active?"),
        ("Level 2: Easy", "How many active users are there?"),
        ("Level 4: Complex", "List the email domains of all active users."),
        ("Level 5: Very Complex", "Find the number of active users who registered with a '@gmail.com' email address.")
    ]),
    # Schema 14: posts
    ("Tables: CREATE TABLE posts (post_id INT, user_id INT, content VARCHAR, likes INT)", [
        ("Level 1: Very Easy", "How many likes does post_id 42 have?"),
        ("Level 2: Easy", "Show the total likes for all posts by user_id 7."),
        ("Level 4: Complex", "Find the user_id with the highest total number of likes across all their posts."),
        ("Level 5: Very Complex", "List the user_ids whose average post likes are greater than the overall average post likes of all users.")
    ]),
    # Schema 15: teams
    ("Tables: CREATE TABLE teams (team_id INT, name VARCHAR, city VARCHAR, wins INT)", [
        ("Level 1: Very Easy", "How many wins does the 'Lakers' team have?"),
        ("Level 2: Easy", "Show all teams located in 'Los Angeles'."),
        ("Level 4: Complex", "Find the city with the highest total number of team wins."),
        ("Level 5: Very Complex", "List the cities that have more than one team, ordered by their total wins in descending order.")
    ]),
    # Schema 16: players
    ("Tables: CREATE TABLE players (player_id INT, name VARCHAR, team_id INT, goals INT, age INT)", [
        ("Level 1: Very Easy", "What is the age of the player 'Ronaldo'?"),
        ("Level 2: Easy", "How many goals has team_id 10 scored in total?"),
        ("Level 4: Complex", "Find the team_id that has the highest average player age."),
        ("Level 5: Very Complex", "Show the names of players who have scored more goals than any other player in their specific age group.")
    ]),
    # Schema 17: flights
    ("Tables: CREATE TABLE flights (flight_id INT, airline VARCHAR, origin VARCHAR, destination VARCHAR, price FLOAT)", [
        ("Level 1: Very Easy", "What is the price of flight_id 205?"),
        ("Level 2: Easy", "How many flights are departing from 'JFK'?"),
        ("Level 4: Complex", "Find the airline with the lowest average flight price."),
        ("Level 5: Very Complex", "List the origin and destination pairs that have flights from more than 3 different airlines.")
    ]),
    # Schema 18: passengers
    ("Tables: CREATE TABLE passengers (passenger_id INT, name VARCHAR, flight_id INT, seat VARCHAR)", [
        ("Level 1: Very Easy", "What seat does passenger 'Bob' have?"),
        ("Level 2: Easy", "How many passengers are on flight_id 300?"),
        ("Level 4: Complex", "Find the flight_id with the highest number of passengers."),
        ("Level 5: Very Complex", "Show the names of passengers who share the exact same name but are on different flights.")
    ]),
    # Schema 19: restaurants
    ("Tables: CREATE TABLE restaurants (restaurant_id INT, name VARCHAR, cuisine VARCHAR, rating FLOAT)", [
        ("Level 1: Very Easy", "What is the rating of 'Pasta House'?"),
        ("Level 2: Easy", "Count how many 'Italian' restaurants there are."),
        ("Level 4: Complex", "Find the cuisine with the highest average rating."),
        ("Level 5: Very Complex", "List the cuisines that have at least 5 restaurants and an average rating above 4.0.")
    ]),
    # Schema 20: reviews
    ("Tables: CREATE TABLE reviews (review_id INT, restaurant_id INT, user_id INT, rating FLOAT, comment VARCHAR)", [
        ("Level 1: Very Easy", "Show the comment for review_id 15."),
        ("Level 2: Easy", "What is the average rating given by user_id 99?"),
        ("Level 4: Complex", "Find the restaurant_id with the most reviews."),
        ("Level 5: Very Complex", "List the user_ids who have given a 5.0 rating to every single restaurant they reviewed.")
    ]),
    # Schema 21: teachers
    ("Tables: CREATE TABLE teachers (teacher_id INT, name VARCHAR, subject VARCHAR, salary INT)", [
        ("Level 1: Very Easy", "What subject does 'Mr. Smith' teach?"),
        ("Level 2: Easy", "Show the total salary paid to 'Math' teachers."),
        ("Level 4: Complex", "Find the subject with the lowest average teacher salary."),
        ("Level 5: Very Complex", "List the names of teachers whose salary is exactly 10% higher than the minimum salary in their subject.")
    ]),
    # Schema 22: courses
    ("Tables: CREATE TABLE courses (course_id INT, name VARCHAR, teacher_id INT, credits INT)", [
        ("Level 1: Very Easy", "How many credits is the 'Algebra' course?"),
        ("Level 2: Easy", "How many courses does teacher_id 3 teach?"),
        ("Level 4: Complex", "Find the teacher_id who teaches the most total credits."),
        ("Level 5: Very Complex", "Show the names of courses that share the same name but are taught by different teachers.")
    ]),
    # Schema 23: doctors
    ("Tables: CREATE TABLE doctors (doctor_id INT, name VARCHAR, specialty VARCHAR, hospital_id INT)", [
        ("Level 1: Very Easy", "What is the specialty of Dr. House?"),
        ("Level 2: Easy", "How many 'Cardiology' doctors are there?"),
        ("Level 4: Complex", "Find the hospital_id that has the most diverse set of specialties."),
        ("Level 5: Very Complex", "List the specialties that are present in every single hospital_id in the database.")
    ]),
    # Schema 24: animals
    ("Tables: CREATE TABLE animals (animal_id INT, name VARCHAR, species VARCHAR, zoo_id INT)", [
        ("Level 1: Very Easy", "What species is the animal named 'Simba'?"),
        ("Level 2: Easy", "How many 'Lion' animals are in zoo_id 1?"),
        ("Level 4: Complex", "Find the zoo_id with the highest count of unique species."),
        ("Level 5: Very Complex", "Show the species that have more than 10 animals in zoo_id 2 but less than 5 animals in zoo_id 3.")
    ]),
    # Schema 25: zoos
    ("Tables: CREATE TABLE zoos (zoo_id INT, name VARCHAR, city VARCHAR, area FLOAT)", [
        ("Level 1: Very Easy", "What city is the 'Central Zoo' located in?"),
        ("Level 2: Easy", "What is the total area of all zoos?"),
        ("Level 4: Complex", "Find the city with the largest total zoo area."),
        ("Level 5: Very Complex", "List the cities that have exactly two zoos, where one zoo's area is double the area of the other.")
    ]),
]

questions_list = []

# Generate 100 WITH schema
for schema, qs in base_questions:
    for level, question in qs:
        full_prompt = f"{schema}\\nQuestion: {question}"
        questions_list.append((level + " (With Schema)", full_prompt))
        
# Generate 100 WITHOUT schema
for schema, qs in base_questions:
    for level, question in qs:
        full_prompt = f"Question: {question}"
        questions_list.append((level + " (Without Schema)", full_prompt))

script_code = f"""import urllib.request
import json
import time

url = "http://localhost:11434/api/generate"
model_name = "sql_coder_v2:latest"

questions = {json.dumps([q[1] for q in questions_list], indent=4)}
levels = {json.dumps([q[0] for q in questions_list], indent=4)}

markdown_output = "# 200 SQL Tests Evaluation Report (Hardcoded Version)\\n\\n"

for i in range(200):
    q = questions[i]
    lvl = levels[i]
    
    payload = {{
        "model": model_name,
        "prompt": q,
        "stream": False
    }}
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={{'Content-Type': 'application/json'}})
    
    try:
        start_time = time.time()
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            sql_response = result.get("response", "").strip()
            duration = round(time.time() - start_time, 2)
            
            markdown_output += f"### Test {{i+1}} - {{lvl}}\\n"
            markdown_output += f"**Prompt sent to model:**\\n```text\\n{{q}}\\n```\\n\\n"
            markdown_output += f"**Generated SQL ({{duration}}s):**\\n```sql\\n{{sql_response}}\\n```\\n\\n---\\n"
            print(f"Tested {{i+1}}/200: {{lvl}}")
    except Exception as e:
        print(f"Error on question {{i+1}}: {{e}}")

with open("200_tests_report.md", "w") as f:
    f.write(markdown_output)

print("\\nFinished! Wrote results to 200_tests_report.md")
"""

with open("run_200_tests.py", "w") as f:
    f.write(script_code)
