function isNumber(evt){
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true; 
    }

function isSpecial(evt){
    evt = (evt) ? evt : window.event;
        var charCode = (evt.which) ? evt.which : evt.keyCode;
        if (charCode == 45 || charCode == 173 || charCode == 63 || charCode == 189 || charCode == 61 || charCode == 187 || charCode == 59 || charCode == 186 || charCode == 95 || charCode == 47 || charCode == 46 || charCode == 62 || charCode == 60 || charCode == 44 || charCode == 58 || charCode == 34 || charCode == 39 || charCode == 125 || charCode == 123 || charCode == 91 || charCode == 40 || charCode == 91 || charCode == 41 || charCode == 42 || charCode == 43 || charCode == 33 || charCode == 64 || charCode == 35 || charCode == 36 || charCode == 37 || charCode == 94 || charCode == 38 || charCode == 93) {
            return false;
        }
        return true;
    }   


function isChar(){
        var charCode = event.keyCode;
        if ((charCode > 64 && charCode < 91) || (charCode > 96 && charCode < 123) || charCode == 8){
            return true;
        }
        else{
            return false;
        }
                        
}

function isSpecialAge(evt){
    evt = (evt) ? evt : window.event;
        var charCode = (evt.which) ? evt.which : evt.keyCode;
        if (charCode == 173 || charCode == 63 || charCode == 189 || charCode == 61 || charCode == 187 || charCode == 59 || charCode == 186 || charCode == 95 || charCode == 47 || charCode == 46 || charCode == 62 || charCode == 60 || charCode == 44 || charCode == 58 || charCode == 34 || charCode == 39 || charCode == 125 || charCode == 123 || charCode == 91 || charCode == 40 || charCode == 91 || charCode == 41 || charCode == 42 || charCode == 43 || charCode == 33 || charCode == 64 || charCode == 35 || charCode == 36 || charCode == 37 || charCode == 94 || charCode == 38 || charCode == 93) {
            return false;
        }
        return true;
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
