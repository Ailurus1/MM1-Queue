# $M/M/1/\infty$
Single-threaded implementation of the main mechanisms of the $M/M/1/\infty$ [queue](https://en.wikipedia.org/wiki/M/M/1_queue) from queueing theory with some small provided experiments showing basic metrics obtained during work of the system with various parameters.

---
```bash
pip install -r requirements.txt
```
or using `poetry`
```bash
poetry init
```
and then in Python code
```Python
from queue_simulation.markovian import Markovian

...

queue = Markovian(<your lmbda value>, <you mu value>)
metrics = queue.run(10000)
```
