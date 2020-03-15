var pid = 0
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
checkCookie();
sentences = []
count = 0
global_level = 0
experiment_level = [1,2,3,4]
shuffleArray(experiment_level)
getClientSentences(experiment_level[global_level])
changeLevelDisplay()
function getClientSentences(level){
	document.cookie = "level="+level;
	console.log("Getting Client Sentences for Level:", level)
	console.log(pid)
		var payload = {
			'pid': pid,
			'level': level.toString()
		};
		url='https://www.getfactcheck.me/readClientSentences'
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
					document.getElementById("experimentSentences").innerHTML = sentences[count]
					}
				);
	
		}
	}
		)}

function changeLevelDisplay(){
	document.getElementById("levelDisplay").innerHTML = "Level "+experiment_level[global_level];
}

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

// Button Click Events
document.getElementById('next').addEventListener('click', function(){
			count += 1
			console.log("Count:", count)
			if (count == 1){
				console.log('Moving to Feedback Page')
				if (experiment_level[global_level] == 1){
					window.open("https://harshitsethi.typeform.com/to/DyauDC");
				}
				else if (experiment_level[global_level] == 2){
					window.open("https://harshitsethi.typeform.com/to/g2wikq");
				}
				else if (experiment_level[global_level] == 3){
					window.open("https://harshitsethi.typeform.com/to/UwkUPV");
				}
				else {
					window.open("https://harshitsethi.typeform.com/to/T5HCPC");

				}
				console.log("Moving to next level")
				global_level += 1
				if (global_level<4){
				getClientSentences(experiment_level[global_level])
				count = 0
				changeLevelDisplay()
			}
				else{
				console.log("All levels completed")
				window.location.replace("https://www.getfactcheck.me/post");

				}
			document.getElementById("experimentSentences").innerHTML = sentences[count]
		}
			
		}
		);
