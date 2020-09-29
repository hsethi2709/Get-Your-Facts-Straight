var pid = 0
var fact_check = true;
var global_level = 0;
// var experiment_level = [1,2,3,4]

// shuffleArray(experiment_level)
total_sentences = []
for (var i = 0; i <= 11; i++) {
	total_sentences.push(i);
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
		experiment_level = [1,4,5]
		shuffleArray(experiment_level)
		document.cookie = "experiment_array="+JSON.stringify(experiment_level);
	}
	sentence_done = JSON.parse(getCookie('sentence_done'))
	if (sentence_done == null){
		sentence_done = []
		document.cookie = "sentence_done="+JSON.stringify(sentence_done);
	}
	count = (getCookie('sentence_count'))
	if (count == null){
		count = 0
		document.cookie = "sentence_count="+0;
	}
	else{
		count = parseInt(count)
	}
	truth_count = (getCookie('truth_count'))
	if (truth_count == null){
		truth_count = 0
		document.cookie = "truth_count="+0;
	}
	else{
		truth_count = parseInt(truth_count)
	}
	false_count = (getCookie('false_count'))
	if (false_count == null){
		false_count = 0
		document.cookie = "false_count="+0;
	}
	else{
		false_count = parseInt(false_count)
	}
  }
checkCookie();
if (global_level == 3){
	console.log("All levels completed")
	window.location.replace("https://www.getfactcheck.me/postExperimentInstruction");
}
sentences = []
randomElement = null
block_statement = null
while((randomElement == null || sentence_done.includes(randomElement)) && sentence_done.length != 12)
{
randomElement = total_sentences[Math.floor(Math.random() * total_sentences.length)];
}
getClientSentences(experiment_level[global_level])
document.cookie = "level="+experiment_level[global_level];

changeLevelDisplay()

function getClientSentences(level){
	document.cookie = "level="+level;
	console.log("Getting Client Sentences")
	console.log(pid)
		var payload = {
			'pid': pid
		};
		// url='http://localhost:5000/readMasterSentences'
		url='https://www.getfactcheck.me/readMasterSentences'
		fetch(url, {
			method:'get',
			headers: {
				'Content-Type': 'application/json'
			  },
			// body: JSON.stringify(payload)
		}).then(function(response) {
			if (response.status == 200) {
				response.json().then(function(data){
					sentences = data
					document.getElementById("experimentSentences").innerHTML = sentences[randomElement]['sentence']+"<br>"

					}
				);
	
		}
	}
		)}

function changeLevelDisplay(){
	if (experiment_level[global_level] == 1){
		document.getElementById("levelDisplay").innerHTML = "Labelled Evidence"
		document.getElementById("levelInstruction").style.display = "block";
		document.getElementById("levelInstruction").innerHTML = "You will be shown a piece of evidence along with a label that states whether the evidence confirms or refutes the statement's claim."
	}
	else if (experiment_level[global_level] == 5){
		document.getElementById("levelDisplay").innerHTML = "With Confidence Score"
		document.getElementById("levelInstruction").style.display = "block";
		document.getElementById("levelInstruction").innerHTML = "You will be shown a piece of evidence along with a score that indicates the confidence of the algorithm about the provided evidence being a fact."

	}
	else if (experiment_level[global_level] == 3){
		document.getElementById("levelDisplay").innerHTML = "Both Supporting and Refuting Arguments without Label"
		document.getElementById("levelInstruction").style.display = "block";
		document.getElementById("levelInstruction").innerHTML = "You will be shown both supporting and refuting evidences without a label in this condition for each claim."
	}
	else if (experiment_level[global_level] == 4){
		document.getElementById("levelDisplay").innerHTML = "No labels"
		document.getElementById("levelInstruction").style.display = "block";
		document.getElementById("levelInstruction").innerHTML = "You will be shown a piece of evidence we found to either confirm or refute the statement made."
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
				sentence_done.push(randomElement)
				console.log(sentence_done.length)
				if (sentences[randomElement]['ground_truth'] == true)
				{
					truth_count += 1
					document.cookie = "truth_count="+truth_count;
					console.log("True Statement "+ truth_count)
					if (truth_count == 2){
						block_statement = true
					}
				}
				else
				{
					false_count += 1
					console.log("False Statement "+ false_count)
					document.cookie = "false_count="+false_count;
					if (false_count == 2){
						block_statement = false
					}
				}
				while ((randomElement == null || sentence_done.includes(randomElement) || sentences[randomElement]['ground_truth'] == block_statement) && sentence_done.length != 12)
					{
					randomElement = total_sentences[Math.floor(Math.random() * total_sentences.length)];
					}
				count += 1
				document.getElementById("levelInstruction").style.display = "none";
				console.log("Count:", count)
				if (count % 4 == 0){

					console.log('Moving to Feedback Page')
					
					if (experiment_level[global_level] == 1){
						window.location.replace("https://www.getfactcheck.me/feedback_1");
					}
					else if (experiment_level[global_level] == 5){
						window.location.replace("https://www.getfactcheck.me/feedback_2");
					}
					else if (experiment_level[global_level] == 3){
						window.location.replace("https://www.getfactcheck.me/feedback_3");
					}
					else {
						window.location.replace("https://www.getfactcheck.me/feedback_4");
					}
					console.log("Moving to next level")
					global_level += 1
					document.cookie = "experiment_stage="+global_level;
					document.cookie = "false_count="+0;
					document.cookie = "truth_count="+0;
					
			}
			document.getElementById("experimentSentences").innerHTML = sentences[randomElement]['sentence']+"<br>"
			document.cookie = "fact_check="+false;
			document.cookie = "sentence_count="+count;
			document.cookie = "sentence_done="+JSON.stringify(sentence_done)

				
				}}
		);
