var pid = Math.floor(Math.random() * 200) + 1;
checkPID();
function checkPID(){
	console.log("PID", pid)
	var payload = {
		"pid": pid
	};
	url='https://www.getfactcheck.me/checkDuplicatePID'
	fetch(url, {
		method:'post',
		headers: {
			'Content-Type': 'application/json'
		  },
		body: JSON.stringify(payload)
	}).then(function(response) {
		response.json().then(function(data) {
			console.log(data)
			
		if (data.status == 'false') {
            log_in();
		}
		else{
			pid = Math.floor(Math.random() * 200) + 1;
			checkPID();
		}
	})
	})
	}

function log_in(){
	console.log(getCookie('pid'))
	if (getCookie('pid') == null){
	document.cookie = "pid="+pid;
	document.cookie = "fact_check="+false;
	console.log("PID is:", pid);
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
            window.location.assign("https://www.getfactcheck.me/pre");
		}    
		}
		);
	}
	else if (getCookie('experiment_status') == null)
		{
			window.location.assign("https://www.getfactcheck.me/pre");
		}
	else if (getCookie('experiment_status') == 0)
	{
		window.location.assign("https://www.getfactcheck.me/experiment")
	}
	else if (getCookie('experiment_status') == 1)
	{
		window.location.assign("https://www.getfactcheck.me/thankyou")
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
	pid = getCookie("pid");
	if (pid != null) {
	 document.getElementById('pidLabel').innerHTML = pid
	} else {
	  pid = prompt("Please enter your Participant ID:", "");
	  if (pid != "" && pid != null) {
		document.cookie = "pid="+pid;
		document.getElementById('pidLabel').innerHTML = pid
	  }
	}
  }
