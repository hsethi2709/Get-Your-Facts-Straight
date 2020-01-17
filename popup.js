// dynamic changing of html content
function start(){
	chrome.storage.sync.get('signed_in', function(data){
		console.log("The current value is:", data.signed_in)
	});
	chrome.storage.sync.get('signed_in', function(data) {
    if (data.signed_in) {
		document.getElementById('login').style.display = "none";
		document.getElementById('level').style.display = "block";
		
    } else {
		document.getElementById('login').style.display = "block";
		document.getElementById('level').style.display = "none";

    }
  });
}
start();
console.log(pid)
// Retrieving Selected Text and calling the API for the response  
function getText() {
chrome.tabs.executeScript( {
	code: "window.getSelection().toString();"
}, function(selection) {
	if (selection == "" || selection == null){
	document.getElementById("sentence").innerHTML = "Please select a sentence to fact check";
	}
	else{

	// Add loading animation
	const div = document.createElement('div');
	div.setAttribute("id","loader");
	div.setAttribute("class","loader");
	document.body.appendChild(div);

	// making fact check button invisible
	document.getElementById("fact_check").style.visibility='hidden'
	url='http://www.getfactcheck.me/index?sentence='.concat(selection[0])
	fetch(url)
	.then(function(response) {
		if (response.status !== 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			return;
		}

		response.json().then(function(data) {
			document.getElementById("loader").remove();
			document.getElementById("fact_check").style.visibility='visible'
			document.getElementById("evidence_head").style.visibility='visible'

			const evidence_div = document.createElement('ul')
			evidence_div.setAttribute("id", "evidence")
			document.getElementById("claim").innerHTML = "Claim: "+data.claim;
			var ul = document.querySelector("ul");
			for (var i = 0; i < data.evidence.length; i++) {
				var evidence_item = data.evidence[i];
				var listItem = document.createElement("li");
				listItem.textContent = evidence_item;
				ul.appendChild(listItem);
			}
			document.getElementById("sentence").innerHTML = "Result: "+data.label;
			document.getElementById("feedback").style.display='block';

		});
	});
	}});
}

// click events
document.getElementById('fact_check').addEventListener('click',getText);
document.getElementById('level1').addEventListener('click', function(){
	document.getElementById('level').style.display = "none";
	document.getElementById('experiment').style.display = "block";
	document.getElementById('feedback').style.display = "block";
});
document.getElementById('login_button').addEventListener("click", function(){
	chrome.storage.sync.set({signed_in: true})
	pid = document.getElementById('pid').value;
	age = document.getElementById('age').value;
	console.log("PID and AGE are:", pid, age)
	if (pid == "" || pid == null){
		document.getElementById('pid').focus();
	}
	else if (age == "" || age == null){
		document.getElementById('age').focus();
	}
	else{
	chrome.storage.sync.set({p_id: pid})
	chrome.storage.sync.set({p_age: age})
	url='http://www.getfactcheck.me/addUser'
	fetch(url, {
		method:'post',
		body: JSON.stringify({p_id: pid, p_age:age })
	})
	.then(function(response) {
		if (response.status !== 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			return;
		}
	start();
	}
  });
document.getElementById("logout_button").addEventListener('click', function(){
	chrome.storage.sync.set({signed_in: false})
	start();
});