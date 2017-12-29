
## 极光验证码

  极光验证码,使用工作量证明(PoW)算法解决人机识别问题.传统的验证码是使用图片/音频等人类可以识别的因素来区分机器与人类.使用工作量证明的意义在于,访问站点时,需要花时间来计算一些有难度的数据,再提交到服务器进行验证.在人类访问站点时,操作频率往往不会太高,这些数据比较快就能算出来.当机器人爬取站点数据或者做帐号密码爆破时,需要进行多次数据计算,导致机器人的CPU 占用变高,消耗其硬件资源


### 极光验证码工作原理

  下图是极光验证码的工作原理,注意Tick1 和Tick2 的区别
  
  ![](picture\captcha_logic.png)
  
  1.首先,浏览器加载到验证码,向服务器请求数据`/get_captcha` <br/>
  2.接下来,服务器随机生成工作量计算数据和Tick1,Tick1 的意义在于给工作任务定义一个唯一ID <br/>
  3.浏览器获取到工作量计算数据之后,进行大量的hash 计算,最后返回工作量计算到服务器验证计算工作`/valid_captha` <br/>
  4.然后,服务器对浏览器的工作量计算进行验证,并分配Tick2 ,Tick2 用于保存验证的结果<br/>
  5.最后,浏览器把需要验证/获取的数据加上Tick2 上传到服务器,让服务器对验证码和数据进行验证
  
  
### 如何使用极光验证码(后端)
  
  目前Demo 版只支持Python Torando ,以后可能会移植到PHP 版本<br/>
  
  极光验证码的文件如下:
  
```

    pow.py    工作量证明生成与验证逻辑
    tick.py   验证码Tick 查询逻辑

```
  
  验证码的使用逻辑封装在`tick.py` 里,只需要`import tick` 即可使用.首先在tornado 里注册验证码需要用到的handle 
  
```python

    class get_captcha_handle()     获取验证码
    class valid_captcha_handle()   校验验证码
  
```
  
  示例代码:
  
```python

    handler = [
        ('/get_captcha',tick.get_captcha_handle) ,
        ('/valid_captcha',tick.valid_captcha_handle)
    ]
    http_server = tornado.web.Application(handlers = handler)
  
```
  
  至此,后端已经完成验证码模块的导入,我们还需要做的最后一件事是对用户上传的Tick2 进行验证,验证的接口在`tick.py`
  
```python

    import tick    #  导入极光验证码
    
    #  省略多余代码

    tick.captcha.check_tick(tick_id)    #  只需要传递tick2 到check_tick() 函数即可得到验证码校验结果

```
  
  示例代码:
  
```python

    class login_handle(tornado.web.RequestHandler) :  #  server.py 的代码

        def post(self) :
            tick_id = self.get_argument('tick')  #  获取浏览器提交上来的Tick2
            valid_state = tick.captcha.check_tick(tick_id)  #  验证Tick2 的结果

            if valid_state :  #  验证通过
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

```
  
  
### 如何使用极光验证码(前端)

  导入验证码模块和验证码UI 还在设计中,后面再更新
  
  当验证码计算完成并且获取到Tick2 时,会把Tick2 保存在全局变量`pass_tick` 中,在接下来和后端的校验中直接把Tick2 上传到服务器即可
  
  示例代码:
  
```javascript

    function submit() {
        guest_code = document.getElementById('guest_code');
        post_data = {
            'guest_code' : guest_code.value ,
            'tick'       : pass_tick  //  直接读取全局变量pass_tick 获取Tick2
        }

        check_state = request_post('/login',post_data);

        alert(check_state);

        return check_state;
    }

```
  

### 极光验证码的工作量证明算法(Proof of Work)

  工作量证明是指系统为达到某目标而设置的工作度量方法,需要由工作者和验证者两方共同完成.
  
  1.工作者需要完成的工作必须有一定的量,这个量由验证者给出<br/>
  2.验证者可以迅速的检验工作量是否达标,注意这里的检验完成过程必须简单
  
  
  
```python

    def valid(data = 'test',nonce = '000') :
        start_time = time.time()
        data = sha256(data)
        calcute = 0

        while not data.startswith(nonce) :
            data = sha256(data)
            calcute += 1

        end_time = time.time()

        return end_time - start_time,calcute
        
```
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

