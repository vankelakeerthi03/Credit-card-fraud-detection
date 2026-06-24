<script>

const form = document.getElementById("fraudForm");
const resultDiv = document.getElementById("result");
const mapDiv = document.getElementById("map");
const locationSelect = document.getElementById("Location");

/* Map Update */
locationSelect.addEventListener("change", function () {

    if (!this.value) {
        mapDiv.innerHTML = "🗺️ Select Location";
        return;
    }

    const coords = this.value.split(",");

    if (coords.length === 2) {
        mapDiv.innerHTML =
        `<iframe width="100%" height="250"
        src="https://maps.google.com/maps?q=${coords[0]},${coords[1]}&z=14&output=embed">
        </iframe>`;
    }

});

/* Live Location */
function getLocation() {

    if (!navigator.geolocation) {
        alert("Location not supported");
        return;
    }

    navigator.geolocation.getCurrentPosition(function(position){

        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        locationSelect.value = lat + "," + lon;

        mapDiv.innerHTML =
        `<iframe width="100%" height="250"
        src="https://maps.google.com/maps?q=${lat},${lon}&z=14&output=embed">
        </iframe>`;

    });

}

/* Form Submit */
form.addEventListener("submit", async (e) => {

    e.preventDefault();

    resultDiv.style.display = "block";
    resultDiv.className = "loading";
    resultDiv.innerHTML = "🔍 Analyzing Transaction...";

    const formData = new FormData(form);

    const data = {
        Time: parseFloat(formData.get("Time")) || 0,
        Amount: parseFloat(formData.get("Amount")) || 0,
        location: formData.get("Location")
    };

    try {

        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const res = await response.json();

        resultDiv.className = res.prediction === 1 ? "fraud" : "safe";

        let coords = ["0","0"];

        if (data.location && data.location.includes(",")) {
            coords = data.location.split(",");
        }

        const probability = res.fraud_probability || 0;

        resultDiv.innerHTML = `
        <div style="font-size:26px;margin-bottom:10px">
        ${res.status}
        </div>

        <div class="customer-card">
        👤 ${formData.get("CustomerName") || "N/A"} <br>
        ID: ${formData.get("CustomerID") || "N/A"} | 📱 ${formData.get("Mobile") || "N/A"}
        </div>

        <div class="otp-box">
        🔐 OTP: ${res.otp}
        </div>

        <div style="margin-top:10px">
        📍 ${data.location || "N/A"}<br>
        🏪 ${formData.get("Shop") || "N/A"}<br>
        💰 ₹${data.Amount}
        </div>

        <div style="margin-top:15px">
        <iframe width="100%" height="250"
        src="https://maps.google.com/maps?q=${coords[0]},${coords[1]}&z=14&output=embed">
        </iframe>
        </div>

        <div class="risk-score">
        Fraud Probability: ${(probability * 100).toFixed(2)}%
        </div>
        `;

    } catch (error) {

        resultDiv.className = "fraud";

        resultDiv.innerHTML = `
        ❌ Connection Error <br><br>
        Make sure backend is running <br>
        <b>python app.py</b>
        `;
    }

});

</script>