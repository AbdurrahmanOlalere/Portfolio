window.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('animated-gallery');
    if (!container) return;

    let imageFiles = [];
    const dataEl = document.getElementById('image-data');

    if (dataEl) {
        try { imageFiles = JSON.parse(dataEl.textContent || '[]'); }
        catch (e) { console.error('Invalid image JSON:', e); }
    }

    if (!Array.isArray(imageFiles) || imageFiles.length === 0) {
        console.warn('No images to display');
        return;
    }

    // CREATE TWO SLIDES
    const slides = [document.createElement('div'), document.createElement('div')];
    slides.forEach(s => {
        s.className = 'bg-slide';
        container.appendChild(s);
    });

    // Preload images
    const preload = src => new Promise(res => {
        const i = new Image();
        i.onload = () => res(src);
        i.src = src;
    });

    Promise.all(imageFiles.map(preload)).then(() => {
        let current = 0;
        slides[0].style.backgroundImage = `url("${imageFiles[0]}")`;
        slides[0].classList.add('visible');

        setInterval(() => {
            const next = (current + 1) % imageFiles.length;
            const slideToShow = slides[next % 2];
            const slideToHide = slides[current % 2];

            slideToShow.style.backgroundImage = `url("${imageFiles[next]}")`;
            slideToShow.classList.add('visible');
            slideToHide.classList.remove('visible');

            current = next;
        }, 3000);
    });
});
