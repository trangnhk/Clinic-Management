document.addEventListener("DOMContentLoaded", function () {
    fetchDoctors();
});

function fetchDoctors() {
    fetch("/api/patient/doctors")
        .then(res => res.json())
        .then(data => renderDoctors(data))
        .catch(err => console.error(err));
}

function renderDoctors(doctors) {
    const container = document.getElementById("doctor-list");

    container.innerHTML = "";

    doctors.forEach(d => {
        const card = `
            <div class="col-md-3 mb-4">
                <div class="card shadow-sm">

                    <img src="${d.avatar || 'https://res.cloudinary.com/dxfbpkmen/image/upload/v1767284497/g9ujloutytyvkempxomj.png'}" 
                         class="card-img-top doctor-img" 
                         alt="Doctor">

                    <div class="card-body text-center">
                        <h5 class="card-title">${d.name}</h5>
                        <p class="text-muted">${d.specialization || ''}</p>

                        <p>⭐ ${d.rating}/5</p>

                        <button class="btn btn-outline-primary btn-sm">
                            View detail
                        </button>
                    </div>

                </div>
            </div>
        `;

        container.innerHTML += card;
    });
}