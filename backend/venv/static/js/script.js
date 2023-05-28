box = document.getElementById("imageContainer")

function bgChange(){
    box.style.backgroundImage = 'url("' + img + '")' 
}

function fetchImages() {
    fetch("{{ url_for('static', filename='/img/swords.png') }}")
        .then(response => response.json())
        .then(data => {
            var images = data.images; //array of images
            var currentIndex = 0; //current index of the images
            var imageContainer = document.getElementById("imageContainer")

            function animateBackgroudImages() {
                currentIndex++; //Increment the index

                if (currentIndex >= images.length ) {
                    currentIndex = 0;
                }

                var imagePath = "{{ url_for('static', filename='img/swords.png/') }}" + images[currentIndex];
                imageContainer.innerHTML = "<img src='" + imagePath + "'>";

                setTimeout(scrollBackgroundImages, 2000); // Call the function again after 2 seconds (adjust as needed)
                
  
            }

            //Start image scrolling
            animateBackgroudImages();

        })
        .catch(error => {
            console.log('Error fetching images:', error);
        });

}
