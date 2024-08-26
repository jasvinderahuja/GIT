# My repository of SQL queries:
- [Basics of SQL](SQL_basics.md)
- [MySQL Employee database queries](MySQL_EmployeeRecords_Rmarkdown.md)
Follow above link for a demonstration of the following commands–
```sql

use employee
SHOW TABLES
ALTER TABLE proj_table MODIFY COLUMN project_id VARCHAR(10)
ALTER TABLE proj_table ADD PRIMARY KEY(project_id)
UPDATE emp_record_table SET proj_id=NULL WHERE proj_id='NA'
ALTER TABLE emp_record_table ADD CONSTRAINT fk_proj FOREIGN KEY(proj_id) REFERENCES proj_table(PROJECT_ID)
ALTER TABLE data_science_team ADD CONSTRAINT fk_emp_record_table_emp_id FOREIGN KEY(emp_id) REFERENCES emp_record_table(emp_id)
DESCRIBE emp_record_table
SELECT * FROM emp_record_table WHERE proj_id = 'NA' OR proj_id IS NULL
SELECT emp_id, first_name, last_name, gender, dept FROM emp_record_table
SELECT emp_id, first_name, last_name, gender, dept FROM emp_record_table WHERE emp_rating < 2
SELECT emp_id, first_name, last_name, gender, dept FROM emp_record_table WHERE emp_rating BETWEEN 2 AND 4
SELECT emp_id, first_name, last_name, gender, dept FROM emp_record_table WHERE emp_rating < 2 OR emp_rating BETWEEN 2 AND 4 OR emp_rating > 4
SELECT CONCAT(first_name, ",", last_name) AS NAME FROM emp_record_table WHERE dept='FINANCE'
SELECT * FROM emp_record_table WHERE emp_id IN (SELECT DISTINCT manager_id from emp_record_table)
SELECT * FROM emp_record_table WHERE dept = 'HEALTHCARE' UNION SELECT * FROM emp_record_table WHERE dept = 'FINANCE'
SELECT emp_id, first_name, last_name, role, dept, MAX(emp_rating) AS max_emp_rating FROM emp_record_table GROUP BY emp_id, first_name, last_name, role, dept
SELECT ROLE, MIN(salary), MAX(salary) FROM emp_record_table GROUP BY ROLE
SELECT *, RANK() OVER (ORDER by exp DESC) FROM emp_record_table
DROP VIEW IF EXISTS vw_country
CREATE VIEW vw_country AS SELECT first_name, last_name, country FROM emp_record_table WHERE salary > 6000
SELECT * FROM ( SELECT * FROM emp_record_table WHERE exp > 10 ) AS T
DROP PROCEDURE IF EXISTS sp_exp
CREATE PROCEDURE sp_exp() BEGIN SELECT * FROM emp_record_table WHERE exp > 3; END;
--MySQL workbench version
CREATE PROCEDURE sp_exp() BEGIN SELECT * FROM emp_record_table WHERE exp > 3; END;

SELECT * ,
	CASE WHEN exp <= 2 THEN 'JUNIOR DATA SCIENTIST'
    WHEN exp > 2 AND EXP  <= 5 THEN 'ASSOCIATE DATA SCIENTIST'
    WHEN exp > 5 AND EXP  <= 10 THEN 'SENIOR DATA SCIENTIST'
    WHEN exp > 10 AND EXP  <= 12 THEN 'LEAD DATA SCIENTIST'
    WHEN exp > 12 AND EXP  <= 16 THEN 'MANAGER'
    END AS designation
FROM emp_record_table

CREATE INDEX ix_firstname ON emp_record_table(FIRST_NAME)
SELECT * , salary*0.05*emp_rating as bonus FROM emp_record_table
SELECT CONTINENT, COUNTRY, AVG(SALARY) AS average_salary FROM emp_record_table GROUP BY continent, country;

```
- [MySQL Orders database queries](MySQL_Orders.md)