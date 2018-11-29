function initMap() {
  const defaultCoordinates = {lat: 50.4501, lng: 30.5234};

  let map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
    center: defaultCoordinates
  });

  let geocoder = new google.maps.Geocoder();
  $(document).on('keyup', '#map-input', function() {
    const address = this.value;
    geocoder.geocode({'address': address}, function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
        if (status !== google.maps.GeocoderStatus.ZERO_RESULTS) {
          map.setCenter(results[0].geometry.location);
        } else {
          console.log('No results found')
        }
      } else {
        console.log('Geocode was not successful for the following reason: ' + status)
      }
    });
  });

  $.get('/mentor/mia_list/', (res) => {
    const addresses = res;

    function getGeo () {
      for (let addressObj of addresses) {
        let infowindow = new google.maps.InfoWindow({
          content:
            `<b>
            ${addressObj.address}
            <br>
            ТСЦ: ${addressObj.tsc_number}
            <br>
            Розклад: ${addressObj.schedule}
            <br>
            ${addressObj.phone_number_fax_str}
            <br>
            Email: ${addressObj.email}
            </b>`,
          size: new google.maps.Size(150, 50)
        });
        let marker = new google.maps.Marker({
          position: {lat: addressObj.lat, lng: addressObj.lng},
          map: map,
          title: addressObj.address
        });
        google.maps.event.addListener(marker, 'click', function () {
          infowindow.open(map, marker);
        });
      }
    }
    getGeo();
  });
}
