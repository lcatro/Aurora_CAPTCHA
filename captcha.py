
import base64
import json
import thread
import time

import tornado.web
import tornado.ioloop

import pow


class tick_result :
    
    tick_state_success = 0
    tick_state_error = 1
    tick_state_expire = 2
    

class tick_pool :
    
    __tick_expire_time = 360  #  360 s = 6 min
    
    @staticmethod
    def get_current_time() :
        return time.time()
    
    def __init__(self) :
        self.tick = {}
        self.internal_lock = thread.allocate_lock()
        
    def lock(self) :
        self.internal_lock.acquire()
        
    def unlock(self) :
        self.internal_lock.release()
        
    def add_tick(self,tick_data) :
        self.lock()
        
        random_id = pow.make_string(32)
        magic = pow.make_string(32)
        
        while self.tick.has_key(random_id) :
            random_id = pow.make_string(32)
        
        self.tick[random_id] = {
            'tick_data' : tick_data ,
            'magic' : magic ,
            'time' : tick_pool.get_current_time()
        }
        
        self.unlock()
        
        return random_id , magic
        
    def is_exist_tick(self,tick_id) :
        result = tick_result.tick_state_error
        
        self.lock()
        
        if self.tick.has_key(tick_id) :
            if self.tick[tick_id]['time'] + tick_pool.__tick_expire_time > tick_pool.get_current_time() :
                result = tick_result.tick_state_success
            else :
                result = tick_result.tick_state_expire
        
        self.unlock()
        
        return result
        
    def remove_tick(self,tick_id) :
        self.lock()
        
        if self.tick.has_key(tick_id) :
            self.tick.pop(tick_id)
        
        self.unlock()
        
    def get_tick_magic(self,tick_id) :
        result = tick_result.tick_state_error
        
        self.lock()
        
        if self.tick.has_key(tick_id) :
            if self.tick[tick_id]['time'] + tick_pool.__tick_expire_time > tick_pool.get_current_time() :
                result = self.tick[tick_id]['magic']
            else :
                result = tick_result.tick_state_expire
        
        self.unlock()
        
        return result
        
    def get_tick_data(self,tick_id) :
        result = tick_result.tick_state_error
        
        self.lock()
        
        if self.tick.has_key(tick_id) :
            if self.tick[tick_id]['time'] + tick_pool.__tick_expire_time > tick_pool.get_current_time() :
                result = self.tick[tick_id]['tick_data']
            else :
                result = tick_result.tick_state_expire
        
        self.unlock()
        
        return result
        
class captcha_valid :
    
    def __init__(self) :
        self.tick_pow_list = tick_pool()
        self.tick_valid_state = tick_pool()
    
    def get_captcha(self) :
        pow_list = pow.random_make_pow()
        tick_id , magic_number = self.tick_pow_list.add_tick(pow_list)
        
        captcha_data = {
            'pow_list' : pow_list ,
            'tick' : tick_id ,
            'magic' : magic_number
        }
        
        return captcha_data
    
    def valid_captcha(self,tick_id,magic,pow_list) :
        tick_status = self.tick_pow_list.is_exist_tick(tick_id)
        
        if not tick_result.tick_state_success == tick_status :
            return self.tick_valid_state.add_tick(tick_status)
        
        tick_status = self.tick_pow_list.get_tick_magic(tick_id)
        
        if not magic == tick_status :
            return self.tick_valid_state.add_tick(tick_status)
            
        self.tick_pow_list.remove_tick(tick_id)
            
        valid_result = pow.valid_pow(pow_list)
        
        if valid_result :
            return self.tick_valid_state.add_tick(tick_result.tick_state_success)
        
        return self.tick_valid_state.add_tick(tick_result.tick_state_error)
        
    def check_tick(self,tick_id) :
        tick_status = self.tick_valid_state.is_exist_tick(tick_id)
        
        if not tick_result.tick_state_success == tick_status :
            return tick_status
        
        result = self.tick_valid_state.get_tick_data(tick_id)
        
        self.tick_valid_state.remove_tick(tick_id)
        
        return result
        
        
class get_captcha_handle(tornado.web.RequestHandler) :  #  handle by tornado ..
    
    def get(self) :
        return_json = captcha.get_captcha()
        
        self.write(json.dumps(return_json))

class valid_captcha_handle(tornado.web.RequestHandler) :
    
    def post(self) :
        tick_id = self.get_argument('tick')
        magic = self.get_argument('magic')
        pow_list = self.get_argument('pow_list')
        pow_list = json.loads(pow_list)
        
        for pow_index in pow_list :
            pow_index['data'] = base64.b64decode(pow_index['data'])
            pow_index['data'] = base64.b64decode(pow_index['data'])
        
        valid_tick,ignore_magic = captcha.valid_captcha(tick_id,magic,pow_list)
        
        self.write(json.dumps({
            'tick' : valid_tick
        }))
        
        
captcha = captcha_valid()
        