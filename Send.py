import datetime
import shlex
import subprocess
import time


class ChuckConnector(object):
    def __init__(self, interval):
        chuck_command = shlex.split('chuck --loop')
        self.chuck_process = subprocess.Popen(
            chuck_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.interval = interval
        time.sleep(1)

    def _clear_chuck(self):
        cmd = 'chuck - 1'
        subprocess.call(shlex.split(cmd))

    def send_bits(self, bits, interval):
        for b in bits:
            self.set_freq(-1)
            time.sleep(self.interval)
            self.set_freq(b)
            time.sleep(self.interval)

    def send_bit(self, bit):
        self.set_freq(-1)
        time.sleep(self.interval)
        self.set_freq(bit)
        time.sleep(self.interval)

    def set_freq(self, freq):
        self._clear_chuck()
        cmd = 'chuck + chuck_files/{fn}'

        if freq == 0:
            cmd = cmd.format(fn='sin_low.ck')
        elif freq == 1:
            cmd = cmd.format(fn='sin_high.ck')
        else:
            cmd = cmd.format(fn='sin_start.ck')
        subprocess.Popen(shlex.split(cmd))

    def send_string(self, s):
        s_bytes = list(ord(b) for b in s)
        for byte in s_bytes:
            for i in xrange(8):
                b = (byte >> i) & 1
                self.send_bit(b)

    def stop(self):
        self._clear_chuck()
        self.chuck_process.kill()


def main():
    cc = ChuckConnector(0.015)
    u_in = None

    while not u_in == 'quit':
        u_in = raw_input('Message: ')
        print 'sending...'
        start = datetime.datetime.now()
        cc.send_string(u_in)
        delta = datetime.datetime.now() - start
        print 'complete. time: {s}'.format(s=str(delta))

    cc.stop()


if __name__ == '__main__':
    main()
