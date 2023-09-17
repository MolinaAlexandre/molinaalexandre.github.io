function chargerTraductions(langue) {
    const jsonURL = `https://molinaalexandre.github.io/language/${langue}.json`;

    fetch(jsonURL)
        .then(response => response.json())
        .then(data => {
            document.getElementById('AboutMe').textContent = data['AboutMe'];
            document.getElementById('AboutMeText').textContent = data['AboutMeText'];
            document.getElementById('ContactInfo').textContent = data['ContactInfo'];
            document.getElementById('Follow').textContent = data['Follow'];
            document.getElementById('CV').textContent = data['CV'];
            document.getElementById('Email').textContent = data['Email'];
            document.getElementById('Github').textContent = data['Github'];
            document.getElementById('Carousel0').textContent = data['Carousel0'];
            document.getElementById('Carousel1').textContent = data['Carousel1'];
            document.getElementById('Carousel2').textContent = data['Carousel2'];
            document.getElementById('Carousel3').textContent = data['Carousel3'];
            document.getElementById('My Project').textContent = data['My Project'];
            for (let i = 0; i < 3; i++){
                let answer = 'Learn More' + i;
                document.getElementById(answer).textContent = data['Learn More'];
                answer = 'Project\'s Details' + i;
                document.getElementById(answer).textContent = data['Project\'s Details'];
                answer = 'Realisation Date' + i;
                document.getElementById(answer).textContent = data['Realisation Date'];
                answer = 'Made For' + i;
                document.getElementById(answer).textContent = data['Made For'];
                answer = 'Used Language' + i;
                document.getElementById(answer).textContent = data['Used Language'];
                answer = 'Visit Project\'s Page' + i;
                document.getElementById(answer).textContent = data['Visit Project\'s Page'];
            }
        });
}

function changerLangue(langue) {
    chargerTraductions(langue);
}

chargerTraductions('english');