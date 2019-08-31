function getText() {
chrome.tabs.executeScript( {
	code: "window.getSelection().toString();"
}, function(selection) {

	url='http://localhost:5000/index?sentence='.concat(selection[0])
	fetch(url)
	.then(function(response) {
		if (response.status !== 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			return;
		}

		response.json().then(function(data) {
			document.getElementById("sentence").innerHTML = data['message'];
		});
	});
});
}

document.getElementById('fact_check').addEventListener('click',getText);

