const APPOINTMENT_ID = window.APPOINTMENT_ID;
const DETAIL_API = `/api/patient/appointments/${APPOINTMENT_ID}/medical-history`;
const REVIEW_API = `/api/patient/appointments/${APPOINTMENT_ID}/review`;


const el = {
    appointmentStatus: document.getElementById("appointment-status"),
    examDate: document.getElementById("exam-date"),

    patientFullname: document.getElementById("patient-fullname"),
    patientId: document.getElementById("patient-id"),
    patientDob: document.getElementById("patient-dob"),
    patientPhone: document.getElementById("patient-phone"),
    patientAddress: document.getElementById("patient-address"),
    patientEmail: document.getElementById("patient-email"),

    doctorName: document.getElementById("doctor-name"),

    diagnosisBox: document.getElementById("diagnosis-box"),

    prescriptionTable: document.getElementById("prescription-table"),
    medicineTotal: document.getElementById("medicine-total"),

    paymentDeposit: document.getElementById("payment-deposit"),
    paymentMedicine: document.getElementById("payment-medicine"),
    paymentLab: document.getElementById("payment-lab"),
    paymentFinal: document.getElementById("payment-final"),
    paymentTotal: document.getElementById("payment-total"),

    labTable: document.getElementById("lab-table"),

    reviewBtn: document.getElementById("review-btn"),
    submitReviewBtn: document.getElementById("submit-review-btn"),

    ratingValue: document.getElementById("rating-value"),
    reviewComment: document.getElementById("review-comment"),
    stars: document.querySelectorAll("#star-rating span")
};

document.addEventListener("DOMContentLoaded", () => {

    loadMedicalHistory();

    bindStarRating();

    el.submitReviewBtn.addEventListener(
        "click",
        submitReview
    );
});

async function loadMedicalHistory() {

    try {

        const res = await authFetch(
            DETAIL_API,
            { method: "GET" }
        );

        const data = await res.json();

        if (!res.ok) {
            alert(data.error || "Cannot load data");
            return;
        }

        renderAppointment(data.appointment_info);
        renderPatient(data.patient_info);
        renderDoctor(data.doctor_info);
        renderDiagnosis(data.medical_result);
        renderPrescription(data.prescription);
        renderPayment(data.payment);
        renderLabResults(data.test_results);

    } catch (error) {

        console.error(error);
        alert("Cannot load medical history");
    }
}

function renderAppointment(info) {

    if (!info) return;

    el.appointmentStatus.innerText =
        formatStatus(info.status);

    el.examDate.innerText =
        formatDate(info.date);
}

function renderPatient(info) {

    if (!info) return;

    el.patientFullname.value =
        info.fullname || "";

    el.patientId.value =
        formatPatientId(info.id);

    el.patientDob.value =
        formatDate(info.date_of_birth);

    el.patientPhone.value =
        info.phone_number || "";

    el.patientAddress.value =
        info.address || "";

    el.patientEmail.value =
        info.email || "";
}

function renderDoctor(info) {

    if (!info) return;

    el.doctorName.innerText =
        info.fullname || "-";
}

function renderDiagnosis(info) {

    el.diagnosisBox.innerText =
        info?.diagnosis || "No diagnosis";
}

function renderPrescription(data) {

    const items = data?.items || [];

    if (!items.length) {

        el.prescriptionTable.innerHTML = `
            <tr>
                <td colspan="6">
                    No prescription
                </td>
            </tr>
        `;

        el.medicineTotal.innerText =
            formatMoney(0);

        return;
    }

    let html = "";

    items.forEach(item => {

        html += `
            <tr>
                <td>${item.no}</td>
                <td>${item.medicine_name || "-"}</td>
                <td>${item.dosage || "-"}</td>
                <td>${item.quantity || 0}</td>
                <td>${formatMoney(item.unit_price)}</td>
                <td>${formatMoney(item.amount)}</td>
            </tr>
        `;
    });

    el.prescriptionTable.innerHTML = html;

    el.medicineTotal.innerText =
        formatMoney(
            data.total_medicine_cost || 0
        );
}

function renderPayment(data) {

    const summary = data?.summary || {};

    el.paymentDeposit.value =
        formatMoney(summary.deposit || 0);

    el.paymentMedicine.value =
        formatMoney(summary.medicine || 0);

    el.paymentLab.value =
        formatMoney(summary.lab_test || 0);

    el.paymentFinal.value =
        formatMoney(summary.final || 0);

    el.paymentTotal.value =
        formatMoney(data.total_paid || 0);
}

function renderLabResults(items) {

    if (!items || !items.length) {

        el.labTable.innerHTML = `
            <tr>
                <td colspan="3">
                    No laboratory result
                </td>
            </tr>
        `;

        return;
    }

    let html = "";

    items.forEach((item, index) => {

        html += `
            <tr>
                <td>${index + 1}</td>
                <td>${item.test_name || "-"}</td>
                <td>${formatStatus(item.status)}</td>
            </tr>
        `;
    });

    el.labTable.innerHTML = html;
}

function bindStarRating() {

    el.stars.forEach(star => {

        star.addEventListener("click", () => {

            const rating =
                Number(star.dataset.value);

            el.ratingValue.value = rating;

            paintStars(rating);
        });
    });
}

function paintStars(rating) {

    el.stars.forEach(star => {

        const value =
            Number(star.dataset.value);

        if (value <= rating) {
            star.classList.remove("text-secondary");
            star.classList.add("text-warning");
        } else {
            star.classList.remove("text-warning");
            star.classList.add("text-secondary");
        }
    });
}

async function submitReview() {

    const rating =
        Number(el.ratingValue.value);

    const comment =
        el.reviewComment.value.trim();

    if (!rating) {
        alert("Please select rating");
        return;
    }

    const payload = {
        rating: rating,
        comment: comment
    };

    try {

        const res = await authFetch(
            REVIEW_API,
            {
                method: "POST",
                body: JSON.stringify(payload)
            }
        );

        const data = await res.json();

        if (!res.ok) {
            alert(data.error || "Review failed");
            return;
        }

        alert("Review success");

        const modalEl =
            document.getElementById("reviewModal");

        const modal =
            bootstrap.Modal.getInstance(modalEl);

        modal.hide();

        resetReviewForm();

    } catch (error) {

        console.error(error);
        alert("Review failed");
    }
}

function resetReviewForm() {

    el.ratingValue.value = "";
    el.reviewComment.value = "";

    paintStars(0);
}

function formatDate(dateStr) {

    if (!dateStr) return "-";

    const d = new Date(dateStr);

    if (isNaN(d)) return dateStr;

    return d.toLocaleDateString("vi-VN");
}

function formatMoney(value) {

    return Number(value || 0)
        .toLocaleString("vi-VN") + " VND";
}

function formatStatus(status) {

    if (!status) return "-";

    return status
        .replaceAll("_", " ")
        .toUpperCase();
}

function formatPatientId(id) {

    if (!id) return "-";

    return String(id)
        .padStart(6, "0");
}