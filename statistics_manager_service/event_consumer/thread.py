import threading

from statistics_manager_service.event_consumer.kafka_consumer import consumer_loop


class EventConsumer:
    def __init__(self):
        self.exitEvent = threading.Event()

        self.threads = {}

        # Create Kafka consumer threads
        thread = threading.Thread(name='consumer', target=consumer_loop, args=(self.exitEvent,))

        self.threads['consumer'] = thread

    # Start threads
    def start(self):
        for thread in self.threads.values():
            thread.start()

    # Stop threads and wait for them to exit
    def stop(self):
        self.exitEvent.set()

        # Join all threads
        for thread in self.threads.values():
            thread.join()