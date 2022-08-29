function VG(e, t) {
    switch (arguments.length) {
        case 1:
            return parseInt(Math.random() * e + 1, 10);
        case 2:
            return parseInt(Math.random() * (t - e + 1) + e, 10);
        default:
            return 0
    }
}

const cF = "zxcvbnmlkjhgfdsaqwertyuiop0987654321QWERTYUIOPLKJHGFDSAZXCVBNM"
    , zG = cF + "-@#$%^&*+!";

function ar(e = []) {
    return e.map(t => zG[t]).join("")
}

function YG(e) {
    return [...Array(e)].map(() => cF[VG(0, 61)]).join("")
}

function get_f() {
    let s = Date.now();
    let l = YG(16);

    return {
        "X-Dgi-Req-App": "ggzy-portal",
        "X-Dgi-Req-Nonce": l,
        "X-Dgi-Req-Timestamp": s.toString(),
    }
}

function get_c() {
    return ar([8, 28, 20, 42, 21, 53, 65, 6]);

}