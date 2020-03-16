# To get the solutions to all 8 queries and put it in a file
from neo4j import GraphDatabase, basic_auth

# connection with authentication
driver = GraphDatabase.driver(
    "bolt://localhost", auth=basic_auth("neo4j", "1"), encrypted=False)

# driver = GraphDatabase.driver("bolt://localhost", encrypted=False)
session = driver.session()

output_string = ""

# [Q1]
output_string += "### Q1 ###\n"
result = session.run(
    "MATCH (actor:Actor)-[:ACTS_IN]->(movie:Movie) RETURN actor.name AS actor_name, COUNT(movie) AS number_of_films_acted_in ORDER BY number_of_films_acted_in DESC LIMIT 20")
for record in result:
    output_string += record['actor_name'] + ", " + \
        str(record['number_of_films_acted_in']) + "\n"
output_string += "\n"

# [Q2]
output_string += "### Q2 ###\n"
result = session.run(
    "MATCH (user:User)-[rated:RATED]->(movie:Movie) WHERE rated.stars <= 3  RETURN movie.title as movie_title, rated.stars")
for record in result:
    output_string += record['movie_title'] + "\n"
output_string += "\n"

# [Q3]
output_string += "### Q3 ###\n"
result = session.run(
    "MATCH (user:User)-[rated:RATED]->(movie:Movie),(actor:Actor)-[:ACTS_IN]->(movie:Movie) RETURN movie.title AS movie_title, COUNT(actor) AS number_of_cast_members ORDER BY number_of_cast_members DESC LIMIT 1")
for record in result:
    output_string += record['movie_title'] + ", " + \
        str(record['number_of_cast_members']) + "\n"
output_string += "\n"

# [Q4]
output_string += "### Q4 ###\n"
result = session.run(
    "MATCH ((actor:Actor)-[:ACTS_IN]->(movie:Movie)<-[:DIRECTED]-(director:Director)) WITH actor, collect(DISTINCT director) AS num_directors WHERE length(num_directors) >= 3 RETURN actor.name AS actor_name, length(num_directors) AS `number_of_directors_he/she_has_worked_with`")
for record in result:
    output_string += record['actor_name'] + ", " + \
        str(record['number_of_directors_he/she_has_worked_with']) + "\n"
output_string += "\n"

# [Q5]
output_string += "### Q5 ###\n"
result = session.run(
    "MATCH (bacon2:Actor)-[:ACTS_IN]->(movie2:Movie)<-[:ACTS_IN]-(bacon1:Actor)-[:ACTS_IN]->(movie:Movie)<-[:ACTS_IN]-(bacon0:Actor {name: 'Kevin Bacon'}) RETURN bacon2.name AS actor_name")
for record in result:
    output_string += record['actor_name'] + "\n"
output_string += "\n"

# [Q6]
output_string += "### Q6 ###\n"
result = session.run(
    "MATCH (actor:Actor)-[:ACTS_IN]->(movie:Movie) WHERE actor.name='Tom Hanks' RETURN movie.genre as genre, count(movie) as num")
for record in result:
    output_string += record['genre'] + "\n"
output_string += "\n"

# [Q7]
output_string += "### Q7 ###\n"
result = session.run(
    "MATCH (director:Director)-[:DIRECTED]->(movie:Movie) WITH director.name as director_name, count(movie.genre) as number_of_genres WHERE number_of_genres > 2 RETURN director_name, number_of_genres")
for record in result:
    output_string += record['director_name'] + \
        ", " + str(record['number_of_genres']) + "\n"
output_string += "\n"

# [Q8]
output_string += "### Q8 ###\n"
result = session.run("MATCH (director:Director)-[:DIRECTED]->(movie:Movie), (actor:Actor)-[:ACTS_IN]->(movie1:Movie) WHERE movie=movie1 RETURN director.name as director_name, actor.name as actor_name, count(director.name) as number_of_times_director_directed_actor ORDER BY number_of_times_director_directed_actor DESC LIMIT 5")
for record in result:
    output_string += record['director_name'] + ", " + str(record['actor_name']) + ", " + str(
        record['number_of_times_director_directed_actor']) + "\n"
output_string += "\n"

with open("output.txt", "w", encoding='utf-8') as output_file:
    output_file.write(output_string)

session.close()
