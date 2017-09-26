import random
import datetime
import time
from prime_factorization.factorizer import PrimeFactorizer
from finger_counter.finger_counter import FingerCounter

def weight_score(factors, guesses, time_taken):
    """Weigth score according to how many primes were missed.
    Each number missed and each wrong number is punished once.
    """
    n_to_guess = len(factors)
    n_wrong_guesses = 0
    for guess in guesses:
        try:
            factors.remove(guess)
        except ValueError:
            n_wrong_guesses += 1

    punishments = len(factors) + n_wrong_guesses
    if n_to_guess > punishments:
        punishment_factor = 1 + punishments
        weighted_time_taken = time_taken * punishment_factor
        return weighted_time_taken
    else:
        return None


def main():
    font = cv2.FONT_HERSHEY_SIMPLEX
    fx, fy, fh = 10, 50, 45
    text_color = (0, 255, 0)

    number_to_factorize = random.randint(2, 9)
    factorizer = PrimeFactorizer()
    prime_factors = factorizer.factorize(number_to_factorize)
    print(number_to_factorize, prime_factors)

    finger_counter = FingerCounter()

    # Setting up the camera.
    cam = cv2.VideoCapture(0)
    window = cv2.namedWindow('window', cv2.WINDOW_NORMAL)
    # Setting up the interface.
    cv2.putText(window, (x0,y0), 'factorize: {}'.format(number_to_factorize),
                (fx,fy), font, 1.2, dataColor, 2, 1)
    while True:
        key = cv2.waitKey(0) & 0xff
        if key == ord(' '):
            # Take picture and predict.
            ret, frame = cam.read()
            count = finger_counter.count(frame)
            print('count', count)
        elif key == ord('q'):
            break
        else:
            continue
    # Start measuring time.
    start_time = datetime.datetime.now()

    # Let the user put his hand in the rectangle/ in front of the camera and let him press space whenever
    # he wants to enter a new number. Press enter once done.
    guesses = [2]
    time.sleep(1)

    # End measuring time.
    end_time = datetime.datetime.now()
    total_time = (end_time - start_time).total_seconds()
    # Compare the users guess with the result.
    score = weight_score(prime_factors, guesses, total_time)
    print('score', score)

if __name__ == '__main__':
    main()
