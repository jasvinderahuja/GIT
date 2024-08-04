---
title: "Queries on orders database in MySQL"
author: "Jas Ahuja"
date: "2024-06-07"
output:
  html_document:
    keep_md: yes
    code_folding: show
    toc: true
    toc_depth: 3
    toc_float: true
    theme: readable
    css: style.css
  pdf_document:
    extra_dependencies: ["adjustbox"]
    toc: true
    toc_depth: 3
email: jasvinderahuja@gmail.com
Category: "SQL"
Tags: ["SQL", "Data Exploration", "Data Summarization"]
---
[Sample DB resources](https://dataedo.com/kb/databases/all/sample-databases)
## Setup

_css chunk to make tables fit_

<style type="text/css">
#TOC {
  margin: 3px 0px 3px 3px;
}

td{font-size: 12px;}
</style>

- Connection to the database through R-markdown


```r
library(DBI)
library(dplyr)
library(dbplyr)
library(tidyverse)

mypassword = readLines("mypass.gitignore") %>% trimws()

conn <- dbConnect(RMySQL::MySQL(),
                  dbname = "",
                  Server = "localhost",
                  port = 3306,
                  user = "root",
                  password = mypassword)

knitr::opts_chunk$set(connection = "conn", echo = TRUE, comment = NA, message = FALSE, warning = FALSE)
```

- create db and use it  


```sql
create database deliveries

```


```sql

use deliveries
```

- Now create the table "fact_deliveries"  

```sql
create table fact_deliveries(
	delivery_id character(30) not null,
	delivery_date date not null,
	delivery_status character(30) not null,
	order_type character(30) not null,
	total_amount float not null,
	merchant_id character(30) not null,
	merchant_rating float,
	consumer_id character(30),
    city_id character(30),
    city_name character(30)

);
```

- Insert values into the db  


```sql
INSERT INTO fact_deliveries(delivery_id, delivery_date, delivery_status, order_type,
                           total_amount, merchant_id, merchant_rating, consumer_id, city_id,
                           city_name)
VALUES 
('D1', '2021-01-01', 'Placed', 'Delivery', 100.0, 'M1', null, 'C1', 'city1', 'San Francisco'),
('D2', '2021-01-02', 'Placed', 'Pickup', 50.0, 'M2', 4.5, 'C2', 'city2', 'Los Angeles'),
('D1', '2021-01-01', 'Completed', 'Delivery', 100.0, 'M1', 2.5, 'C1', 'city1', 'San Francisco'),
('D2', '2021-01-02', 'Cancelled', 'Pickup', 50.0, 'M2', 4.5, 'C2', 'city2', 'Los Angeles'),
('D3', '2021-02-02', 'Placed', 'Pickup', 150.0, 'M1', null, 'C1', 'city2', 'Los Angeles')

```

- fact_deliveries EDA  


```sql

DESCRIBE fact_deliveries

```


<div class="knitsql-table">


Table: Displaying records 1 - 10

|Field           |Type     |Null |Key |Default |Extra |
|:---------------|:--------|:----|:---|:-------|:-----|
|delivery_id     |char(30) |NO   |    |NA      |      |
|delivery_date   |date     |NO   |    |NA      |      |
|delivery_status |char(30) |NO   |    |NA      |      |
|order_type      |char(30) |NO   |    |NA      |      |
|total_amount    |float    |NO   |    |NA      |      |
|merchant_id     |char(30) |NO   |    |NA      |      |
|merchant_rating |float    |YES  |    |NA      |      |
|consumer_id     |char(30) |YES  |    |NA      |      |
|city_id         |char(30) |YES  |    |NA      |      |
|city_name       |char(30) |YES  |    |NA      |      |

</div>
## to get the query into r-tibble  for any EDA 


```r
the_query = "SELECT * FROM fact_deliveries LIMIT 100"
act_deliveries_tb <- dbGetQuery(conn, the_query)
act_deliveries_tb
```

