const cor = "FCC404";
const servicos = [
    {
        nome: "Moveis",
        img:`https://img.icons8.com/ios/50/${cor}/furniture.png`,
        alt: 'furniture'
    },
    {
        nome: "Limpeza",
        img:`https://img.icons8.com/wired/64/${cor}/housekeeping.png`,
        alt: 'housekeeping'
    },
    {
        nome: "Alimentos",
        img:`https://img.icons8.com/ios/50/${cor}/omlette.png`,
        alt: 'omlette'
    },
    {
        nome: "Roupas",
        img:`https://img.icons8.com/carbon-copy/100/${cor}/clothes.png`,
        alt: 'clothes'
    },
    {
        nome: "Tecnologia",
        img:`https://img.icons8.com/dotty/80/${cor}/workstation.png`,
        alt: 'workstation'
    },
    {
        nome: "Construção Civil",
        img:`https://img.icons8.com/dotty/80/${cor}/engineer.png`,
        alt: 'engineer'
    },
]


function createIcons(servico){
    console.log(servico);
    return (`<div class="flex flex-col justify-center items-center cursor-pointer hover:opacity-90">
            <div class="bg-1-darkBackground p-5 rounded-full">
            <img width="60" height="60" src=${servico.img} alt=${servico.alt} class="text-0-primaryTextColor"/>
            </div>
            <span class="mt-2 text-lg" >${servico.nome}</span>
        </div>`
        )
}

function createIconsTemplate(servicos){
    var icons = document.querySelector("#icones");

    
    for(var servico in servicos){

        icons.innerHTML+=createIcons(servicos[servico])

    }
}

createIconsTemplate(servicos)