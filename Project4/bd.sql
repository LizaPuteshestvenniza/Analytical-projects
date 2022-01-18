# Необходимый запросы

#1
SELECT
    DISTINCT city
FROM
    airports;
    
#2
SELECT
    departure_airport,
    COUNT(flight_id) as cnt_flights
FROM
    flights
GROUP BY
    departure_airport
ORDER BY
    cnt_flights DESC;

#3
SELECT
    aircrafts.model as model,
    COUNT(aircrafts.aircraft_code) as flights_amount
FROM
    aircrafts
    INNER JOIN flights ON aircrafts.aircraft_code=flights.aircraft_code
WHERE
    EXTRACT (month FROM CAST(flights.departure_time as date)) = '09'
GROUP BY
    aircrafts.model;
    
#4
SELECT
    CASE WHEN aircrafts.model LIKE '%Airbus%' THEN
        'Airbus'
    WHEN aircrafts.model LIKE '%Boeing%' THEN
        'Boeing'
    WHEN (aircrafts.model NOT LIKE '%Airbus%') AND (aircrafts.model NOT LIKE '%Boeing%') THEN
        'other'
    END as type_aircraft,
    COUNT(flights.flight_id) as flights_amount
FROM
    aircrafts
    INNER JOIN flights ON aircrafts.aircraft_code=flights.aircraft_code
WHERE
    EXTRACT (month FROM flights.departure_time) = '09'
GROUP BY
    type_aircraft;
    
#5
SELECT
    SUBQ.city as city,
    AVG(SUBQ.flight) as average_flights
FROM
    (SELECT
        airports.city as city,
        COUNT(flights.flight_id) as flight,
        DATE_TRUNC('day', flights.arrival_time) AS trunc_date
     FROM
         flights
         INNER JOIN airports ON flights.arrival_airport=airports.airport_code
         GROUP BY
             city,
             trunc_date
    ) as SUBQ
WHERE
    EXTRACT(month FROM SUBQ.trunc_date) = '08'
GROUP BY
    city;

#6
SELECT
    festival_name,
    EXTRACT(week FROM festival_date) as festival_week
FROM
    festivals
WHERE
    festival_city = 'Москва' AND
    festival_date BETWEEN '2018-07-23' AND '2018-09-30';

#7
SELECT
    tickets.week_number AS week_number,
    tickets.ticket_no AS ticket_amount,
    fest.festival_week AS festival_week,
    fest.festival_name AS name
FROM
    (
    SELECT
        airports.city,
        EXTRACT (WEEK FROM flights.arrival_time) AS week_number,
        COUNT (ticket_flights.ticket_no) AS ticket_no
    FROM
        airports
        INNER JOIN flights ON airports.airport_code = flights.arrival_airport
        INNER JOIN ticket_flights ON flights.flight_id = ticket_flights.flight_id
    WHERE (EXTRACT (WEEK FROM flights.arrival_time) BETWEEN '30' AND '39')
        AND city = 'Москва'
    GROUP BY
        airports.city,
        EXTRACT (WEEK FROM flights.arrival_time)
    ) AS tickets
 
LEFT JOIN   
 
        (
    SELECT
        festival_name,
        EXTRACT (WEEK FROM festival_date) AS festival_week
    FROM
        festivals
    WHERE
        (festival_date BETWEEN '2018-07-23' AND '2018-09-30')
        AND
        festival_city = 'Москва'
        ) 
    AS fest
ON tickets.week_number = fest.festival_week;
