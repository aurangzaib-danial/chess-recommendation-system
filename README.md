# Chess Recommendation System [uwyo-cosc-4550-project]

## Requirements
- Python version 3.7 or above

## Required python package
```
$ pip3 install chess
```

## Setting up Stockfish Command Line Program
This is required for this application to work.

### Ubuntu
```
$ sudo apt install stockfish
```

### MacOS
```
$ brew install stockfish
```

### Windows
Download POPCNT version for windows from the following link

https://stockfishchess.org/download/

On line 6 in `app.py` update following before running the program

```python
engine = chess.engine.SimpleEngine.popen_uci("stockfish")
```
to

```python
engine = chess.engine.SimpleEngine.popen_uci(r"{add-path-of-downloaded-stockfish-folder}\{add-file-name-of-executable}.exe")
```

## Run the Program
```
$ python3 app.py
```


## License
Chess Recommendation System is released under the [MIT License](https://opensource.org/licenses/MIT).
