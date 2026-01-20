import time
import traceback

from kafka import KafkaConsumer
from kafka.errors import KafkaError

from statistics_manager_service import generalLogger, Config, db

from statistics_manager_service.event_consumer.event_processor import process_events
from statistics_manager_service.controllers.utils import seconds_to_days_minutes_hours


# Function that the thread is going to execute
def consumer_loop(exitEvent):
    generalLogger.info("Configuring Kafka consumer...")

    # Loop to keep trying to connect to broker if it is not up or an exception occurs.
    while (exitEvent.is_set() == False):
        try:
            consumer = KafkaConsumer(
                Config.KAFKA_TOPIC,
                group_id=Config.KAFKA_GROUP_ID,
                bootstrap_servers=Config.KAFKA_BROKER_ENDPOINT,
                consumer_timeout_ms=Config.KAFKA_CONSUMER_TIMEOUT_MS,
                enable_auto_commit=False,
                auto_offset_reset='earliest',
                reconnect_backoff_ms=1000,
                reconnect_backoff_max_ms=5000,
                session_timeout_ms=20000,
                max_poll_records=50
            )
            # break

        except KafkaError as e:
            generalLogger.error(e)
            generalLogger.info(
                f'Reconnecting in {Config.KAFKA_RECONNECT_SLEEP_SECONDS} seconds...'
            )

            time.sleep(Config.KAFKA_RECONNECT_SLEEP_SECONDS)
            continue

        # if exitEvent.is_set():
        #     generalLogger.info('Consumer received event. Exiting...')
        #     return

        start = time.time()
        total_time = 0
        # Consume events until the program receives an exit signal
        while not exitEvent.wait(timeout=Config.KAFKA_WAIT_FOR_EVENT_SECONDS):

            current_time = time.time()
            if current_time - start >= 300:  # Log every x seconds
                total_time += 300
                generalLogger.info(
                    f"Kafka Event Consumer thread is healthy for {total_time} seconds....")
                start = current_time

            try:
                session = db.create_scoped_session()
                msg = next(consumer)
                process_events(session, msg)
                consumer.commit()

            except StopIteration:
                pass

            except (OperationalError, DatabaseError) as e:
                generalLogger.error(repr(e))
                traceback.print_exc()
                session.rollback()
                consumer.commit()
                continue

            except Exception as e:
                generalLogger.error(
                    "Exception occured while listening for events")
                generalLogger.error(e)
                traceback.print_exc()
                break

            session.close()
            # Missing sending error event to other topic

    # Close connection to the broker
    consumer.close(autocommit=False)
    generalLogger.info('Consumer received event. Exiting...')
