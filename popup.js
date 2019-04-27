function getText() {
chrome.tabs.executeScript( {
	code: "window.getSelection().toString();"
}, function(selection) {
	document.getElementById("sentence").innerHTML = selection[0];
});
}

document.getElementById('fact_check').addEventListener('click',getText);

