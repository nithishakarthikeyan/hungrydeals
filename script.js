const API_URL = "http://127.0.0.1:8000/restaurants";

async function loadRestaurants() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();

    const container = document.getElementById("restaurants");
    container.innerHTML = "";

    data.restaurants.forEach((restaurant) => {
      const div = document.createElement("div");
      div.className = "restaurant";

      div.innerHTML = `
        <div class="restaurant-info">
            <h2>${restaurant.name}</h2>
            <p><strong>⭐️ Rating:</strong> ${restaurant.rating}</p>
            <p><strong>🤑 Price:</strong> ${restaurant.price}</p>
            <p><strong>📍 Address:</strong> ${restaurant.address}</p>
            <p><strong>🍔 Categories:</strong> ${restaurant.categories.join(", ")}</p>
        </div>

        <div class="restaurant-image">
            <img src="${restaurant.image}" alt="${restaurant.name}" />
        </div>
`       ;


      container.appendChild(div);
    });

  } catch (error) {
    console.error("Error loading restaurants:", error);
  }
}

loadRestaurants();

