# My Bomberman Game

## How to run this project
First, you should clone this repository into your machine, using the command:
```script
git clone https://github.com/Andre-Polimanti/my-bomberman.git
cd my-bomberman
```
Then, to create a local virtual environment and activate it, run, depending on your current OS:
On Windows:
```script
python -m venv venv
venv\Scripts\activate
```
On Ubuntu/Debian and Fedora:
```script
python3 -m venv venv
source venv/bin/activate
```
Having done this, you should install the dependencies listed on the requirements.txt file contained in this project, do so by running:
On Windows:
```script
pip install -r requirements.txt
```
On Ubuntu/Debian:
```script
sudo apt update
sudo apt install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev
pip install -r requirements.txt
```
On Fedora:
```script
sudo dnf install gcc python3-devel SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel freetype-devel
pip install -r requirements.txt
```
Finally, to execute this project, run:
```script
python src/main.py
```

## Game Controls
### Keyboard
+ Player 1
    - For movement, use the arrow keys.
    - For bombing, use the Enter key of the numeric keyboard.
+ Player 2
    - For movement, use the WASD keys.
    - For bombing, use space key.
## Shortcuts
+ Window
  + ESC: Close window/application
  + M: Minimize window
+ Game
  + R: Restart Game