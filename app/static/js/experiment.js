var pid = 0
var fact_check = true;
var global_level = 0;
var experiment_level = [1,2,3,4]
shuffleArray(experiment_level)
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
	if (getCookie('experiment_status') == null)
	{
		document.cookie = "experiment_status=0";
	}
	pid = getCookie("pid");
	if (pid != null) {
	 document.getElementById('pidLabel').innerHTML = pid
	} else {
	  pid = prompt("Please enter your Participant ID:", "");
	  if (pid != "" && pid != null) {
		document.cookie = "pid="+pid+";"+"level="+2;
		document.getElementById('pidLabel').innerHTML = pid
	  }
	}
	fact_check = getCookie("fact_check")
	if (fact_check == null){
		document.cookie = "fact_check="+false;
	}
	global_level = (getCookie('experiment_stage'))
	if (global_level == null){
		global_level = 0
		document.cookie = "experiment_stage="+0;
	}
	else{
		global_level = parseInt(global_level)
	}
	experiment_level = JSON.parse(getCookie('experiment_array'))
	if (experiment_level == null){
		experiment_level = [1,2,3,4]
		shuffleArray(experiment_level)
		document.cookie = "experiment_array="+JSON.stringify(experiment_level);
	}
  }
checkCookie();
sentences = []
count = 0
getClientSentences(experiment_level[global_level])
document.cookie = "level="+experiment_level[global_level];
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
					document.getElementById("experimentSentences").innerHTML = sentences[count]+"<br>"
					}
				);
	
		}
	}
		)}

function changeLevelDisplay(){
	if (experiment_level[global_level] == 1){
		document.getElementById("levelDisplay").innerHTML = "Single Evidence"
		document.getElementById("levelInstruction").style.display = "block";
		document.getElementById("levelInstruction").innerHTML = "You will be shown a single supporting or refuting evidence along with a label in this condition for each claim."
	}
	else if (experiment_level[global_level] == 2){
		document.getElementById("levelDisplay").innerHTML = "Three Evidences"
		document.getElementById("levelInstruction").style.display = "block";
		document.getElementById("levelInstruction").innerHTML = "You will be shown three supporting or refuting evidences along with a label in this condition for each claim."

	}
	else if (experiment_level[global_level] == 3){
		document.getElementById("levelDisplay").innerHTML = "Both Supporting and Refuting Arguments without Label"
		document.getElementById("levelInstruction").style.display = "block";
		document.getElementById("levelInstruction").innerHTML = "You will be shown both supporting and refuting evidences without a label in this condition for each claim."
	}
	else if (experiment_level[global_level] == 4){
		document.getElementById("levelDisplay").innerHTML = "No Label, Only Evidences"
		document.getElementById("levelInstruction").style.display = "block";
		document.getElementById("levelInstruction").innerHTML = "You will be shown only supporting or refuting evidences without a label in this condition for each claim."
	}	
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
			if (getCookie("fact_check") == "false"){
				document.getElementById("error").style.display = "block";
			}
			else{
				document.getElementById("error").style.display = "none";
			count += 1
			document.getElementById("levelInstruction").style.display = "none";
			console.log("Count:", count)
			if (count == 5){
				console.log('Moving to Feedback Page')
				if (experiment_level[global_level] == 1){
					window.open("https://harshitsethi.typeform.com/to/DyauDC?pid="+pid);
				}
				else if (experiment_level[global_level] == 2){
					window.open("https://harshitsethi.typeform.com/to/g2wikq?pid="+pid);
				}
				else if (experiment_level[global_level] == 3){
					window.open("https://harshitsethi.typeform.com/to/UwkUPV?pid="+pid);
				}
				else {
					window.open("https://harshitsethi.typeform.com/to/T5HCPC?pid="+pid);

				}
				console.log("Moving to next level")
				global_level += 1
				document.cookie = "experiment_stage="+global_level;
				if (global_level<4){
				getClientSentences(experiment_level[global_level])
				count = 0
				changeLevelDisplay()
			}
				else{
				console.log("All levels completed")
				window.location.replace("https://www.getfactcheck.me/postExperimentInstruction");

				}
		}
		document.getElementById("experimentSentences").innerHTML = sentences[count]+"<br>"
		document.cookie = "fact_check="+false;

			
		}}
		);
