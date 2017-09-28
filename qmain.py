import random
import cv2
import datetime
import numpy as np
from prime_factorization.factorizer import PrimeFactorizer
from finger_counter.finger_counter import FingerCounter
from collections import Counter

def q_add_one_mod_5(n):
    qasm = """
OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[3];

// Inputs.
{}x q[0];
{}x q[1];
{}x q[2];

cx q[2],q[3];
cx q[1],q[4];
x q[2];
ccx q[1],q[2],q[4];
cx q[3],q[1];
cx q[4],q[0];
reset q[3];
reset q[4];
ccx q[0],q[1],q[3];
cx q[3],q[1];
cx q[3],q[0];
ccx q[2],q[3],q[1];
cx q[3],q[2];
reset q[3];
x q[0];
x q[1];
x q[2];
ccx q[0],q[1],q[3];
ccx q[2],q[3],q[4];
x q[0];
x q[1];
x q[2];
reset q[3];
cx q[4],q[2];
cx q[4],q[1];
measure q[0] -> c[2];
measure q[1] -> c[1];
measure q[2] -> c[0];
"""
    binary = bin(n)[2:].zfill(3)
    comments = ['' if int(bi) else '//' for bi in binary ]
    qasm = qasm.format(*comments)
    qp = QuantumProgram()
    qp.load_qasm_text(qasm, name='circuit')
    qobj = qp.compile(['circuit'])
    result = qp.run(qobj, wait=2, timeout=240)
    counted_result = Counter(result.get_counts('circuit'))
    # Turn binary back to decimal.
    output = int(counted_result.most_common()[0][0], 2)

    return output

def q_add_mod_5(a, b):
    acc = a
    for _ in range(b):
        acc = q_add_one(acc)
    return acc

def generate_numbers_to_guess():
    number_a = random.randint(0, 7)
    number_b = random.randint(1, 8 - number_a)
    return number_a, number_b

def calc_solution(number_a, number_b):
    """Emulator for the quantum calculation."""
    solution = (number_a + number_b) % 5
    if solution == 0:
        solution = 5
    return solution

def main():
    font = cv2.FONT_HERSHEY_SIMPLEX
    fx, fy, fh = 10, 50, 45
    x0 = y0 = 100
    text_color = (0, 255, 0)


    while True:
        number_a, number_b = generate_numbers_to_guess()
        solution = q_add_mod_5(number_a, number_b)
        text = 'Solve {} + {} mod 5'.format(number_a, number_b)
        print(text)

        finger_counter = FingerCounter()

        # Setting up the camera.
        cam = cv2.VideoCapture(0)
        # Setting up the interface.
        window = cv2.namedWindow('window', cv2.WINDOW_NORMAL)
        cv2.imshow("window", frame)
        cv2.putText(window, text, (fx,fy), font, 1.2, text_color, 2, 1)
        cv2.waitKey(2)

        try:
            # Start measuring time.
            start_time = datetime.datetime.now()
            while True:
                ret, frame = cam.read()
                frame = cv2.flip(frame, 1)
                key = cv2.waitKey(1) & 0xff
                # Let the user put his hand in the rectangle/ in front of the camera and let him press space whenever
                # he wants to enter a new number. Press q once done.
                if key == ord(' '):
                    # Take picture and predict.
                    count = finger_counter.count(frame)
                    print('count', count)
                    if count is not None:
                        guess = count
                if key == ord('q'):
                    break
                else:
                    cv2.rectangle(frame, (x0, y0), (x0 + 300 - 1, y0 + 300 - 1), [0, 0, 255], 12)
                    cv2.imshow("window", frame)
                    continue
        except Exception as e:
            cam.release()
            cv2.destroyAllWindows()
            raise e

        # End measuring time.
        end_time = datetime.datetime.now()
        total_time = (end_time - start_time).total_seconds()
        print(total_time)
        # Compare the users guess with the result.
        if guess == solution:
            score = total_time
        else:
            score = "I don’t like tests. That's why I didn't go to college. Don't test me, because I will fail a majority of the time."

        print('score', score)
        cam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
