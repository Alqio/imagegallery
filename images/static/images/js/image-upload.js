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
        console.log("File:" + file + ", name: " + file.name + ", type: " + file.type);
		// xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
        
        var url = "/sign_s3?file_name=" + file.name + "&file_type=" + file.type

		$.getJSON(url, function(data) {
	        console.log("success JEE");
            console.log(data);
    	});
        
        // TÄHÄN URLIIN KANS ALKUOSA DOMAINISTA (WINDOW.LOCATION)
        $.ajax({
            url: url,
            type: "get",
			dataType: "json"
        }).done(function(data) {
            console.log("SUCCESS, S3_SIGNED.");
            var response = JSON.parse(data);
            console.log(response);
            uploadFile(file, response.data, response.data);
        }).fail(function(request, status, error) {
        	console.log("request: " + request + ", status: " + status + ", error: " + error);

            console.log("get request to " + url + " failed.");
        });

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
