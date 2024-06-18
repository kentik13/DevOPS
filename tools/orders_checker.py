import mysql.connector
from telegram import Bot
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)

# List of database connection configurations
db_configs = [
    {
        'user': 'user',
        'password': 'password',
        'host': 'host',
        'database': 'database'
    },
    {
        'user': 'user',
        'password': 'password',
        'host': 'host',
        'database': 'database'
    },
    # Add more database configurations as needed
]

# Telegram bot configuration
telegram_token = 'YOUR_TOKEN'
chat_id = 'YOUR_CHAT_ID'

# SQL queries
query_hourly_count = """
SELECT COALESCE(b.hourly_count, 0) as hourly_count
FROM (
        WITH RECURSIVE DateTimeSeries AS (
            SELECT (NOW() - INTERVAL 1 HOUR - INTERVAL MINUTE(NOW()) MINUTE - INTERVAL SECOND(NOW()) SECOND) as `datetime`
        )
        SELECT `datetime` FROM DateTimeSeries
    ) a 
LEFT JOIN
    (
        SELECT
            count(*) as hourly_count,
            STR_TO_DATE(FROM_UNIXTIME(o.cdate), '%Y-%m-%d %H') AS `t`
        FROM
            jos_vm_orders o
        LEFT JOIN jos_vm_api2_orders a ON o.order_id = a.order_id  
        WHERE
            FROM_UNIXTIME(o.cdate) >= CURDATE() - INTERVAL 1 DAY
            and a.order_id IS NULL
        GROUP BY
            DATE_FORMAT(FROM_UNIXTIME(o.cdate), '%Y-%m-%d %H')
        order by
            o.order_id desc
    ) b
ON b.t = a.datetime;
"""

