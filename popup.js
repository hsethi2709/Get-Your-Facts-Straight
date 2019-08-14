function getText() {
chrome.tabs.executeScript( {
	code: "window.getSelection().toString();"
}, function(selection) {

	url='http://localhost:5000/index?sentence='.concat(selection[0])
	fetch(url);
	document.getElementById("sentence").innerHTML = selection[0];
});
}

document.getElementById('fact_check').addEventListener('click',getText);

