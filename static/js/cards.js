
function createCard(){

    var card = `<div class="bg-2-primaryBackground w-2/3 h-72 rounded-lg block mx-auto my-0 text-center">
    <img src="/templates/img/slider1.jpg" alt="teste" class="h-1/2 w-full rounded-lg">
    <p class="font-bold text-0-primaryTextColor text-lg p-2">Sushi</p>
    <p class="text-1-secoundTextColor text-sm p-2">Lorem ipsum dolor sit amet consectetur adipisicing elit. Asperiores excepturi praesentium explicabo quibus...</p>
    <p class="text-blue-500"> Ver Mais</p>
</div>
`
    return card
}

function createCardTemplate(quantidade = 6){
    const products = document.querySelector("#Products");

    for(i=0;i<quantidade;i++){
        products.innerHTML += createCard();
    }


}

createCardTemplate(6)