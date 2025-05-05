window.initAutocomplete = function () {
    const input = document.getElementById("hotelSearch");
    const mapUrlInput = document.getElementById("pickupMapUrl");
    const mapContainer = document.getElementById("hotelMapContainer");
  
    const autocomplete = new google.maps.places.Autocomplete(input, {
      types: ["establishment"],
      componentRestrictions: { country: "MY" },
    });
  
    autocomplete.addListener("place_changed", function () {
      const place = autocomplete.getPlace();
  
      // ✅ Set formatted address or name
      input.value = place.formatted_address || place.name;
  
      if (place.place_id) {
        // ✅ Save map link to hidden field for backend
        const mapUrl = `https://www.google.com/maps/place/?q=place_id:${place.place_id}`;
        mapUrlInput.value = mapUrl;
  
        // ✅ Show embedded map
        mapContainer.innerHTML = `
          <iframe 
            width="100%" 
            height="200" 
            style="border:0; border-radius: 8px; margin-top: 10px;"
            loading="lazy"
            allowfullscreen
            referrerpolicy="no-referrer-when-downgrade"
            src="https://www.google.com/maps/embed/v1/place?key=AIzaSyCth5rYzXAhrYyTrxZnIuzMPb9sMqSEd44&q=place_id:${place.place_id}">
          </iframe>
        `;
      }
  
      // Clear suggestion dropdown if any (not required with Maps Autocomplete but safe)
      const suggestionBox = document.getElementById("hotelSuggestions");
      if (suggestionBox) suggestionBox.innerHTML = "";
    });
  };
  