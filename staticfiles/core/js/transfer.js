document.addEventListener('DOMContentLoaded', () => {
  const calendarInput = document.getElementById("customDateInput");
  const calendar = document.getElementById("customCalendar");

  // 🟩 Make these GLOBAL to track current state
  let currentMonth = new Date().getMonth();
  let currentYear = new Date().getFullYear();

  function generateCalendar(month, year) {
    const now = new Date();
    const today = now.getDate();
    const todayMonth = now.getMonth();
    const todayYear = now.getFullYear();

    const daysInMonth = new Date(year, month + 1, 0).getDate();

    let calendarHTML = `
      <div class="calendar-header">
        <button id="prevMonth">&lt;</button>
        <span id="monthYear">${new Date(year, month).toLocaleString('default', { month: 'long' })} ${year}</span>
        <button id="nextMonth">&gt;</button>
      </div>
      <table><tr>`;

    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    days.forEach(day => calendarHTML += `<th>${day}</th>`);
    calendarHTML += '</tr><tr>';

    const firstDay = new Date(year, month, 1).getDay();
    for (let i = 0; i < firstDay; i++) {
      calendarHTML += '<td class="disabled"></td>';
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const thisDate = new Date(year, month, day);
      const isPast = thisDate < new Date(todayYear, todayMonth, today);
      calendarHTML += `<td class="${isPast ? 'disabled' : 'selectable'}">${day}</td>`;
      if ((firstDay + day) % 7 === 0) calendarHTML += '</tr><tr>';
    }

    calendarHTML += '</tr></table>';
    calendar.innerHTML = calendarHTML;

    // ✅ Add event listeners to the new buttons
    document.getElementById("prevMonth").addEventListener("click", (e) => {
      e.stopPropagation();
    
      if (currentMonth === 0) {
        currentMonth = 11;
        currentYear--;
      } else {
        currentMonth--;
      }
      generateCalendar(currentMonth, currentYear);
    });

    document.getElementById("nextMonth").addEventListener("click", (e) => {
      e.stopPropagation();
    
      if (currentMonth === 11) {
        currentMonth = 0;
        currentYear++;
      } else {
        currentMonth++;
      }
      generateCalendar(currentMonth, currentYear);
    });

    // ✅ Add click listeners for dates
    calendar.querySelectorAll(".selectable").forEach(cell => {
      cell.addEventListener("click", () => {
        calendarInput.value = `${cell.innerText} ${new Date(currentYear, currentMonth).toLocaleString('default', { month: 'short' })} ${currentYear}`;
        calendar.style.display = "none";
      });
    });
  }

  // Show calendar on input click
  document.querySelector(".calendar-wrapper").addEventListener("click", () => {
    calendar.style.display = calendar.style.display === "block" ? "none" : "block";
    generateCalendar(currentMonth, currentYear);
  });

  document.addEventListener("click", e => {
    const calendarWrapper = document.querySelector(".calendar-wrapper");
  
    // Don't hide if clicking inside calendar or on nav buttons
    const isInsideCalendar = calendarWrapper.contains(e.target);
    const isNavButton = e.target.id === "prevMonth" || e.target.id === "nextMonth";
  
    if (!isInsideCalendar && !isNavButton) {
      calendar.style.display = "none";
    }
  });
  
});
document.addEventListener("DOMContentLoaded", function () {
  const fromWrapper = document.getElementById("fromInputWrapper");
  const fromInput = document.getElementById("fromInput");
  const fromDropdown = document.getElementById("fromDropdown");

  const toWrapper = document.getElementById("toInputWrapper");
  const toInput = document.getElementById("toInput");
  const toDropdown = document.getElementById("toDropdown");

  // Show/hide FROM dropdown
  fromWrapper.addEventListener("click", function (e) {
    e.stopPropagation();
    fromDropdown.classList.toggle("show");
  });

  // FROM item selection
  document.querySelectorAll("#fromDropdown .dropdown-item").forEach(item => {
    item.addEventListener("click", function (e) {
      e.stopPropagation();
      const selectedCity = this.textContent;

      if (selectedCity === toInput.value) {
        fromWrapper.classList.add("shake");
        setTimeout(() => fromWrapper.classList.remove("shake"), 500);
        return;
      }

      fromInput.value = selectedCity;
      fromDropdown.classList.remove("show");
    });
  });

  // Show/hide TO dropdown
  toWrapper.addEventListener("click", function (e) {
    e.stopPropagation();
    toDropdown.classList.toggle("show");
  });

  // TO item selection
  document.querySelectorAll("#toDropdown .dropdown-item").forEach(item => {
    item.addEventListener("click", function (e) {
      e.stopPropagation();
      const selectedCity = this.textContent;

      if (selectedCity === fromInput.value) {
        toWrapper.classList.add("shake");
        setTimeout(() => toWrapper.classList.remove("shake"), 500);
        return;
      }

      toInput.value = selectedCity;
      toDropdown.classList.remove("show");
    });
  });

  // Close both dropdowns on outside click
  document.addEventListener("click", function () {
    fromDropdown.classList.remove("show");
    toDropdown.classList.remove("show");
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const searchBtn = document.querySelector(".search-btn");
  const fromInput = document.getElementById("fromInput");
  const toInput = document.getElementById("toInput");
  const dateInput = document.getElementById("customDateInput");

  const fromWrapper = document.getElementById("fromInputWrapper");
  const toWrapper = document.getElementById("toInputWrapper");
  const calendarWrapper = document.querySelector(".calendar-wrapper");

  searchBtn.addEventListener("click", function (e) {
    let hasError = false;

    if (fromInput.value.trim() === "") {
      fromWrapper.classList.add("shake");
      hasError = true;
      setTimeout(() => fromWrapper.classList.remove("shake"), 500);
    }

    if (toInput.value.trim() === "") {
      toWrapper.classList.add("shake");
      hasError = true;
      setTimeout(() => toWrapper.classList.remove("shake"), 500);
    }

    if (dateInput.value.trim() === "") {
      calendarWrapper.classList.add("shake");
      hasError = true;
      setTimeout(() => calendarWrapper.classList.remove("shake"), 500);
    }

    // prevent form submission or action if any field is empty
    if (hasError) {
      e.preventDefault();
    } else {
      console.log("Form is ready to submit");
      // You can trigger form submission or redirect here
    }
  });

  document.querySelector(".search-btn").addEventListener("click", function(e) {
    const fromVal = document.getElementById("fromInput").value;
    const toVal = document.getElementById("toInput").value;
    const dateVal = document.getElementById("customDateInput").value;
  
    if (!fromVal || !toVal || !dateVal) {
      alert("Please select all fields");
      e.preventDefault();
      return;
    }
  
    // Populate hidden form inputs
    document.getElementById("hiddenFrom").value = fromVal;
    document.getElementById("hiddenTo").value = toVal;
    document.getElementById("hiddenDate").value = dateVal;
  });
  
});