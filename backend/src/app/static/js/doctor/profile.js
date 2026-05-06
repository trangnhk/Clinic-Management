document.addEventListener("DOMContentLoaded", () => {
    const doctorAvatar = document.getElementById("doctorAvatar");
    const doctorFullname = document.getElementById("doctorFullname");
    const doctorPhone = document.getElementById("doctorPhone");
    const doctorCode = document.getElementById("doctorCode");
    const doctorAddress = document.getElementById("doctorAddress");
    const doctorDob = document.getElementById("doctorDob");
    const doctorSpecialization = document.getElementById("doctorSpecialization");
    const doctorExperience = document.getElementById("doctorExperience");
    const doctorRating = document.getElementById("doctorRating");
    const doctorDescription = document.getElementById("doctorDescription");

    const monthSelect = document.getElementById("monthSelect");
    const yearSelect = document.getElementById("yearSelect");
    const btnLoadCalendar = document.getElementById("btnLoadCalendar");

    const prevMonthBtn = document.getElementById("prevMonthBtn");
    const nextMonthBtn = document.getElementById("nextMonthBtn");

    const calendarTitle = document.getElementById("calendarTitle");
    const calendarGrid = document.getElementById("calendarGrid");

    // =============================
    // STATE
    // =============================
    const today = new Date();

    let currentMonth = today.getMonth() + 1;
    let currentYear = today.getFullYear();

    let daysWithSchedule = [];
    let daysWithAppointments = [];

    // =============================
    // EVENTS
    // =============================
    function bindEvents() {
        btnLoadCalendar.addEventListener("click", () => {
            currentMonth = parseInt(monthSelect.value) || currentMonth;
            currentYear = parseInt(yearSelect.value) || currentYear;

            loadCalendar(currentMonth, currentYear);
        });

        prevMonthBtn.addEventListener("click", () => {
            currentMonth--;

            if (currentMonth < 1) {
                currentMonth = 12;
                currentYear--;
            }

            syncSelect();
            loadCalendar(currentMonth, currentYear);
        });

        nextMonthBtn.addEventListener("click", () => {
            currentMonth++;

            if (currentMonth > 12) {
                currentMonth = 1;
                currentYear++;
            }

            syncSelect();
            loadCalendar(currentMonth, currentYear);
        });
    }

    // =============================
    // DEFAULT SELECT
    // =============================
    function setDefaultMonthYear() {
        monthSelect.value = currentMonth;
        yearSelect.value = currentYear;
    }

    function syncSelect() {
        monthSelect.value = currentMonth;
        yearSelect.value = currentYear;
    }

    // =============================
    // PROFILE
    // =============================
    async function loadDoctorProfile() {
        try {
            const response = await authFetch("/api/doctor/profile");

            if (!response.ok) {
                throw new Error("Cannot load profile");
            }

            const data = await response.json();
            renderDoctorProfile(data);

        } catch (error) {
            console.error(error);
            showToast("Failed to load doctor profile", "danger");
        }
    }

    function renderDoctorProfile(data) {
        doctorAvatar.src =
            data.avatar ||
            "";

        doctorAvatar.onerror = function () {
            this.src = "";
        };

        doctorFullname.textContent = data.fullname || "N/A";
        doctorPhone.textContent = data.phone_number || "N/A";
        doctorCode.textContent = data.doctor_id || "N/A";
        doctorAddress.textContent = data.address || "N/A";
        doctorDob.textContent = formatDate(data.date_of_birth);
        doctorSpecialization.textContent = data.specialization || "N/A";

        doctorExperience.textContent =
            data.experience_years != null
                ? `${data.experience_years} years`
                : "N/A";

        doctorRating.textContent = `${data.rating || 0} ★`;

        doctorDescription.textContent =
            data.description || "No description";
    }

    // =============================
    // CALENDAR
    // =============================
    async function loadCalendar(month, year) {
        try {
            calendarGrid.innerHTML = loadingCells();

            const response = await authFetch(
                `/api/doctor/profile/calendar?month=${month}&year=${year}`
            );

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.error || "Cannot load calendar");
            }

            const data = await response.json();

            daysWithSchedule =
                data.days_with_schedule || [];

            daysWithAppointments =
                data.days_with_appointments || [];

            renderCalendar(month, year);

        } catch (error) {
            console.error(error);
            showToast("Failed to load calendar", "danger");
        }
    }

    function renderCalendar(month, year) {
        calendarGrid.innerHTML = "";

        const monthNames = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ];

        calendarTitle.textContent =
            `${monthNames[month - 1]} ${year}`;

        const firstDay = new Date(year, month - 1, 1);
        const totalDays = new Date(year, month, 0).getDate();

        let startDay = firstDay.getDay();
        startDay = startDay === 0 ? 7 : startDay;

        // ô trống đầu tháng
        for (let i = 1; i < startDay; i++) {
            const empty = document.createElement("div");
            empty.className = "calendar-day empty";
            calendarGrid.appendChild(empty);
        }

        // render ngày
        for (let day = 1; day <= totalDays; day++) {
            const cell = document.createElement("div");
            cell.className = "calendar-day";

            const isToday =
                today.getDate() === day &&
                today.getMonth() + 1 === month &&
                today.getFullYear() === year;

            const hasSchedule =
                daysWithSchedule.includes(day);

            const hasAppointment =
                daysWithAppointments.includes(day);

            if (isToday) {
                cell.classList.add("today");
            }

            // ngày có lịch làm việc
            if (hasSchedule) {
                cell.classList.add("has-event");
            }

            // ngày có appointment thật
            if (hasAppointment) {
                cell.classList.add("has-appointment");
            }

            cell.innerHTML = `
                <div class="calendar-day-number">${day}</div>
            `;

            // click nếu có appointment
            if (hasAppointment) {
                cell.style.cursor = "pointer";

                cell.addEventListener("click", () => {
                    window.location.href =
                        `/doctor/appointments?date=${year}-${pad(month)}-${pad(day)}`;
                });
            }

            calendarGrid.appendChild(cell);
        }
    }

    function loadingCells() {
        let html = "";

        for (let i = 0; i < 42; i++) {
            html += `<div class="calendar-day empty"></div>`;
        }

        return html;
    }

    // =============================
    // HELPERS
    // =============================
    function pad(number) {
        return number.toString().padStart(2, "0");
    }

    function formatDate(dateStr) {
        if (!dateStr) return "N/A";

        const date = new Date(dateStr);

        return `${pad(date.getDate())}/${pad(date.getMonth() + 1)}/${date.getFullYear()}`;
    }

    function showToast(message, type = "success") {
        const toast = document.createElement("div");

        toast.className =
            `alert alert-${type} position-fixed top-0 end-0 m-3 shadow`;

        toast.style.zIndex = "9999";
        toast.textContent = message;

        document.body.appendChild(toast);

        setTimeout(() => toast.remove(), 2500);
    }

    // =============================
    // INIT
    // =============================
    function init() {
        setDefaultMonthYear();
        bindEvents();
        loadDoctorProfile();
        loadCalendar(currentMonth, currentYear);
    }

    init();
});