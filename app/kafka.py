import os
from googleapiclient.discovery import build
from confluent_kafka import Producer, Consumer, KafkaError
import json
import socket
import threading

# YouTube API setup
api_service_name = "youtube"
api_version = "v3"
# Use an environment variable for the API key
#api_key = os.getenv('YOUTUBE_API_KEY', '')  # Replace with your own key
# video_id = "q-_ezD9Swz4"

comments = []

def video_comments(video_id,api_key):
    """ Fetch YouTube comments for the given video ID. """
    youtube = build(api_service_name, api_version, developerKey=api_key)
    video_response = youtube.commentThreads().list(part='snippet,replies', videoId=video_id).execute()

    while video_response:
        for item in video_response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append({
                'comment': comment,
                'video_id': video_id,
                'timestamp': item['snippet']['topLevelComment']['snippet']['publishedAt']
            })
            replycount = item['snippet']['totalReplyCount']
            if replycount > 0:
                for reply in item['replies']['comments']:
                    reply_text = reply['snippet']['textDisplay']
                    comments.append({
                        'comment': reply_text,
                        'video_id': video_id,
                        'timestamp': reply['snippet']['publishedAt']
                    })

        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=video_response['nextPageToken']
            ).execute()
        else:
            break
    return comments

def kafka_produce(comments):
    """ Produce comments to the Kafka topic. """
    conf = {
        'bootstrap.servers': 'host.docker.internal:9092',  # Make sure Kafka is accessible here
        'client.id': socket.gethostname(),
        'security.protocol': 'PLAINTEXT'
    }

    producer = Producer(conf)

    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    for comment in comments:
        try:
            # Send each comment as a JSON string to Kafka
            producer.produce('youtube-comments', json.dumps(comment).encode('utf-8'), callback=delivery_report)
            producer.poll(0)  # Trigger delivery callbacks
        except BufferError:
            print('Local producer queue is full (%d messages awaiting delivery): try again\n' % len(producer))
        except Exception as e:
            print(f"Unexpected error: {e}")

    print('Flushing records...')
    producer.flush()  # Ensure all records are sent

def kafka_consume():
    """ Consume messages from the Kafka topic. """
    conf = {
        'bootstrap.servers': 'host.docker.internal:9092',
        'group.id': 'YTCommentsGroup',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe(['youtube-comments'])  # Subscribe to topic

    try:
        while True:
            msg = consumer.poll(1.0)  # Poll for new messages
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            print('Received message: {}'.format(msg.value().decode('utf-8')))  # Print the consumed message
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    video_comments(video_id)  # Fetch YouTube comments

    # Start the Kafka consumer in a separate thread
    consumer_thread = threading.Thread(target=kafka_consume)
    consumer_thread.start()

    # Produce fetched comments to Kafka
    kafka_produce(comments)

    # Wait for the consumer thread to finish (it will run indefinitely until interrupted)
    consumer_thread.join()
