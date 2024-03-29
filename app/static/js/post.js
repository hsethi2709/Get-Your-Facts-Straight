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
            window.location.assign("https://www.getfactcheck.me/pre");

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
var opinion_choice = null
function getSentences(level){
	console.log("Getting All Sentences")
		// url='http://localhost:5000/readMasterSentences'
		url='https://www.getfactcheck.me/readMasterSentences'
		fetch(url, {
			method:'get',
			headers: {
				'Content-Type': 'application/json'
			  }
		}).then(function(response) {
			if (response.status == 200) {
				response.json().then(function(data){
					console.log(data)
					sentences = data
					document.getElementById("sentences").innerHTML = sentences[count]['sentence']
					document.getElementById('counter').innerHTML = "Fact Inclination Progress: "+(count+1)+"/12"
					}
				);
	
		}
	}
		)}

// Function to shuffle the levels
function shuffleArray(array) {
			for (var i = array.length - 1; i > 0; i--) {
				var j = Math.floor(Math.random() * (i + 1));
				var temp = array[i];
				array[i] = array[j];
				array[j] = temp;
			}
			return (array)
		}
// Function to submit confidence and opinion about the sentence
function submitConfidence(evt){
	if (opinion_choice == null){
		document.getElementById("error").style.display = "block";
	}
	else{
		confidence_scale = evt;
		if (opinion_choice == true) {
			opinion_choice = "True"
		}
		else{
			opinion_choice = "Fake"
		}
		var payload = {
			"pid": pid,
			"sentence":document.getElementById("sentences").innerHTML,
			"label": opinion_choice,
			"sentence_id":sentences[count]['_id'].toString(),
			"stage": "post",
			"confidence_scale": confidence_scale
		};
		// url='http://localhost:5000/addSentenceToClient' 
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
				console.log("Count:", count)
				if (count == 12)
					{
						console.log("All levels completed")
						document.cookie = "experiment_status=1";
						window.location.assign("https://www.getfactcheck.me/post");
					}
				else{
					document.getElementById("sentences").innerHTML = sentences[count]['sentence']
					document.getElementById("error").style.display = "none";
					document.getElementById("confidence").style.display = "none";
					document.getElementById('fake').style.backgroundColor = "#ffffff00"
					document.getElementById('true').style.backgroundColor = "#ffffff00"
					document.getElementById('counter').innerHTML = "Fact Inclination Progress: "+(count+1)+"/12"
					opinion_choice = null;
					}
			}
			else{
				document.getElementById("sentences").innerHTML = sentences[count]['sentence']
				document.getElementById("error").style.display = "none";
				document.getElementById("confidence").style.display = "none";
				document.getElementById('fake').style.backgroundColor = "#ffffff00"
				document.getElementById('true').style.backgroundColor = "#ffffff00"
				document.getElementById('counter').innerHTML = "Fact Inclination Progress: "+(count+1)+"/12"
				opinion_choice = null;
			}

			}
			);
		}
}
// Button Click Events
document.getElementById('true').addEventListener('click', function(){
	opinion_choice = true;
	document.getElementById('true').style.backgroundColor = "red"
	document.getElementById('fake').style.backgroundColor = "#ffffff00"
	document.getElementById("confidence").style.display = "block";

});

document.getElementById('fake').addEventListener('click', function(){
	opinion_choice = false;
	document.getElementById('fake').style.backgroundColor = "red"
	document.getElementById('true').style.backgroundColor = "#ffffff00"
	document.getElementById("confidence").style.display = "block";
});


