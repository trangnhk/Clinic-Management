const pathParts = window.location.pathname
    .split("/")
    .filter(Boolean);

const appointmentId = pathParts[pathParts.length - 1];

let appointment = null;
let examinationId = null;

document.addEventListener("DOMContentLoaded", async () => {
    await loadDetail();
    await loadMedicines();
    await loadTests();
});

async function loadDetail() {

    const res =
        await authFetch(`/api/doctor/appointments/${appointmentId}`);

    const data = await res.json();

    appointment = data;

    renderDetail(data);
}

function renderDetail(data) {

    examDate.innerText = formatDate(data.date);

    patientCode.innerText = data.patient.patient_code;
    patientName.innerText = data.patient.fullname;
    patientDob.innerText = formatDate(data.patient.date_of_birth);
    patientPhone.innerText = data.patient.phone_number;
    patientEmail.innerText = data.patient.email;
    patientAddress.innerText = data.patient.address;

    symptoms.value = data.symptoms || "";

    setStatus(data.status);

    if (data.examination) {

        examinationId = data.examination.id;

        diagnosis.value = data.examination.diagnosis || "";

        renderPrescription(
            data.examination.prescription?.details || []
        );

        renderLabTests(
            data.examination.lab_tests || []
        );
    }
}


function setStatus(status) {

    const map = {
        WAITING_EXAMINATION: "Waiting Examination",
        IN_PROGRESS: "In Progress",
        PENDING_RESULT: "Pending Result",
        COMPLETED: "Completed"
    };

    statusBadge.innerText = map[status] || status;
}

async function saveExam() {

    const diag = diagnosis.value.trim();

    if (!diag) {
        alert("Diagnosis is required");
        return;
    }

    const body = {
        appointment_id: parseInt(appointmentId),
        diagnosis: diag,
        symptoms: symptoms.value
    };

    // create
    if (appointment.status === "WAITING_EXAMINATION") {

        const res = await authFetch(
            "/api/doctor/examinations",
            {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify(body)
            }
        );

        const data = await res.json();

        if (!res.ok) {
            alert(data.error);
            return;
        }

        examinationId = data.id;
        alert("Saved successfully");
    }
    else {
        if (!examinationId) {
            alert("Examination not found");
            return;
        }

        const res = await authFetch(
            `/api/doctor/examinations/${examinationId}`,
            {
                method: "PATCH",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify({
                    diagnosis: diag,
                    symptoms: symptoms.value
                })
            }
        );

        const data = await res.json();

        if (!res.ok) {
            alert(data.error);
            return;
        }
    }

    const saveRes = await authFetch(
        `/api/doctor/examinations/${examinationId}/save`,
        { method: "POST" }
    );

    const saveData = await saveRes.json();

    if (!saveRes.ok) {
        alert("Saved exam but failed to update payment: " + saveData.error);
        return;
    }

    alert("Updated successfully");
    loadDetail();
}

async function completeExam() {

    await saveExam();

    const res = await authFetch(
        `/api/doctor/appointments/${appointmentId}/complete`,
        {method:"POST"}
    );

    const data = await res.json();

    if (!res.ok) {
        alert(data.error);
        return;
    }

    alert("Completed successfully");

    goBack();
}

async function addMedicine() {

    if (!examinationId) {
        alert("Please Save first");
        return;
    }

    const body = {
        medicine_id: parseInt(medicineSelect.value),
        quantity: parseInt(quantity.value),
        dosage: dosage.value,
        instruction: instruction.value
    };

    const res = await authFetch(
        `/api/doctor/examinations/${examinationId}/prescriptions`,
        {
            method:"POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(body)
        }
    );

    const data = await res.json();

    if (!res.ok) {
        alert(data.error);
        return;
    }

    loadDetail();
}

async function deletePrescription(id) {

    if (!confirm("Delete item?")) return;

    await authFetch(
        `/api/doctor/prescriptions/${id}`,
        {method:"DELETE"}
    );

    loadDetail();
}

function renderPrescription(list) {

    let html = "";
    let total = 0;

    list.forEach((x,i)=>{

        total += x.subtotal;

        html += `
        <tr>
            <td>${i+1}</td>
            <td>${x.medicine_name}</td>
            <td>${x.quantity}</td>
            <td>${money(x.unit_price)}</td>
            <td>${money(x.subtotal)}</td>
            <td>
                <button class="btn btn-sm btn-outline-danger"
                        onclick="deletePrescription(${x.id})">
                    X
                </button>
            </td>
        </tr>`;
    });

    prescriptionTable.innerHTML = html;
    totalAmount.innerText = money(total);
}

async function addLabTest() {

    if (!examinationId) {
        alert("Please Save first");
        return;
    }

    const res = await authFetch(
        `/api/doctor/examinations/${examinationId}/lab-tests`,
        {
            method:"POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({
                test_id: parseInt(testSelect.value)
            })
        }
    );

    const data = await res.json();

    if (!res.ok) {
        alert(data.error);
        return;
    }

    loadDetail();
}

async function deleteLab(id) {

    await authFetch(
        `/api/doctor/lab-tests/${id}`,
        {method:"DELETE"}
    );

    loadDetail();
}

function renderLabTests(list) {

    let html = "";

    list.forEach((x,i)=>{

        html += `
        <tr>
            <td>${i+1}</td>
            <td>${x.test_name}</td>
            <td>${money(x.test_price)}</td>
            <td>${x.status}</td>
            <td>
                ${x.status=="PENDING"
                ? `<button class="btn btn-sm btn-outline-danger"
                           onclick="deleteLab(${x.id})">X</button>`
                : "-"}
            </td>
        </tr>`;
    });

    labTable.innerHTML = html;
}

async function loadMedicines() {

    const res = await authFetch("/api/doctor/medicines");
    const data = await res.json();

    console.log("Medicine data:", data);

    medicineSelect.innerHTML =
        data.map(x =>
            `<option value="${x.id}">
                ${x.name}
            </option>`
        ).join("");
}

async function loadTests() {

    const res = await authFetch("/api/doctor/tests");
    const data = await res.json();

    testSelect.innerHTML =
        data.map(x =>
            `<option value="${x.id}">
                ${x.name}
            </option>`
        ).join("");
}


function goBack() {

    const date =
        appointment?.date || "";

    window.location.href =
        `/doctor/appointments?date=${date}`;
}

function formatDate(date) {

    if (!date) return "-";

    const d = new Date(date);

    return d.toLocaleDateString("en-GB");
}

function money(v) {
    return Number(v || 0).toLocaleString() + " VND";
}