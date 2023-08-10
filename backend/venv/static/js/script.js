const container = document.querySelector('.animation-container');

// Function to display images as animation
function displayAnimation(imageUrls) {
let currentIndex = 0;

// Preload images
    const images = [];
    for (const imageUrl of imageUrls) {
        const image = new Image();
        image.src = imageUrl;
        images.push(image);
    }

    // Sort the images by URL before starting the animation
    images.sort((a, b) => {
        return a.src.localeCompare(b.src);
    });
    

    function showImage() {

        const image = images[currentIndex];

        //image.onload = function() { don't need this since i'm Using Preloaded Images from images Array:
        const animatedImage = document.createElement('img');
        const screenWidth = window.innerWidth;
        const screenHeight = window.innerHeight;
        const imgHeight = screenHeight * 0.75;
        const imgWidth = screenWidth;

        animatedImage.src = image.src;
        animatedImage.id = 'animated-image'; // Set the id attribute

        // Styling the img for proper scale
        animatedImage.style.height = `${imgHeight}px`;
        animatedImage.style.width = `${imgWidth}px`;

        // Check if container exists before setting innerHTML
        if (container != null) {
        container.innerHTML = '';
        container.appendChild(animatedImage);
        
        }
            
            
        //};
        //image.src = imageUrls[currentIndex]; don't need this either since i've preloaded the images

        currentIndex++;
        if (currentIndex >= imageUrls.length) {
        currentIndex = 0;
        }

    setTimeout(showImage, 100); // Adjust the delay as per your requirements
}

showImage();
}

// Make a GET request to retrieve the image URLs
fetch('/get_images')
.then(response => response.json())
.then(data => {
    const imageUrls = data.image_urls;
    displayAnimation(imageUrls);
})
.catch(error => console.log(error));



