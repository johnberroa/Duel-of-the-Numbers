import random
import cv2
import datetime
import numpy as np
from prime_factorization.factorizer import PrimeFactorizer
from finger_counter.finger_counter import FingerCounter

def score_it(answers, player_answers, player_time):
    def wrong(ans, play):
        error = 0
        for a in play:
            if a not in ans:
                error += 1
        return error

    score = player_time * (
    1 + ((np.abs(len(answers) - len(player_answers)) + (wrong(answers, player_answers))) / len(answers)) * 2)

    return score


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
    x0 = y0 = 100
    text_color = (0, 255, 0)


    while True:
        number_to_factorize = random.randint(2, 9)
        factorizer = PrimeFactorizer()
        prime_factors = factorizer.factorize(number_to_factorize)
        print(number_to_factorize, prime_factors)

        finger_counter = FingerCounter()
        guess = []

        # Setting up the camera.
        cam = cv2.VideoCapture(0)

        window = cv2.namedWindow('window', cv2.WINDOW_NORMAL)
        # window2 = cv2.namedWindow('WINDOW2', cv2.WINDOW_NORMAL)
        # Setting up the interface.
        cv2.putText(window, 'factorize: {}'.format(number_to_factorize),
                    (fx,fy), font, 1.2, text_color, 2, 1)
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
                        guess.append(count)
                if key == ord('q'):
                    break
                else:
                    cv2.rectangle(frame, (x0, y0), (x0 + 300 - 1, y0 + 300 - 1), [0, 0, 255], 12)
                    cv2.imshow("WINDOW", frame)
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
        score = score_it(prime_factors, guess, total_time)
        # score = weight_score(prime_factors, guess, total_time)
        print('score', score)
        cam.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
