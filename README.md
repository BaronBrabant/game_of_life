# game_of_life
Small game of life written in python, possible predecessor of physical version

## How to use

1. Clone the repository
2. Download the required libraries with:
    ```
    pip install -r requirements.txt
    ```
3. Run the game with:
    ```
    python game_of_life.py
    ```
4. Enjoy!

You can click on the squares to activate or deactivate them (even when the game is running!).
Enjoy watchingyour creations unfold.

5. (Optional) Import setup

You can now download RLE files to quickly import a start position for a game of life.
To do this simply:

1. Download an RLE file from the internet and put in the folder:
```
./rle/

example file: ./rle/sawmill
```

2. Run the game with the rle option and the path to file:
```
python game_of_life.py -rle rle/sawmill
```

3. Enjoy and send me an email if you have issue!
