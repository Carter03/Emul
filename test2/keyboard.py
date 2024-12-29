import evdev
import time

class Kbrd:
    def __init__(self):
        self.target_length = 6
        self.pressed_keys = []
        self.have_kb = False
        self.dev = None
        self.wait_for_keyboard()

    def wait_for_keyboard(self, event_id=0):
        while not self.have_kb:
            try:
                self.dev = evdev.InputDevice('/dev/input/event{}'.format(
                    event_id))
                self.have_kb = True
            except OSError:
                print('Keyboard not found, waiting 3 seconds and retrying')
                time.sleep(3)
        print('found a keyboard')

    def event_loop(self, call_func):
        print('Listening...')
        for event in self.dev.read_loop():
            # only bother if we hit a key and its an up or down event
            if event.type == evdev.ecodes.EV_KEY and event.value < 2:
                key_str = evdev.ecodes.KEY[event.code]
                call_func(key_str.split('_')[-1])


class YouTubeConverter:
    def __init__(self, params):
        self.kspace, self.ospace = params
        self.curr_key = 'A'
        self._keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                      'H', 'I', 'J', 'K', 'L', 'M', 'N',
                      'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                      'V', 'W', 'X', 'Y', 'Z', '-', '.']

    def get_abs_pos(self, key):
        if key in ('BACKSPACE', 'ENTER', 'SPACE'):
            if key == 'BACKSPACE': return (self.get_abs_pos('G')[0] + self.ospace, self.get_abs_pos('G')[1])
            if key == 'ENTER': return (self.get_abs_pos('Z')[0], self.get_abs_pos('Z')[1] + self.ospace)
            if key == 'SPACE': return (self.get_abs_pos('W')[0], self.get_abs_pos('W')[1] + self.ospace)

        idx = self._keys.index(key)
        x, y = idx%7, idx//7
        return x*self.kspace, y*self.kspace

    def key_move(self, new_key):
        if new_key not in self._keys + ['BACKSPACE', 'ENTER', 'SPACE']:
            return None
        
        x_rel = self.get_abs_pos(new_key)[0] - self.get_abs_pos(self.curr_key)[0]
        y_rel = self.get_abs_pos(new_key)[1] - self.get_abs_pos(self.curr_key)[1]
        self.curr_key = new_key

        return x_rel, y_rel
        
        


if __name__ == '__main__':
    # print('Setting up keyboard')
    # kb = Kbrd()

    # print('starting event loop')
    # kb.event_loop()
    # y = YouTubeConverter((10, 15))
    # while True:
    #     c = input('>>  ')
    #     print(y.key_move(c))
    pass