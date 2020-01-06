const getCity = async (city) => {

    const key = "Fh5vrLhE3vXwyjaDYjJQxhOpRc5Dp12a";


    const url = "http://dataservice.accuweather.com/locations/v1/cities/search";
    
    
    let search = "http://dataservice.accuweather.com/locations/v1/cities/search";
    
    
    const query = `?apikey=${key}&q=${city}`;
    
    
    const request = await fetch(search + query);
    
    const data = await request.json();


    if (!data[0]){
        console.log("city not found");
    } else {
        console.log(data);

        //console.log(data[0].EnglishName);
        //console.log(data[0].Country.EnglishName);

    }

}

const citySearch = document.getElementById("city-search");

citySearch.addEventListener("keyup", e =>{
    let find = citySearch.value;
    getCity(find);

});



