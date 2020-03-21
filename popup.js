// dynamic changing of html content
var level_value;
function getCookies() 
    {
        chrome.cookies.get({"url": "https://www.getfactcheck.me", "name": "level"}, function(cookie) {
			if (cookie == null){
				level_value = 2;
			}
			else
			{
			level_value = cookie.value;
			}
			chrome.storage.sync.set({level: level_value})
			console.log("Level Value set as", level_value)
			document.getElementById('login').style.display = "none";
			if (level_value == 3)
				{
				document.getElementById('level3experiment').style.display = "block";
				}
			else
				{
				document.getElementById('experiment').style.display = "block";
				}	
        });
	}
	
function start(){
	chrome.storage.sync.get('signed_in', function(data){
		console.log("The current value is:", data.signed_in)
	});
	chrome.storage.sync.get('signed_in', function(data) {
    if (data.signed_in) {
		getCookies();
		
	} 
	else {
		document.getElementById('login').style.display = "inline-block";
		document.getElementById('experiment').style.display = "none";
		document.getElementById('level3experiment').style.display = "none";

    }
  });
}
start();
document.getElementById('myRange').addEventListener("change", function() {
    document.getElementById("sliderValue").textContent = document.getElementById('myRange').value;
}, false);
document.getElementById('myRange_3').addEventListener("change", function() {
    document.getElementById("sliderValue_3").textContent = document.getElementById('myRange_3').value;
}, false);
// Retrieving Selected Text and calling the API for the response  
function getText() {
chrome.tabs.executeScript( {
	code: "window.getSelection().toString();"
}, function(selection) {
	if (selection == "" || selection == null){
	document.getElementById("error").innerHTML = "Please select a sentence to fact check";
	}
	else{
	// Add loading animation
	const div = document.createElement('div');
	div.setAttribute("id","loader");
	div.setAttribute("class","loader");
	document.body.appendChild(div);

	// making fact check button invisible
	document.getElementById("fact_check").style.display='none'
	document.getElementById("logout_button").style.display='none'
	document.getElementById("fact_check_3").style.display='none'
	chrome.storage.sync.get('level', function(data){
	
	// sending request to the server
	var level_data = data.level;
	console.log("Sending request for level", level_data)
	var raw = JSON.stringify({"level":level_data});
	var requestOptions = {
  	method: 'POST',
  	headers: {
		"Content-Type": "application/json",
	},
  	body: raw
	};
	url='https://www.getfactcheck.me/index?sentence='.concat(selection[0])
	fetch(url, requestOptions)
	.then(function(response) {
		if (response.status != 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			document.getElementById("loader").remove();
			document.getElementById("error").innerHTML = "Oops! Something went wrong!";
			return;
		}

		response.json().then(function(data) {
			if (level_data == 3){
				document.getElementById("loader").remove();
				// document.getElementById("fact_check_3").style.visibility='visible';
				document.getElementById("claim_3").innerHTML = "Claim: "+data.claim;
				document.getElementById("evidence_support").style.display='block';
				ul = document.getElementById("support")
				console.log(data)
				for (var i = 0; i < data.SUPPORTS.length; i++) {
					var evidence_item = data.SUPPORTS[i][2];
					var prediction_score = data.SUPPORTS[i][1];
					var listItem = document.createElement("li");
					listItem.style.marginBottom = "6px";
					listItem.innerHTML = evidence_item + "<br><b>Prediction Score:</b> " + (Math.exp(prediction_score) / (Math.exp(prediction_score)+1)*100).toFixed(2) +"%";
					ul.appendChild(listItem);
				}
				document.getElementById("evidence_refutes").style.display='block';
				ul = document.getElementById("refutes")
				if (data.REFUTES.length == 0){
					var listItem = document.createElement("li");
					listItem.style.marginBottom = "6px";
					listItem.innerHTML = "NONE";
					ul.appendChild(listItem);
				}
				for (var i = 0; i < data.REFUTES.length; i++) {
					var evidence_item = data.REFUTES[i][2];
					var prediction_score = data.REFUTES[i][1];
					var listItem = document.createElement("li");
					listItem.style.marginBottom = "6px";
					listItem.innerHTML = evidence_item + "<br><b>Prediction Score:</b> " + (Math.exp(prediction_score) / (Math.exp(prediction_score)+1)*100).toFixed(2);
					ul.appendChild(listItem);
				}
				document.getElementById("feedback_3").style.display='inline-block';

				
			}
			else{
			document.getElementById("loader").remove();
			// document.getElementById("fact_check").style.visibility='visible';
			// document.getElementById("logout_button").style.visibility='visible';
			document.getElementById("evidence_head").style.display='inline-block';
			document.getElementById("claim").innerHTML = "Claim: "+data.claim;

			// Populating Evidences List
			var ul = document.querySelector("ul");
			var evidence_count = 0;
			if (level_data == 1 && data.evidence.length > 1){
				evidence_count = 1;
			}
			else if (level_data == 2 && data.evidence.length >= 3){
				evidence_count = 3;	
			}
			else 
			{
				evidence_count = data.evidence.length;
			}
			for (var i = 0; i < evidence_count; i++) {
				var evidence_item = data.evidence[i];
				var listItem = document.createElement("li");
				listItem.textContent = evidence_item;
				ul.appendChild(listItem);
			}
		
			if (level_data != 4)
		{
			document.getElementById("error").innerHTML = "Result: "+data.label;
		}
			document.getElementById("feedback").style.display='inline-block';

		}});
	});
	});

	}});
}

