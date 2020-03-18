// e ：{"/api/nuser/account/get":{},"/api/music-vip-membership/front/vip/info":{},"/api/purchased/redvip/vipstatus":{}}
// t：010001
// n：00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
// a：0CoJUm6Qyw8W8jud
//l
function a(e, t, n, a) {

    var u = {}
        , s = r(16);
    return u.encText = o(e, a),
        u.encText = o(u.encText, s),
        u.encSecKey = i(s, t, n),
        u
}

//o
function o(e, t) {
    var n = s.enc.Utf8.parse(t)
        , r = s.enc.Utf8.parse("0102030405060708")
        , o = s.enc.Utf8.parse(e);
    return s.AES.encrypt(o, n, {
        iv: r,
        mode: s.mode.CBC
    }).toString()

}

//s.enc.Utf8.parse
parse: function (e) {
    return l.parse(unescape(encodeURIComponent(e)))
}

// l
parse: function (e) {
    for (var t = e.length, n = [], r = 0; r < t; r++)
        n[r >>> 2] |= (255 & e.charCodeAt(r)) << 24 - r % 4 * 8;
    console.info(n)
    console.info(t)
    return new a.init(n, t)
}

//a.init
init: function (e, t) {
    e = this.words = e || [],
        this.sigBytes = void 0 != t ? t : 4 * e.length
}
,