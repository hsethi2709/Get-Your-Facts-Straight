function getProfileInformation(pid){
    console.log(pid)
    var payload = {
        'pid': pid,
    };
    url='https://www.getfactcheck.me/getProfileInfo'
    fetch(url, {
        method:'post',
        headers: {
            'Content-Type': 'application/json'
          },
        body: JSON.stringify(payload)
    }).then(function(response) {
        if (response.status == 200) {
            response.json().then(function(data){
                console.log(data)
                user_data = data.participant_details;
                for (var condition in user_data){
                    console.log(condition)
                    table = document.getElementById("table-"+condition)
                    table.innerHTML = ""
                    for (var sentence in user_data[condition]["pre"]){
                        var row = document.createElement("tr")
                        var td_sentence = document.createElement("td")
                        var td_pre = document.createElement("td")
                        var td_unaware = document.createElement("td")
                        var td_post = document.createElement("td")
                        console.log(sentence)
                        td_sentence.innerHTML = sentence.replace("_",".")
                        td_pre.innerHTML = user_data[condition]['pre'][sentence]['label']  
                        var unaware = (user_data[condition]['pre'][sentence]['unaware'] == true) ? "Yes" : "No"
                        td_unaware.innerHTML =  unaware;
                        td_post.innerHTML = user_data[condition]['post'][sentence.replace("_",".")]  
                        row.appendChild(td_sentence)
                        row.appendChild(td_pre)
                        row.appendChild(td_unaware)
                        row.appendChild(td_post)
                        table.appendChild(row)
                    }

                    
                }
                }
            );

    }
}
    )
}

function getPID(){

    url='https://www.getfactcheck.me/getListOfParticipants'
    fetch(url, {
        method:'get',
        headers: {
            'Content-Type': 'application/json'
          }
    }).then(function(response) {
        if (response.status == 200) {
            response.json().then(function(data){
                console.log(data)
                for (var pid in data.participants){
                    console.log(data.participants[pid]) 
                    var menu = document.getElementById('dropdown_menu')
                    var link = document.createElement("a");
                    link.classList.add("dropdown-item");
                    link.role = "presentation";
                    link.href = "javascript:getProfileInformation("+data.participants[pid]+")";
                    link.innerHTML = data.participants[pid];
                    menu.appendChild(link)
                }
    
        }    
        );
    }}
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
        getPID();
    }
    else{
        window.location.assign("https://www.getfactcheck.me/dashboard_login");
    }
    }


