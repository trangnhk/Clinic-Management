document.addEventListener("DOMContentLoaded", () => {

    const examDate = document.getElementById("examDate");
    const tbody = document.getElementById("appointmentTableBody");

    init();

    // ===========================
    // INIT
    // ===========================
    function init() {

        const urlParams = new URLSearchParams(window.location.search);

        let date = urlParams.get("date");

        // nếu không có date -> hôm nay
        if (!date) {
            date = getToday();
            redirectToDate(date);
            return;
        }

        examDate.value = date;

        loadAppointments(date);

        bindEvents();
    }

    // ===========================
    // EVENTS
    // ===========================
    function bindEvents() {

        examDate.addEventListener("change", () => {

            const selectedDate = examDate.value;

            if (!selectedDate) return;

            redirectToDate(selectedDate);
        });
    }

    // ===========================
    // REDIRECT
    // ===========================
    function redirectToDate(date) {
        window.location.href =
            `/doctor/appointments?date=${date}`;
    }

    // ===========================
    // LOAD API
    // ===========================
    async function loadAppointments(date) {

        try {

            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="py-5 text-muted">
                        Loading appointments...
                    </td>
                </tr>
            `;

            const response = await authFetch(
                `/api/doctor/appointments?date=${date}`
            );

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.error || "Cannot load data");
            }

            const data = await response.json();

            renderTable(data);

        } catch (error) {

            console.error(error);

            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="py-5 text-danger">
                        Failed to load appointments
                    </td>
                </tr>
            `;
        }
    }

    // ===========================
    // RENDER
    // ===========================
    function renderTable(data) {
        console.info("Appointments data:", data);

        if (!data || data.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="py-5 text-muted">
                        No appointments on this date
                    </td>
                </tr>
            `;
            return;
        }

        let html = "";

        data.forEach(item => {

            html += `
                <tr>
                    <td>${item.start_time}</td>
                    <td>${item.patient?.id ? formatPatientCode(item.patient.id) : "-"}</td>
                    <td>${item.patient?.name || "-"}</td>
                    <td>${formatDate(item.patient?.date_of_birth)}</td>
                    <td>${item.symptoms || "-"}</td>
                    <td>${formatStatus(item.status)}</td>
                    <td>
                        ${renderAction(item)}
                    </td>
                </tr>
            `;
        });

        tbody.innerHTML = html;
    }

    function renderAction(item) {

        if (item.can_examine) {
            return `
                <a href="/doctor/examination/${item.appointment_id}"
                   class="btn btn-sm btn-danger">
                    Examine
                </a>
            `;
        }

        if (item.can_complete) {
            return `
                <a href="/doctor/examination/${item.appointment_id}"
                   class="btn btn-sm btn-outline-danger">
                    View
                </a>
            `;
        }

        return "-";
    }

    // ===========================
    // HELPERS
    // ===========================
    function getToday() {

        const today = new Date();

        return today.toISOString().split("T")[0];
    }

    function formatPatientCode(id) {
        return "BN" + String(id).padStart(9, "0");
    }

    function formatDate(date) {

        if (!date) return "-";

        const d = new Date(date);

        const dd = String(d.getDate()).padStart(2, "0");
        const mm = String(d.getMonth() + 1).padStart(2, "0");
        const yy = d.getFullYear();

        return `${dd}/${mm}/${yy}`;
    }

    function formatStatus(status) {

        const map = {
            WAITING_EXAMINATION: "Waiting Examination",
            IN_PROGRESS: "In Progress",
            PENDING_RESULT: "Pending Result",
            COMPLETED: "Completed"
        };

        return map[status] || status;
    }

});