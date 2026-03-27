function sendSOS() {
    fetch('/sos', {
        method: 'POST'
    })
    .then(res => res.json())
    .then(data => {
        alert("🚨 EMERGENCY ALERT SENT!\nAuthorities Notified!");
    });
}
