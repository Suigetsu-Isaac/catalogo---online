
const path = "/templates/img/"
const cards = [
    {
        nome: "Sushi",
        img : path+"Sushi.png"
    },
    {
        nome: "Feijoada",
        img : path+"Feijoada.png"
    },
    {
        nome: "Pizza",
        img : path+"Pizza.png"
    },
    {
        nome: "Manutenção de Computadores",
        img : path+"Manutencao.png"
    },
    {
        nome: "Montagem de Móveis",
        img : path+"Montagem.png"
    },
    {
        nome: "Limpeza de Piscina",
        img : path+"Limpeza.png"
    },
]

function createCard(card){

    return `<div class="bg-2-primaryBackground w-2/3 h-72 rounded-lg block mx-auto my-0 text-center">
    <img src=${card.img} alt="teste" class="h-1/2 w-full rounded-lg">
    <p class="font-bold text-0-primaryTextColor text-lg p-2">${card.nome}</p>
    <p class="text-1-secoundTextColor text-sm p-2">Lorem ipsum dolor sit amet consectetur adipisicing elit. Asperiores excepturi praesentium explicabo quibus...</p>
    <p class="text-blue-500 cursor-pointer hover:to-blue-500"> Ver Mais</p>
</div>
`
     
}

function createCardTemplate(cards){
    const products = document.querySelector("#Products");

    for(var card in cards){
        console.log(cards[card])
        products.innerHTML += createCard(cards[card]);
    }


}

createCardTemplate(cards)