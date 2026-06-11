async function sendBestilling(event) {
    event.preventDefault();
    let navn = document.getElementById('kundenavn').value;
    let produkt = document.getElementById('produktvalg').value;
    let melding = document.getElementById('statusMelding');

    try {
        // Sender data til Python-backend
        let response = await fetch('/api/bestill', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ navn: navn, produkt: produkt })
        });
        
        let resultat = await response.json();
        melding.textContent = resultat.melding;
        
        if (resultat.status === "ok") {
            melding.style.color = "green";
        } else {
            melding.style.color = "red"; // Rødt hvis sikkerhetsfeil/valideringsfeil
        }
    } catch (error) {
        melding.textContent = "Kunne ikke koble til serveren.";
        melding.style.color = "red";
    }
}