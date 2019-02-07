# Duel of the Numbers
A mixing of neuromorphic and quantum computing for the Comparative Machine Learning class

## The Game
Two random numbers are generated and the player must make with their fingers the sum mod 5 of said generated numbers.  Neuromorphic hardware detects the number of digits via a convolutional neural network.  This is checked via generating the answer via quantum computing.  After one player plays a round, the next player is up, and the game continues.

### Manual
Indicate the solution with your fingers. To do so, put your hand completely into the red square. Press space and the recognized number will appear below the task. Simply retry if it is not correct. To evaluate your solution press 'q'. You get more points the faster you come up with the solution.

## How it Works
Fingers are detected using a slightly modified version of Jared Vasquez's *How Many Fingers* [code](https://github.com/jgv7/CNN-HowManyFingers).

Quantum computing is simulated through IBM's QASM.

Neuromorphic computing is simulated through a CNN.
Get the model [here](https://drive.google.com/file/d/0B5sZ8q5iqYbtRVpqMU4yRlRDdEU/view)