query_four_weeks_average = """
SELECT 
 COALESCE(b.four_weeks_hourly_average, 0) as four_weeks_hourly_average
FROM (
        WITH RECURSIVE DateTimeSeries AS (
            SELECT (NOW() - INTERVAL 1 HOUR - INTERVAL MINUTE(NOW()) MINUTE - INTERVAL SECOND(NOW()) SECOND) as `datetime`
        )
        SELECT `datetime` FROM DateTimeSeries
    ) a 
LEFT JOIN
    (
        SELECT
          DATE_ADD(t, INTERVAL 7 DAY) as hourly_datetime,
          AVG(orders_count) AS four_weeks_hourly_average
        FROM
          (
            SELECT
              COUNT(*) AS orders_count,
              STR_TO_DATE(FROM_UNIXTIME(o.cdate), '%Y-%m-%d %H') AS `t`
            FROM
              jos_vm_orders o
              LEFT JOIN jos_vm_api2_orders a ON o.order_id = a.order_id
            WHERE
              FROM_UNIXTIME(o.cdate) BETWEEN DATE_FORMAT(
                DATE_ADD(DATE_SUB(NOW(), INTERVAL 8 DAY), INTERVAL 1 HOUR),
                '%Y-%m-%d %H:00:01'
              )
              AND DATE_FORMAT(
                DATE_ADD(DATE_SUB(NOW(), INTERVAL 7 DAY), INTERVAL 2 HOUR),
                '%Y-%m-%d %H:59:59'
              )
                and a.order_id IS NULL
            GROUP BY
              HOUR(FROM_UNIXTIME(o.cdate))
            UNION
            SELECT
              COUNT(*) AS orders_count,
              STR_TO_DATE(FROM_UNIXTIME(o.cdate), '%Y-%m-%d %H') AS `t`
            FROM
              jos_vm_orders o
              LEFT JOIN jos_vm_api2_orders a ON o.order_id = a.order_id
            WHERE
              FROM_UNIXTIME(o.cdate) BETWEEN DATE_FORMAT(
                DATE_ADD(
                  DATE_SUB(NOW(), INTERVAL 15 DAY),
                  INTERVAL 1 HOUR
                ),
                '%Y-%m-%d %H:00:01'
              )
              AND DATE_FORMAT(
                DATE_ADD(
                  DATE_SUB(NOW(), INTERVAL 14 DAY),
                  INTERVAL 2 HOUR
                ),
                '%Y-%m-%d %H:59:59'
              )
                and a.order_id IS NULL
            GROUP BY
              HOUR(FROM_UNIXTIME(cdate))
            UNION
            SELECT
              COUNT(*) AS orders_count,
              STR_TO_DATE(FROM_UNIXTIME(o.cdate), '%Y-%m-%d %H') AS `t`
            FROM
              jos_vm_orders o
              LEFT JOIN jos_vm_api2_orders a ON o.order_id = a.order_id
            WHERE
              FROM_UNIXTIME(o.cdate) BETWEEN DATE_FORMAT(
                DATE_ADD(
                  DATE_SUB(NOW(), INTERVAL 22 DAY),
                  INTERVAL 1 HOUR
                ),
                '%Y-%m-%d %H:00:01'
              )
              AND DATE_FORMAT(
                DATE_ADD(
                  DATE_SUB(NOW(), INTERVAL 21 DAY),
                  INTERVAL 2 HOUR
                ),
                '%Y-%m-%d %H:59:59'
              )
                and a.order_id IS NULL
            GROUP BY
              HOUR(FROM_UNIXTIME(o.cdate))
            UNION
            SELECT
              COUNT(*) AS orders_count,
              STR_TO_DATE(FROM_UNIXTIME(cdate), '%Y-%m-%d %H') AS `t`
            FROM
              jos_vm_orders o
              LEFT JOIN jos_vm_api2_orders a ON o.order_id = a.order_id
            WHERE
              FROM_UNIXTIME(o.cdate) BETWEEN DATE_FORMAT(
                DATE_ADD(
                  DATE_SUB(NOW(), INTERVAL 29 DAY),
                  INTERVAL 1 HOUR
                ),
                '%Y-%m-%d %H:00:01'
              )
              AND DATE_FORMAT(
                DATE_ADD(
                  DATE_SUB(NOW(), INTERVAL 28 DAY),
                  INTERVAL 2 HOUR
                ),
                '%Y-%m-%d %H:59:59'
              )
                and a.order_id IS NULL
            GROUP BY
              HOUR(FROM_UNIXTIME(o.cdate))
          ) AS subquery
        GROUP BY
          HOUR(t)
    ) b
ON b.hourly_datetime = a.datetime;
"""

# Asynchronous function to send a message to the Telegram bot
async def send_telegram_message(token, chat_id, message):
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message)

# Asynchronous function to process each database configuration
async def process_database(db_config):
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Execute the hourly count query
        cursor.execute(query_hourly_count)
        hourly_count_result = cursor.fetchone()
        hourly_count = hourly_count_result['hourly_count']

        # Execute the four-weeks average query
        cursor.execute(query_four_weeks_average)
        four_weeks_average_result = cursor.fetchone()
        four_weeks_hourly_average = four_weeks_average_result['four_weeks_hourly_average']

        # Compare results and send a warning if necessary
        if hourly_count < four_weeks_hourly_average:
            message = (
                f"⚠️ Warning for {db_config['database']} at {db_config['host']}: "
                f"Hourly order count ({hourly_count}) is less than the "
                f"four-weeks hourly average ({four_weeks_hourly_average}).⚠️"
            )
            await send_telegram_message(telegram_token, chat_id, message)
            logging.info(f"Warning sent to Telegram bot for {db_config['database']} at {db_config['host']}.")
        else:
            logging.info(f"Hourly count for {db_config['database']} at {db_config['host']} is within the acceptable range.")

    except mysql.connector.Error as err:
        logging.error(f"Error with {db_config['database']} at {db_config['host']}: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logging.info(f"Database connection closed for {db_config['database']} at {db_config['host']}.")

# Asynchronous main function to execute the script
async def main():
    tasks = [process_database(db_config) for db_config in db_configs]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
