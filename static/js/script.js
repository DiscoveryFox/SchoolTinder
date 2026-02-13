const container = document.getElementById("cardContainer");
let isDragging = false;
let startX = 0;
let currentCard = null;

const cardColors = [];/* eig bilder dann */ 

for(let i = 1;i >=1;i--){
    const card =document.createElement("div");
    card.className= "card";
    card.style.backgroundColor = cardColors[i-1];
    const cardContent= document.createElement("div");
    cardContent =document.createElement("div");
    cardContent.className = "card-Content";
    cardContent.textContent = i;
    card.appendChild(cardContent);
    container.appendChild(card);

}


function getTopCard(){
    return container.querySelector(".card:last-child");
}
container.addEventListener("mousedown",(e)=> {
    currentCard=getTopCard();
    if(!currentCard) return;
    isDragging = true;
    startX = e.clientX;
    currentCard.style.transition = "none"
});

container.addEventListener("mousemove",(e)=> {
    if(!isDragging ||!currentCard)return;
    const deltaX = e.clientX - startX;
    currentCard.style.transform = `translateX(${deltaX}px) rotate(${
        deltaX/10
    }deg)`;
});

container.addEventListener("mouseup",(e)=>{
    if(!isDragging || !currentCard) return;
    const deltaX =e.clientX - startX;
    handleSwipe(deltaX);
});
container.addEventListener("touchstart", (e)=>{
    currentCard = getTopCard();
    if(!currentCard) return;
    isDragging = true;
    startX = e.touches[0].clientX;
    currentCard.style.transition = "none"
});

container.addEventListener("touchmove", (e)=>{
    if(!isDragging || !currentCard) return;
    const deltaX = e.toches[0].clientX - startX;
    currentCard.style.transform = `translateX(${deltaX}px) rotate(${
        deltaX/10
    }deg)`;
});

container.addEventListener("touchend",(e)=>{
    if(!isDragging || !currentCard) return;
    const deltaX = e.changedTouches[0].clientX - startX;
    handleSwipe(deltaX);
});

function handleSwipe(deltaX){
    const sensitivity = 50;
    if(Math.abs(deltaX)> sensitivity){
        currentCard.style.transition = "transform 0.4s ease, opacity 0.4s ease";
        currentCard.style.transform = `translateX(${deltaX > 0 = ? 1000 : -1000}px) rotate(${deltaX >0 ? 45:-45}deg)`;
        currentCard.style.opacity = 0;
        setTimeout(() => {
            currentCard.remove();
            currentCard= null;
        }, 400);
    }else{
        currentCard.style.transition = "transform 0.3s ease";
        currentCard.style.transform = "translateX (0) rotate(0)";
    }
    isDragging = false
}
