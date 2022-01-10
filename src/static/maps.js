function initMap(){
    const centerLatLgn = {lat: 39.582076, lng: -96.4617602}
    const data = JSON.parse(document.getElementById("helper").getAttribute('data'))
    console.log(data)
    

    var options = {
        zoom:4.1,
        center: centerLatLgn
    };
    

    var map = new google.maps.Map(document.getElementById('map'), options);
    var lineSymbol = {
        path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW
      };

    for (var i = 0; i < data.length; i++) {
        if (i == 0){
            new google.maps.Marker({
                position: {lat: parseFloat(data[i].x_coordinate), lng: parseFloat(data[i].y_coordinate)},
                map,
                title: "Marker ${location.id}",
                icon: 'https://maps.google.com/mapfiles/kml/paddle/blu-blank.png',
            });
        }
        else{
            new google.maps.Marker({
                position: {lat: parseFloat(data[i].x_coordinate), lng: parseFloat(data[i].y_coordinate)},
                map,
                title: "Marker ${location.id}",
            });
        }
    }
    for (var i = 0; i < data.length-1; i++) {
        var line = new google.maps.Polyline({
            path: [{lat: parseFloat(data[i].x_coordinate), lng: parseFloat(data[i].y_coordinate)}, {lat: parseFloat(data[i+1].x_coordinate), lng: parseFloat(data[i+1].y_coordinate)}],
            icons: [{
                icon: lineSymbol,
                offset: '100%'
                }],
            map: map
        });
        var line = new google.maps.Polyline({
            path: [{lat: parseFloat(data[data.length -1].x_coordinate), lng: parseFloat(data[data.length -1].y_coordinate)}, {lat: parseFloat(data[0].x_coordinate), lng: parseFloat(data[0].y_coordinate)}],
            icons: [{
                icon: lineSymbol,
                offset: '100%'
                }],
            map: map
        });
    }
}