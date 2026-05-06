const PROFILE_API = "/api/patient/profile";
const PER_PAGE = 5;

let currentPage = 1;
let totalPages = 1;

const el = {
    fullname: document.getElementById("fullname"),
    patientId: document.getElementById("patient-id"),
    dob: document.getElementById("dob"),
    phone: document.getElementById("phone"),
    address: document.getElementById("address"),
    email: document.getElementById("email"),

    // Medical history
    historyTable: document.getElementById("history-table"),

    // Laboratory result
    labTable: document.getElementById("laboratory-table"),

    // Pagination
    prevBtn: document.getElementById("prev-btn"),
    nextBtn: document.getElementById("next-btn"),
    pageInfo: document.getElementById("page-info"),

    // Modal edit
    editFullname: document.getElementById("edit-fullname"),
    editPhone: document.getElementById("edit-phone"),
    editDob: document.getElementById("edit-dob"),
    editAddress: document.getElementById("edit-address"),

    saveBtn: document.getElementById("save-profile-btn")
};


document.addEventListener("DOMContentLoaded", () => {

    loadProfile(1);

    el.prevBtn.addEventListener("click", () => {
        if (currentPage > 1) {
            loadProfile(currentPage - 1);
        }
    });

    el.nextBtn.addEventListener("click", () => {
        if (currentPage < totalPages) {
            loadProfile(currentPage + 1);
        }
    });

    el.saveBtn.addEventListener("click", updateProfile);
});

async function loadProfile(page = 1) {

    try {

        const res = await authFetch(
            `${PROFILE_API}?page=${page}&per_page=${PER_PAGE}`,
            { method: "GET" }
        );

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || "Cannot load profile");
        }

        // Profile
        renderProfile(data.profile);

        // Medical history
        renderAppointments(
            data.medical_history?.items || []
        );

        renderPagination(
            data.medical_history?.pagination || {
                page: 1,
                pages: 1
            }
        );

        // Laboratory results
        renderLaboratoryResults(
            data.laboratory_results || []
        );

    } catch (error) {

        console.error(error);

        el.historyTable.innerHTML = `
            <tr>
                <td colspan="5">Cannot load medical history</td>
            </tr>
        `;

        if (el.labTable) {
            el.labTable.innerHTML = `
                <tr>
                    <td colspan="4">Cannot load laboratory results</td>
                </tr>
            `;
        }
    }
}

function renderProfile(profile) {

    if (!profile) return;

    el.fullname.value = profile.fullname || "";
    el.patientId.value = profile.id || "";
    el.dob.value = profile.date_of_birth || "";
    el.phone.value = profile.phone_number || "";
    el.address.value = profile.address || "";
    el.email.value = profile.email || "";

    // Fill modal
    el.editFullname.value = profile.fullname || "";
    el.editPhone.value = profile.phone_number || "";
    el.editDob.value = profile.date_of_birth || "";
    el.editAddress.value = profile.address || "";
}

function renderAppointments(items) {

    if (!items.length) {
        el.historyTable.innerHTML = `
            <tr>
                <td colspan="5">No appointment history</td>
            </tr>
        `;
        return;
    }

    let html = "";

    items.forEach(item => {

        html += `
            <tr>
                <td>${item.id}</td>
                <td>${formatDate(item.date)}</td>
                <td>${item.doctor || "-"}</td>
                <td>${formatStatus(item.status)}</td>
                <td>
                    <a href="/medical-history/${item.id}"
                       class="btn btn-sm btn-primary">
                       Detail
                    </a>
                </td>
            </tr>
        `;
    });

    el.historyTable.innerHTML = html;
}

function renderLaboratoryResults(items) {

    if (!el.labTable) return;

    if (!items.length) {
        el.labTable.innerHTML = `
            <tr>
                <td colspan="4">No laboratory results</td>
            </tr>
        `;
        return;
    }

    let html = "";

    items.forEach(item => {

        html += `
            <tr>
                <td>${formatDate(item.date)}</td>
                <td>${item.doctor_name || "-"}</td>
                <td>${item.test_name || "-"}</td>
                <td>${formatStatus(item.status)}</td>
            </tr>
        `;
    });

    el.labTable.innerHTML = html;
}

function renderPagination(pagination = {}) {

    currentPage = pagination.page || 1;
    totalPages = pagination.pages || 1;

    el.pageInfo.innerText = `Page ${currentPage} / ${totalPages}`;

    el.prevBtn.disabled = currentPage <= 1;
    el.nextBtn.disabled = currentPage >= totalPages;
}

async function updateProfile() {

    const payload = {
        fullname: el.editFullname.value.trim(),
        phone_number: el.editPhone.value.trim(),
        date_of_birth: el.editDob.value,
        address: el.editAddress.value.trim()
    };

    try {

        const res = await authFetch(PROFILE_API, {
            method: "PATCH",
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.error || "Update failed");
            return;
        }

        alert("Update profile successfully");

        const modal = bootstrap.Modal.getInstance(
            document.getElementById("editProfileModal")
        );

        modal.hide();

        loadProfile(currentPage);

    } catch (error) {

        console.error(error);
        alert("Update failed");
    }
}

function formatDate(dateStr) {

    if (!dateStr) return "-";

    const d = new Date(dateStr);

    if (isNaN(d)) return dateStr;

    return d.toLocaleDateString("vi-VN");
}

function formatStatus(status) {

    if (!status) return "-";

    return String(status)
        .replaceAll("_", " ")
        .toUpperCase();
}