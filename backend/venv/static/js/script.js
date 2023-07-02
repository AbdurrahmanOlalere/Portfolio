// Get the canvas element
const canvas = document.getElementById('gif-canvas');
const ctx = canvas.getContext('2d');

// Function to set the canvas size based on the screen size
function setCanvasSize() {
    const desiredWidth = window.innerWidth * 0.75;
    const desiredHeight = window.innerHeight * 0.75;

    canvas.width = desiredWidth;
    canvas.height = desiredHeight;

    // Start displaying the GIF
    displayGif();
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
window.addEventListener('resize', setCanvasSize);

  
  
  

// Make a request to the Flask server to generate the GIF
/* fetch("/generate_gif", {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      const gifUrl = data.gif_url;
  
      // Create an image element to display the generated GIF
      const gifImg = document.createElement("img");
      gifImg.src = gifUrl;
  
      // Append the image to the animation container
      const animationContainer = document.getElementById("animation-container");
      animationContainer.appendChild(gifImg);
    });
    // this isn't working  so i'l comment it out becuase ikeep getting 404 errors for this
   */
  
