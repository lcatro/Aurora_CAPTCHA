# coding: utf-8
import thread

import pow


class tick_pool:
    def __init__(self):
        self.tick = {}
        self.internal_lock = thread.allocate_lock()

    def lock(self):
        self.internal_lock.acquire()

    def unlock(self):
        self.internal_lock.release()

    def add_tick(self, tick_data):
        self.lock()

        random_id = pow.make_string(32)
        magic = pow.make_string(32)

        while self.tick.has_key(random_id):
            random_id = pow.make_string(32)

        self.tick[random_id] = {
            'tick_data': tick_data,
            'magic': magic
        }

        self.unlock()

        return random_id, magic

    def is_exist_tick(self, tick_id):
        result = False

        self.lock()

        if self.tick.has_key(tick_id):
            result = True

        self.unlock()

        return result

    def remove_tick(self, tick_id):
        self.lock()

        if self.tick.has_key(tick_id):
            self.tick.pop(tick_id)

        self.unlock()

    def get_tick_magic(self, tick_id):
        result = False

        self.lock()

        if self.tick.has_key(tick_id):
            result = self.tick[tick_id]['magic']

        self.unlock()

        return result

    def get_tick_data(self, tick_id):
        result = False

        self.lock()

        if self.tick.has_key(tick_id):
            result = self.tick[tick_id]['tick_data']

        self.unlock()

        return result


class captcha_valid:
    def __init__(self):
        self.tick_pow_list = tick_pool()
        self.tick_valid_state = tick_pool()

    def get_captcha(self):
        pow_list = pow.random_make_pow()
        tick_id, magic_number = self.tick_pow_list.add_tick(pow_list)

        captcha_data = {
            'pow_list': pow_list,
            'tick': tick_id,
            'magic': magic_number
        }

        return captcha_data

    def valid_captcha(self, tick_id, magic, pow_list):
        if not self.tick_pow_list.is_exist_tick(tick_id):
            return self.tick_valid_state.add_tick(False)

        if not magic == self.tick_pow_list.get_tick_magic(tick_id):
            return self.tick_valid_state.add_tick(False)

        self.tick_pow_list.remove_tick(tick_id)

        valid_result = pow.valid_pow(pow_list)

        if valid_result:
            return self.tick_valid_state.add_tick(True)

        return self.tick_valid_state.add_tick(False)

    def check_tick(self, tick_id):
        if not self.tick_valid_state.is_exist_tick(tick_id):
            return False

        result = self.tick_valid_state.get_tick_data(tick_id)

        self.tick_valid_state.remove_tick(tick_id)

        return result