```
   delivery_id delivery_date delivery_status order_type total_amount
1           D1    2021-01-01          Placed   Delivery          100
2           D2    2021-01-02          Placed     Pickup           50
3           D1    2021-01-01       Completed   Delivery          100
4           D2    2021-01-02       Cancelled     Pickup           50
5           D3    2021-02-02          Placed     Pickup          150
6           D1    2021-01-01          Placed   Delivery          100
7           D2    2021-01-02          Placed     Pickup           50
8           D1    2021-01-01       Completed   Delivery          100
9           D2    2021-01-02       Cancelled     Pickup           50
10          D3    2021-02-02          Placed     Pickup          150
   merchant_id merchant_rating consumer_id city_id     city_name
1           M1              NA          C1   city1 San Francisco
2           M2             4.5          C2   city2   Los Angeles
3           M1             2.5          C1   city1 San Francisco
4           M2             4.5          C2   city2   Los Angeles
5           M1              NA          C1   city2   Los Angeles
6           M1              NA          C1   city1 San Francisco
7           M2             4.5          C2   city2   Los Angeles
8           M1             2.5          C1   city1 San Francisco
9           M2             4.5          C2   city2   Los Angeles
10          M1              NA          C1   city2   Los Angeles
```

## Now onto the question set-  


```sql
SELECT DISTINCT delivery_status FROM fact_deliveries 
```


<div class="knitsql-table">


Table: 3 records

|delivery_status |
|:---------------|
|Placed          |
|Completed       |
|Cancelled       |

</div>

### 1. Find the daily count of orders:
Expected output: delivery_date, num_orders


```sql

SELECT delivery_date, COUNT(DISTINCT delivery_id) as n_orders
  FROM fact_deliveries
  WHERE delivery_status != 'Cancelled'
  GROUP BY 1

```


<div class="knitsql-table">


Table: 3 records

|delivery_date | n_orders|
|:-------------|--------:|
|2021-01-01    |        1|
|2021-01-02    |        1|
|2021-02-02    |        1|

</div>

### 2. Find the DoD (day over day) count of orders to see how the business is doing
_Can brainstorm what is meant by - How business is doing?_
_There may not be an expectation outlined in the interviews_
Expected output: delivery_date, curr_day_orders, prev_day_orders. 

Options to consider - window functions:  
- LAG
- LEAD
- RANK
- DENSE RANK
STEPS -  
1. prepare inner dataframe - date, orders
2. apply window functions and get - date, current day orders, previous day orders
_NB: CTE (common table expression) is a good idea for readability. Here - (inner query) AS A - part._


```sql

SELECT A.delivery_date, A.n_orders as current_day_orders,
  LAG(A.n_orders, 1) OVER (ORDER BY A.delivery_date) as prev_day_orders
  FROM
(
  SELECT delivery_date, COUNT(DISTINCT delivery_id) as n_orders
  FROM fact_deliveries
  WHERE delivery_status != 'Cancelled'
  GROUP BY 1
) AS A

```


<div class="knitsql-table">


Table: 3 records

|delivery_date | current_day_orders| prev_day_orders|
|:-------------|------------------:|---------------:|
|2021-01-01    |                  1|              NA|
|2021-01-02    |                  1|               1|
|2021-02-02    |                  1|               1|

</div>

### 3. Daily count of orders across various cities
Expected output: city_name, delivery_date, num_order

_Further reading - how to get from day to - 
- week
- month
- quarter
- year


```sql

SELECT city_name, delivery_date, COUNT(DISTINCT delivery_id) as n_orders
FROM fact_deliveries
GROUP BY 1,2

```


<div class="knitsql-table">


Table: 3 records

|city_name     |delivery_date | n_orders|
|:-------------|:-------------|--------:|
|Los Angeles   |2021-01-02    |        1|
|Los Angeles   |2021-02-02    |        1|
|San Francisco |2021-01-01    |        1|

