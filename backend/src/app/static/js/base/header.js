document.addEventListener("DOMContentLoaded", () => {
    loadNavbar();
});

async function loadNavbar() {

    try {

        const token = localStorage.getItem("access_token");

        let headers = {};

        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        const res = await fetch("/api/menu/", {
            method: "GET",
            headers: headers
        });

        const data = await res.json();

        renderNavbar(
            data.menus,
            data.role,
            data.user
        );

    } catch (error) {
        console.error("Load navbar failed:", error);
    }
}

function renderNavbar(menus, role, user) {

    const menuList = document.getElementById("menu-list");
    const userBox = document.getElementById("user-box");

    menuList.innerHTML = "";
    userBox.innerHTML = "";

    /* LEFT MENU */
    menus.forEach(item => {

        const activeClass =
            window.location.pathname === item.url
                ? "active fw-bold text-primary"
                : "";

        menuList.innerHTML += `
            <li class="nav-item">
                <a class="nav-link px-3 ${activeClass}"
                   href="${item.url}">
                    ${item.name}
                </a>
            </li>
        `;
    });


    /* RIGHT USER */
    if (user) {

        const avatar =
            user.avatar
                ? user.avatar
                : "https://cdn-icons-png.flaticon.com/512/149/149071.png";

        let profileUrl = "/profile";
        let extraMenu = "";

        // PATIENT
        if (role === "PATIENT") {
            profileUrl = "/profile";

            extraMenu = `
                <li>
                    <a class="dropdown-item"
                       href="/appointments">
                        <i class="fa fa-calendar me-2"></i>
                        My Appointments
                    </a>
                </li>
            `;
        }

        // DOCTOR
        else if (role === "DOCTOR") {
            profileUrl = "/doctor/profile";
        }

        // ADMIN
        else if (role === "ADMIN") {
            profileUrl = "/admin";
        }

        userBox.innerHTML = `
            <li class="nav-item dropdown">

                <a class="nav-link dropdown-toggle d-flex align-items-center"
                   href="#"
                   id="userDropdown"
                   role="button"
                   data-bs-toggle="dropdown"
                   aria-expanded="false">

                    <img src="${avatar}"
                         width="36"
                         height="36"
                         class="rounded-circle border me-2"
                         style="object-fit:cover;">

                    <span class="fw-semibold">
                        ${user.username}
                    </span>
                </a>

                <ul class="dropdown-menu dropdown-menu-end shadow">

                    <li>
                        <a class="dropdown-item"
                           href="${profileUrl}">
                            <i class="fa fa-user me-2"></i>
                            Profile
                        </a>
                    </li>

                    ${extraMenu}

                    <li><hr class="dropdown-divider"></li>

                    <li>
                        <a class="dropdown-item text-danger"
                           href="#"
                           onclick="logout()">
                            <i class="fa fa-sign-out-alt me-2"></i>
                            Logout
                        </a>
                    </li>

                </ul>

            </li>
        `;

    } else {

        userBox.innerHTML = `
            <li class="nav-item">
                <a class="nav-link fw-semibold px-3"
                   href="/login">
                    Login
                </a>
            </li>
        `;
    }
}


function logout() {

    const ok = confirm("Do you want to logout?");

    if (!ok) return;

    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    window.location.href = "/";
}