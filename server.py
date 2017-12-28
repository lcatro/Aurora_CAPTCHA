
import json
import os

import tornado.web
import tornado.ioloop

import tick


class login_handle(tornado.web.RequestHandler) :
    
    def post(self) :
        tick_id = self.get_argument('tick')
        valid_state = tick.captcha.check_tick(tick_id)
        
        if valid_state :
            username = self.get_argument('username')
            password = self.get_argument('password')
            
            if 'root' == username and '2140' == password :
                result = 'Pass Success'
            else :
                result = 'Pass Error'
        else :
            result = 'Captcha Error ..'
        
        self.write(json.dumps({
            'status' : result
        }))
        
class main_handle(tornado.web.RequestHandler) :
    
    @staticmethod
    def load_sha256_js() :
        file = open('sha256.js')
        data = file.read()
        
        file.close()
        
        return data
    
    def get(self) :
        page = '''
        <html>
        
            <script>  //  Sha256.js
            
            %s
            
            </script>
        
            <script>
            
            %s
            
            function submit() {
                username_text = document.getElementById('username');
                password_text = document.getElementById('password');
                username = username_text.value;
                password = password_text.value;
                post_data = {
                    'username' : username ,
                    'password' : password ,
                    'tick'     : pass_tick
                }
                
                check_state = request_post('/login',post_data);
                
                alert(check_state);
                
                return check_state;
            }
            
            </script>
        
            <body>
                username: <input id="username" type="text" value="" /> <br/>
                password: <input id="password" type="text" value="" /> <br/>
                %s
                <input type="button" value="submit" onclick="submit()" />
            </body>
        
        </html>
        ''' % (main_handle.load_sha256_js(), \
               tick.get_captcha_javascript_code(), \
               tick.get_captcha_html_code())
        
        self.write(page)
        
        
def start_server(local_port) :
    handler = [
        ('/get_captcha',tick.get_captcha_handle) ,
        ('/valid_captcha',tick.valid_captcha_handle) ,
        ('/login',login_handle) ,
        ('/',main_handle) ,
        ('/captcha_picture/(.*)',tornado.web.StaticFileHandler,{'path':'captcha_picture'})
    ]
    http_server = tornado.web.Application(handlers = handler)
    
    http_server.listen(local_port)
    tornado.ioloop.IOLoop.current().start()



start_server(80)

