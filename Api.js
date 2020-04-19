// change this variable to set the IP where is deployed the project
const dockerIP = "localhost";

//modele
function Registration(){
    //attribution
    let data = {

      id: document.getElementById('uname').value,

      password: document.getElementById('password').value,
    }

    //Transfert coté docker en json
    let req = $.ajax({
        url: 'http://'+dockerIP+':5001/users/',
        type: 'POST',
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: [function(){
            alert('User Created');
        }],
        error: [function () {
            alert('User creation Failure');
        }]
    });

    req.then(function(response) {
        console.log(response)
    }, function(xhr) {
        console.error('failed to fetch xhr', xhr)
    })
}

//modele
function Connection(){

    let data = $("form").serialize()

    //demande de get les infos renseignées au docker
    let req = $.ajax({
        //appel du docker avec un get
        url: 'http://'+  dockerIP +':5001/users/',
        type:'GET',
        data: data,
        success: [function(){
            alert('User Connected');
            window.location.reload(false);
        }],
        error: [function () {
            alert('Error connection');
        }]
    });

    req.then(function(response) {
        let regex = /b'(?<token>.+)'/gm;
        let m;
        let token;
        //tokens "pré-stockés"
        while ((m = regex.exec(response["response"].toString())) !== null) {
            if (m.index === regex.lastIndex) {
                regex.lastIndex++;
            }
            token = m[1]
        }
        //assignement d'un token
        localStorage.setItem('token', token);
        localStorage.setItem('username', document.getElementById('id').value);
    }, function(xhr) {
        console.error('failed to fetch xhr', xhr)
    })
}

//déconnection : 
function Deco() {
    //destruction du local storage (token, id, ...) et reload
    localStorage.clear();
    window.location.reload(false);
}
