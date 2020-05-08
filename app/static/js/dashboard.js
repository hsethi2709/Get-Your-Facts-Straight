
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
totalPID();
getTrustScore();
getSatisfactionScore();
