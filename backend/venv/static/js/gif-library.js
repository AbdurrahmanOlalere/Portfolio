// Get the canvas element
const canvas = document.getElementById('gif-canvas');
const ctx = canvas.getContext('2d');

// Function to set the canvas size based on the screen size
function setCanvasSize() {
    const desiredWidth = window.innerWidth * 0.75;
    const desiredHeight = window.innerHeight * 0.75;

    canvas.width = desiredWidth;
    canvas.height = desiredHeight;

  // Load the image files
  const imageFiles = [
    {% for image_file in images %}
      "{{ url_for('static', filename='img/swords/' + image_file) }}",
    {% endfor %}
  ]
}

  // Function to display the images as a GIF
  function displayGif() {
    let currentIndex = 0;

    function render() {
      const image = new Image();
      image.onload = function() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(image, 0, 0);
      };
      image.src = imageFiles[currentIndex];

      currentIndex++;
      if (currentIndex >= imageFiles.length) {
        currentIndex = 0;
      }

      setTimeout(render, 200); // Adjust the delay as per your requirements
    }

    render();
  }

  // Call the setCanvasSize function initially
    setCanvasSize();

  // Handle window resize events
  window.addEventListener('resize', setCanvasSize)

  // Start displaying the GIF
  displayGif();

