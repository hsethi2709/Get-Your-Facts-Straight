var pid = 10;

function getPID()
{
    return (pid);
}

function log_in(){
	pid = document.getElementById('pid').value;
	age = document.getElementById('age').value;
	console.log("PID and AGE are:", pid, age);

	if (pid == "" || pid == null){
		document.getElementById('pid').focus();
	}
	else if (age == "" || age == null){
		document.getElementById('age').focus();
    }
    else
        {
        var payload = {
		_id: pid,
		p_age: age
	};
	url='https://www.getfactcheck.me/addUser'
	fetch(url, {
		method:'post',
		headers: {
			'Content-Type': 'application/json'
		  },
		body: JSON.stringify(payload)
	}).then(function(response) {
		if (response.status == 200) {
            window.location.replace("https://www.getfactcheck.me/pre");

		}
	        
		}
		);
        }
}
                                    
        
