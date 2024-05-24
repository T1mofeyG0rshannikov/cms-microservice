function containsCyrillic(str) {
    return /[\u0400-\u04FF\u2DE0-\u2DFF]/i.test(str);
}

function validatePassword(value){
    return value.length > 5;
}
