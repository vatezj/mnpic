import $http from '@/assets/js/http'

export function testpost(data) {
    return $http.post('api/home/guessLike',data);
}

export function testget(data) {
    return $http.get('api/home/guessLike',data);
}

export function getpic($data) {
    return $http.get('api/index/mnpic?'+queryParams($data));
}

function queryParams (data, isPrefix) {
    isPrefix = isPrefix ? isPrefix : false
    let prefix = isPrefix ? '?' : ''
    let _result = []
    for (let key in data) {
      let value = data[key]
      // 去掉为空的参数
      if (['', undefined, null].includes(value)) {
        continue
      }
      if (value.constructor === Array) {
        value.forEach(_value => {
          _result.push(encodeURIComponent(key) + '[]=' + encodeURIComponent(_value))
        })
      } else {
        _result.push(encodeURIComponent(key) + '=' + encodeURIComponent(value))
      }
    }

    return _result.length ? prefix + _result.join('&') : ''
  }


