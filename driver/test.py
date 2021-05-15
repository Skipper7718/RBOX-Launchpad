from pynput.keyboard import Key, Controller, KeyCode
from time import sleep

l = Controller()

sleep(4)
l.tap(Key.f13)

print(len(["123","§"]))

# l.press('A')
# l.release('A')