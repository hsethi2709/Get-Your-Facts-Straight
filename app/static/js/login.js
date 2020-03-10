function log_in(){
	pid = document.getElementById('pid').value;
	document.cookie = "pid="+pid;
	age = document.getElementById('age').value;
	console.log("PID and AGE are:", pid, age);

	if (pid == "" || pid == null){
		document.getElementById('pid').focus();
	}
	else if (age == "" || age == null){
		document.getElementById('age').focus();
    }
    else
        {
        var payload = {
		_id: pid,
		p_age: age
	};
	url='https://www.getfactcheck.me/addUser'
	fetch(url, {
		method:'post',
		headers: {
			'Content-Type': 'application/json'
		  },
		body: JSON.stringify(payload)
	}).then(function(response) {
		if (response.status == 200) {
            window.location.replace("https://www.getfactcheck.me/pre");

		}
	        
		}
		);
        }
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

function checkCookie() {
	var username = getCookie("pid");
	if (username != "") {
	 document.getElementById('pidLabel').innerHTML = username
	} else {
	  username = prompt("Please enter your Participant ID:", "");
	  if (username != "" && username != null) {
		setCookie("pid", username, 365);
	  }
	}
  }

function getSentences(){
	for (level = 1; level < 5; level++) {
		var payload = {
			'level': level
		};
		url='https://www.getfactcheck.me/readMasterSentences'
		fetch(url, {
			method:'post',
			headers: {
				'Content-Type': 'application/json'
			  },
			body: JSON.stringify(payload)
		}).then(function(response) {
			if (response.status == 200) {
				console.log(response)
	
			}
				
			}
			);
	
	}
}
