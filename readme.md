
### 极光验证码

  极光验证码,使用工作量证明(PoW)算法解决人机识别问题.传统的验证码是使用图片/音频等人类可以识别的因素来区分机器与人类.使用工作量证明的意义在于,访问站点时,需要花时间来计算一些有难度的数据,再提交到服务器进行验证.在人类访问站点时,操作频率往往不会太高,这些数据比较快就能算出来.当机器人爬取站点数据或者做帐号密码爆破时,需要进行多次数据计算,导致机器人的CPU 占用变高,消耗其硬件资源

### 极光验证码的工作量证明算法(Proof of Work)

  工作量证明是指系统为达到某目标而设置的工作度量方法,需要由工作者和验证者两方共同完成.
  
  1.工作者需要完成的工作必须有一定的量,这个量由验证者给出
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
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

