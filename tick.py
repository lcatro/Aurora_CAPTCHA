
import base64
import json
import thread

import tornado.web
import tornado.ioloop

import pow


class tick_pool :
    
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
            'magic' : magic
        }
        
        self.unlock()
        
        return random_id , magic
        
    def is_exist_tick(self,tick_id) :
        result = False
        
        self.lock()
        
        if self.tick.has_key(tick_id) :
            result = True
        
        self.unlock()
        
        return result
        
    def remove_tick(self,tick_id) :
        self.lock()
        
        if self.tick.has_key(tick_id) :
            self.tick.pop(tick_id)
        
        self.unlock()
        
    def get_tick_magic(self,tick_id) :
        result = False
        
        self.lock()
        
        if self.tick.has_key(tick_id) :
            result = self.tick[tick_id]['magic']
        
        self.unlock()
        
        return result
        
    def get_tick_data(self,tick_id) :
        result = False
        
        self.lock()
        
        if self.tick.has_key(tick_id) :
            result = self.tick[tick_id]['tick_data']
        
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
        if not self.tick_pow_list.is_exist_tick(tick_id) :
            return self.tick_valid_state.add_tick(False)
        
        if not magic == self.tick_pow_list.get_tick_magic(tick_id) :
            return self.tick_valid_state.add_tick(False)
            
        self.tick_pow_list.remove_tick(tick_id)
            
        valid_result = pow.valid_pow(pow_list)
        
        if valid_result :
            return self.tick_valid_state.add_tick(True)
        
        return self.tick_valid_state.add_tick(False)
        
    def check_tick(self,tick_id) :
        if not self.tick_valid_state.is_exist_tick(tick_id) :
            return False
        
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
        
def get_captcha_javascript_code() :
    js_code = '''
    
        function build_url_argument_string(url_argument_list) {
            var url_argument_string='';

            if (undefined == url_argument_list)
                return '';

            for (var url_argument_index in url_argument_list)
                eval('url_argument_string+="'+url_argument_index+'="+url_argument_list.'+url_argument_index+'+"&"');

            if (url_argument_string.length)
                url_argument_string=url_argument_string.substr(0,url_argument_string.length-1);

            return url_argument_string;
        }

        function request_get(request_url,request_argument_list) {
            var request = new XMLHttpRequest();

            request.open('get',request_url + '?' + build_url_argument_string(request_argument_list),false);
            request.send();

            if (4 == request.readyState)
                return JSON.parse(request.responseText);

            return false;
        }

        function request_post(request_url,request_argument_list) {
            var request = new XMLHttpRequest();

            request.open('post',request_url,false);
            request.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
            request.send(build_url_argument_string(request_argument_list));

            if (4 == request.readyState)
                return JSON.parse(request.responseText);

            return false;
        }

        function calculate_pow(pow_list) {
            pow_result_list = [];

            for (pow_index in pow_list) {
                pow_index = pow_list[pow_index];
                string = pow_index['string'];
                bit_flag = pow_index['bit_flag'];
                bit_offset = pow_index['bit_offset'];
                hash_loop = pow_index['hash_loop'];
                data_record = [ string ];

                while (true) {
                    string = sha256(string);

                    if (bit_flag == string.substr(bit_offset,2))
                        break;

                    if (1 == hash_loop) {
                        data_record = [ string ];
                    } else {
                        if (data_record.length < hash_loop) {
                            data_record.push(string);
                        } else {
                            data_record = data_record.slice(1,hash_loop);

                            data_record.push(string);
                        }
                    }
                }

                pow_result_list.push({
                    'data' : btoa(btoa(data_record[0])) ,
                    'bit_flag' : bit_flag ,
                    'bit_offset' : bit_offset ,
                    'hash_loop' : hash_loop ,
                });
            }

            return pow_result_list;
        }

        function valid_captcha() {
            captcha_data = request_get('/get_captcha');
            pow_list = captcha_data['pow_list'];
            pow_result_list = calculate_pow(pow_list);
            pow_result_list = JSON.stringify(pow_result_list);
            post_data = {
                'pow_list' : pow_result_list ,
                'tick'     : captcha_data['tick'] ,
                'magic'    : captcha_data['magic'] ,
            };

            tick = request_post('/valid_captcha',post_data);

            console.log(post_data);
            console.log(tick);

            return tick['tick'];
        }
        
        pass_tick = '';
        
        function captcha_click() {
            div_captcha = document.getElementById('captcha');
            p_output = document.getElementById('output');
            p_output.text = 'Validing';
            pass_tick = valid_captcha();
            p_output.text = 'Passing';
        }
        
    '''
    
    return js_code

def get_captcha_html_code() :
    html = '''
        <div id='captcha' width='60' height='20' onclick='captcha_click();' >
            <p id='output'>Click For Valid</p>
        </div>
    '''
    
    return html
    
        
captcha = captcha_valid()
        