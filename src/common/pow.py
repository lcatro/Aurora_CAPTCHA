# coding: utf8
import hashlib
import random
import time

random_string_length = 16
random_bit_flag_length = 2
random_bit_offset_range = random_string_length - random_bit_flag_length


def sha256(data):
    return hashlib.sha256(data).digest()


def make_string(length):
    string = ''
    char_list = range(48, 57) + range(65, 90) + range(97, 122)

    for index in range(length):
        string += chr(random.choice(char_list))

    return string


def random_make_pow():
    pow_list = []

    for pow_index in range(12):  # make 16 pow work ..
        random_string = make_string(random_string_length)
        random_bit_flag = make_string(random_bit_flag_length)  # bit_flag = 2
        random_bit_offset = random.randint(0, random_bit_offset_range)  # bit_offset = (0,len - bit_flag)
        random_hash_loop = random.randint(2, 4)  # hash_loop = (1,5)

        pow_list.append({
            'string': random_string,
            'bit_flag': random_bit_flag,
            'bit_offset': random_bit_offset,
            'hash_loop': random_hash_loop,
        })

    return pow_list


def valid_pow(pow_list):
    try:
        for pow_index in pow_list:
            result_hash = pow_index['data']
            bit_flag = pow_index['bit_flag']
            bit_offset = pow_index['bit_offset']
            hash_loop = pow_index['hash_loop']

            for hash_index in range(hash_loop):
                result_hash = sha256(result_hash)

            if not bit_flag == result_hash[bit_offset: bit_offset + random_bit_flag_length]:
                return False

        return True
    except:
        pass

    return False


def test_pow():
    start_time = time.time()
    pow_list = random_make_pow()
    pow_result_list = []

    for pow_index in pow_list:
        string = pow_index['string']
        bit_flag = pow_index['bit_flag']
        bit_offset = pow_index['bit_offset']
        hash_loop = pow_index['hash_loop']
        data_record = [string]

        while True:
            string = sha256(string)

            if bit_flag == string[bit_offset: bit_offset + random_bit_flag_length]:
                break

            if 1 == hash_loop:
                data_record = [string]
            else:
                if len(data_record) < hash_loop:
                    data_record += [string]
                else:
                    data_record = data_record[1: hash_loop] + [string]

        pow_result_list.append({
            'data': data_record[0],
            'bit_flag': bit_flag,
            'bit_offset': bit_offset,
            'hash_loop': hash_loop,
        })

    print 'valid_pow:', valid_pow(pow_result_list)

    end_time = time.time()

    print 'Using:', end_time - start_time


if __name__ == '__main__':
    test_pow()


    def test_case():

        def valid(data='test', nonce='000'):
            start_time = time.time()
            data = sha256(data)
            calcute = 0

            while not data.startswith(nonce):
                data = sha256(data)
                calcute += 1

            end_time = time.time()

            return end_time - start_time, calcute

        def random_valid_list():
            start_time = time.time()

            for loop in range(16):
                random_string = make_string(16)

                print random_string, 'Using: ', valid(random_string, make_string(2))
                print random_string, 'Using: ', valid(random_string, make_string(2))

            end_time = time.time()

            return end_time - start_time

        '''
        print 'test 00  Using:',valid('test','00')
        print 'test 007 Using:',valid('test','007')
        print 'test 005 Using:',valid('test','005')
        print 'AAAAAAAA 00  Using:',valid('AAAAAAAA','00')
        print 'AAAAAAAA 007 Using:',valid('AAAAAAAA','007')
        print 'AAAAAAAA 005 Using:',valid('AAAAAAAA','005')
        print 'AAAAAAAA 000 Using:',valid('AAAAAAAA','000')
        '''

        # print 'AAAAAAAA 005 Using:',valid(make_string(4),'005')
        # print 'AAAAAAAA 000 Using:',valid(make_string(4),'000')
        # print 'Using:',valid('000')
