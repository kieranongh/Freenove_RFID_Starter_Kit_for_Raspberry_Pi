from datetime import datetime
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

RECEIVED_SIGNAL = [[], []]  #[[time of reading], [signal reading]]
MAX_DURATION = 3
RECEIVE_PIN = 17

def sniff():
    RECEIVED_SIGNAL = [[], []]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    cumulative_time = 0
    beginning_time = datetime.now()
    print('**Started recording**')
    while cumulative_time < MAX_DURATION:
        time_delta = datetime.now() - beginning_time
        RECEIVED_SIGNAL[0].append(time_delta)
        RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))
        cumulative_time = time_delta.seconds
    print('**Ended recording**')
    print(f"{len(RECEIVED_SIGNAL[0])} samples recorded")
    GPIO.cleanup()

    print('**Processing results**')
    my_range = range(len(RECEIVED_SIGNAL[0]))
    print(f'my_range => {my_range}')
    for i in my_range:
        try:
            RECEIVED_SIGNAL[0][i] = RECEIVED_SIGNAL[0][i].seconds + RECEIVED_SIGNAL[0][i].microseconds/1000000.0
        except Exception as e:
            print(f'e => {e}')

    print('**Plotting results**')
    plt.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
    plt.axis([0, MAX_DURATION, -1, 2])
    plt.savefig("foo.png")
    return RECEIVED_SIGNAL

def plot(x, y, name):
    plt.plot(x, y)
    plt.axis([x[0], x[-1], -1, 2])
    plt.savefig(name or "foo.png")

if __name__ == '__main__':
    sniff()