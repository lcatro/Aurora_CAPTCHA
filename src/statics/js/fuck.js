/**
 * Created by wangjin on 2017/12/29.
 */
importScripts('http://localhost:8081/statics/js/sha256.js');

function calculate_pow(pow_list) {
    var pow_result_list = [];

    for (var pow_index in pow_list) {
        pow_index = pow_list[pow_index];
        var string = pow_index['string'];
        var bit_flag = pow_index['bit_flag'];
        var bit_offset = pow_index['bit_offset'];
        var hash_loop = pow_index['hash_loop'];
        var data_record = [string];

        while (true) {
            string = sha256(string);

            if (bit_flag === string.substr(bit_offset, 2)) {
                break;
            }

            if (1 === hash_loop) {
                data_record = [string];
            } else {
                if (data_record.length < hash_loop) {
                    data_record.push(string);
                } else {
                    data_record = data_record.slice(1, hash_loop);

                    data_record.push(string);
                }
            }
        }

        pow_result_list.push({
            'data': btoa(btoa(data_record[0])),
            'bit_flag': bit_flag,
            'bit_offset': bit_offset,
            'hash_loop': hash_loop
        });
    }

    return pow_result_list;
}

function valid_captcha(pow_list, tick, magic) {
    var pow_result_list = calculate_pow(pow_list);
    pow_result_list = JSON.stringify(pow_result_list);
    var post_data = {
        'pow_list': pow_result_list,
        'tick': tick,
        'magic': magic
    };

    return post_data;
}


this.onmessage = function (message) {
    /*
     message = {
     'func': sha256,
     'oper': 'start',
     'pow_list': pow_list,
     'tick': tick,
     'magic': magic
     }
     */
    var data = valid_captcha(message.data.pow_list, message.data.tick, message.data.magic);
    this.postMessage({
        'result': data
    });
};

