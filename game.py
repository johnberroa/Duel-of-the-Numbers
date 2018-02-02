from qiskit import QuantumProgram
import random
import cv2
import datetime
import numpy as np
from finger_counter.finger_counter import FingerCounter
from collections import Counter


class Game:

    def __init__(self, n_players=2):
        self._cam = cv2.VideoCapture(0)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fx = 10
        self.fy = 50
        self.fh = 45
        self.x0 = 100
        self.y0 = 100
        self.text_color = (0, 0, 255)
        self.finger_counter = FingerCounter()
        self.n_players = n_players

    def play(self) -> bool:
        player_results = []
        for player_idx in range(1, self.n_players + 1):
            self.announce_next_round(player_idx)
            player_results.append(self.round())
            self.announce_score(player_results[-1]['score'])
        self.announce_winner(player_results)
        return self.wanna_play_again()

    def round(self):
        number_a, number_b = generate_numbers_to_guess()
        solution = self.get_solution(number_a, number_b)

        text = 'Solve {} + {} mod 5'.format(number_a, number_b)
        guess = None
        start_time = datetime.datetime.now()
        try:
            while True:
                ret, frame = self._cam.read()
                frame = cv2.flip(frame, 1)
                key = get_key(delay=1)
                # Let the user put his hand in the rectangle/ in front of the camera and let him press space whenever
                # he wants to enter a new number. Press q once done.
                if key == ord(' '):
                    # Take picture and predict.
                    guess = self.finger_counter.count(frame)
                elif key == ord('q'):
                    if guess is not None:
                        return self.get_score(start_time, guess, solution)
                    continue
                else:
                    cv2.putText(frame, str(guess), (self.fx, self.fy + 40), self.font, 1.2, self.text_color, 2, 1)
                    cv2.rectangle(frame, (self.x0, self.y0), (self.x0 + 300 - 1, self.y0 + 300 - 1), [0, 0, 255], 12)
                    cv2.putText(frame, text, (self.fx, self.fy), self.font, 1.2, self.text_color, 2, 1)

                    cv2.imshow("window", frame)
                    continue

        except Exception as e:
            self.cleanup()
            raise e

    def get_solution(self):
        raise NotImplementedError

    def announce_next_round(self, player):
        _, frame = self._cam.read()
        xx, yy, _ = frame.shape
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, f"Player {player}'s Turn!!", (xx // 2, yy // 2), self.font, 1.2, self.text_color, 2, 1)
        cv2.putText(frame, "Please wait...", (xx // 2, yy // 2 + 45), self.font, 1.2, self.text_color, 2, 1)
        cv2.imshow("window", frame)
        cv2.waitKey(3_000)

    def announce_score(self, score):
        _, frame = self._cam.read()
        xx, yy, _ = frame.shape
        cv2.putText(frame, score, (xx // 2, yy // 2), self.font, 1.2, self.text_color, 2, 1)
        cv2.putText(frame, "Press any button to continue", (10, yy // 2 + 45), self.font, 1.2, self.text_color, 2, 1)
        cv2.imshow("window", frame)
        cv2.waitKey(0)

    def announce_winner(self, player_results):
        _, frame = self._cam.read()
        xx, yy, _ = frame.shape
        players_who_got_it_right = np.flatnonzero(
            np.array([player_result['score_f'] for player_result in player_results])) + 1
        if players_who_got_it_right.size == 0:
            text = 'You are all losers'
        elif players_who_got_it_right.size == 1:
            text = f'WINNER: PLAYER {players_who_got_it_right[0]}!!!'
        else:
            text = "IT'S A TIE!!! WHAT A GAME!!!"

        cv2.putText(frame, text, (10, yy // 2), self.font, 1.2, self.text_color, 2, 1)
        cv2.imshow("window", frame)
        cv2.waitKey(5_000)

    def wanna_play_again(self) -> bool:
        _, frame = self._cam.read()
        xx, yy, _ = frame.shape
        cv2.putText(frame, "Press p to play again", (10, yy // 2), self.font, 1.2, self.text_color,
                    2, 1)
        cv2.putText(frame, "or q to quit.", (10, yy // 2 + 45), self.font, 1.2, self.text_color,
                    2, 1)
        cv2.imshow("window", frame)
        key = get_key(delay=0)
        return key == ord('p')

    def get_score(self, start_time, guess, solution):
        # End measuring time.
        end_time = datetime.datetime.now()
        total_time = (end_time - start_time).total_seconds()
        # Compare the users guess with the result.
        if guess == solution:
            score_f = 1
            score = 'Score: {:.2f}'.format(total_time)
        else:
            score_f = 0
            score = "I don't like tests."

        return {'score_f': score_f,
                'score': score}

    def cleanup(self):
        self._cam.release()
        cv2.destroyAllWindows()


class Mod5Game(Game):
    def get_solution(self, number_a, number_b):
        """Emulator for the quantum calculation."""
        solution = (number_a + number_b) % 5
        if solution == 0:
            solution = 5
        return solution


class QuantumMod5Game(Game):
    def get_solution(self, number_a, number_b):
        acc = number_a
        for _ in range(number_b):
            acc = self.q_add_one_mod_5(acc)
        return acc

    def q_add_one_mod_5(self, n):
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
        comments = ['' if int(bi) else '//' for bi in binary]
        qasm = qasm.format(*comments)
        qp = QuantumProgram()
        qp.load_qasm_text(qasm, name='circuit')
        qobj = qp.compile(['circuit'])
        result = qp.run(qobj, wait=2, timeout=240)
        counted_result = Counter(result.get_counts('circuit'))
        # Turn binary back to decimal.
        output = int(counted_result.most_common()[0][0], 2)

        return output


def generate_numbers_to_guess():
    number_a = random.randint(0, 7)
    number_b = random.randint(1, 8 - number_a)
    return number_a, number_b


def get_key(delay=0):
    return cv2.waitKey(delay) & 0xff
