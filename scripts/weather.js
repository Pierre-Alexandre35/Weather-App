const key = "EoeGCZZsPF6gOnhzti6sgAasYAmGKaDL";




const getCity = async(city) =>{
    console.log("data");

    const base = "http://dataservice.accuweather.com/locations/v1/cities/search"
    const query = `?apiKey=${key}&q=${city}`;
    const response = await fetch(base + query);
    const data = await response.json();
    console.log(data);

}

getCity(Paris);