</div>

### 4.Find the list of merchants with a minimum of 3 avg merchant_rating
Expected output: merchant_id
_I want to add the merchant_rating also..._


```sql

SELECT A.merchant_id, A.avg_merchant_rating
  FROM
    (
    SELECT DISTINCT merchant_id, AVG(merchant_rating) AS avg_merchant_rating 
      FROM fact_deliveries
      WHERE merchant_rating IS NOT NULL
      GROUP BY 1
    ) AS A
  HAVING A.avg_merchant_rating >= 3

```


<div class="knitsql-table">


Table: 1 records

|merchant_id | avg_merchant_rating|
|:-----------|-------------------:|
|M2          |                 4.5|

</div>
_NB: Postgres-SQL may not work with HAVING_ 
_NB2: Try the WITH version of this command_   
 

### 5. Merchants that have the highest average ratings
Expected output: merchant_id

Choices -  
- row number (monotonic, one row one rank)  
- rank (if two rows have same rank then next is rank+1, it will skip the tied value)  
- dense rank (the tied value will not be skipped!)  

_[Follow this link for illustration of differences](https://community.sisense.com/t5/knowledge/difference-between-row-number-rank-and-dense-rank/ta-p/9021)_

```sql

SELECT B.merchant_id FROM
 (
 --
  SELECT A.merchant_id,
    ROW_NUMBER() OVER (ORDER BY A.avg_merchant_rating DESC) AS rnk FROM
        (
          SELECT merchant_id, AVG(merchant_rating) AS avg_merchant_rating 
          FROM fact_deliveries
          WHERE merchant_rating IS NOT NULL
          GROUP BY 1
        ) AS A
--
    ) AS B
WHERE B.rnk = 1
  

```


<div class="knitsql-table">


Table: 1 records

|merchant_id |
|:-----------|
|M2          |

</div>

### 6. In every city, find the merchant with the highest rating
Expected output: merchant_id, city_name
_PARTITION BY A.city_name_


```sql

SELECT B.merchant_id, B.city_name FROM
 (
 --
  SELECT A.merchant_id, A.city_name,
    ROW_NUMBER() OVER (PARTITION BY A.city_name ORDER BY A.avg_merchant_rating DESC) AS rnk FROM
        (
          SELECT merchant_id, city_name, AVG(merchant_rating) AS avg_merchant_rating 
          FROM fact_deliveries
          WHERE merchant_rating IS NOT NULL
          GROUP BY 1,2
        ) AS A
--
    ) AS B
WHERE B.rnk = 1

```


<div class="knitsql-table">


Table: 2 records

|merchant_id |city_name     |
|:-----------|:-------------|
|M2          |Los Angeles   |
|M1          |San Francisco |

</div>

### 7.  Find the merchant who has maximum cancelled orders overall
Expected output: merchant_id


```sql

SELECT merchant_id 
FROM (
 --
  SELECT merchant_id,
    ROW_NUMBER() OVER (ORDER BY A.num_orders DESC) AS rnk FROM
        (
          SELECT merchant_id, COUNT(delivery_id) AS num_orders 
          FROM fact_deliveries
          WHERE delivery_status = 'Cancelled'
          GROUP BY 1
        ) AS A
--
    ) AS B
WHERE B.rnk = 1

```


<div class="knitsql-table">


Table: 1 records

|merchant_id |
|:-----------|
|M2          |

</div>

### 8. Find the merchants who has maximum cancelled orders each day
Expected output: merchant_id, delivery_date, num_orders


```sql

SELECT B.merchant_id, B.delivery_date  
 FROM (
--
  SELECT A.merchant_id, A.delivery_date,
    ROW_NUMBER() OVER (PARTITION BY A.delivery_date ORDER BY A.num_orders DESC) AS rnk 
    FROM
        (
          SELECT merchant_id, delivery_date, COUNT(delivery_id) AS num_orders 
          FROM fact_deliveries
          WHERE delivery_status = 'Cancelled'
          GROUP BY 1,2
        ) AS A
--
 ) AS B
WHERE B.rnk = 1

```


<div class="knitsql-table">


Table: 1 records

|merchant_id |delivery_date |
|:-----------|:-------------|
|M2          |2021-01-02    |

</div>

### 9. Find the consumers and merchants from whom consumers ordered 3 or more times
Expected output: merchant_id, consumer_id


```sql

SELECT A.consumer_id, A.merchant_id FROM
( SELECT consumer_id, merchant_id, COUNT(delivery_id) AS num_orders 
  FROM fact_deliveries
  GROUP BY 1,2
) AS A 
WHERE A.num_orders >= 3

```


<div class="knitsql-table">


Table: 2 records

|consumer_id |merchant_id |
|:-----------|:-----------|
|C1          |M1          |
|C2          |M2          |

</div>
-- Alternative, having version-


```sql

 SELECT consumer_id, merchant_id, COUNT(delivery_id) AS num_orders 
  FROM fact_deliveries
  GROUP BY 1,2
HAVING num_orders >= 3

```


<div class="knitsql-table">


Table: 2 records

|consumer_id |merchant_id | num_orders|
|:-----------|:-----------|----------:|
|C1          |M1          |          6|
|C2          |M2          |          4|

</div>


### 10. Find the top performing merchants for each day (top performing means those having maximum orders/deliveries)
Expected output: delivery_date, merchant_id


```sql
SELECT B.delivery_date, B.merchant_id
FROM
(
    SELECT A.delivery_date, A.merchant_id, ROW_NUMBER() OVER (ORDER BY A.n_deliveries DESC) AS rnk
    FROM 
        ( 
          SELECT delivery_date, merchant_id, COUNT(delivery_id) as n_deliveries
          FROM fact_deliveries
          GROUP BY 1,2
          ) AS A
    ) AS B
WHERE rnk = 1

```


<div class="knitsql-table">


Table: 1 records

|delivery_date |merchant_id |
|:-------------|:-----------|
|2021-01-01    |M1          |

</div>

### 11. The number of customers who placed an order with the top merchant that day
Expected output: delivery_date, merchant_id, num_customers


```sql

WITH top_merchants AS (
  SELECT B.delivery_date, B.merchant_id
  FROM
  (
    SELECT A.delivery_date, A.merchant_id, ROW_NUMBER() OVER (ORDER BY A.n_deliveries DESC) AS rnk
    FROM 
        ( 
          SELECT delivery_date, merchant_id, COUNT(delivery_id) as n_deliveries
          FROM fact_deliveries
          GROUP BY 1,2
          ) AS A
    ) AS B
  WHERE rnk = 1
)

SELECT tm.delivery_date, tm.merchant_id, COUNT(DISTINCT fd.consumer_id) as n_customers
  FROM top_merchants tm 
    LEFT JOIN fact_deliveries fd
      ON tm.delivery_date = fd.delivery_date
        AND tm.merchant_id = fd.merchant_id
  GROUP BY 1,2

```


<div class="knitsql-table">


Table: 1 records

|delivery_date |merchant_id | n_customers|
|:-------------|:-----------|-----------:|
|2021-01-01    |M1          |           1|

</div>

__OK! The next ones are a bit hard and I am not sure I can do them in an interview setting yet. I understand and can come up with this logic due to my _R::dplyr_ and _pandas_ experience. But you will need to give me some time to code it!!__

### 12.  The number of first-time customers who placed an order with the top merchant that day. 
Expected output: delivery_date, merchant_id, num_first_time_customers

_Plan_
- Find top merchants (as above)
- First time customer (per customer min(delivery_date))
- Join 1 and 2

12.a    First order per customer = Min delivery date per customer  


```sql
-- a=per_customer_first_order      
SELECT consumer_id, min(delivery_date) AS first_order_date
  FROM fact_deliveries
  GROUP BY 1
-- a_end
```


<div class="knitsql-table">


Table: 2 records

|consumer_id |first_order_date |
|:-----------|:----------------|
|C1          |2021-01-01       |
|C2          |2021-01-02       |

</div>
12b. merchant for min delivery date per customer  


```sql
CREATE VIEW first_order_merchant AS
-- b=min_delivery_date_per_customer

  WITH per_customer_first_order AS
    (
-- a=per_customer_first_order      
      SELECT consumer_id, min(delivery_date) AS first_order_date
        FROM fact_deliveries
        GROUP BY 1
-- a_end
    )
  SELECT DISTINCT A.consumer_id, A.first_order_date, B.merchant_id
  FROM per_customer_first_order A
    LEFT JOIN fact_deliveries B
    ON A.consumer_id = B.consumer_id
    AND A.first_order_date = B.delivery_date
-- b_end

```


```sql
SELECT * FROM first_order_merchant
```


<div class="knitsql-table">


Table: 2 records

|consumer_id |first_order_date |merchant_id |
|:-----------|:----------------|:-----------|
|C1          |2021-01-01       |M1          |
|C2          |2021-01-02       |M2          |

</div>

12c. Get top merchants


```sql
CREATE VIEW top_merchants AS
(
-- c=get top merchants
  SELECT delivery_date, merchant_id, rnk
  FROM (
    SELECT delivery_date, merchant_id,
           ROW_NUMBER() OVER (PARTITION BY delivery_date ORDER BY num_orders DESC) AS rnk
     FROM (
          SELECT delivery_date, merchant_id, COUNT(delivery_id) AS num_orders
          FROM fact_deliveries
          GROUP BY 1,2
          ) AS A
     ) AS B
  WHERE rnk=1

  -- c_end
)

```


```sql
SELECT * FROM top_merchants
```


<div class="knitsql-table">


Table: 3 records

|delivery_date |merchant_id | rnk|
|:-------------|:-----------|---:|
|2021-01-01    |M1          |   1|
|2021-01-02    |M2          |   1|
|2021-02-02    |M1          |   1|

</div>


12.d.   Combine VIEWS and get a final result
_NB: This is how I would like to do it. But we could do it in one query also. See next-_  
_Also, we could make a function/procedure too but that would be an overkill? And, it involves extra syntax.._
_Expected output: delivery_date, merchant_id, num_first_time_customers_


```sql

SELECT E.merchant_id, E.delivery_date, COUNT(F.consumer_id) AS num_first_time_customers
FROM top_merchants E
  LEFT JOIN first_order_merchant F
  ON E.merchant_id = F.merchant_id
  AND E.delivery_date = F.first_order_date
GROUP BY 1,2

```


<div class="knitsql-table">


Table: 3 records

|merchant_id |delivery_date | num_first_time_customers|
|:-----------|:-------------|------------------------:|
|M1          |2021-01-01    |                        1|
|M2          |2021-01-02    |                        1|
|M1          |2021-02-02    |                        0|

</div>

### 12. The way to do this in one query is-


```sql

WITH 
per_customer_first_order AS
    (
-- a=per_customer_first_order      
      SELECT consumer_id, min(delivery_date) AS first_order_date
        FROM fact_deliveries
        GROUP BY 1
-- a_end
    ),
first_order_merchant AS
  (
-- b=min_delivery_date_per_customer
  SELECT DISTINCT A.consumer_id, A.first_order_date, B.merchant_id
  FROM per_customer_first_order A
    LEFT JOIN fact_deliveries B
    ON A.consumer_id = B.consumer_id
    AND A.first_order_date = B.delivery_date
-- b_end
  ),
top_merchants AS
(
-- c=get top merchants
  SELECT delivery_date, merchant_id, rnk
  FROM (
    SELECT delivery_date, merchant_id,
           ROW_NUMBER() OVER (PARTITION BY delivery_date ORDER BY num_orders DESC) AS rnk
     FROM (
          SELECT delivery_date, merchant_id, COUNT(delivery_id) AS num_orders
          FROM fact_deliveries
          GROUP BY 1,2
          ) AS A
     ) AS B
  WHERE rnk=1

  -- c_end
)



SELECT E.merchant_id, E.delivery_date, COUNT(F.consumer_id) AS num_first_time_customers
FROM top_merchants E
  LEFT JOIN first_order_merchant F
  ON E.merchant_id = F.merchant_id
  AND E.delivery_date = F.first_order_date
GROUP BY 1,2

```


<div class="knitsql-table">


Table: 3 records

|merchant_id |delivery_date | num_first_time_customers|
|:-----------|:-------------|------------------------:|
|M1          |2021-01-01    |                        1|
|M2          |2021-01-02    |                        1|
|M1          |2021-02-02    |                        0|

</div>

### 13.
The Day-over-Day (DoD) change in orders for daily top merchants from the previous day. 
Expected output: delivery_date, merchant_id, curr_day_orders, prev_day_orders 
- first check if date is formatted properly.


```sql

DESCRIBE fact_deliveries
```


<div class="knitsql-table">


Table: Displaying records 1 - 10

|Field           |Type     |Null |Key |Default |Extra |
|:---------------|:--------|:----|:---|:-------|:-----|
|delivery_id     |char(30) |NO   |    |NA      |      |
|delivery_date   |date     |NO   |    |NA      |      |
|delivery_status |char(30) |NO   |    |NA      |      |
|order_type      |char(30) |NO   |    |NA      |      |
|total_amount    |float    |NO   |    |NA      |      |
|merchant_id     |char(30) |NO   |    |NA      |      |
|merchant_rating |float    |YES  |    |NA      |      |
|consumer_id     |char(30) |YES  |    |NA      |      |
|city_id         |char(30) |YES  |    |NA      |      |
|city_name       |char(30) |YES  |    |NA      |      |

</div>
_Here, it is but if not, checkout this [article by Solomon Ayanlakin ](https://medium.com/@sia_ibk/exploring-various-date-time-related-functions-in-sql-d1b9ba06b0c6)


```sql

WITH
orders_perMerchant_perDay AS
( SELECT delivery_date, merchant_id, count(delivery_id) as n_orders
  FROM fact_deliveries
  GROUP BY 1,2
),
RankMerchant_perDay AS
( SELECT delivery_date, merchant_id, 
       ROW_NUMBER() OVER (PARTITION BY delivery_date ORDER BY n_orders DESC) AS rnk
  FROM orders_perMerchant_perDay
  GROUP BY 1,2
),
topRankMerchant_perDay AS
( SELECT delivery_date, merchant_id
  FROM RankMerchant_perDay
  WHERE rnk = 1
)

SELECT a.delivery_date, a.merchant_id, 
  COUNT(CASE WHEN b.delivery_date = a.delivery_date THEN delivery_id ELSE '' END) AS prev_day_orders,
  COUNT(CASE WHEN b.delivery_date = a.delivery_date THEN delivery_id ELSE '' END) AS curr_day_orders
  FROM topRankMerchant_perDay a
    LEFT JOIN fact_deliveries b
      ON a.merchant_id = b.merchant_id
      AND a.delivery_date >= b.delivery_date - 1
      AND a.delivery_date <= b.delivery_date
 GROUP BY 1,2

```


<div class="knitsql-table">


Table: 3 records

|delivery_date |merchant_id | prev_day_orders| curr_day_orders|
|:-------------|:-----------|---------------:|---------------:|
|2021-01-01    |M1          |               4|               4|
|2021-01-02    |M2          |               4|               4|
|2021-02-02    |M1          |               2|               2|

</div>



