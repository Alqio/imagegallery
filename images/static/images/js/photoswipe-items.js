$(document).ready(function() {
    
    var pswpElement = document.querySelectorAll('.pswp')[0];
    
    var options = {
        index: 0,
		barsSize: {top:44, bottom:0},
        addCaptionHTMLFn: function(item, captionEl, isFake) {
            captionEl.children[0].innerHTML = "<h3>" + item.title + "</h3><br/><h5>" + item.description + "</h5>";
            return true;
        }
    }
    var album_id = $('#album-id').text(); 
    
    // console.log("/api/album/" + album_id + "/");
    
    var items = [];

    path = "/api/album/" + album_id + "/"
    if (album_id == "") {
        console.log("Could not find album id. Going to index instead.");
        path = "/api/index/";
    }

    $.getJSON(path, function(data) {
        // console.log("ITEMS: ");
        data["results"].forEach(function(list_item) {
            // console.log(list_item["image"]);
            let image = {};
            let item = list_item["image"];
		    let text = item["name"];

            image["src"] = item["pic"];
            image["w"] = item["width"];
            image["h"] = item["height"];
            image["title"] = text;
            image["description"] = item["description"];
            items.push(image);

        });
    });



    $(".img-description-layer").click(function() {
        var parent = $(this).parent();

        let image_id = parent.find(".image-id").text();
        options["index"] = parseInt(image_id);
        
        var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
        gallery.init();
        console.log("gallery inited!");
    });
    
    

});

