// ✅ Declare these at the very top — globally
let adultPrice = 0;
let childPrice = 0;
let adultCountDisplay;
let childCountDisplay;

document.addEventListener("DOMContentLoaded", function () {
  adultPrice = parseFloat(document.getElementById("adultPriceText").getAttribute("data-price"));
  childPrice = parseFloat(document.getElementById("childPriceText").getAttribute("data-price"));
});


document.addEventListener("DOMContentLoaded", function () {
  const calendarBtn = document.getElementById("calendarBtn");
  const selectedDateText = document.getElementById("selectedDate");
  const hiddenDateInput = document.getElementById("hiddenDate");

  const timeBtn = document.getElementById("timeBtn");
  const selectedTime = document.getElementById("selectedTime");
  const timeDropdown = document.getElementById("timeDropdown");




  let calendarOpen = false;

  

  // ✅ Flatpickr Calendar Initialization
  const fp = flatpickr(hiddenDateInput, {
    dateFormat: "Y-m-d",
    defaultDate: new Date(),
    minDate: "today",
    appendTo: document.querySelector(".calendar-wrapper"),
    onChange: function (selectedDates, dateStr, instance) {
      const formatted = instance.formatDate(selectedDates[0], "d M Y");
      selectedDateText.textContent = formatted;

      // 👇 Save actual value in hidden input for Django
      hiddenDateInput.value = dateStr;
      fp.close(); // Close calendar after selection
    },
    onOpen: function () {
      calendarOpen = true;
    },
    onClose: function () {
      calendarOpen = false;
    }
  });

  // ✅ Toggle calendar when clicking the calendar button
  calendarBtn.addEventListener("click", function (e) {
    e.preventDefault();
    e.stopPropagation();
    calendarOpen ? fp.close() : fp.open();
  });

  // ✅ Toggle time dropdown
  timeBtn.addEventListener("click", function (e) {
    e.preventDefault();
    e.stopPropagation();
    timeDropdown.classList.toggle("show");
  });

  // ✅ Select a time from the dropdown
  document.querySelectorAll(".time-option").forEach(option => {
    option.addEventListener("click", function () {
      const time = this.textContent;
      selectedTime.textContent = time;
      timeDropdown.classList.remove("show");
    });
  });

  // ✅ Close dropdowns when clicking outside
  document.addEventListener("click", function (e) {
    if (calendarOpen) fp.close();
    if (!timeBtn.contains(e.target) && !timeDropdown.contains(e.target)) {
      timeDropdown.classList.remove("show");
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const fullNameInput = document.getElementById("fullName");
  const emailInput = document.getElementById("email");
  const phoneInput = document.getElementById("phoneNumber");
  const paymentBtn = document.querySelector(".payment-btn");

  // ✅ Fix: Assign the count displays
  adultCountDisplay = document.getElementById("adultCount");
  childCountDisplay = document.getElementById("childCount");

  let adultCount = 1;
  let childCount = 0;
  
  function updateTotalPrice() {
    const total = (adultCount * adultPrice) + (childCount * childPrice);
    document.querySelector('.total-label').textContent = `Total Price : RM ${total.toFixed(2)}`;
  }
  

  // Update counter display
  function updateCountDisplay(type) {
    if (type === 'adult') {
      adultCountDisplay.textContent = adultCount;
    } else {
      childCountDisplay.textContent = childCount;
    }
    updateTotalPrice();
  }
  
  // Counter Buttons
  document.querySelectorAll(".counter button").forEach((btn) => {
    btn.addEventListener("click", function () {
      const type = this.closest(".traveller-box").querySelector(".traveller-type").textContent.toLowerCase();
      if (this.textContent === "+" || this.textContent === "＋") {
        if (type === "adult") adultCount++;
        if (type === "child") childCount++;
      } else {
        if (type === "adult" && adultCount > 1) adultCount--;
        if (type === "child" && childCount > 0) childCount--;
      }
      updateCountDisplay(type);
    });
  });

  // Input validation
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
  

  // Live Validation
  fullNameInput.addEventListener("input", () => {
    validateField(fullNameInput, validateName, "fullNameError", "Please enter a valid name (letters only)");
  });

  emailInput.addEventListener("input", () => {
    validateField(emailInput, validateEmail, "emailError", "Please enter a valid email");
  });

  phoneInput.addEventListener("input", () => {
    validateField(phoneInput, validatePhone, "phoneError", "Phone must be digits (7–15)");
  });

  paymentBtn.addEventListener("click", function (e) {
    e.preventDefault();
  
    const validName = validateField(fullNameInput, validateName, "fullNameError", "Please enter a valid name (letters only)");
    const validEmail = validateField(emailInput, validateEmail, "emailError", "Please enter a valid email");
    const validPhone = validateField(phoneInput, validatePhone, "phoneError", "Phone must be digits (7–15)");
    const isHotelRequired = document.getElementById("hotelSearch") !== null;
    const validHotel = !isHotelRequired || validateHotel();  // ✅ Only validate if field exists
  
    if (validName && validEmail && validPhone && adultCount >= 1 && validHotel) {
      // ✅ All validations passed
      fetch('/create-checkout-session/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
          full_name: document.getElementById("fullName").value,
          email: document.getElementById("email").value,
          phone: document.getElementById("phoneNumber").value,
          hotel_address: document.getElementById("hotelSearch") ? document.getElementById("hotelSearch").value : "{{ transfer.pickup_location }}",
          pickup_map_url: document.getElementById("pickupMapUrl") ? document.getElementById("pickupMapUrl").value : "",
          
          from_city: "{{ from_city }}",
          to_city: "{{ to_city }}",
          adults: adultCount,
          children: childCount,
          date: document.getElementById("hiddenDate").value,
          transfer_id: parseInt(document.getElementById("transferId").value),



          time: document.getElementById("selectedTime").textContent,
          adult_price: adultPrice * 100,
          child_price: childPrice * 100,
        
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
      if (adultCount < 1) {
        alert("Please select at least 1 adult.");
      }
    }
  });
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
