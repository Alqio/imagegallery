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
    $("#id_pic").change(function(){
        var files = document.getElementById("id_pic").files;
        var file = files[0];
        if (!file) {
            console.log("no file selected");
        }


        getSignedRequest(file);

    });

    $("#nappi").click(function(){
        var files = document.getElementById("id_pic").files;
        var file = files[0];

        getSignedRequest(file);
    });

    function getSignedRequest(file) {
        console.log("File:" + file + ", name: " + file.name + ", type: " + file.type);
        
        var url = "/sign_s3?file_name=" + file.name + "&file_type=" + file.type

        $.ajax({
            url: url,
            type: "get",
			dataType: "json"
        }).done(function(data) {
            console.log("SUCCESS, S3_SIGNED.");
            console.log(data);
            uploadFile(file, data.data,  data.url);
        }).fail(function(request, status, error) {
            console.log("get request to " + url + " failed.");
        });

    }

    function uploadFile(file, s3Data, url){
		var postData = new FormData();

        console.log(s3Data);
 
		for(key in s3Data.fields){
			postData.append(key, s3Data.fields[key]);
		}

		postData.append('file', file);

        $.ajax({
            type: "POST",
            url: s3Data['url'],
            data: postData,
            processData: false,
            contentType: false,
        }).done(function(data){
			document.getElementById("image-url").value = url;
            console.log("successfully uploaded file.");
        }).fail(function(request, status, error) {
            console.log("failed to post data to " + s3Data['url']);
            console.log("request: " + request + ", status: " + status + ", error: " + error);
        });

	}

});
