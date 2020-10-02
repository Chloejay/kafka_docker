from main import * 

if __name__ == "__main__":
    BOOTSTRAP_SERVER ="localhost:9092"
    TOPIC= ["topic_test_2"]
    SESS_TIMEOUT= 20000
    GROUP_ID= "msg_more_consumer"
    RETRIES= 5
    REASSIGN = True
    FILE_PATH= "consumer2.csv"
    pprint("Starting Python Consumer.")
    main(TOPIC, BOOTSTRAP_SERVER, SESS_TIMEOUT, GROUP_ID, RETRIES, REASSIGN, FILE_PATH)