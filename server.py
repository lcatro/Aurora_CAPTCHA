
import json
import os

import tornado.web
import tornado.ioloop

import captcha


class login_handle(tornado.web.RequestHandler) :
    
    def post(self) :
        tick_id = self.get_argument('tick')
        valid_state = captcha.captcha.check_tick(tick_id)
        
        if valid_state :
            guest_code = self.get_argument('guest_code')
            
            if '514230' == guest_code :
                result = 'Pass Success'
            else :
                result = 'Pass Error'
        else :
            result = 'Captcha Error ..'
        
        self.write(json.dumps({
            'status' : result
        }))
        
class main_handle(tornado.web.RequestHandler) :
    
    def get(self) :
        page = '''
        <html>
        
            <title>Aurora CAPTCHA Demo by LCatro</title>
        
            <script src="/captcha/aurora_ui.js"></script>
        
            <script>
           
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

                function request_post(request_url,request_argument_list) {
                    var request = new XMLHttpRequest();

                    request.open('post',request_url,false);
                    request.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
                    request.send(build_url_argument_string(request_argument_list));

                    if (4 == request.readyState)
                        return JSON.parse(request.responseText);

                    return false;
                }

                function submit() {
                    if (undefined == window.pass_tick) {
                        alert('Please Click CAPTCHA ..');
                        
                        return 'No Click Captcha';
                    }
                
                    guest_code = document.getElementById('guest_code');
                    post_data = {
                        'guest_code' : guest_code.value ,
                        'tick'       : window.pass_tick
                    }

                    check_state = request_post('/login',post_data);

                    alert(check_state['status']);

                    return check_state;
                }
            
            </script>
        
            <body>
                Guest Code: <input id="guest_code" type="text" value="" />
                <br/>
                <img id="captcha" src="/captcha_picture/start.png" onload="captcha_load()" />
                <br/>
                <input type="button" value="submit" onclick="submit()" />
            </body>
        
        </html>
        '''
        
        self.write(page)
        
        
def start_server(local_port) :
    handler = [
        ('/get_captcha',captcha.get_captcha_handle) ,
        ('/valid_captcha',captcha.valid_captcha_handle) ,
        ('/captcha/(.*)',tornado.web.StaticFileHandler,{'path':'captcha'}) ,
        ('/captcha_picture/(.*)',tornado.web.StaticFileHandler,{'path':'captcha_picture'}) ,
        ('/login',login_handle) ,
        ('/',main_handle) ,
    ]
    http_server = tornado.web.Application(handlers = handler)
    
    http_server.listen(local_port)
    tornado.ioloop.IOLoop.current().start()



start_server(80)

