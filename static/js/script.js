const container = document.getElementById("cardContainer");
let isDragging = false;
let startX = 0;
let currentCard = null;

const cardColors = [];/* eig bilder dann */ 

for(let i = 1;i >=1;i--){
    const card =document.createElement("div");
    card.className= "card";
    card.style.backgroundColor = cardColors[i-1];
    const cardContent= document.createElement("dov");
    cardContent =document.createElement("div");
    cardContent.className = "card-Content";
}

