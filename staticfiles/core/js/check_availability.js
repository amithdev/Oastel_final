document.addEventListener("DOMContentLoaded", function () {
    const calendarBtn = document.getElementById("calendarBtn");
    const selectedDateSpan = document.getElementById("selectedDate");
    const availabilityMessage = document.getElementById("availabilityMessage");
    const hiddenDateInput = document.getElementById("hiddenDate");
    const proceedToPaymentButton = document.getElementById("payButton");

    const tourType = document.getElementById("tourType")?.value; // 'private' or 'featured'
    const tourSlug = document.getElementById("tourSlugInput")?.value;
    const isTransfer = document.getElementById("is_transfer")?.value === "true";
    const transferId = document.getElementById("transferIdInput")?.value;
  
    const fp = flatpickr(hiddenDateInput, {
      minDate: "today",
      onChange: function (selectedDates, dateStr) {
        selectedDateSpan.textContent = selectedDates[0].toDateString();
        availabilityMessage.innerHTML = "⏳ Checking...";
  
        let payload = {
          date: dateStr,
          is_transfer: isTransfer,
          tour_slug: tourSlug,
          tour_type: tourType,
        };
  
        if (isTransfer) {
          payload.transfer_id = transferId;
        } else {
          payload.tour_slug = tourSlug;
          payload.tour_type = tourType;
        }
  
        fetch("/check-availability/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify(payload),
        })
          .then((res) => res.json())
          .then((data) => {
            const slotStatus = document.getElementById("availabilityMessage");
            const payButton = document.getElementById("payButton");
            const selectedTime = document.getElementById("selectedTime");
            const timeBtn = document.getElementById("timeBtn");
          
            if (data.available) {
              slotStatus.innerHTML = "<span style='color:green'>✅ Slot is available</span>";
              payButton.disabled = false;
              slotAvailable = true;  // ✅ THIS IS CRUCIAL
          
              if (data.start_time) {
                selectedTime.textContent = data.start_time;
                timeBtn.disabled = false;
              }
            } else {
              let message = "<span style='color:red'>❌ Slot is not available</span>";
              if (data.next_available) {
                message += `<br><span style="color:gray;">Next available: ${data.next_available}</span>`;
              }
              slotStatus.innerHTML = message;
          
              payButton.disabled = true;
              timeBtn.disabled = true;
              selectedTime.textContent = "Select Time";
              slotAvailable = false;  // ❌ Disable
            }
          });
          
          
      },
    });
  
    calendarBtn.addEventListener("click", function () {
      fp.open();
    });
  
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });
  