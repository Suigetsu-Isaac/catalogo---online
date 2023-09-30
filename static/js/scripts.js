
const precoPorAnuncio = 1

// Função Principal que irá ser chamada
// Ela pega os valores e os despacha para as funções auxiliares

function preview(){
    
    let range = document.querySelector('#vigencia').value

    let dataInicio = document.querySelector('#dataInicio').value
    let dataFim = document.querySelector('#dataFim').value

    let diferenca = calcularData(dataInicio, dataFim)

    if (diferenca){
        let resultado = parseInt(range) * precoPorAnuncio * diferenca
        inner(resultado)
    }

}
// Função responsavel pelo calculo da diferença entre as datas
function calcularData(data1,data2){
    
    data1 = new Date(data1);
    data2 = new Date(data2);
    
    // Verificando se foi escrita as datas de forma correta
    if (data1.toString() === 'Invalid Date' || data2.toString() === 'Invalid Date'){
        alert("Erro na formatação das datas")
        return null;
    }

    if (data1 >= data2){
        alert("a data Inicio é maior ou igual que a data Fim")
        return null
    }

    var diferencaEmMilissegundos = Math.abs(data1 - data2);

    // Converta a diferença para dias
    var diferencaEmDias = Math.ceil(diferencaEmMilissegundos / (1000 * 60 * 60 * 24));
    return diferencaEmDias
    

}

// Função responsavel por pegar os dados e coloca-lo no HTML

function inner (resultado){
    let inner = document.querySelector('#preview')

    inner.innerHTML = `<h1> R$ ${String(resultado)}.00 </h1>`
}