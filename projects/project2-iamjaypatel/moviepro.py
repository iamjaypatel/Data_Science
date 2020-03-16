import sqlite3 as lite
import csv
import re
con = lite.connect('cs1656.sqlite')

with con:
    cur = con.cursor()

    ########################################################################
    ### CREATE TABLES ######################################################
    ########################################################################
    # DO NOT MODIFY - START
    cur.execute('DROP TABLE IF EXISTS Actors')
    cur.execute(
        "CREATE TABLE Actors(aid INT, fname TEXT, lname TEXT, gender CHAR(6), PRIMARY KEY(aid))")

    cur.execute('DROP TABLE IF EXISTS Movies')
    cur.execute(
        "CREATE TABLE Movies(mid INT, title TEXT, year INT, rank REAL, PRIMARY KEY(mid))")

    cur.execute('DROP TABLE IF EXISTS Directors')
    cur.execute(
        "CREATE TABLE Directors(did INT, fname TEXT, lname TEXT, PRIMARY KEY(did))")

    cur.execute('DROP TABLE IF EXISTS Cast')
    cur.execute("CREATE TABLE Cast(aid INT, mid INT, role TEXT)")

    cur.execute('DROP TABLE IF EXISTS Movie_Director')
    cur.execute("CREATE TABLE Movie_Director(did INT, mid INT)")
    # DO NOT MODIFY - END

    ########################################################################
    ### READ DATA FROM FILES ###############################################
    ########################################################################
    # actors.csv, cast.csv, directors.csv, movie_dir.csv, movies.csv
    # UPDATE THIS

    with open("actors.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        for line in reader:
            cur.execute("INSERT INTO Actors VALUES(?, ?, ?, ?)", line)

    with open("cast.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        for line in reader:
            cur.execute("INSERT INTO Cast VALUES(?, ?, ?)", line)

    with open("directors.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        for line in reader:
            cur.execute("INSERT INTO Directors VALUES(?, ?, ?)", line)

    with open("movie_dir.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        for line in reader:
            cur.execute("INSERT INTO Movie_Director VALUES(?, ?)", line)

    with open("movies.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        for line in reader:
            cur.execute("INSERT INTO Movies VALUES(?, ?, ?, ?)", line)

    ########################################################################
    ### INSERT DATA INTO DATABASE ##########################################
    ########################################################################
    # UPDATE THIS TO WORK WITH DATA READ IN FROM CSV FILES

    # Sample Data, it is already inside the csv files, hence they are not needed here...

    # cur.execute("INSERT INTO Actors VALUES(1001, 'Harrison', 'Ford', 'Male')")
    # cur.execute("INSERT INTO Actors VALUES(1002, 'Daisy', 'Ridley', 'Female')")
    # cur.execute("INSERT INTO Actors VALUES(1003, 'Q1 Test', 'LastName', 'Female')")
    # cur.execute("INSERT INTO Actors VALUES(1004, 'Q4', 'Test', 'Male')")
    # cur.execute("INSERT INTO Actors VALUES(1005, 'Tommy', 'Lame', 'Male')")

    # cur.execute("INSERT INTO Movies VALUES(101, 'Star Wars VII: The Force Awakens', 2015, 8.2)")
    # cur.execute("INSERT INTO Movies VALUES(102, 'Rogue One: A Star Wars Story', 2016, 8.0)")
    # cur.execute("INSERT INTO Movies VALUES(103, 'Movie A', 1982, 8.0)")
    # cur.execute("INSERT INTO Movies VALUES(104, 'Movie B', 2016, 8.0)")
    # cur.execute("INSERT INTO Movies VALUES(105, 'Q2 Test Movie', 2016, 9.0)")

    # cur.execute("INSERT INTO Cast VALUES(1001, 101, 'Han Solo')")
    # cur.execute("INSERT INTO Cast VALUES(1002, 101, 'Rey')")
    # cur.execute("INSERT INTO Cast VALUES(1003, 103, 'Rey')")
    # cur.execute("INSERT INTO Cast VALUES(1003, 104, 'Rey')")
    # cur.execute("INSERT INTO Cast VALUES(1004, 103, 'Rey')")
    # cur.execute("INSERT INTO Cast VALUES(1003, 105, 'Rey')")
    # cur.execute("INSERT INTO Cast VALUES(1005, 105, 'Rey')")

    # cur.execute("INSERT INTO Directors VALUES(5000, 'J.J.', 'Abrams')")
    # cur.execute("INSERT INTO Directors VALUES(5001, 'Q10 Test', 'LastName')")

    # cur.execute("INSERT INTO Movie_Director VALUES(5000, 101)")
    # cur.execute("INSERT INTO Movie_Director VALUES(5001, 103)")

    con.commit()

    ########################################################################
    ### QUERY SECTION ######################################################
    ########################################################################
    queries = {}

    # DO NOT MODIFY - START
    # DEBUG: all_movies ########################
    queries['all_movies'] = '''
SELECT * FROM Movies
'''
    # DEBUG: all_actors ########################
    queries['all_actors'] = '''
SELECT * FROM Actors
'''
    # DEBUG: all_cast ########################
    queries['all_cast'] = '''
SELECT * FROM Cast
'''
    # DEBUG: all_directors ########################
    queries['all_directors'] = '''
SELECT * FROM Directors
'''
    # DEBUG: all_movie_dir ########################
    queries['all_movie_dir'] = '''
SELECT * FROM Movie_Director
'''
    # DO NOT MODIFY - END

    ########################################################################
    ### INSERT YOUR QUERIES HERE ###########################################
    ########################################################################
    # NOTE: You are allowed to also include other queries here (e.g.,
    # for creating views), that will be executed in alphabetical order.
    # We will grade your program based on the output files q01.csv,
    # q02.csv, ..., q12.csv

    # Q01 ########################
    queries['q01'] = '''
SELECT fname, lname FROM Actors WHERE EXISTS(
    SELECT * FROM Movies AS m JOIN Cast AS c ON c.mid = m.mid
    WHERE Actors.aid = c.aid AND m.year > 1980 AND m.year < 1990)
    AND EXISTS(SELECT * FROM Movies AS m JOIN Cast AS c ON c.mid = m.mid
    WHERE Actors.aid = c.aid AND m.year >= 2000)
ORDER BY Actors.lname, Actors.fname ASC
'''

    # Q02 ########################
    queries['q02'] = '''
SELECT m.title, m.year FROM Movies AS m WHERE 
    m.year = (SELECT f.year FROM Movies AS f WHERE f.title = 'Rogue One: A Star Wars Story')
    AND m.rank > (SELECT rank FROM Movies WHERE title = 'Rogue One: A Star Wars Story')
ORDER BY M.title ASC
'''

    # Q03 ########################
    queries['q03'] = '''
SELECT fname, lname FROM (
    SELECT fname, lname, count(aid) AS num FROM Actors WHERE aid = (
	SELECT c.aid FROM Movies AS m JOIN Cast AS c ON c.mid = m.mid 
	WHERE m.title LIKE '%Star Wars%'
	and c.aid = Actors.aid)
    GROUP BY fname, lname
    ORDER BY num DESC )
'''

    # Q04 ########################
    queries['q04'] = '''
SELECT fname, lname FROM Actors WHERE NOT EXISTS(
    SELECT * FROM Movies AS m JOIN Cast AS c ON c.mid = m.mid
    WHERE Actors.aid = c.aid AND m.year > 1985)
ORDER BY Actors.lname, Actors.fname ASC
'''

    # Q05 ########################
    queries['q05'] = '''
SELECT d.fname, d.lname, total.num 
FROM Directors AS d JOIN
    (SELECT did, count(did) AS num
    FROM Movie_Director
    GROUP BY did) AS total ON d.did = total.did
ORDER BY total.num DESC
LIMIT 20
'''

    # Q06 ########################
    queries['q06'] = '''
WITH a AS (SELECT title, COUNT(*) AS num FROM Cast c JOIN Movies m ON c.mid = m.mid
GROUP BY title)
SELECT title, a.num FROM a
WHERE a.num = (SELECT MAX(x.num) FROM a AS x)
ORDER BY a.num DESC
LIMIT 10
'''

    # Q07 ########################
    queries['q07'] = '''
WITH female AS (SELECT mid, COUNT(*) AS Fnum 
FROM Cast c JOIN Actors a ON c.aid = a.aid
WHERE a.gender = 'Female'
GROUP By mid)

SELECT k.title AS title, d.Fnum AS female_num, d.Mnum AS male_num FROM Movies k JOIN (
SELECT f.mid,
CASE WHEN Mnum IS NULL THEN 0 ELSE Mnum END AS Mnum, 
CASE WHEN Fnum IS NULL THEN 0 ELSE Fnum END AS Fnum 
FROM female f LEFT OUTER JOIN (SELECT mid, COUNT(*) AS Mnum
FROM Cast c JOIN Actors a ON c.aid = a.aid
WHERE a.gender = 'Male'
GROUP BY mid) m ON m.mid = f.mid) d ON d.mid = k.mid
WHERE d.Fnum > d.Mnum
ORDER BY title ASC
'''

    # Q08 ########################
    queries['q08'] = '''
SELECT fname, lname, out FROM (
SELECT aid, fname, lname, count(distinct did) AS out FROM (SELECT * FROM (SELECT * 
FROM (SELECT * FROM Actors A JOIN Cast C on A.aid = C.aid) ac 
JOIN Movies m on m.mid = ac.mid) acm JOIN movie_director md on md.mid = acm.mid)
GROUP BY aid, fname, lname	
HAVING out >= 7)
'''

    # Q09 ########################
    queries['q09'] = '''
WITH min_year AS (SELECT MIN(year) AS min, m.mid, aid, fname, lname 
FROM (SELECT * FROM Actors a JOIN Cast c on a.aid = c.aid) ac
JOIN Movies m on m.mid = ac.mid
GROUP By aid) 

SELECT fname, lname, COUNT(*) FROM (
    SELECT fname, lname, COUNT(*)
    FROM (SELECT * FROM Actors a JOIN Cast c on a.aid = c.aid) ac 
    JOIN Movies m on m.mid = ac.mid
    WHERE m.year = (
    SELECT min FROM min_year m WHERE m.aid = ac.aid)
    GROUP BY fname, lname
    ORDER BY COUNT(*) DESC )
WHERE fname LIKE 'T%'
'''

    # Q10 ########################
    queries['q10'] = '''
SELECT final.lname, final.title FROM (SELECT * FROM (SELECT * FROM (SELECT * 
FROM Actors a JOIN Cast c on a.aid = c.aid) 
ac JOIN Movies m on ac.mid = m.mid) acm JOIN Movie_Director md on md.mid = acm.mid) final 
JOIN Directors d on final.did = d.did
WHERE final.lname = d.lname
ORDER BY final.lname ASC
'''

    # Q11 ########################
    queries['q11'] = '''
WITH Recursive bacon AS (SELECT c.aid, c.mid, 0 AS rank
FROM Cast c JOIN Actors a on a.aid = c.aid WHERE a.fname = 'Kevin'
and a.lname = 'Bacon'
UNION ALL
SELECT c1.aid, c2.mid, b.rank + 1
FROM bacon b JOIN Cast c1 on c1.mid = b.mid
AND b.rank < 2
JOIN Cast c2 on c1.aid = c2.aid)

SELECT fname, lname FROM Actors WHERE aid IN 
    (SELECT aid
    FROM bacon 
    GROUP BY aid
    HAVING MIN(rank) = 2)
'''

    # Q12 ########################
    queries['q12'] = '''
SELECT fname, lname, COUNT(*), AVG(rank) 
FROM (SELECT * FROM Actors a JOIN Cast c on a.aid = c.aid) ac 
JOIN Movies m on m.mid = ac.mid
GROUP BY aid, fname, lname
ORDER BY AVG(rank) DESC
LIMIT 20
'''

########################################################################
### SAVE RESULTS TO FILES ##############################################
########################################################################
# DO NOT MODIFY - START
for (qkey, qstring) in sorted(queries.items()):
    try:
        cur.execute(qstring)
        all_rows = cur.fetchall()

        print("=========== ", qkey, " QUERY ======================")
        print(qstring)
        print("----------- ", qkey, " RESULTS --------------------")
        for row in all_rows:
            print(row)
        print(" ")

        save_to_file = (re.search(r'q0\d', qkey)
                        or re.search(r'q1[012]', qkey))
        if (save_to_file):
            with open(qkey+'.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerows(all_rows)
                f.close()
            print("----------- ", qkey+".csv",
                  " *SAVED* ----------------\n")

    except lite.Error as e:
        print("An error occurred:", e.args[0])
    # DO NOT MODIFY - END
