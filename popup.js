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
	url='https://45.113.232.191//index?sentence='.concat(selection[0])
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
			//document.getElementById("sentence").innerHTML = "Message Received:"+data.evidence;

		});
	});
	}});
}

document.getElementById('fact_check').addEventListener('click',getText);

