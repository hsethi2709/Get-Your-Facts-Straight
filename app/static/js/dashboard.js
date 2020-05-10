
function totalPID(){

url='https://www.getfactcheck.me/getTotalParticipants'
fetch(url, {
    method:'get',
    headers: {
        'Content-Type': 'application/json'
      }
}).then(function(response) {
    if (response.status == 200) {
        response.json().then(function(data){
            console.log(data)
            document.getElementById("totalPID").innerHTML = data.count;

    }    
    );
}}
);
}

function getTrustScore(){
    url='https://www.getfactcheck.me/getAverageTrustScore'
fetch(url, {
    method:'get',
    headers: {
        'Content-Type': 'application/json'
      },
}).then(function(response) {
    if (response.status == 200) {
        response.json().then(function(data){
            console.log(data)
            for(var key in data){
                document.getElementById("condition-"+key).style.width = data[key]+"%";
                document.getElementById("condition-"+key).innerHTML = data[key];
            }
            

    }    
    );
}}
);
}
function getSatisfactionScore(){
    url='https://www.getfactcheck.me/getAverageSatisfactionScore'
fetch(url, {
    method:'get',
    headers: {
        'Content-Type': 'application/json'
      },
}).then(function(response) {
    if (response.status == 200) {
        response.json().then(function(data){
            console.log(data)
            for(var key in data){
                document.getElementById("condition-s-"+key).style.width = data[key]+"%";
                document.getElementById("condition-s-"+key).innerHTML = data[key];
            }
            

    }    
    );
}}
);
}

function log_in(){
    username = document.getElementById('username').value;
    password = document.getElementById('password').value;
    console.log(username, password)
    var payload = {
            "username": username,
            "password": password
        };
        url='https://www.getfactcheck.me/checkPassword'
        fetch(url, {
            method:'post',
            headers: {
                'Content-Type': 'application/json'
              },
            body: JSON.stringify(payload)
        }).then(function(response) {
            response.json().then(function (data) {
                if (data.status == "True"){
                    document.cookie = "dashboard_login=True; max-age=60";
                    window.location.href = "https://www.getfactcheck.me/dashboard";
                }
                else{
                    alert("Please try again!");
                }
            })
            }
            );
        
        }

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}  

if (window.location.href != "https://www.getfactcheck.me/dashboard_login"){
login = getCookie("dashboard_login")
if (login!= null)
{
totalPID();
getTrustScore();
getSatisfactionScore();
}
else{
    window.location.assign("https://www.getfactcheck.me/dashboard_login");
}
}