 // ✅ Declare these globally at the top
 let adultPrice = 0;
 let childPrice = 0;
 let adultCountDisplay;
 let childCountDisplay;
 
 let adultCount = 1;    // ✅ Move outside and initialize
 let childCount = 0;    // ✅ Move outside and initialize
 
 let slotAvailable = false;  // ✅ already global
 
 // ✅ Smart minTravelers setup
 let minTravelersElement = document.getElementById("minTravelersInput");
 let minTravelers = minTravelersElement ? parseInt(minTravelersElement.value) || 1 : 1;
 
 document.addEventListener("DOMContentLoaded", function () {
   // ✅ Read the tour type early
   const tourType = document.getElementById('tourTypeInput')?.value || 'featured';
   const isPrivateTour = document.getElementById('is_private_tour')?.value === "true";
 
   // ✅ Prices
   adultPrice = parseFloat(document.getElementById("adultPriceText").getAttribute("data-price"));
   // Safely read child price only if available
   const childPriceTextElement = document.getElementById("childPriceText");
   childPrice = childPriceTextElement ? parseFloat(childPriceTextElement.getAttribute("data-price")) : 0;
 
   // ✅ Counter Displays
   adultCountDisplay = document.getElementById("adultCount");
   childCountDisplay = document.getElementById("childCount"); // Might be null
 
   let adultCount = minTravelers;  // Set adult count always to minTravelers
   let childCount = 0;
 
   function updateTotalPrice() {
     let total;
     if (isPrivateTour) {
       const groupMultiplier = adultCount / minTravelers;
       total = (groupMultiplier * adultPrice) + (childCount * childPrice);
     } else {
       total = (adultCount * adultPrice) + (childCount * childPrice);
     }
     document.querySelector('.total-label').textContent = `Total Price : RM ${total.toFixed(2)}`;
    }
 
   function updateCountDisplay(type) {
     if (type === 'adult' && adultCountDisplay) {
       adultCountDisplay.textContent = adultCount;
     } else if (type === 'child' && childCountDisplay) {
       childCountDisplay.textContent = childCount;
     }
     updateTotalPrice();
   }
 
   // ✅ Initialize Display
   updateCountDisplay('adult');
   updateCountDisplay('child');
 
   // ✅ Counter Button Actions
   document.querySelectorAll(".counter-btn").forEach((btn) => {
     btn.addEventListener("click", function () {
       const type = this.getAttribute("data-type"); // 'adult' or 'child'
 
       if (this.textContent.trim() === "+" || this.textContent.trim() === "＋") {
         if (type === "adult") {
           if (isPrivateTour) {
             adultCount += minTravelers; 
           } else {
             adultCount += 1;
           }
         } else if (type === "child") {
           childCount += 1;
         }
       } else {
         if (type === "adult") {
           if (isPrivateTour && adultCount > minTravelers) {
             adultCount -= minTravelers;
           } else if (!isPrivateTour && adultCount > minTravelers) {
             adultCount -= 1;
           }
         } else if (type === "child" && childCount > 0) {
           childCount -= 1;
         }
       }
 
       updateCountDisplay(type);
     });
   });
 
  


   const proceedToPaymentButton = document.getElementById("proceedToPaymentButton");

 
 
 
   // ✅ Form Validation
   const fullNameInput = document.getElementById("fullName");
   const emailInput = document.getElementById("email");
   const phoneInput = document.getElementById("phoneNumber");
   const paymentBtn = document.querySelector(".payment-btn");
 
   function validateName(name) {
     return /^[A-Za-z\s]+$/.test(name);
   }
 
   function validateEmail(email) {
     return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
   }
 
   function validatePhone(phone) {
     return /^\d{7,15}$/.test(phone);
   }
 
   function showError(input, message, errorId) {
     input.classList.add("invalid");
     document.getElementById(errorId).textContent = message;
   }
 
   function clearError(input, errorId) {
     input.classList.remove("invalid");
     document.getElementById(errorId).textContent = "";
   }
 
   function validateField(input, validatorFn, errorId, message) {
     const value = input.value.trim();
     if (!validatorFn(value)) {
       showError(input, message, errorId);
       return false;
     } else {
       clearError(input, errorId);
       return true;
     }
   }
 
   function getCookie(name) {
     let cookieValue = null;
     if (document.cookie && document.cookie !== '') {
       const cookies = document.cookie.split(';');
       for (let i = 0; i < cookies.length; i++) {
         const cookie = cookies[i].trim();
         if (cookie.substring(0, name.length + 1) === (name + '=')) {
           cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
           break;
         }
       }
     }
     return cookieValue;
   }
 
   // ✅ Live Validation
   fullNameInput.addEventListener("input", () => {
     validateField(fullNameInput, validateName, "fullNameError", "Please enter a valid name (letters only)");
   });
   emailInput.addEventListener("input", () => {
     validateField(emailInput, validateEmail, "emailError", "Please enter a valid email");
   });
   phoneInput.addEventListener("input", () => {
     validateField(phoneInput, validatePhone, "phoneError", "Phone must be digits (7–15)");
   });
 
   const hotelInput = document.getElementById("hotelSearch");
   const hotelError = document.getElementById("hotelError");
 
   function validateHotel() {
     const value = hotelInput ? hotelInput.value.trim() : '';
     if (hotelInput && value === "") {
       hotelInput.classList.add("invalid");
       hotelError.textContent = "Please select your hotel or pickup location.";
       return false;
     } else {
       hotelInput.classList.remove("invalid");
       hotelError.textContent = "";
       return true;
     }
   }
 
   function validateTime() {
     const selectedTime = document.getElementById("selectedTime").textContent.trim();
     return selectedTime !== "" && selectedTime !== "Select Time" && selectedTime !== "Select Date";
   }
   
 
   paymentBtn.addEventListener("click", function (e) {
     e.preventDefault();
   
     const validName = validateField(fullNameInput, validateName, "fullNameError", "Please enter a valid name (letters only)");
     const validEmail = validateField(emailInput, validateEmail, "emailError", "Please enter a valid email");
     const validPhone = validateField(phoneInput, validatePhone, "phoneError", "Phone must be digits (7–15)");
     const isHotelRequired = document.getElementById("hotelSearch") !== null;
     const validHotel = !isHotelRequired || validateHotel();
     const isTransfer = document.getElementById('is_transfer')?.value === 'true';
     const isPrivateTour = document.getElementById("is_private_tour")?.value === "true";
     
     const dateSelected = document.getElementById("hiddenDate").value;
     const timeSelected = validateTime();
   
     if (validName && validEmail && validPhone && adultCount >= 1 && validHotel && dateSelected && timeSelected && slotAvailable) {
       
       let finalAdultPrice;
       let finalChildPrice;
       let adultsToSend;
   
       if (isPrivateTour) {
         finalAdultPrice = adultPrice * 100;
         adultsToSend = Math.ceil(adultCount / minTravelers);
       } else {
         finalAdultPrice = adultPrice * 100;
         adultsToSend = adultCount;
       }
   
       finalChildPrice = childPrice * 100;
   
       fetch('/create-checkout-session/', {
   method: 'POST',
   headers: {
     'Content-Type': 'application/json',
     'X-CSRFToken': getCookie('csrftoken')
   },
   body: JSON.stringify({
     full_name: fullNameInput.value,
     email: emailInput.value,
     phone: phoneInput.value,
     hotel_address: hotelInput ? hotelInput.value : "",
     pickup_map_url: document.getElementById("pickupMapUrl")?.value || "",
 
     from_city: typeof from_city !== 'undefined' ? from_city : "",
     to_city: typeof to_city !== 'undefined' ? to_city : "",
     date: dateSelected,
     adults: adultsToSend,
     children: childCount,
     time: document.getElementById("selectedTime").textContent.trim(),
     adult_price: finalAdultPrice,
     child_price: finalChildPrice,
     is_transfer: isTransfer,
     is_private_tour: isPrivateTour,
     min_travelers: minTravelers,
     
     // ✅ ADD this 👇 to fix booking type issue!
     transfer_id: document.getElementById("transferIdInput")?.value || null, 
     tour_slug: document.getElementById("tourSlugInput")?.value || null,
   })
 })
 
       .then(response => response.json())
       .then(data => {
         if (data.sessionId) {
           return stripe.redirectToCheckout({ sessionId: data.sessionId });
         } else {
           console.error("Stripe session error:", data.error);
           alert("Failed to create checkout session.");
         }
       })
       .then(result => {
         if (result && result.error) {
           alert(result.error.message);
         }
       })
       .catch(error => {
         console.error('Error:', error);
         alert("Something went wrong. Please try again.");
       });
   
     } else {
       if (!slotAvailable) {
         alert("Selected date is not available. Please choose another date.");
       } else if (!dateSelected || !timeSelected) {
         alert("Please select a valid date and time.");
       } else {
         alert("Please complete all required fields correctly.");
       }
     }
   });
   })