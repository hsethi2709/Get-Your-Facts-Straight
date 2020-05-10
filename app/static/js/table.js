function getSentenceInformation(condition){
    console.log(condition)
    switch(condition){
        case 1:
            document.getElementById('condition-label').innerHTML = "<strong>Condition 1 - Single Evidence</strong>";
            break;
        case 2:
            document.getElementById('condition-label').innerHTML = "<strong>Condition 2 - Three Evidences</strong>";
            break;
        case 3:
            document.getElementById('condition-label').innerHTML = "<strong>Condition 3 - Both Supporting & Refuting Evidence, No Label</strong>";
            break;
        case 4:
            document.getElementById('condition-label').innerHTML = "<strong>Condition 4 - No Label, Only Evidence</strong>";
            break;
    }
        
    var payload = {
        'condition': condition.toString(),
    };
    url='https://www.getfactcheck.me/getSentenceAverageSatisfactionScore'
    fetch(url, {
        method:'post',
        headers: {
            'Content-Type': 'application/json'
          },
        body: JSON.stringify(payload)
    }).then(function(response) {
        if (response.status == 200) {
            response.json().then(function(data){
                console.log(data);
                table = document.getElementById('table')
                table.innerHTML = ""
                for (var sentence in data){
                    var row = document.createElement("tr")
                    var td_sentence = document.createElement("td")
                    var td_trust = document.createElement("td")
                    var td_satisfaction = document.createElement("td")
                    td_sentence.innerHTML = sentence
                    td_trust.innerHTML = data[sentence]['trust']
                    td_satisfaction.innerHTML = data[sentence]['satisfaction']
                    row.appendChild(td_sentence)
                    row.appendChild(td_trust)
                    row.appendChild(td_satisfaction)
                    table.appendChild(row)


                }
            })}})}


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
}
else{
    window.location.assign("https://www.getfactcheck.me/dashboard_login");
}
}
