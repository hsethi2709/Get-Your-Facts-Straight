import Mercury from '@postlight/mercury-parser';
// function getURL(){
//	chrome.tabs.query({'active': true, 'currentWindow': true}, function(tabs) {
	//	var url = tabs[0].url;
		//console.log(url);
	//});

	//}

function getParsedPage() {
	Mercury.parse().then(result => console.log(result));
}
	
document.getElementById("fact_check").addEventListener('click', getParsedPage());