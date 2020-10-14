from main import * 

if __name__ == "__main__":
    BOOTSTRAP_SERVER ="localhost:29092"
    GROUP_ID= "more_consumers"
    SESS_TIMEOUT= 20000
    TOPIC= ["topic_test"]
    RETRIES= 5
    REASSIGN = True
    FILE_PATH= "src/create_consumer/consumer/consumer1.csv"
    pprint("Starting Python Consumer.")
    main(TOPIC, BOOTSTRAP_SERVER, SESS_TIMEOUT, GROUP_ID, RETRIES, REASSIGN, FILE_PATH)