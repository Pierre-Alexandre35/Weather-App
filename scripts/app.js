const search = document.querySelector("#city-search");
const results = document.querySelector(".result");


// works
search.addEventListener("keyup", e =>{
    let city = search.value;
    if(city != ""){
        loadCities(city);
    }
});


// works
const loadCities = (city) => {
    $.ajax({
        url: "config/fetch-cities.php",
        method: "GET",
        async: true,
        data: {
            query: city
        },
        success: function(data){
            results.innerHTML = data;
            temp();
        },
        error: function(error){
            console.log("AJAX error in request: " + JSON.stringify(err, null, 2));
        }
    });
}

const temp = () =>{
    console.log(1);
    window.addEventListener("click", e=>{
        const city = e.target.parentElement.children[0].innerHTML;
        apply(city);
    })
}
