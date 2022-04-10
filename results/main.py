import pika, sys, os
import json

def main():

    #create a global window of 100 values
    global window
    window = [-99999999999999999999] * 100
    
    #Defining the callback function
    def on_message_received(ch, method, properties, body):

        #parse the json message
        random_number = json.loads(body)['rand']
        sequence_number = json.loads(body)['sequence_number']

        return processing_fucntion(random_number, sequence_number)

    #Function to process the incoming message
    def processing_fucntion(random_number, sequence_number):

        #index i, which is the last two digits of the sequence number
        i = sequence_number % 100

        #assign the current random_number to its position
        window[i] = random_number

        #find maximum value in the list
        running_max = max(window)

        #convert the message to json format and publish
        message = json.dumps({'rand': random_number,'sequence_number': sequence_number, 'running_max': running_max})
        channel.basic_publish(exchange='', routing_key='solution', body = message)

        #stop on last message
        if sequence_number == 9999:
            channel.stop_consuming()
            connection.close()
            print("\n Connection Closed")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        return
            

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Set up a consumer and start to wait for messages
    channel.basic_consume(queue='rand', auto_ack=True, on_message_callback=on_message_received)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()
    print("This string is after we start consuming")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
