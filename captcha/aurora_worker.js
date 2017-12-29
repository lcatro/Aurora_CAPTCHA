
importScripts('/captcha/sha256.js');


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

    return tick['tick'];
}

onmessage = function () {
    postMessage(valid_captcha());
}

