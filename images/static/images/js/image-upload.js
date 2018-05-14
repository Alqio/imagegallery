$(document).ready(function() {
    $("#form-image").submit(function(event) {
        console.log("Image submitted");
        
        // django automatically gives id #id_pic to the file field
        var files = document.getElementById("id_pic").files;
        var file = files[0];

        if (!file) {
            console.log("no file selected");
        }

        getSignedRequest(file);
        
    });

    function getSignedRequest(file) {
        var xhr = new XMLHttpRequest();
		xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
		xhr.onreadystatechange = function(){
			if(xhr.readyState === 4){
				if(xhr.status === 200){
					var response = JSON.parse(xhr.responseText);
					uploadFile(file, response.data, response.url);
				} else{
                    console.log("Could not get signed URL. xhr.status: " + xhr.status);
                    
				}
			}

		};

		xhr.send();
    }

	function uploadFile(file, s3Data, url){
		var xhr = new XMLHttpRequest();
		xhr.open("POST", s3Data.url);

		var postData = new FormData();

		for(key in s3Data.fields){
			postData.append(key, s3Data.fields[key]);
		}

		postData.append('file', file);

		xhr.onreadystatechange = function() {
			if(xhr.readyState === 4){
		  		if(xhr.status === 200 || xhr.status === 204){
					console.log("Uploaded file");
		  		}else{
                    console.log("Could not upload file.");
		  		}
			}
		};

		xhr.send(postData);
	}


});
