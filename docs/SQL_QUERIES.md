# SQL Queries for Cryptocurrency Analysis

This document provides examples of SQL queries you can use to analyze your cryptocurrency data. These queries demonstrate the use of advanced SQL features like WINDOW FUNCTIONS for calculating rolling averages and trend analysis.

## Basic Queries

### Get Latest Prices

```sql
-- PostgreSQL
WITH latest_prices AS (
    SELECT 
        coin_id,
        MAX(timestamp) as latest_timestamp
    FROM 
        crypto_prices
    GROUP BY 
        coin_id
)
SELECT 
    cp.*
FROM 
    crypto_prices cp
JOIN 
    latest_prices lp ON cp.coin_id = lp.coin_id AND cp.timestamp = lp.latest_timestamp
ORDER BY 
    cp.market_cap DESC;

-- MySQL
SELECT cp.*
FROM crypto_prices cp
INNER JOIN (
    SELECT coin_id, MAX(timestamp) as latest_timestamp
    FROM crypto_prices
    GROUP BY coin_id
) latest ON cp.coin_id = latest.coin_id AND cp.timestamp = latest.latest_timestamp
ORDER BY cp.market_cap DESC;
```

### Get Price History for a Specific Coin

```sql
-- PostgreSQL
SELECT 
    coin_id,
    coin_name,
    price_usd,
    timestamp,
    price_change_percentage_24h
FROM 
    crypto_prices
WHERE 
    coin_id = "bitcoin"
    AND timestamp >= CURRENT_TIMESTAMP - INTERVAL "30 days"
ORDER BY 
    timestamp;

-- MySQL
SELECT 
    coin_id,
    coin_name,
    price_usd,
    timestamp,
    price_change_percentage_24h
FROM 
    crypto_prices
WHERE 
    coin_id = "bitcoin"
    AND timestamp >= CURRENT_TIMESTAMP - INTERVAL 30 DAY
ORDER BY 
    timestamp;
```

## Advanced Queries with WINDOW FUNCTIONS

### Calculate 7-Day Rolling Average Price

```sql
-- PostgreSQL
SELECT 
    coin_id,
    timestamp,
    price_usd,
    AVG(price_usd) OVER (
        PARTITION BY coin_id 
        ORDER BY timestamp 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as rolling_avg_price
FROM 
    crypto_prices
WHERE 
    coin_id = "bitcoin"
ORDER BY 
    timestamp;

-- MySQL
SELECT 
    coin_id,
    timestamp,
    price_usd,
    AVG(price_usd) OVER (
        PARTITION BY coin_id 
        ORDER BY timestamp 
        ROWS 6 PRECEDING
    ) as rolling_avg_price
FROM 
    crypto_prices
WHERE 
    coin_id = "bitcoin"
ORDER BY 
    timestamp;
```

### Detect Market Trends (Bullish/Bearish)

```sql
-- PostgreSQL
WITH daily_prices AS (
    SELECT 
        coin_id,
        DATE(timestamp) as date,
        AVG(price_usd) as avg_daily_price
    FROM 
        crypto_prices
    WHERE 
        coin_id = "bitcoin"
        AND timestamp >= CURRENT_TIMESTAMP - INTERVAL "30 days"
    GROUP BY 
        coin_id, DATE(timestamp)
),
price_changes AS (
    SELECT 
        coin_id,
        date,
        avg_daily_price,
        LAG(avg_daily_price, 1) OVER (PARTITION BY coin_id ORDER BY date) as prev_day_price,
        avg_daily_price - LAG(avg_daily_price, 1) OVER (PARTITION BY coin_id ORDER BY date) as daily_change,
        AVG(avg_daily_price) OVER (
            PARTITION BY coin_id 
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as rolling_7day_avg
    FROM 
        daily_prices
)
SELECT 
    coin_id,
    date,
    avg_daily_price,
    daily_change,
    CASE 
        WHEN daily_change > 0 THEN "up"
        WHEN daily_change < 0 THEN "down"
        ELSE "unchanged"
    END as daily_direction,
    rolling_7day_avg,
    CASE 
        WHEN avg_daily_price > rolling_7day_avg THEN "above_average"
        ELSE "below_average"
    END as avg_comparison,
    CASE 
        WHEN COUNT(*) FILTER (WHERE daily_change > 0) OVER (
            PARTITION BY coin_id 
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) >= 4 THEN "bullish"
        WHEN COUNT(*) FILTER (WHERE daily_change < 0) OVER (
            PARTITION BY coin_id 
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) >= 4 THEN "bearish"
        ELSE "neutral"
    END as market_trend
FROM 
    price_changes
WHERE 
    prev_day_price IS NOT NULL
ORDER BY 
    date;
```

### Calculate Daily Returns for Portfolio Analysis

