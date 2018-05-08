$(document).ready(function() {
    
    var pswpElement = document.querySelectorAll('.pswp')[0];
    
    var options = {
        index: 0,
		barsSize: {top:44, bottom:0},
        addCaptionHTMLFn: function(item, captionEl, isFake) {
            captionEl.children[0].innerHTML = item.title + "<br/><small>" + item.description + "</small>";
            return true;
        }
    }
    var album_id = $('#album-id').text(); 
    
    console.log("/api/album/" + album_id + "/");
    
    var items = [];

    $.getJSON("/api/album/" + album_id + "/", function(data) {
        console.log("ITEMS: ");
        data["results"].forEach(function(list_item) {
            console.log(list_item["image"]);
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
        console.log("all items pushed.");
        console.log("request done!");
        console.log(items);
    });



    $(".img-description-layer").click(function() {
        var parent = $(this).parent();

        let image_id = parent.find(".image-id").text();
        options["index"] = parseInt(image_id);
        console.log("image_id: " + image_id);
        
        var gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
        gallery.init();
        console.log("gallery inited!");
    });
    
    

});

