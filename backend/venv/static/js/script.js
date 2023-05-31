$(document).ready(function() {
    var imageContainer = $('#image-container');
    var images = [];  // Array to store image paths

    // Function to load image paths from a folder
    function loadImagesFromFolder() {
        $.ajax({
            url: '/get_images',  // Flask route to retrieve image paths
            method: 'GET',
            success: function(response) {
                images = response.images;
                startImageLoop();
            },
            error: function(error) {
                console.error('Error loading images:', error);
            }
        });
    }

    // Function to start the image loop
    function startImageLoop() {
        var currentIndex = 0;
        var totalImages = images.length;

        function displayImage() {
            var imagePath = images[currentIndex];
            imageContainer.attr('src', imagePath);

            currentIndex = (currentIndex + 1) % totalImages;  // Loop through images

            setTimeout(displayImage, 2000);  // Delay between image changes (in milliseconds)
        }

        displayImage();  // Start displaying images
    }

    loadImagesFromFolder();  // Load images from the folder
});
