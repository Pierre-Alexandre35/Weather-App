const key = "EoeGCZZsPF6gOnhzti6sgAasYAmGKaDL";




const getCity = async(city) =>{
    const base = "http://dataservice.accuweather.com/locations/v1/cities/search"
    const query = `?apikey=${key}&q=${city}`;
    const response = await fetch(base + query);
    const data = await response.json();
    console.log(data[0].Key);
    return(data[0].Key);

}

const getWeather = async(id) =>{
    const base = "http://dataservice.accuweather.com/currentconditions/v1/";
    const query = `${id}?apikey=${key}`;
    const response = await fetch(base + query);
    const data = await response.json();
    console.log(data);

}

getCity("Paris").then(data =>{
    return getWeather(data);
}).catch(err=> console.log(err));