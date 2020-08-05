
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

pid = getCookie('pid')
sentences = []
count = 0
final_count = 0
global_level = 1
experiment_level = [1,2,3,4]
var opinion_choice = null
function getSentences(level){
	console.log("Getting Sentences for Level:", level)
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
		var checked = document.getElementById('noIdea').checked;
		var payload = {
			"pid": pid,
			"sentence":document.getElementById("sentences").innerHTML,
			"label": opinion_choice,
			"level": global_level.toString(),
			"stage": "pre",
			"unaware": checked,
			"confidence_scale": confidence_scale
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
				console.log("Count:", count)
				final_count += 1
				if (final_count == 5){
					console.log("Moving to next level")
					global_level += 1
					if (global_level<5){
					getSentences(global_level)
					count = 0
					final_count = 0	
					}
					else{
					console.log("All levels completed")
					window.location.assign("https://www.getfactcheck.me/training");
					}
			}
			document.getElementById("sentences").innerHTML = sentences[count]
			document.getElementById('noIdea').checked = false;
			document.getElementById("error").style.display = "none";
			opinion_choice = null;
			}}
			);
		}
}

// Button Click Events
document.getElementById('true').addEventListener('click', function(){
	opinion_choice = true;
});

document.getElementById('fake').addEventListener('click', function(){
	opinion_choice = false;
});

