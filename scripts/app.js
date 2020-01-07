const search = document.querySelector("#city-search");


const results = document.querySelector(".result");


search.addEventListener("keyup", e =>{
    let city = search.value;
    if(city != ""){
        loadCities(city);
    }
});

const loadCities = (city) => {
    $.ajax({
        url: "config/fetch-cities.php",
        method: "GET",
        data: {
            query: city
        },
        success: function(data){
            results.innerHTML = data;
        }
    });
}