function sendFeedback(){
	chrome.storage.sync.get(['level','p_id','p_age'], function(data){
		if (data.level == 3) {
			var payload = {}
	payload = {
		id: data.p_id,
		p_age: data.p_age,
		sentence:document.getElementById('claim_3').innerHTML,
		level: data.level,
		"satisfaction_value": document.getElementById('myRange_3').value,
		"trust_value": document.getElementById('trustRange_3').value
	};
}
else{
	payload = {
		id: data.p_id,
		p_age: data.p_age,
		sentence:document.getElementById('claim').innerHTML,
		level: data.level,
		"satisfaction_value": document.getElementById('myRange').value,
		"trust_value": document.getElementById('trustRange').value
	};
}
	url='https://www.getfactcheck.me/sendFeedback'
	fetch(url, {
		method:'post',
		headers: {
			'Content-Type': 'application/json'
		  },
		body: JSON.stringify(payload)
	}).then(function(response) {
		if (response.status == 200) {
			if (data.level ==3){
			document.getElementById('thanks_3').innerHTML = "Thanks for the feedback!"		}
			else {
				document.getElementById('thanks').innerHTML = "Thanks for the feedback!"
			}
		}
	
		}
		);
});
}

document.getElementById('submitFeedback').addEventListener('click', sendFeedback)
document.getElementById('submitFeedback_3').addEventListener('click', sendFeedback)
// document.getElementById('thumbsUp').addEventListener('click', sendUpFeedback);
// document.getElementById('thumbsDown').addEventListener('click', sendDownFeedback);
// document.getElementById('thumbsUp_3').addEventListener('click', sendUpFeedback);
// document.getElementById('thumbsDown_3').addEventListener('click', sendDownFeedback);
// click events
document.getElementById('fact_check').addEventListener('click',getText);
document.getElementById('fact_check_3').addEventListener('click',getText);

document.getElementById('level1').addEventListener('click', function(){
	document.getElementById('level').style.display = "none";
	document.getElementById('experiment').style.display = "block";
	chrome.storage.sync.set({level: 1})

});
document.getElementById('level2').addEventListener('click', function(){
	document.getElementById('level').style.display = "none";
	document.getElementById('experiment').style.display = "block";
	chrome.storage.sync.set({level: 2})

});
document.getElementById('level3').addEventListener('click', function(){
	document.getElementById('level').style.display = "none";
	document.getElementById("level3experiment").style.display='block'
	chrome.storage.sync.set({level: 3})

});
document.getElementById('level4').addEventListener('click', function(){
	document.getElementById('level').style.display = "none";
	document.getElementById('experiment').style.display = "block";
	chrome.storage.sync.set({level: 4})

});
document.getElementById('login_button').addEventListener("click", function(){
	chrome.storage.sync.set({signed_in: true})
	pid = document.getElementById('pid').value;
	age = document.getElementById('age').value;
	console.log("PID and AGE are:", pid, age);

	if (pid == "" || pid == null){
		document.getElementById('pid').focus();
	}
	else if (age == "" || age == null){
		document.getElementById('age').focus();
	}
	else{

	chrome.storage.sync.set({p_id: pid})
	chrome.storage.sync.set({p_age: age})
	// var payload = {
	// 	_id: pid,
	// 	p_age: age
	// };
	start();
	// url='https://www.getfactcheck.me/addUser'
	// fetch(url, {
	// 	method:'post',
	// 	headers: {
	// 		'Content-Type': 'application/json'
	// 	  },
	// 	body: JSON.stringify(payload)
	// }).then(function(response) {
	// 	if (response.status == 200) {
	// 		start();		
	// 	}
	
	// 	}
	// 	);
	}
});
document.getElementById("logout_button").addEventListener('click', function(){
	chrome.storage.sync.set({signed_in: false})
	start();
});


