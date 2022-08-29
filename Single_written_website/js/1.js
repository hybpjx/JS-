function get_t() {

    var chars = "0123456789abcdef";
    var curTime = parseInt(Math.random() * (9999 - 1000 + 1) + 1000) + "" + Date.parse(new Date());
    var sig = chars.charAt(parseInt(Math.random() * (15 - 15 + 1) + 10)) + chars.charAt(curTime.length) + "" + curTime;

    var key = "";
    var keyIndex = -1;
    for (var i = 0; i < 6; i++) {
        var c = sig.charAt(keyIndex + 1);
        key += c;
        keyIndex = chars.indexOf(c);
        if (keyIndex < 0 || keyIndex >= sig.length) {
            keyIndex = i;
        }
    }

    var timestamp = parseInt(Math.random() * (9999 - 1000 + 1) + 1000) + "_" + key + "_" + Date.parse(new Date());
    var tkey = "";
    var tkeyIndex = -1;
    for (var i = 0; i < 6; i++) {
        var c = timestamp.charAt(tkeyIndex + 1);
        tkey += c;
        tkeyIndex = chars.indexOf(c);
        if (tkeyIndex < 0 || tkeyIndex >= timestamp.length) {
            tkeyIndex = i;
        }
    }

    return {sig, timestamp, tkey}
}



// function getkey() {
//     var chars = "0123456789abcdef";
//     var curTime = parseInt(Math.random() * (9999 - 1000 + 1) + 1000) + "" + Date.parse(new Date());
//     var sig = chars.charAt(parseInt(Math.random() * (15 - 15 + 1) + 10)) + chars.charAt(curTime.length) + "" + curTime;
//
//     var key = "";
//     var keyIndex = -1;
//     for (var i = 0; i < 6; i++) {
//         var c = sig.charAt(keyIndex + 1);
//         key += c;
//         keyIndex = chars.indexOf(c);
//         if (keyIndex < 0 || keyIndex >= sig.length) {
//             keyIndex = i;
//         }
//     }
//
//     var timestamp = parseInt(Math.random() * (9999 - 1000 + 1) + 1000) + "_" + key + "_" + Date.parse(new Date());
//
//     var tkey = "";
//     var tkeyIndex = -1;
//     for (var i = 0; i < 6; i++) {
//         var c = timestamp.charAt(tkeyIndex + 1);
//         tkey += c;
//         tkeyIndex = chars.indexOf(c);
//         if (tkeyIndex < 0 || tkeyIndex >= timestamp.length) {
//             tkeyIndex = i;
//         }
//     }
//
//     return {sig, timestamp, tkey}
// }