```sql
-- PostgreSQL
WITH daily_prices AS (
    SELECT 
        coin_id,
        DATE(timestamp) as date,
        FIRST_VALUE(price_usd) OVER (
            PARTITION BY coin_id, DATE(timestamp) 
            ORDER BY timestamp
        ) as daily_price
    FROM 
        crypto_prices
    WHERE 
        coin_id IN ("bitcoin", "ethereum")
        AND timestamp >= CURRENT_TIMESTAMP - INTERVAL "90 days"
),
unique_daily_prices AS (
    SELECT DISTINCT coin_id, date, daily_price
    FROM daily_prices
),
daily_returns AS (
    SELECT
        coin_id,
        date,
        daily_price,
        LAG(daily_price, 1) OVER (PARTITION BY coin_id ORDER BY date) as prev_day_price,
        (daily_price - LAG(daily_price, 1) OVER (PARTITION BY coin_id ORDER BY date)) / 
            LAG(daily_price, 1) OVER (PARTITION BY coin_id ORDER BY date) * 100 as daily_return_pct
    FROM
        unique_daily_prices
)
SELECT
    coin_id,
    date,
    daily_price,
    prev_day_price,
    daily_return_pct,
    SUM(daily_return_pct) OVER (PARTITION BY coin_id ORDER BY date) as cumulative_return_pct
FROM
    daily_returns
WHERE
    prev_day_price IS NOT NULL
ORDER BY 
    coin_id, date;
```

## Portfolio Analysis Queries

### Calculate Portfolio Value Over Time

```sql
-- Assuming you have a portfolio table with coin_id and quantity columns
-- PostgreSQL
WITH portfolio AS (
    SELECT "bitcoin" as coin_id, 0.5 as quantity
    UNION ALL
    SELECT "ethereum" as coin_id, 5 as quantity
),
daily_prices AS (
    SELECT 
        cp.coin_id,
        DATE(cp.timestamp) as date,
        FIRST_VALUE(cp.price_usd) OVER (
            PARTITION BY cp.coin_id, DATE(cp.timestamp) 
            ORDER BY cp.timestamp
        ) as daily_price
    FROM 
        crypto_prices cp
    WHERE 
        cp.timestamp >= CURRENT_TIMESTAMP - INTERVAL "90 days"
        AND cp.coin_id IN (SELECT coin_id FROM portfolio)
),
unique_daily_prices AS (
    SELECT DISTINCT coin_id, date, daily_price
    FROM daily_prices
),
portfolio_daily_value AS (
    SELECT
        udp.date,
        udp.coin_id,
        p.quantity,
        udp.daily_price,
        p.quantity * udp.daily_price as coin_value
    FROM
        unique_daily_prices udp
    JOIN
        portfolio p ON udp.coin_id = p.coin_id
)
SELECT
    date,
    SUM(coin_value) as total_portfolio_value,
    json_object_agg(coin_id, coin_value) as coin_values
FROM
    portfolio_daily_value
GROUP BY
    date
ORDER BY
    date;
```

### Calculate Correlation Between Coins

```sql
-- PostgreSQL
WITH daily_prices AS (
    SELECT 
        coin_id,
        DATE(timestamp) as date,
        FIRST_VALUE(price_usd) OVER (
            PARTITION BY coin_id, DATE(timestamp) 
            ORDER BY timestamp
        ) as daily_price
    FROM 
        crypto_prices
    WHERE 
        coin_id IN ("bitcoin", "ethereum")
        AND timestamp >= CURRENT_TIMESTAMP - INTERVAL "90 days"
),
unique_daily_prices AS (
    SELECT DISTINCT coin_id, date, daily_price
    FROM daily_prices
),
price_matrix AS (
    SELECT
        date,
        MAX(CASE WHEN coin_id = "bitcoin" THEN daily_price END) as btc_price,
        MAX(CASE WHEN coin_id = "ethereum" THEN daily_price END) as eth_price
    FROM
        unique_daily_prices
    GROUP BY
        date
    HAVING
        MAX(CASE WHEN coin_id = "bitcoin" THEN daily_price END) IS NOT NULL
        AND MAX(CASE WHEN coin_id = "ethereum" THEN daily_price END) IS NOT NULL
)
SELECT
    CORR(btc_price, eth_price) as correlation_coefficient,
    COUNT(*) as data_points
FROM
    price_matrix;
```

### Identify Best and Worst Performing Days

```sql
-- PostgreSQL
WITH daily_prices AS (
    SELECT 
        coin_id,
        DATE(timestamp) as date,
        FIRST_VALUE(price_usd) OVER (
            PARTITION BY coin_id, DATE(timestamp) 
            ORDER BY timestamp
        ) as daily_price
    FROM 
        crypto_prices
    WHERE 
        coin_id = "bitcoin"
        AND timestamp >= CURRENT_TIMESTAMP - INTERVAL "365 days"
),
unique_daily_prices AS (
    SELECT DISTINCT coin_id, date, daily_price
    FROM daily_prices
),
daily_returns AS (
    SELECT
        date,
        daily_price,
        LAG(daily_price, 1) OVER (ORDER BY date) as prev_day_price,
        (daily_price - LAG(daily_price, 1) OVER (ORDER BY date)) / 
            LAG(daily_price, 1) OVER (ORDER BY date) * 100 as daily_return_pct
    FROM
        unique_daily_prices
    WHERE
        coin_id = "bitcoin"
)
(SELECT
    date,
    daily_price,
    daily_return_pct,
    "best" as day_type
FROM
    daily_returns
WHERE
    prev_day_price IS NOT NULL
ORDER BY
    daily_return_pct DESC
LIMIT 10)
UNION ALL
(SELECT
    date,
    daily_price,
    daily_return_pct,
    "worst" as day_type
FROM
    daily_returns
WHERE
    prev_day_price IS NOT NULL
ORDER BY
    daily_return_pct ASC
LIMIT 10)
ORDER BY
    day_type, ABS(daily_return_pct) DESC;
```
