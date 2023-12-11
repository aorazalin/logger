# Logger component

## Usage
Simply run `python3 app.py`

## Tests
Unit tests are under `tests/` folder.

## Design

Main part of the logic is `LogComponent` class which implements an abstract interfance `ILog` for logging. The whole logic of `LogComponent` can be summarized by keeping track of jobs (i.e. logs) to perform in a lock-safe queue and performing them when resources are available, which is done by a separately added worker thread. 
