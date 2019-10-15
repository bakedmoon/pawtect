function isNumber(e){
    var regex = new RegExp(/[^0-9]/g);
    var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);
    if (regex.test(str)) {
        return false;
    }
    else
    {
    return true;
    }
    }

function isSpecial(e){
    var regex = new RegExp(/^[a-zA-Z\s]+$/);
    var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);
    if (regex.test(str)) {
        return true;
    }
    else
    {
    return false;
    }
    }   

function isSpecialAge(e){
    let regex = new RegExp(/^[a-zA-z\d\-\s]/)
    var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);
    if (regex.test(str)) {
        return true;
    }
    else
    {
    return false;
    }
}   

function isSpacebar(evt){
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if(charCode == 32){
        return false;
    }else{
        return true;
    }
}
