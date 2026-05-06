let selectedScheduleId = null;
let selectedTimeText = "";
let createdAppointmentId = null;

document.addEventListener("DOMContentLoaded", async () => {

    await loadProfile();
    await loadSpecializations();

    document.getElementById("specialization")
        .addEventListener("change", loadDoctors);

    document.getElementById("doctor")
        .addEventListener("change", loadTimeslots);

    document.getElementById("appt-date")
        .addEventListener("change", loadTimeslots);

    document.getElementById("confirm-btn")
        .addEventListener("click", confirmBooking);

    document.getElementById("cancel-btn")
        .addEventListener("click", () => location.reload());
});

async function loadProfile() {

    const res = await authFetch("/api/patient/profile");
    const data = await res.json();

    const p = data.profile;

    document.getElementById("fullname").value = p.fullname || "";
    document.getElementById("email").value = p.email || "";
    document.getElementById("dob").value = p.date_of_birth || "";
    document.getElementById("address").value = p.address || "";
    document.getElementById("patient-id").value = p.id || "";
    console.info("Profile loaded:", p);
}

async function loadSpecializations() {

    const res = await fetch("/api/patient/specializations");
    const data = await res.json();

    const select = document.getElementById("specialization");

    data.forEach(item => {
        select.innerHTML += `
            <option value="${item.id}">
                ${item.name}
            </option>
        `;
    });
}

async function loadDoctors() {

    const specId = document.getElementById("specialization").value;

    const res = await fetch(
        `/api/patient/doctors?specialization_id=${specId}`
    );

    const data = await res.json();

    const select = document.getElementById("doctor");

    select.innerHTML = `<option value="">Choose doctor</option>`;

    data.forEach(item => {
        select.innerHTML += `
            <option value="${item.id}">
                ${item.name}
            </option>
        `;
    });
}

async function loadTimeslots() {

    const doctorId = document.getElementById("doctor").value;
    const date = document.getElementById("appt-date").value;

    if (!doctorId || !date) return;

    const res = await fetch(
        `/api/patient/timeslots?doctor_id=${doctorId}&date=${date}`
    );

    const data = await res.json();

    const box = document.getElementById("timeslots");
    box.innerHTML = "";

    data.forEach(slot => {

        const btn = document.createElement("button");

        btn.className = "btn btn-outline-secondary col-2 m-1";
        btn.innerText = slot.start_time;

        btn.onclick = () => {

            document.querySelectorAll("#timeslots button")
                .forEach(b => b.classList.remove("btn-success"));

            btn.classList.add("btn-success");

            selectedScheduleId = slot.schedule_id;
            selectedTimeText = slot.start_time;
        };

        box.appendChild(btn);
    });
}

async function confirmBooking() {

    if (!selectedScheduleId) {
        alert("Please choose time slot");
        return;
    }

    const ok = confirm("Confirm booking appointment?");

    if (!ok) return;

    try {

        const payload = {
            doctor_id: Number(document.getElementById("doctor").value),
            schedule_id: selectedScheduleId,
            date: document.getElementById("appt-date").value,
            notes: document.getElementById("notes").value
        };

        const res = await authFetch("/api/patient/appointments", {
            method: "POST",
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        createdAppointmentId = data.id;

        showPaymentModal(data);

    } catch (err) {
        alert("Booking failed");
    }
}

function showPaymentModal(appt) {

    const body = document.getElementById("payment-body");

    body.innerHTML = `
        <div class="row mb-3">
            <div class="col-md-6">
                <b>Patient:</b> ${appt.patient_name}
            </div>
            <div class="col-md-6">
                <b>Doctor:</b> ${appt.doctor_name}
            </div>
        </div>

        <div class="row mb-3">
            <div class="col-md-6">
                <b>Date:</b> ${appt.date}
            </div>
            <div class="col-md-6">
                <b>Time:</b> ${selectedTimeText}
            </div>
        </div>

        <hr>

        <div class="row mb-3">
            <div class="col-md-6">
                Consultation fee:
                <b>500,000 VND</b>
            </div>

            <div class="col-md-6">
                Deposit:
                <b>100,000 VND</b>
            </div>
        </div>

        <div class="text-center">
            <button class="btn btn-primary px-5"
                    onclick="makePayment()">
                Payment
            </button>
        </div>
    `;

    const modal = new bootstrap.Modal(
        document.getElementById("paymentModal")
    );

    modal.show();
}

async function makePayment() {

    try {

        const res = await authFetch("/api/patient/payments", {
            method: "POST",
            body: JSON.stringify({
                appointment_id: createdAppointmentId,
                amount: 100000
            })
        });

        const data = await res.json();

        alert("Payment successful!");

        window.location.href = "/";

    } catch (err) {
        alert("Payment failed");
    }
}