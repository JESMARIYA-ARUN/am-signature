document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       PASSWORD STRENGTH METER
    ========================== */

    const passwordInput = document.querySelector("#id_password1");
    const bar = document.getElementById("strength-bar");
    const text = document.getElementById("strength-text");

    if (passwordInput && bar && text) {
        passwordInput.addEventListener("input", () => {
            const val = passwordInput.value;
            let strength = 0;

            if (val.length >= 8) strength++;
            if (/[A-Z]/.test(val)) strength++;
            if (/[0-9]/.test(val)) strength++;
            if (/[^A-Za-z0-9]/.test(val)) strength++;

            bar.className = "strength-bar";

            if (!val) {
                bar.style.width = "0%";
                text.textContent = "";
                return;
            }

            if (strength <= 1) {
                bar.style.width = "33%";
                bar.classList.add("weak");
                text.textContent = "Weak password";
            } 
            else if (strength <= 3) {
                bar.style.width = "66%";
                bar.classList.add("medium");
                text.textContent = "Medium strength";
            } 
            else {
                bar.style.width = "100%";
                bar.classList.add("strong");
                text.textContent = "Strong password";
            }
        });
    }

    /* =========================
       AUTO HIDE DJANGO MESSAGES
    ========================== */

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove("show");
            alert.classList.add("fade");

            setTimeout(() => alert.remove(), 500);
        }, 4000); 
    });

    document.querySelectorAll(".qty-btn").forEach(button => {
        button.addEventListener("click", function () {

            const itemId = this.dataset.id;
            const action = this.dataset.action;

            fetch(`/orders/update/${itemId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `action=${action}`
            })
            .then(res => res.json())
            .then(data => {
                if (data.removed) {
                    const row = document.getElementById(`cart-item-${itemId}`);
                    if (row) row.remove();

                    document.getElementById("cart-total").innerText = data.cart_total;

                    if (document.querySelectorAll("[id^='cart-item-']").length === 0) {
                        location.reload(); 
                    }
                    return;
                }


                document.getElementById(`qty-${itemId}`).innerText = data.quantity;
                document.getElementById(`item-total-${itemId}`).innerText = data.item_total;
                document.getElementById("cart-total").innerText = data.cart_total;
            });
        });
    });
});

// CSRF helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        document.cookie.split(";").forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
            }
        });
    }
    return cookieValue;
}




