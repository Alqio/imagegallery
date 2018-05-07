var pswpElement = document.querySelectorAll('.pswp')[0];

function get_items(album_id) {
    console.log("ITEMS: ");
    console.log("/api/album/" + album_id + "/");

    $.getJSON("/api/album/" + album_id + "/", function(data) {
        console.log("get went through");
        let items = [];
        //console.log(data['results']);
        data["results"].forEach(function(list_item) {
            console.log(list_item["image"]);
            let image = {};
            let item = list_item["image"];
            image["src"] = item["pic"];
            image["width"] = item["width"];
            image["height"] = item["height"];
            image["title"] = item["name"];
            
            items.push(image);

        });
        return items;
    });
}

let items = get_items(1);

console.log("ITEMS FINISHED:");
console.log(items);

