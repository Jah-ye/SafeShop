async function sendBestilling(event) {
        event.preventDefault();
        
        let navn = document.getElementById('kundenavn').value;
        let produkt = document.getElementById('produktvalg').value;
        let frakt = document.getElementById('fraktvalg').value; 
        let melding = document.getElementById('statusMelding');
        
        melding.className = "";
        melding.textContent = "Sender bestilling...";
        
        try {
            let response = await fetch('/api/bestill', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    navn: navn, 
                    produkt: produkt,
                    fraktmetode: frakt 
                })
            });
            
            let resultat = await response.json();
            melding.textContent = resultat.melding;
            
            if (resultat.status === "ok") {
                melding.className = "suksess";
            } else {
                melding.className = "feil";
            }
        } catch (error) {
            melding.textContent = "Kunne ikke koble til Python-serveren.";
            melding.className = "feil";
        }
    }