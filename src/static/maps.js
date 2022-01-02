function initMap(){
    const centerLatLgn = {lat: 39.582076, lng: -96.4617602}
    const myLatLgn1 = {lat: 40.3573, lng:-74.6672}
    const myLatLgn2 = {lat: 41.3573, lng:-79.6672}
    var options = {
        zoom:4.1,
        center: centerLatLgn
    };
    var map = new google.maps.Map(document.getElementById('map'), options);
    new google.maps.Marker({
        position: myLatLgn1,
        map,
        title: "Marker1",
    });
    new google.maps.Marker({
        position: myLatLgn2,
        map,
        title: "Marker2",
    })
}