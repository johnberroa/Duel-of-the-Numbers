import random
import datetime
import time
from prime_factorization.factorizer import PrimeFactorizer

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
    number_to_factorize = random.randint(2, 9)
    factorizer = PrimeFactorizer()
    prime_factors = factorizer.factorize(number_to_factorize)
    print(number_to_factorize, prime_factors)

    # Setting up the camera.

    # Setting up the interface.

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
