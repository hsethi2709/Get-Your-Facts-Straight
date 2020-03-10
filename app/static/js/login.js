var pid = 0
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
sentences = []
count = 0
final_count = 0
global_level = 1
function getSentences(level){
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
				response.json().then(function(data){
					console.log(data)
					sentences = data
					document.getElementById("sentences").innerHTML = sentences[count]
					}
				);
	
		}
	}
		)}
// Button Click Events
document.getElementById('true').addEventListener('click', function(){
	var payload = {
		"pid": pid,
		"Sentence":document.getElementById("sentences").innerHTML,
		"label": "True"

	};
	url='https://www.getfactcheck.me/addSentenceToClient'
	fetch(url, {
		method:'post',
		headers: {
			'Content-Type': 'application/json'
		  },
		body: JSON.stringify(payload)
	}).then(function(response) {
		if (response.status == 200) {
			count += 1
			final_count += 1
			if (final_count == 1){
				console.log("Moving to next level")
				global_level += 1
				if (global_level<5){
				getSentences(global_level)
				count = 0
				final_count = 0	
			}
				else{
				console.log("All levels completed")
				}
			document.getElementById("sentences").innerHTML = sentences[count]
		}
			
		}}
		);

});

document.getElementById('fake').addEventListener('click', function(){
	var payload = {
		"pid": pid,
		"Sentence":document.getElementById("sentences").innerHTML,
		"label": "Fake"

	};
	url='https://www.getfactcheck.me/addSentenceToClient'
	fetch(url, {
		method:'post',
		headers: {
			'Content-Type': 'application/json'
		  },
		body: JSON.stringify(payload)
	}).then(function(response) {
		if (response.status == 200) {
			count += 1
			final_count += 1
			if (final_count == 1){
				console.log("Moving to next level")
				global_level += 1
				if (global_level<5){
				getSentences(global_level)
				count = 0
				final_count = 0	
			}
				else{
				console.log("All levels completed")
				}
			document.getElementById("sentences").innerHTML = sentences[count]
		}
			
		}}
		);

});

document.getElementById('alreadyKnow').addEventListener('click', function(){
		count += 1
		if (final_count == 1){
			console.log("Moving to next level")
			global_level += 1
			if (global_level<5){
			getSentences(global_level)
			count = 0
			final_count = 0	
		}
			else{
			console.log("All levels completed")
			}
		document.getElementById("sentences").innerHTML = sentences[count]
	}
		
	
});